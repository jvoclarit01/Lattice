---
name: skill-experiment-tracking
description: Tracking ML experiments — picking between MLflow, Weights & Biases, Neptune, Comet, and TensorBoard, structuring runs/projects/artifacts, deciding self-host vs SaaS, and avoiding the "200 untitled runs" anti-pattern. Use when starting a new ML project, when comparing tools, when migrating between trackers, or when a tracker has become a graveyard. For the registry/promotion workflow built on top of tracking see `skill-mlops`; for reproducibility seeds and env pinning see `skill-reproducibility`.
---

# Experiment Tracking

A tracker is the layer that makes "the run is the result" enforceable. Without one, knowledge lives in CSVs, screenshots, and the hippocampus of whoever ran the experiment last. With one, you can answer "which config produced our best validation AUC, and what data did it use?" — instantly.

## When to Activate

Use when:
- Starting a new ML project (set this up first, not later)
- Comparing tracking tools for an org-wide standard
- Migrating from one tracker to another (pain — plan it carefully)
- Cleaning up a project where runs are unsearchable
- Designing how runs, experiments, projects, and artifacts map to your team
- Adding a registry on top of an existing tracker
- A teammate asks "what was the best run last week?"

**Trigger phrases:** "MLflow vs W&B", "experiment tracking", "log my hyperparameters", "compare runs", "model registry", "Neptune", "Comet", "self-host vs SaaS", "TensorBoard isn't enough".

## When NOT to Use

| Situation | Use instead |
|---|---|
| Production model registry / promotion gates | `skill-mlops` |
| Versioning data and large artifacts (datasets, big files) | `skill-data-versioning` |
| Setting deterministic seeds & env pinning | `skill-reproducibility` |
| Production-time monitoring of a deployed model | `skill-monitoring` |
| Visualizing one model's training curves locally | TensorBoard (lighter than this skill) |
| Tracking LLM prompts and outputs | `skill-prompt-engineering` (Promptfoo / Langfuse) |

## Iron Laws

1. **Every training run is a logged run, or it didn't happen.** Notebook runs without tracking go in a sandbox folder. The moment a result is shared, it has a tracked run with config + git SHA + data version.
2. **Pick one tool per org, then commit.** Mixing MLflow and W&B "because both have nice features" creates two graveyards instead of one knowledge base. Choose, document, enforce.
3. **An experiment without a meaningful name is a graveyard plot.** `Run-2026-04-12-19-32-untitled-29` is not a name. The run name encodes the hypothesis being tested: `lr-sweep-baseline-augmentation-on`.

## Decision Matrix

| Need | Pick | Why |
|---|---|---|
| Open source, self-host required (regulated, sovereignty) | **MLflow** | The de-facto open-source standard; rich registry; runs anywhere |
| Best-in-class UI, collab-heavy, OK with SaaS | **Weights & Biases** | Polished UX; sweeps; reports; the strongest collaboration story |
| Heavy hyperparameter sweeps, granular metric logging at scale | **Neptune** | Built for high-frequency metric streams; strong for RL/long runs |
| Want full audit + experiment+production lineage | **Comet** | Strong artifact lineage; enterprise audit features |
| Just want loss curves for one model in a notebook | **TensorBoard** | Zero-setup; no registry; outgrows you fast |
| You're already on Vertex AI / SageMaker | The vendor's experiment tracking | Tight integration; lock-in trade-off |
| LLM-specific (prompts, traces, evals) | Langfuse / Arize Phoenix | LLM domain modeling; not a substitute for ML tracking |

**Default for a new team without a regulatory constraint:** W&B if you can use SaaS, MLflow if you can't.

## Self-Host vs SaaS

