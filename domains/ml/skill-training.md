---
name: skill-training
description: Training ML models from scratch (or near-scratch) — designing the training loop, picking optimizers and schedules, scaling across GPUs, monitoring loss curves, and preventing the failure modes that quietly waste compute. Use when authoring or auditing a training pipeline, debugging a loss that won't decrease, scaling a single-GPU loop to multi-GPU, or reviewing a teammate's training script. For fine-tuning a pretrained model see `skill-finetuning`; for parameter-efficient methods (LoRA, QLoRA) also see `skill-finetuning`.
---

# Training

Training is where most ML compute is wasted. Bugs in a training loop don't crash — they produce a model that runs but is silently worse than what was possible. The discipline is to make the loop deterministic-where-possible, monitored, and resumable, then to read the loss curves before reading anything else.

## When to Activate

Use when:
- Writing or modifying a training loop (PyTorch, TF, JAX)
- Loss isn't decreasing, decreasing then exploding, or oscillating
- Scaling from single-GPU to DDP, FSDP, or DeepSpeed
- Picking an optimizer or learning-rate schedule
- Adding gradient accumulation, mixed precision, or gradient checkpointing
- Adding checkpointing, resumption, or training-from-checkpoint logic
- Reviewing a colleague's training script before they spend GPU-weeks on it

**Trigger phrases:** "train a model", "training loop", "loss won't go down", "NaN loss", "OOM during training", "DDP", "FSDP", "gradient accumulation", "mixed precision", "fp16", "bf16", "warmup", "learning rate schedule".

## When NOT to Use

| Situation | Use instead |
|---|---|
| Fine-tuning a pretrained model | `skill-finetuning` |
| Parameter-efficient adaptation (LoRA, QLoRA, adapters) | `skill-finetuning` |
| Choosing which model architecture to train | `skill-model-architecture` / `skill-model-selection` |
| Cleaning data before training | `skill-data-preprocessing` |
| Picking metrics for the eval inside the training loop | `skill-ml-evaluation` |
| Tracking experiments and runs | `skill-experiment-tracking` |
| Provisioning the cluster the training runs on | `skill-compute-infra` |
| Reproducibility (seeds, GPU determinism) | `skill-reproducibility` |

## Iron Laws

1. **The training loop is for one job: take a batch, compute loss, step, log.** Anything else (data preprocessing, eval, checkpointing) is a separate function. A 200-line training loop is a bug surface.
2. **Validate every 1-5% of training, not "at the end."** A loss-curve viewed in a notebook hours later is a wasted experiment. Log per-step train loss and per-N-steps val loss to your tracker.
3. **Save a checkpoint before you need one.** Save every N steps AND on best-val-metric. A crashed run with no checkpoint is GPU-hours of pure cost.
4. **Seed it, log the seed, log the framework versions.** Without these you can't reproduce a result and can't debug a regression — see `skill-reproducibility`.

## The Canonical PyTorch Loop

```python
import torch
from torch import nn
from torch.utils.data import DataLoader

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = MyModel().to(device)
optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=0.01)
criterion = nn.CrossEntropyLoss()
scaler = torch.cuda.amp.GradScaler()                           # mixed precision

def train_one_epoch(loader: DataLoader, epoch: int) -> float:
    model.train()
    running = 0.0
    for step, (inputs, labels) in enumerate(loader):           # tuple, not single batch
        inputs, labels = inputs.to(device, non_blocking=True), labels.to(device, non_blocking=True)
        optimizer.zero_grad(set_to_none=True)                  # faster than zero_grad()
        with torch.cuda.amp.autocast(dtype=torch.bfloat16):
            outputs = model(inputs)
            loss = criterion(outputs, labels)
        scaler.scale(loss).backward()
        scaler.unscale_(optimizer)                             # for grad clipping
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        scaler.step(optimizer)
        scaler.update()
        running += loss.item()
        if step % 50 == 0:
            log({"train/loss": loss.item(), "train/step": epoch * len(loader) + step})
    return running / len(loader)
```

Things this enforces that bug-prone loops miss:
- `set_to_none=True` is the modern default (faster, exposes use-after-zero bugs)
- `non_blocking=True` requires `pin_memory=True` in the DataLoader to actually overlap H2D copies
- Gradient clipping after `unscale_` is the only correct order with AMP
- Unpacking `(inputs, labels)` matches the standard DataLoader contract — the original homegrown skill silently used `batch` then referenced an undefined `labels` variable

## Mixed Precision

```python
# Recommended in 2026: bf16 on Ampere+ / Hopper / TPU; fp16 on older hardware
with torch.cuda.amp.autocast(dtype=torch.bfloat16):
    outputs = model(inputs)
    loss = criterion(outputs, labels)
```

bf16 has the same exponent range as fp32, so loss scaling is rarely needed and NaN losses are rarer. fp16 needs `GradScaler`. Don't mix them.

