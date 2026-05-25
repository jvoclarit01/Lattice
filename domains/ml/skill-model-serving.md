---
name: skill-model-serving
description: Serving trained models behind an API — framework choice (FastAPI, Triton, vLLM, TGI, TorchServe, BentoML), dynamic batching, streaming, autoscaling, latency vs throughput tradeoffs. Use when building or scaling an inference endpoint, when latency is too high, when GPU utilization is stuck low under load, or when picking between hosted and self-hosted serving. For training-side compute see `skill-compute-infra`; for the orchestration around serving see `skill-mlops`; for production monitoring of the served model see `skill-monitoring`.
---

# Model Serving

Inference is a different problem than training. Training is throughput-bound and bursty; serving is latency-bound and constant. The framework, hardware, and batching strategy that win at training will lose at serving — and the inverse.

## When to Activate

Use when:
- Standing up an inference API for a trained model
- Latency p95 is too high or GPU utilization is stuck at 20%
- Choosing between FastAPI + a model, Triton, vLLM, TGI, TorchServe, BentoML, or a managed endpoint
- Designing dynamic batching or streaming for an LLM
- Sizing replicas for autoscaling on Kubernetes
- Migrating from a single-replica prototype to a real production service

**Trigger phrases:** "deploy this model", "vLLM", "Triton", "dynamic batching", "GPU utilization low", "inference latency", "streaming tokens", "autoscale model API", "throughput too low".

## When NOT to Use

| Situation | Use instead |
|---|---|
| Training-side cluster sizing / DDP | `skill-compute-infra` |
| Pipeline / model-registry / promotion | `skill-mlops` |
| Production monitoring of the served model | `skill-monitoring` |
| Generic web app deployment without an ML model | `webdev/skill-deployment` |
| Choosing the model class itself | `skill-model-selection` |
| Compressing/quantizing the model artifact | `skill-finetuning` (post-training) or vendor docs |

## Iron Laws

1. **Latency and throughput trade off; pick one as the target.** A serving stack tuned for p99 latency will leave throughput on the table, and vice versa. "Both are important" is how you ship neither.
2. **Batching without timeout is a lie.** Dynamic batching needs a max-wait-ms cap or tail latency goes to infinity. The cap is a hard SLA input, not a knob to forget.
3. **Health checks must exercise the model.** A liveness probe that returns 200 because the process is alive doesn't catch a CUDA OOM, a corrupt weight file, or a tokenizer mismatch. Probe the actual `/predict` path with a fixture.

## Framework Decision Matrix

| Need | Pick | Why |
|---|---|---|
| Tabular sklearn / XGBoost behind a REST API | FastAPI + uvicorn / litserve | Trivial, sub-ms overhead, no GPU |
| PyTorch CV / small NN | TorchServe or BentoML | Built-in batching, model archives, multi-model |
| TensorFlow / Keras | TF Serving | First-class TF support, gRPC + REST |
| LLM inference (HF Transformers) | **vLLM** or **TGI** | PagedAttention / continuous batching ≫ naive serving |
| Multi-framework, heavy throughput needs | **Triton Inference Server** | Best-in-class dynamic batching, ensemble pipelines, GPU sharing |
| Want to ship fast with K8s + autoscaling | KServe / Seldon Core | Kubernetes-native; wraps Triton/TF Serving |
| Don't want to operate any of this | SageMaker / Vertex AI / Hugging Face Endpoints | Pay for the operator's labor |

**Default recommendation for LLM serving in 2026:** vLLM if open-weights, TGI for HF integration, or a managed endpoint if you don't want to run GPUs. For non-LLM PyTorch, Triton is the throughput leader; FastAPI is fine for low-traffic or CPU-bound models.

## FastAPI Baseline (CPU / small models)

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib

class PredictRequest(BaseModel):
    features: list[float]

class PredictResponse(BaseModel):
    score: float
    model_version: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = joblib.load("model.joblib")
    app.state.version = open("VERSION").read().strip()
    yield
    # cleanup if needed

app = FastAPI(lifespan=lifespan)

@app.post("/predict", response_model=PredictResponse)
async def predict(req: PredictRequest):
    try:
        score = float(app.state.model.predict_proba([req.features])[0, 1])
    except ValueError as e:
        raise HTTPException(400, f"bad input: {e}")
    return PredictResponse(score=score, model_version=app.state.version)

