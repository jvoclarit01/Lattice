---
name: skill-compute-infra
description: ML compute infrastructure — picking GPU/TPU instance types, sizing distributed training jobs, running on SLURM/Ray/Kubernetes, and applying DDP/FSDP/ZeRO parallelism. Use when training won't fit on one GPU, when you need to choose between A100/H100/MI300, when setting up multi-node jobs, or when sizing a cluster budget. For inference-time serving infra (vLLM, Triton, autoscaling), see `skill-model-serving`; for the lifecycle around training (pipelines, registries), see `skill-mlops`.
---

# ML Compute Infrastructure

Compute is a constraint, not a detail. The choice of accelerator, the parallelism strategy, and the cluster scheduler decide whether a training plan finishes in 6 hours or 6 days, and whether the bill is $200 or $20,000.

## When to Activate

Use when:
- Training a model that won't fit on a single GPU
- Sizing instances for a fine-tuning or pre-training run
- Picking between AWS / GCP / Azure / on-prem / CoreWeave / Lambda Labs
- Setting up multi-node distributed training (SLURM, Ray, Kubernetes)
- Deciding between DDP, FSDP, ZeRO-2/3, tensor parallel, pipeline parallel
- Estimating training cost or wall-clock before committing budget
- Diagnosing GPU underutilization (nvidia-smi shows 30%, you want 90%)

**Trigger phrases:** "OOM on the GPU", "how do I scale to multi-node", "which instance should I use", "DDP vs FSDP", "SLURM script", "is it cheaper to train on H100s or A100s", "training is too slow".

## When NOT to Use

| Situation | Use instead |
|---|---|
| Serving a trained model behind an API | `skill-model-serving` |
| Building the pipeline that schedules training | `skill-mlops` |
| Picking the model architecture itself | `skill-model-architecture` |
| Choosing a cloud serverless platform for a web app | `webdev/skill-deployment` |
| Reproducibility of a single training run | `skill-reproducibility` |

## Iron Laws

1. **Profile before you scale.** A poorly-utilized 8x A100 node costs more than a well-utilized 1x A100. Run `nvidia-smi dmon`, `torch.profiler`, or `nsys` first. Multi-GPU does not fix a data-loading bottleneck.
2. **Match parallelism to the bottleneck.** OOM on weights → FSDP/ZeRO. OOM on activations → activation checkpointing or tensor parallel. Compute-bound → DDP. Picking the wrong axis just adds communication overhead.
3. **Spot/preemptible without checkpointing is a coin-flip with your budget.** If a 24-hour job has no resume-from-checkpoint, never use spot. With checkpointing every 30 minutes, spot saves 60–80%.

## Accelerator Choice

| Workload | Recommended | Why |
|---|---|---|
| Tabular / classical ML | CPU instance (16–32 vCPU) | GPU offers no speedup; XGBoost on CPU beats most GPU configs |
| Single-GPU CV / small LM (<1B params) | 1x A10 / L4 / RTX 6000 | $1–2/hr; sufficient memory; cheap |
| Mid-scale fine-tuning (1–13B) | 1–2x A100 80GB or H100 | 80GB needed for batch size; H100 ≈ 2x A100 throughput on transformers |
| Large-scale pre-training (>13B) | 8x H100 / B200 cluster | NVLink + InfiniBand essential; node-local NVMe for activations |
| Inference at scale | L4 / L40S / H100 PCIe | Optimize $/token; vLLM/TensorRT-LLM throughput |
| Massive embeddings / scientific compute | TPU v5p (GCP) or MI300X (AMD) | Cost-effective for dense matmul; check framework support before committing |

**Memory rule of thumb (training, fp16/bf16 mixed precision):**
- Weights: 2 bytes × params
- Gradients: 2 bytes × params
- Adam optimizer state: 8 bytes × params (fp32 master + momentum + variance)
- Activations: depends on batch size and seq length, often dominant

A 7B-parameter model with Adam needs roughly `7B × 12 ≈ 84GB` just for weights+grads+opt-state — already over a single A100 80GB before activations.

## Parallelism Strategy Decision Tree

```
Does the model fit in single-GPU memory?
├── Yes → DDP (one model replica per GPU, sync gradients all-reduce)
│         Use this 90% of the time. Simple, fast, well-supported.
└── No  → Need to shard. Pick by what overflows:
         ├── Weights/grads/optim only? → ZeRO-2 (DeepSpeed) or FSDP SHARD_GRAD_OP
         ├── Even weights too big?     → ZeRO-3 / FSDP FULL_SHARD
         ├── A single layer too big?    → Tensor parallel (Megatron-LM, vLLM)
         └── Pipeline depth helps?      → Pipeline parallel (PP), usually combined with TP+DP (3D)
```

### DDP (PyTorch)

```python
import os
import torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

def setup_ddp() -> int:
    """Initialize process group from torchrun env vars. Returns local_rank."""
    dist.init_process_group(backend="nccl")
    local_rank = int(os.environ["LOCAL_RANK"])
    torch.cuda.set_device(local_rank)
    return local_rank

local_rank = setup_ddp()
model = MyModel().cuda(local_rank)
model = DDP(model, device_ids=[local_rank])
# Launch with: torchrun --nproc_per_node=8 --nnodes=2 --node_rank=0 ... train.py
```

Each rank holds a full model copy; gradients are all-reduced after `loss.backward()`. Bandwidth requirement scales with model size — at >7B params on slow interconnect, DDP becomes communication-bound.

### FSDP (PyTorch native, replaces ZeRO-3 for most users)