For Hopper/H100 use `torch.compile(model)` — it can buy 1.5-2× throughput when the model is graph-compatible.

## Gradient Accumulation (when you can't fit the batch you want)

```python
ACCUM_STEPS = 4                                                 # effective batch = micro * 4
optimizer.zero_grad(set_to_none=True)
for step, (inputs, labels) in enumerate(loader):
    inputs, labels = inputs.to(device), labels.to(device)
    with torch.cuda.amp.autocast(dtype=torch.bfloat16):
        loss = criterion(model(inputs), labels) / ACCUM_STEPS   # scale loss
    scaler.scale(loss).backward()                               # accumulate
    if (step + 1) % ACCUM_STEPS == 0:
        scaler.unscale_(optimizer)
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        scaler.step(optimizer)
        scaler.update()
        optimizer.zero_grad(set_to_none=True)
```

Forgetting to divide loss by ACCUM_STEPS is the most common mistake — gradients explode and the LR schedule misbehaves.

## Distributed Training

| Strategy | When | Notes |
|---|---|---|
| **DDP** (DistributedDataParallel) | Model fits in one GPU, scale by replicating | Simplest; first thing to try |
| **FSDP** (FullyShardedDataParallel) | Model doesn't fit in one GPU | Shards params, grads, optimizer state |
| **DeepSpeed ZeRO-2/3** | Same as FSDP, more knobs | More mature for very large models |
| **Tensor / Pipeline parallel** | Models > tens of billions of params | Requires careful model-author work |

Skeleton DDP launch:

```python
import os, torch, torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

def setup() -> None:
    dist.init_process_group(backend="nccl")
    torch.cuda.set_device(int(os.environ["LOCAL_RANK"]))

setup()
model = MyModel().cuda()
model = DDP(model, device_ids=[int(os.environ["LOCAL_RANK"])])

# Use DistributedSampler so each rank sees a different shard
from torch.utils.data.distributed import DistributedSampler
sampler = DistributedSampler(dataset, shuffle=True)
loader = DataLoader(dataset, batch_size=BS, sampler=sampler, pin_memory=True, num_workers=4)

for epoch in range(epochs):
    sampler.set_epoch(epoch)                # critical — without this every epoch is identical
    train_one_epoch(loader, epoch)

dist.destroy_process_group()
```

Launch with `torchrun --nproc_per_node=8 train.py`.

Forgetting `sampler.set_epoch(epoch)` is a silent bug — every epoch sees the same data order.

## Optimizers and Schedules

| Optimizer | Sweet spot | Notes |
|---|---|---|
| **AdamW** | Default for transformers, vision transformers, most NN training | `weight_decay` is decoupled from LR — that's the "W" |
| **SGD + Nesterov momentum** | CNNs (ImageNet-style classification) | Often beats Adam on these benchmarks |
| **Lion** | Recent alternative; sometimes better for very large LMs | Newer; less battle-tested but worth a try |
| **Adafactor / 8-bit Adam** | Memory-constrained large-model training | Trades a little quality for big memory savings |

For schedule, the safest default is **linear warmup → cosine decay**:

```python
from torch.optim.lr_scheduler import LambdaLR
import math

def cosine_warmup(step: int, *, warmup: int, total: int, min_ratio: float = 0.1) -> float:
    if step < warmup:
        return step / max(1, warmup)
    progress = (step - warmup) / max(1, total - warmup)
    return min_ratio + (1 - min_ratio) * 0.5 * (1 + math.cos(math.pi * progress))

scheduler = LambdaLR(optimizer, lr_lambda=lambda s: cosine_warmup(s, warmup=1000, total=100_000))
```

Step the scheduler **per step**, not per epoch, when using a step-based schedule. Calling `scheduler.step()` once per epoch silently runs at LR=warmup_init for almost the entire run.

## Reading the Loss Curve First

Before debugging anything else, look at the curve. Each pattern points to a fix:

| Pattern | Likely cause | Fix |
|---|---|---|
| Flat at random-baseline loss | Bug in data, loss, or label encoding | Verify `model(x); criterion(logits, y).backward()` on a single batch first |
| Decreases then explodes (NaN) | LR too high, fp16 without GradScaler, exploding grads | Lower LR, switch to bf16, add grad clip |
| Decreases then plateaus far above zero | Underfitting; capacity or LR too low | Bigger model, more data, longer schedule, higher LR |
| Train falls, val rises | Overfitting | Regularization, dropout, augmentation, early stop, more data |
| Sawtooth / oscillation | Batch size too small for LR, or schedule wrong | Larger effective batch (accumulation), smoother schedule |
| Smooth but slow | LR too low, schedule warmup too long | Higher peak LR, shorter warmup |
| Fine on rank 0, bad on rank N | Distributed training mismatch (BatchNorm, sampler.set_epoch missing) | SyncBatchNorm; verify sampler |