@app.get("/healthz")
async def healthz():
    # Real health: run a fixture through the model
    try:
        app.state.model.predict_proba([[0.0] * app.state.model.n_features_in_])
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(503, f"unhealthy: {e}")
```

The `lifespan` handler loads the model once at startup, not per-request. The `/healthz` runs a real prediction — the canonical lazy-mistake is checking `app.state.model is not None` and shipping a broken model.

## Dynamic Batching (real implementation)

For GPU-served models, batching is what gets you from 30% to 80% utilization. Naive request-by-request inference wastes GPU.

```python
import asyncio
from dataclasses import dataclass
from typing import Any

import torch

@dataclass
class _Pending:
    payload: Any
    future: asyncio.Future

class DynamicBatcher:
    def __init__(self, model, max_batch_size: int = 32, max_wait_ms: int = 10):
        self.model = model
        self.max_batch = max_batch_size
        self.max_wait = max_wait_ms / 1000.0
        self.queue: asyncio.Queue[_Pending] = asyncio.Queue()
        self._task = asyncio.create_task(self._loop())

    async def _loop(self):
        while True:
            first = await self.queue.get()
            batch = [first]
            deadline = asyncio.get_event_loop().time() + self.max_wait
            while len(batch) < self.max_batch:
                timeout = deadline - asyncio.get_event_loop().time()
                if timeout <= 0:
                    break
                try:
                    item = await asyncio.wait_for(self.queue.get(), timeout=timeout)
                except asyncio.TimeoutError:
                    break
                batch.append(item)
            try:
                inputs = torch.stack([b.payload for b in batch]).cuda()
                with torch.inference_mode():
                    outputs = self.model(inputs).cpu()
                for b, out in zip(batch, outputs):
                    b.future.set_result(out)
            except Exception as e:
                for b in batch:
                    if not b.future.done():
                        b.future.set_exception(e)

    async def predict(self, payload) -> Any:
        loop = asyncio.get_event_loop()
        fut = loop.create_future()
        await self.queue.put(_Pending(payload, fut))
        return await fut
```

Key choices: `max_batch_size` ceiling on GPU memory, `max_wait_ms` ceiling on tail latency. Tune them together — large batch + small wait gets the best throughput; small batch + small wait gets the best p99.

## LLM Serving — vLLM

vLLM's PagedAttention + continuous batching make it 10–24x faster than naive HF generate for concurrent requests.

```python
# Server: vllm serve meta-llama/Llama-3.1-8B-Instruct \
#   --port 8000 --max-model-len 8192 --gpu-memory-utilization 0.9

import openai  # vLLM speaks the OpenAI API
client = openai.OpenAI(base_url="http://localhost:8000/v1", api_key="EMPTY")

stream = client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct",
    messages=[{"role": "user", "content": "Summarize this:" }],
    stream=True,
)
for chunk in stream:
    delta = chunk.choices[0].delta.content or ""
    print(delta, end="", flush=True)
```

For 2026 production deployments, vLLM is the default for self-hosted open-weight LLMs. TGI (Text Generation Inference, HuggingFace) is comparable and integrates with HF Hub. Both support tensor parallelism for >1 GPU.

## Triton — Multi-Model + Dynamic Batching

When you serve many models or need ensembling, Triton wins:

```pbtxt
# config.pbtxt
name: "fraud_classifier"
platform: "pytorch_libtorch"
max_batch_size: 64
input  [{ name: "features" data_type: TYPE_FP32 dims: [42] }]
output [{ name: "score"    data_type: TYPE_FP32 dims: [1]  }]

dynamic_batching {
  preferred_batch_size: [16, 32, 64]
  max_queue_delay_microseconds: 10000   # 10ms cap
}

instance_group [{ count: 2 kind: KIND_GPU }]
```

`preferred_batch_size` is a hint to the scheduler to wait for "round" sizes when feasible. Triton handles the queueing, batching, and GPU sharing across replicas — no Python batcher to maintain.

## Streaming (LLMs and beyond)

For LLMs, streaming tokens drops user-perceived latency dramatically (TTFT — time to first token):

```python
from fastapi.responses import StreamingResponse

@app.post("/generate")
async def generate(req: GenRequest):
    async def event_stream():
        async for token in model.stream(req.prompt):
            yield f"data: {token}\n\n"
        yield "data: [DONE]\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream")
