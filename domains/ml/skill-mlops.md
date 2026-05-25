---
name: skill-mlops
description: MLOps — the systems engineering around ML models in production. Pipelines, model registries, CI/CD for ML, scheduled retraining, environment promotion. Use when designing or debugging the lifecycle that takes a notebook to production: training pipeline, registry, deployment, retraining trigger. For training algorithm choices see `skill-training`; for runtime serving infra see `skill-model-serving`; for data versioning see `skill-data-versioning`.
---

# MLOps

MLOps is DevOps with three extra states: data, models, and ground-truth labels. Every CI/CD reflex you have for code applies — but you also need versioning, lineage, and validation gates that don't exist in plain webdev.

## When to Activate

Use when:
- Designing the pipeline that goes from raw data to a deployed model
- Choosing between Kubeflow, Airflow, Prefect, Dagster, Metaflow, or vendor SaaS
- Setting up a model registry (MLflow, SageMaker, Vertex, W&B Registry)
- Defining what "promoting a model from staging to prod" means in your org
- Adding scheduled retraining or shadow-deployment flows
- Building an evaluation gate that blocks deployment when metrics regress

**Trigger phrases:** "automate the training pipeline", "model promotion", "Kubeflow vs Airflow", "shadow deploy", "model registry", "retrain when data drifts", "CI/CD for ML".

## When NOT to Use

| Situation | Use instead |
|---|---|
| Tweaking the training loop itself | `skill-training` |
| Sizing GPUs / cluster shape | `skill-compute-infra` |
| Production drift / quality monitoring | `skill-monitoring` |
| API-level model serving (vLLM, FastAPI, Triton) | `skill-model-serving` |
| Web app deployment / DevOps without an ML model | `webdev/skill-deployment` |
| Versioning datasets specifically | `skill-data-versioning` |

## Iron Laws

1. **Every model in production has a known git commit, data version, and training config.** If you can't answer "what produced this model?" in under a minute, you don't have MLOps — you have hope.
2. **Promotion is a gate, not an event.** "Move to prod" must run an evaluation suite (offline + canary) and block on regression. A merge-button promotion is a bug factory.
3. **No retraining without a rollback.** Automated retraining without the ability to revert to the previous model in <5 minutes is a foot-gun. Retain N previous versions, hot-swappable.

## Reference Architecture

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Raw data     │───▶│ Data         │───▶│ Feature      │
│ (S3/GCS/lake)│    │ validation   │    │ store / dvc  │
└──────────────┘    │ (GE/pandera) │    └──────┬───────┘
                    └──────────────┘           │
                                               ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Model        │◀───│ Eval gate    │◀───│ Training job │
│ registry     │    │ (metrics +   │    │ (orchestrator│
│ (MLflow)     │    │  fairness +  │    │  → cluster)  │
└──────┬───────┘    │  drift)      │    └──────────────┘
       │            └──────────────┘
       ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Canary deploy│───▶│ Shadow /     │───▶│ Full prod    │
│ (1% traffic) │    │ A-B          │    │ rollout      │
└──────────────┘    └──────────────┘    └──────┬───────┘
                                               │
                                               ▼
                                        ┌──────────────┐
                                        │ Monitoring + │
                                        │ retrain      │
                                        │ trigger      │
                                        └──────────────┘
```

Every arrow is a versioned, reproducible artifact. Every box can be re-run from inputs alone.

## Orchestrator Choice

| Tool | Best when | Trade-off |
|---|---|---|
| **Airflow** | You already run Airflow for data jobs; cron-style DAGs | Heavyweight, Python is second-class to "operators", poor for ad-hoc local dev |
| **Prefect** | Pythonic flows, dynamic DAGs, hybrid execution | Smaller ecosystem; managed Cloud is the easy path |
| **Dagster** | Asset-centric thinking (data assets > tasks); strong typing | Steeper conceptual ramp |
| **Kubeflow Pipelines** | Already on Kubernetes, want container-native steps | Operationally heavy; KFP v2 still maturing |
| **Metaflow** | Single-data-scientist flow with transparent S3 versioning | Less rich UI; AWS-leaning |
| **Vertex AI / SageMaker Pipelines** | Already deep on GCP/AWS; want managed | Vendor lock-in; pricey at scale |
| **Step Functions + Batch** | Simple, just orchestrating AWS jobs | Not ML-aware; no native lineage |
| **Plain `make` / shell** | Solo project, <5 steps | Don't pretend this is MLOps; fine for prototypes |

**Default recommendation for a new team:** Prefect or Dagster + MLflow registry. Kubeflow only if you're already a Kubernetes shop with platform engineers.

## Concrete Pipeline (Prefect + MLflow)

```python
from prefect import flow, task
import mlflow
import pandas as pd

@task(retries=2)
def load_data(version: str) -> pd.DataFrame:
    return pd.read_parquet(f"s3://bucket/data/{version}/train.parquet")