```python
from torch.distributed.fsdp import FullyShardedDataParallel as FSDP, MixedPrecision
from torch.distributed.fsdp.wrap import transformer_auto_wrap_policy
from functools import partial
from transformers.models.llama.modeling_llama import LlamaDecoderLayer

bf16 = MixedPrecision(param_dtype=torch.bfloat16,
                      reduce_dtype=torch.bfloat16,
                      buffer_dtype=torch.bfloat16)

wrap_policy = partial(transformer_auto_wrap_policy,
                      transformer_layer_cls={LlamaDecoderLayer})

model = FSDP(model,
             auto_wrap_policy=wrap_policy,
             mixed_precision=bf16,
             device_id=torch.cuda.current_device())
```

Wrap at the transformer-block boundary, not the whole model. Wrapping too coarsely defeats the sharding; wrapping too finely (every Linear) explodes communication overhead.

## Cluster Schedulers

### SLURM (academic / on-prem HPC)

```bash
#!/bin/bash
#SBATCH --job-name=train-llama-7b
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=8
#SBATCH --gres=gpu:h100:8
#SBATCH --cpus-per-task=12
#SBATCH --mem=0                    # all node memory
#SBATCH --time=24:00:00
#SBATCH --output=logs/%x-%j.out

export MASTER_ADDR=$(scontrol show hostnames "$SLURM_JOB_NODELIST" | head -n 1)
export MASTER_PORT=29500
export NCCL_IB_HCA=mlx5            # for InfiniBand fabrics
export NCCL_DEBUG=WARN

srun torchrun \
    --nnodes=$SLURM_NNODES \
    --nproc_per_node=8 \
    --rdzv_backend=c10d \
    --rdzv_endpoint=$MASTER_ADDR:$MASTER_PORT \
    train.py --config configs/llama7b.yaml
```

`#SBATCH --mem=0` requests all node memory. Pinning `NCCL_IB_HCA` to the right HCA avoids NCCL falling back to TCP, which kills throughput.

### Ray (cloud-flexible, dynamic)

```python
import ray
from ray.train.torch import TorchTrainer
from ray.train import ScalingConfig

def train_fn(config):
    # standard PyTorch training loop, Ray handles distributed setup
    ...

trainer = TorchTrainer(
    train_fn,
    scaling_config=ScalingConfig(
        num_workers=16,           # 16 GPUs total
        use_gpu=True,
        resources_per_worker={"GPU": 1, "CPU": 8},
    ),
)
result = trainer.fit()
```

Ray is best when you need elasticity (autoscaling, mixing GPU types) and fault tolerance. Higher overhead than SLURM for simple jobs.

### Kubernetes + Volcano / Kueue

Use when ML training shares a cluster with non-ML workloads. The key add-on is gang scheduling (Volcano `MinAvailable`, Kueue `Workload`) — without it, partial allocations deadlock multi-node jobs.

## Cost Sizing (rough, 2026 spot pricing)

| Instance | $/hr (spot) | TFLOPS bf16 | Best for |
|---|---|---|---|
| 1x A10G (g5.xlarge) | ~$0.40 | 70 | Single-GPU dev, small fine-tuning |
| 1x L4 | ~$0.60 | 121 | Inference, light training |
| 1x A100 80GB | ~$1.50 | 312 | Mid-scale training |
| 1x H100 80GB | ~$3.00 | 989 | Modern training, fine-tune |
| 8x H100 SXM5 | ~$24 | 7900 | Pre-training |
| TPU v5e-8 | ~$8 | 800 | JAX/Flax workloads |

**Estimate before launching:** `total_cost = (tokens / throughput_tokens_per_sec) * $/hr / 3600`. If your number is laughable, change strategy before launching, not after.

## Common Failure Modes

| Pattern | Why it fails / consequence |
|---|---|
| Adding GPUs without profiling | Data loader is the bottleneck; GPUs idle 70% of the time, cost doubles |
| FSDP wrapping the whole model | Tiny shards, all-gather every step, slower than DDP |
| Spot instances with no checkpointing | One preemption near hour 23 of a 24-hour job = total loss |
| `NCCL_DEBUG=INFO` left on in production | Logs flooded with all-reduce traces, masks real errors |
| Mixing GPU generations in one job | NCCL falls back to slowest interconnect; A100+H100 cluster runs at A100 speeds |
| `num_workers=0` in DataLoader | CPU-bound, GPU sits at 20% utilization; set `num_workers ≈ 4×num_gpus` |
| Forgetting `pin_memory=True` | Host→device transfer becomes synchronous, halves throughput |
| Allocating a full-precision optimizer on the same GPU as fp16 weights | OOM at ~70% of expected capacity |

## Integration

- `skill-training` — uses the parallelism patterns from this skill in actual training loops
- `skill-mlops` — schedules these jobs as part of larger pipelines
- `skill-model-serving` — inference-side infra; different constraints (latency, batching)
- `skill-reproducibility` — pinning CUDA/driver/NCCL versions matters for reproducible numerics
- `skill-experiment-tracking` — log hardware + NCCL config alongside metrics
- `shared/skill-performance` — general profiling discipline; this skill is the GPU-specific layer

## Resources

- [PyTorch FSDP tutorial](https://pytorch.org/tutorials/intermediate/FSDP_tutorial.html)
- [DeepSpeed ZeRO docs](https://www.deepspeed.ai/training/) — original ZeRO-1/2/3 reference
- [NVIDIA NCCL tuning guide](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/troubleshooting.html)
- [MosaicML LLM training recipes](https://github.com/mosaicml/llm-foundry) — battle-tested DDP/FSDP configs
- [Ray Train docs](https://docs.ray.io/en/latest/train/train.html)
- [SLURM elastic torchrun](https://pytorch.org/docs/stable/elastic/run.html#elastic-launch)