```

For non-LLM models (long inference, batch jobs), HTTP streaming gets replaced by job-style: client POSTs, gets a job ID, polls or subscribes to a webhook for completion.

## Latency vs Throughput Tuning

| Goal | Knobs |
|---|---|
| Low p99 latency | Small `max_batch_size`, small `max_wait_ms`, no swap, dedicated GPU |
| High throughput | Large batch, longer wait, multiple replicas behind LB, KV-cache pooling (LLM) |
| Both | Two pools: a "fast" small-batch pool for SLA traffic, a "bulk" larger-batch pool for batch jobs |

A useful sanity check: measure latency at QPS=1, then at peak QPS. If p99 inflates more than 2x at peak, the queue is saturating — add replicas before tuning batch size further.

## Autoscaling (Kubernetes / KServe)

```yaml
# KServe InferenceService excerpt
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
spec:
  predictor:
    minReplicas: 2
    maxReplicas: 10
    scaleTarget: 70           # target avg CPU/GPU util %
    scaleMetric: concurrency  # or "qps", "rps"
    containerConcurrency: 16  # max concurrent requests per replica
    triton:
      runtimeVersion: "24.03-py3"
      storageUri: "s3://models/fraud-classifier/v1"
```

For GPU autoscaling, use *concurrency* or queue-depth as the signal — CPU/GPU utilization is laggy and noisy on transformer workloads. `minReplicas: 2` ensures rolling deploys don't drop to zero.

## Hardening for Production

```python
# Timeout the actual inference
@app.post("/predict")
async def predict(req: PredictRequest):
    try:
        return await asyncio.wait_for(_predict_impl(req), timeout=2.0)
    except asyncio.TimeoutError:
        raise HTTPException(504, "model timeout")

# Bound payload size
from fastapi import Request
MAX_BYTES = 1_000_000
@app.middleware("http")
async def limit_body(request: Request, call_next):
    if request.headers.get("content-length", "0").isdigit():
        if int(request.headers["content-length"]) > MAX_BYTES:
            return Response("payload too large", status_code=413)
    return await call_next(request)
```

Plus: rate-limit per API key, validate inputs against a schema, refuse NaN/Inf in features, and log a sampled fraction of inputs+outputs for `skill-monitoring` to consume. For untrusted-source weight artifacts, prefer `safetensors` over framework-default serialization (see `skill-reproducibility`).

## Common Failure Modes

| Pattern | Consequence |
|---|---|
| Loading the model per-request | Cold start every call; throughput floor 10x lower than necessary |
| Loading model weights from network on the request path | Adds network latency to inference; load at startup, cache locally |
| Dynamic batching with no wait cap | Tail latency unbounded; p99 is "whenever traffic stops" |
| Synchronous PyTorch in async FastAPI without thread pool | Event loop blocked; throughput collapses under load |
| Health check returns 200 if process is alive | Broken-model bug ships, K8s never restarts |
| Same image for training and inference | Training deps (CUDA toolkit, datasets) bloat inference image; slower starts, larger surface |
| No request size cap | One adversarial 100MB payload OOMs the replica |
| Logging full inputs+outputs at 10K QPS | Disk fills, latency spikes; sample at 1% |
| Autoscale on CPU for GPU model | CPU stays low while GPU is saturated; autoscaler ignores the bottleneck |
| Streaming endpoint without keep-alive tuning | Proxy timeouts cut connections mid-generation |

## Integration

- `skill-mlops` — promotion of a model into the registry; this skill consumes it
- `skill-compute-infra` — the inference-side hardware (L4/L40S/H100 PCIe) decision
- `skill-monitoring` — instrument every endpoint with metrics from this skill
- `skill-rag` — RAG systems often have a serving layer with retrieval + generation latency budgets
- `skill-prompt-engineering` — prompt-cache-aware serving for LLMs
- `skill-reproducibility` — safe-load formats (safetensors) for weight artifacts
- `webdev/skill-deployment` — generic CD primitives (canary, rolling, traffic split) the ML deploy uses
- `shared/skill-security` — auth/rate-limit/payload validation for inference endpoints
- `shared/skill-performance` — general profiling discipline applied to inference

## Resources

- [vLLM docs](https://docs.vllm.ai/en/latest/) — paged attention, continuous batching, deployment recipes
- [Text Generation Inference (TGI)](https://huggingface.co/docs/text-generation-inference) — HF's serving stack
- [NVIDIA Triton](https://github.com/triton-inference-server/server) — multi-framework, dynamic batching, ensembles
- [KServe](https://kserve.github.io/website/) — Kubernetes-native model serving
- [BentoML docs](https://docs.bentoml.com/) — Python-first serving with packaging
- [LiteLLM proxy](https://docs.litellm.ai/) — front-end multi-provider router for LLM fleets
- [Latency vs throughput in inference — Mosaic](https://www.mosaicml.com/blog/llm-inference) — readable overview of LLM serving tradeoffs