@task
def validate(df: pd.DataFrame) -> pd.DataFrame:
    import pandera as pa
    schema = pa.DataFrameSchema({
        "feature_a": pa.Column(float, pa.Check.in_range(0, 1)),
        "label":     pa.Column(int, pa.Check.isin([0, 1])),
    })
    return schema.validate(df)

@task
def train(df: pd.DataFrame, params: dict) -> str:
    from sklearn.ensemble import GradientBoostingClassifier
    mlflow.set_experiment("daily-retrain")
    with mlflow.start_run() as run:
        mlflow.log_params(params)
        mlflow.set_tag("data_version", df.attrs.get("version", "unknown"))
        model = GradientBoostingClassifier(**params).fit(
            df.drop(columns="label"), df["label"]
        )
        mlflow.sklearn.log_model(model, "model")
        return run.info.run_id

@task
def evaluate_gate(run_id: str, baseline_auc: float = 0.82) -> bool:
    """Block promotion if metrics regress."""
    metrics = mlflow.get_run(run_id).data.metrics
    return metrics.get("val_auc", 0) >= baseline_auc - 0.005  # 0.5pp tolerance

@task
def promote(run_id: str) -> None:
    client = mlflow.MlflowClient()
    mv = client.create_model_version(
        name="fraud-classifier",
        source=f"runs:/{run_id}/model",
        run_id=run_id,
    )
    client.transition_model_version_stage(
        name="fraud-classifier", version=mv.version, stage="Staging",
    )

@flow(name="daily-retrain")
def daily_retrain(data_version: str = "v1.4"):
    df = validate(load_data(data_version))
    run_id = train(df, params={"n_estimators": 200, "max_depth": 5})
    if evaluate_gate(run_id):
        promote(run_id)
    else:
        raise ValueError("Eval gate failed; not promoting.")
```

The gate (`evaluate_gate`) is the part that makes this MLOps and not a glorified cron job. Without it, you automate degradation.

## Promotion Stages

| Stage | What's true | Traffic |
|---|---|---|
| `None` | Just trained, registered | 0% |
| `Staging` | Passed offline eval gate | 0% (live, callable for shadow) |
| `Production` | Passed canary at 1–5% | 100% (or A/B split) |
| `Archived` | Replaced; kept for rollback | 0% |

A model never skips stages. Direct `None → Production` is how the team gets paged at 3am.

## CI for ML

```yaml
# .github/workflows/ml-ci.yml
name: ML CI
on: [pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install -e ".[dev]"
      - name: Lint
        run: ruff check src/ && black --check src/
      - name: Unit tests (pure functions, fast)
        run: pytest tests/unit -x
      - name: Smoke train (1 epoch on toy data)
        run: python -m mypkg.train --config configs/smoke.yaml
      - name: Schema test
        run: python -m mypkg.data.validate fixtures/sample.parquet
```

Two patterns matter: (1) tests run on a tiny fixture, never the real dataset; (2) the smoke train catches "I broke `forward()`" without needing a GPU.

## Common Failure Modes

| Pattern | Consequence |
|---|---|
| No data validation step | Schema drift breaks training silently; the pipeline finishes but the model is garbage |
| Promotion is a manual `kubectl apply` | No audit trail; the person who knows the env quits and now no one can ship |
| Same Python env for training and serving | Library version mismatch causes inference results to differ from offline eval |
| Retraining without comparing to the previous champion | New model wins on training metrics, regresses on prod traffic |
| Storing model artifacts on a developer's laptop | "It worked on my machine" graduates to "the model is on Sarah's external drive" |
| No `data_version` tag on runs | Can't reproduce a result from 6 months ago; data has shifted |
| One giant orchestrator DAG with 50 steps | Single failure restarts everything; impossible to debug |

## Integration

- `skill-training` — the actual training step inside the pipeline
- `skill-data-versioning` — versions the data inputs to your pipelines (DVC, LakeFS)
- `skill-experiment-tracking` — the registry and run log this skill orchestrates around
- `skill-model-serving` — what receives the model after promotion
- `skill-monitoring` — closes the loop; drift detection triggers retraining
- `skill-reproducibility` — every artifact in the registry must be reproducible from inputs
- `skill-bias-and-fairness` — fairness checks belong in the eval gate
- `webdev/skill-deployment` — the underlying CD primitives (rolling deploy, canary)

## Resources

- [Made With ML — MLOps course](https://madewithml.com/courses/mlops/) — opinionated, end-to-end
- [Google's MLOps maturity levels](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)
- [MLflow Model Registry docs](https://mlflow.org/docs/latest/model-registry.html)
- [Prefect for ML pipelines](https://docs.prefect.io/)
- [Dagster + dbt + ML](https://dagster.io/blog/dagster-ml)
- [Designing Machine Learning Systems — Chip Huyen](https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/) (book, the canonical reference)
