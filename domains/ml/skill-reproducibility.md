---
name: skill-reproducibility
description: ML reproducibility — controlling randomness, versioning data and models, pinning environments, and tracking experiments so a result can be reproduced bit-for-bit (or as close as the platform allows). Use when training models, publishing research, debugging a "different results each run" problem, or setting up a new ML repo.
---

# ML Reproducibility

For *general* (non-ML) reproducibility — git discipline, environment pinning, config management — see `shared/skill-reproducibility`. This skill covers the ML-specific layer: stochastic training, GPU non-determinism, data/model versioning, and experiment tracking.

## When to Activate

Use when:
- Training any ML model (every training run should be reproducible)
- Publishing research (reproducibility is a hard requirement)
- A teammate or reviewer can't reproduce your results
- Numbers drift between runs with the "same" config
- Setting up a new ML repository
- Onboarding a collaborator to your project

**Trigger phrases:** "different results each run", "can't reproduce the paper", "this trained better yesterday", "set the seed", "non-deterministic"

## When NOT to Use

- General codebase reproducibility (env, git, configs) → `shared/skill-reproducibility`
- CI build reproducibility → `webdev/skill-devops`
- Reproducible figures in a thesis → `thesis/skill-figures-and-tables`

## Iron Laws

1. **Seed everything, log the seed, log the framework versions.** Without all three, "reproducible" is a wish.
2. **GPU + nondeterministic ops = best-effort only.** Document which kernels remain nondeterministic; don't claim bit-exactness you can't deliver.
3. **Data version is part of the result.** A model trained on `data v1.2` is not the model trained on `data v1.3` — even if every other setting matches.

## Seed Discipline

```python
import os, random
import numpy as np
import torch

def set_all_seeds(seed: int = 42) -> None:
    """Set every RNG that affects training. Call before any data shuffle or model init."""
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    # PyTorch >= 1.8 — also fail loudly on remaining nondeterministic ops
    torch.use_deterministic_algorithms(True, warn_only=True)
```

What this does NOT cover:
- DataLoader workers — pass `worker_init_fn=lambda wid: np.random.seed(seed + wid)` and set `generator=torch.Generator().manual_seed(seed)`
- TensorFlow — different API: `tf.random.set_seed`, `os.environ["TF_DETERMINISTIC_OPS"] = "1"`
- JAX — pass keys explicitly; there is no global state

## What Breaks Reproducibility on GPU

Even with seeds set, these will introduce variance:
- `torch.backends.cudnn.benchmark = True` (selects fastest kernel non-deterministically)
- Mixed precision (fp16/bf16) — different reduction order across runs
- `scatter_add`, `index_add`, certain pooling/loss kernels — known nondeterministic
- `num_workers > 0` without `worker_init_fn`
- Different GPU model, driver, or CUDA version between runs

If bit-exactness is required, run on CPU; otherwise document what level of equivalence you guarantee (e.g., "metrics within ±0.1% across seeds").

## Data Version Control

Code in git, data in DVC (or LFS). Both pinned in commits.

```bash
dvc init
dvc add data/train.csv                              # large file → .dvc pointer
git add data/train.csv.dvc data/.gitignore
git commit -m "chore(data): pin train v1.2"

dvc remote add -d storage s3://my-bucket/dvcstore   # remote backing store
dvc push                                            # upload data
dvc pull                                            # collaborator fetches it
dvc diff <commit-A> <commit-B>                      # see data changes between commits
```

For Git LFS as a simpler alternative when you don't need pipelines:

```bash
git lfs install
git lfs track "*.parquet" "*.h5" "*.bin"
git add .gitattributes data/train.parquet
git commit -m "Add training data via LFS"
```

Pick DVC when you need pipelines/lineage, LFS when you just need large-file storage.

## Reproducible Splits

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y,
)
```

For time-series, never use random splits — use `TimeSeriesSplit` or a date cutoff.
For grouped data (same patient appears in multiple rows), use `GroupKFold` so the same group never spans train/test.

## Experiment Tracking (the run is the result)

Every training run should log: code commit, data version, config, hardware, full metric trajectory, and final artifacts. Pick one tool and use it consistently.

### MLflow

```python
import mlflow
import subprocess