| Dimension | Self-host (MLflow on your infra) | SaaS (W&B / Neptune / Comet Cloud) |
|---|---|---|
| Up-front cost | High (deploy + secure backend, postgres + S3) | Free tier, then per-seat |
| Long-term cost | Cheap once stable | Scales with team size and run volume |
| Setup time | Days–weeks (storage, auth, networking, HA) | Minutes |
| Compliance / data residency | Full control | Vendor + DPA |
| UX polish | Adequate (MLflow); good (Kubeflow Metadata) | Excellent |
| Maintenance | You're the on-call | Vendor's problem |
| Lock-in | Low (open formats) | Medium–High |

Default: SaaS unless you have a specific compliance reason. The "we'll save money self-hosting" instinct underestimates engineering time by ~5x.

## MLflow — Self-Host Reference

```python
import mlflow
import subprocess

mlflow.set_tracking_uri("http://mlflow.internal:5000")
mlflow.set_experiment("fraud-classifier")        # NOT the run name; the project bucket

git_sha = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode()

with mlflow.start_run(run_name="xgb-baseline-2026-q2"):
    mlflow.set_tags({
        "git_commit": git_sha,
        "data_version": "v1.4",
        "owner": "alice",
        "stage": "exploration",        # exploration | candidate | production
    })
    mlflow.log_params({
        "n_estimators": 500,
        "max_depth": 6,
        "learning_rate": 0.05,
    })
    for epoch, loss in enumerate(train(...)):
        mlflow.log_metric("train_loss", loss, step=epoch)
        mlflow.log_metric("val_auc", evaluate(...), step=epoch)

    mlflow.log_artifact("config.yaml")
    mlflow.sklearn.log_model(model, "model",
                             registered_model_name="fraud-classifier")
```

The `tags` are what make runs searchable later (`tags.data_version = 'v1.4' AND tags.stage = 'candidate'`). Without consistent tags, search becomes "scroll through 800 rows".

## Weights & Biases — SaaS Reference

```python
import wandb
import subprocess

git_sha = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode()

run = wandb.init(
    project="fraud-classifier",
    name="xgb-baseline-2026-q2",      # human-meaningful run name
    group="xgb-sweeps",                # group sibling runs
    job_type="train",
    config={"n_estimators": 500, "max_depth": 6, "lr": 0.05,
            "data_version": "v1.4"},
    tags=["xgb", "baseline", f"git-{git_sha[:7]}"],
)

for epoch, loss in enumerate(train(...)):
    wandb.log({"train_loss": loss, "val_auc": evaluate(...)}, step=epoch)

# Save model + register as a versioned artifact
artifact = wandb.Artifact("fraud-classifier", type="model",
                          metadata={"data_version": "v1.4"})
artifact.add_file("model.joblib")
run.log_artifact(artifact)
run.finish()
```

W&B's `group` + `job_type` is the right scaffolding for sweeps and pipelines (e.g., `job_type=preprocess|train|eval` lets you visualize a DAG of related runs).

## TensorBoard — When It's Enough

```python
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter(log_dir="runs/xgb-baseline-2026-q2")
for epoch, loss in enumerate(train(...)):
    writer.add_scalar("train/loss", loss, epoch)
    writer.add_scalar("val/auc", evaluate(...), epoch)
writer.close()
```

TensorBoard is fine for: solo project, single model, no need to compare runs across machines, no registry. It outgrows you the moment you want to share a result, search runs, or promote a model.

## Run Naming Convention

A run name should let a teammate find the experiment without a query:

```
<task>-<approach>-<distinguishing-knob>-<date-or-iter>
```

Examples:
- `fraud-xgb-baseline-2026q2`
- `fraud-nn-larger-hidden-1024`
- `fraud-cv-aug-mixup-alpha-0.4`

Avoid:
- `experiment-1`
- `final-final-v3`
- the auto-generated `Run-1234`
- the date alone (no semantic content)

## Project / Experiment / Run Hierarchy

| Tracker | Container | Group | Unit |
|---|---|---|---|
| MLflow | `experiment` | `tags.group_run_id` (manual) | `run` |
| W&B | `project` | `group` | `run` |
| Neptune | `project` | `tags` / namespaces | `run` |
| Comet | `workspace/project` | `experiment_key` | `experiment` |