## Checkpointing

```python
import torch

def save_checkpoint(path: str, *, model, optimizer, scheduler, scaler, epoch: int,
                    step: int, best_val: float, config: dict) -> None:
    torch.save({
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "scheduler_state_dict": scheduler.state_dict(),
        "scaler_state_dict": scaler.state_dict(),
        "epoch": epoch,
        "step": step,
        "best_val": best_val,
        "config": config,
        "torch_version": torch.__version__,
        "cuda_version": torch.version.cuda,
    }, path)

def load_checkpoint(path: str, *, model, optimizer, scheduler, scaler) -> dict:
    ckpt = torch.load(path, map_location="cpu")
    model.load_state_dict(ckpt["model_state_dict"])
    optimizer.load_state_dict(ckpt["optimizer_state_dict"])
    scheduler.load_state_dict(ckpt["scheduler_state_dict"])
    scaler.load_state_dict(ckpt["scaler_state_dict"])
    return ckpt
```

Save:
- **Optimizer state** (Adam's running moments) — without it, resuming = retraining from scratch with weights initialized
- **Scheduler state** — without it, the LR jumps back to warmup-start
- **GradScaler state** — for AMP training
- **Config and versions** — so the artifact is reproducible months later

For DDP, save only on rank 0 to avoid corrupted files: `if dist.get_rank() == 0: save_checkpoint(...)`.

## Common Failure Modes

| Pattern | Consequence |
|---|---|
| Validating only at end of epoch on a long epoch | Hours wasted before seeing divergence; use step-based eval |
| Not setting `model.train()` / `model.eval()` | BatchNorm / Dropout in wrong mode; metrics lie |
| Forgetting `optimizer.zero_grad()` before backward | Gradients accumulate across steps; effectively trains with huge batch + wrong LR |
| Stepping scheduler per epoch when schedule is step-based | LR stays at warmup-start; model never trains |
| Not using `DistributedSampler.set_epoch(epoch)` | Same data order each epoch; shuffling broken |
| BatchNorm in DDP without SyncBatchNorm | Each rank computes its own stats; degraded model |
| Logging only per-epoch loss in a long run | Can't see fast divergence; tracker becomes useless |
| Training without a single-batch sanity test | Hours wasted on a broken model; do a 1-batch overfit first |
| `pin_memory=False` with `non_blocking=True` | `non_blocking` becomes a no-op; copy doesn't overlap |
| Saving model only at end | Crashes lose the run; save best-val and every N steps |
| `torch.save(model)` instead of `model.state_dict()` | Pickled class breaks across refactors; save state dict only |
| Mixing `fp16` autocast and `bf16` autocast | Loss scaler misbehaves; NaN |

## Sanity Test Before You Commit GPU-Hours

```python
# Overfit a tiny batch — if loss can't go to ~0 on 8 examples, the model is broken
tiny = next(iter(loader))                       # one batch
inputs, labels = tiny[0][:8].to(device), tiny[1][:8].to(device)
for i in range(200):
    optimizer.zero_grad(set_to_none=True)
    loss = criterion(model(inputs), labels)
    loss.backward()
    optimizer.step()
    if i % 20 == 0:
        print(f"step {i}: loss = {loss.item():.4f}")
# Expect loss to fall toward zero. If not, debug before launching full training.
```

This is the cheapest, fastest debugging tool in ML. Run it whenever you change the model, the loss, or the data pipeline.

## Integration

- `skill-finetuning` — uses this skill's loop with frozen layers and adapter modules
- `skill-data-preprocessing` — produces the data this skill consumes
- `skill-experiment-tracking` — every loss/metric this skill logs lands here
- `skill-reproducibility` — seeds, GPU determinism, checkpoint format
- `skill-compute-infra` — the cluster this loop runs on
- `skill-ml-evaluation` — the validation metrics computed inside the loop
- `skill-monitoring` — production tracking after the trained model ships
- `skill-explainability` — debugging a converged-but-wrong model
- `shared/skill-debugging` — scientific method for "loss won't go down" investigations
- `shared/skill-tdd` — sanity tests on the loop are tests; write them

## Resources

- [PyTorch performance tuning guide](https://pytorch.org/tutorials/recipes/recipes/tuning_guide.html)
- [PyTorch DDP tutorial](https://pytorch.org/tutorials/intermediate/ddp_tutorial.html)
- [PyTorch FSDP tutorial](https://pytorch.org/tutorials/intermediate/FSDP_tutorial.html)
- [DeepSpeed ZeRO](https://www.deepspeed.ai/tutorials/zero/)
- [Hugging Face Trainer (handles a lot of this for you)](https://huggingface.co/docs/transformers/main_classes/trainer)
- [Andrej Karpathy — A Recipe for Training Neural Networks](https://karpathy.github.io/2019/04/25/recipe/) — still the best single document on this topic