mlflow.set_experiment("baseline-rf-v1")
with mlflow.start_run():
    mlflow.log_params(config)
    git_sha = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode()
    mlflow.set_tag("git_commit", git_sha)
    mlflow.set_tag("data_version", "v1.2")
    for epoch in range(epochs):
        loss = train_epoch()
        mlflow.log_metric("loss", loss, step=epoch)
    mlflow.sklearn.log_model(model, "model")
    mlflow.log_artifact("config.yaml")
```

### Weights & Biases

```python
import wandb
wandb.init(
    project="my-project",
    config=config,
    tags=[f"data-{data_version}", f"git-{git_sha[:7]}"],
)
wandb.log({"loss": loss, "step": epoch})
wandb.save("config.yaml")
```

Both work. Pick MLflow if you need a self-hosted/private setup; W&B if you want polished UX out of the box. See `skill-experiment-tracking` for deeper comparison.

## Reproducible Model Persistence

Use `joblib` for sklearn models — it handles numpy arrays better than the standard library's serializer:

```python
import joblib
joblib.dump(model, "model.joblib")
loaded = joblib.load("model.joblib")
```

For PyTorch:

```python
torch.save({
    "model_state_dict": model.state_dict(),
    "optimizer_state_dict": opt.state_dict(),
    "epoch": epoch,
    "config": config,
    "torch_version": torch.__version__,
    "cuda_version": torch.version.cuda,
}, "checkpoint.pt")
```

Save the *state dict*, not the whole model object — serialized class instances break across class refactors. For maximum portability, prefer `safetensors` over `torch.save` for weights-only artifacts:

```python
from safetensors.torch import save_file, load_file
save_file(model.state_dict(), "model.safetensors")
state = load_file("model.safetensors")
```

`safetensors` is also safer to load from untrusted sources — it cannot execute code.

## Phase-by-Phase Reproducibility Workflow

**Setup (once per repo):**
1. Pin Python and dependencies: `pyproject.toml` with exact versions, `python = "==3.11.7"`
2. Containerize: `Dockerfile` with pinned base image and pinned CUDA version if GPU
3. Init DVC or LFS for data
4. Decide an experiment tracking tool and add the API key to repo secrets

**Per run:**
1. `set_all_seeds(config.seed)` before anything else
2. Log: code commit hash, config, data version, hardware (GPU model + driver), library versions
3. Save: model state dict, optimizer state, training config, final metrics

**For reproduction by a third party:**
1. They clone the repo at the recorded commit
2. Build the container or recreate the env from `pyproject.toml`
3. `dvc pull` to fetch the recorded data version
4. Run with the recorded seed and config
5. Verify metrics match within stated tolerance

## Common Failure Modes

| Symptom | Likely cause | Fix |
|---|---|---|
| Different metrics each run, same config | Missing seed somewhere (DataLoader workers? augmentation library?) | Audit every RNG-using import; set `worker_init_fn` |
| Reproducible on CPU, not on GPU | cuDNN nondeterminism | Set `cudnn.deterministic=True`, document residual variance |
| Local works, colleague's machine doesn't | Library version drift | Pin exact versions in lock file; containerize |
| Same code, same data, different metrics six months later | Library updates broke determinism | Container image with pinned versions |
| Can't reproduce paper exactly | Floating-point math differs across hardware | Match GPU model and CUDA version, or accept tolerance |

## Integration

- `shared/skill-reproducibility` — general (non-ML) reproducibility discipline
- `skill-experiment-tracking` — deeper coverage of MLflow/W&B/TensorBoard
- `skill-data-versioning` — DVC and Git LFS in depth
- `skill-training` — uses the seeded training loop pattern from this skill
- `skill-ml-evaluation` — reproducible evaluation requires reproducible training
- `thesis/skill-research-methodology` — reproducibility section of a thesis methodology chapter
- `thesis/skill-dataset-documentation` — data card that records what `data v1.2` actually contains

## Resources

- [PyTorch reproducibility guide](https://pytorch.org/docs/stable/notes/randomness.html)
- [MLflow](https://mlflow.org/) · [W&B](https://wandb.ai/) · [DVC](https://dvc.org/)
- [safetensors](https://github.com/huggingface/safetensors)
- [Reproducibility Checklist (NeurIPS)](https://www.cs.mcgill.ca/~jpineau/ReproducibilityChecklist.pdf)