Map this once at the org level and document it. A common mistake is creating a new W&B project per experiment ("project = fraud-xgb-2026-04-12") — projects should be long-lived problem domains, not single experiments.

## What to Log (every run)

| Category | Examples |
|---|---|
| Identity | git SHA, branch, who ran it, when, container image |
| Inputs | data version (DVC hash), feature set version, config YAML |
| Hyperparameters | every knob the model class exposes |
| Hardware | GPU model, CUDA, NCCL version (matters for reproducibility) |
| Metrics | training + validation curves; final test metrics with CIs |
| Artifacts | model weights, fitted preprocessor, eval report, plots |
| Outcome tag | `exploration | candidate | production | failed` |

The `outcome` tag is the most underused field. Without it, queries return every failed run from the last six months.

## Sweep / HPO Integration

```yaml
# wandb-sweep.yaml
program: train.py
method: bayes
metric: { name: val_auc, goal: maximize }
parameters:
  learning_rate:
    distribution: log_uniform_values
    min: 1e-5
    max: 1e-1
  max_depth:
    values: [3, 5, 7, 9]
  n_estimators:
    distribution: int_uniform
    min: 100
    max: 1000
```

`wandb sweep wandb-sweep.yaml` creates the sweep, `wandb agent <id>` runs it. For MLflow, use Optuna or Ray Tune with the MLflow callback. Either way: log the sweep ID alongside each run so children can be regrouped under their parent.

## Migration (the painful path)

When migrating between trackers, do not write a converter — write a forward adapter. Every new run goes to both for a quarter; old runs stay where they were. Pick the date when the new tracker becomes the source of truth and stop dual-writing. Trying to import 5,000 historical W&B runs into MLflow is a six-week project that produces a worse copy of the original.

## Common Failure Modes

| Pattern | Consequence |
|---|---|
| `mlflow.start_run()` with no `run_name` | Tracker fills graveyard with `Run-...` rows |
| Logging git SHA but not the data version | Reproducibility broken; "same code different result" |
| Mixing personal API keys across the team | Runs scattered across accounts; nobody owns the project |
| Not setting an outcome tag | Failed and successful runs equally weighted in queries |
| Logging every step at 1Hz for a 6-hour run | UI overloaded; lower frequency or buffer |
| Running tracker server on developer's laptop | Experiments lost when laptop sleeps; move to a real host on day one |
| TensorBoard for a multi-person project | Shared tensorboard log dir becomes a war zone |
| Logging 50 metrics that nobody looks at | Dashboard noise; pick a primary + 3-5 secondary |
| Storing model artifacts in tracker DB instead of object storage | DB bloats to 100GB; switch to S3-backed artifact store |

## Integration

- `skill-mlops` — registry / promotion lifecycle built on top of run history
- `skill-reproducibility` — every run logs the inputs needed for reproduction
- `skill-data-versioning` — tracker stores the data version pointer; DVC stores the data
- `skill-ml-evaluation` — eval metrics and CIs flow into the tracker
- `skill-monitoring` — production metrics close the loop back to training-time metrics
- `skill-bias-and-fairness` — fairness metrics go in the tracker like any other metric
- `shared/skill-tdd` — a regression in eval metric is a failed test for the model

## Resources

- [MLflow docs](https://mlflow.org/docs/latest/index.html) — runs, registry, deployment integrations
- [Weights & Biases docs](https://docs.wandb.ai/) — sweeps, reports, artifacts
- [Neptune AI](https://docs.neptune.ai/) — strong for RL / long-running runs
- [Comet ML](https://www.comet.com/docs/v2/) — full audit + lineage features
- [TensorBoard guide](https://www.tensorflow.org/tensorboard/get_started)
- [Optuna + tracker callbacks](https://optuna.readthedocs.io/en/stable/reference/integration.html) — for HPO that logs to MLflow/W&B
- [What is an experiment? — Shreya Shankar](https://www.shreya-shankar.com/) — practical writeups on tracker hygiene
