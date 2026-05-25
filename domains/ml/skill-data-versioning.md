---
name: skill-data-versioning
description: Versioning datasets and data artifacts for ML — DVC, Git LFS, lakeFS, MLflow dataset logging, and the discipline of pinning data state to model state. Use when the same code produces different metrics on different days, when a colleague can't reproduce your result, when setting up a new ML repo, or when adopting a feature/data store. For training-config and seed reproducibility see `skill-reproducibility`; for the cleaning steps applied to raw data see `skill-data-preprocessing`.
---

# Data Versioning

A model is `f(code, data, config)`. Git versions the code. The trick is versioning the data with equal rigor — without storing 50GB of parquet in git, and without "I'll just rename it `train_v2_final_FINAL.csv`" entropy.

## When to Activate

Use when:
- Setting up a new ML repository (do this on day one)
- A reviewer or teammate can't reproduce a result
- Same code, same config, different metrics from yesterday
- Migrating data between environments / clouds
- Choosing between DVC, Git LFS, lakeFS, Delta Lake, or a feature store
- Designing how training runs reference dataset snapshots

**Trigger phrases:** "version this dataset", "DVC", "Git LFS", "lakeFS", "data hash", "data didn't change but results changed", "reproduce my run", "dataset registry".

## When NOT to Use

| Situation | Use instead |
|---|---|
| Versioning code, configs, environments | `skill-reproducibility` |
| Cleaning the raw data | `skill-data-preprocessing` |
| Logging metrics / runs / models | `skill-experiment-tracking` |
| Production feature store (online + offline) | `skill-mlops` (Feast / Tecton) |
| Auditing lineage end-to-end | `skill-mlops` (orchestrator + lineage) |
| Data warehouse table versioning at TB scale | `webdev/skill-database` (or Delta/Iceberg directly) |

## Iron Laws

1. **Data version is part of the model version.** Every model artifact records the exact dataset hash that produced it. Without this, "reproducible training" is fiction.
2. **Data does not live in git; pointers do.** A `.dvc` pointer or LFS placeholder goes in git. The actual bytes go to object storage. Mixing them tanks repo clone times for everyone forever.
3. **Schema drift is a versioning event.** A new column, a renamed field, a changed type — these are version bumps, not "small fixes". Otherwise downstream code breaks invisibly.

## Tool Decision Matrix

| Need | Pick | Why |
|---|---|---|
| Code-and-data reproducibility for one ML repo | **DVC** | Git-like UX; pipelines; remote storage; the de-facto open-source default |
| Just need large-file storage in git workflow | **Git LFS** | Simpler than DVC; no pipelines or lineage |
| Branch / commit / merge data like git, at scale | **lakeFS** | Object-store branching; great for parquet lakes |
| Tabular data warehouse with time travel | **Delta Lake / Apache Iceberg** | Built for analytics; less ML-specific |
| HF Hub workflow | **Hugging Face Datasets + revision pinning** | Tight integration with HF tooling |
| Production online/offline feature parity | Feast / Tecton | Solves a different problem; see `skill-mlops` |
| You just want a hash of the dataset | `xxhash` over the bytes | Lightweight; works as a tag without a tool |

**Default for a new ML project:** DVC. It's the right answer for ~80% of cases. Reach for lakeFS if your data lives natively as parquet in S3 and you want git-like branching at lake scale.

## DVC — Setup and Daily Use

```bash
# Repo setup (once)
pip install dvc[s3]
dvc init
git commit -m "chore: init DVC"

# Configure remote storage
dvc remote add -d storage s3://my-org-ml-data/dvcstore
dvc remote modify storage region us-east-1
git add .dvc/config && git commit -m "chore: configure DVC remote"

# Track a dataset
dvc add data/train.parquet
git add data/train.parquet.dvc data/.gitignore
git commit -m "chore(data): pin train v1.4"
dvc push                                          # upload bytes to remote
```

What's in git: `data/train.parquet.dvc` (a tiny YAML pointer with the file's hash), `data/.gitignore` (excludes the actual file). What's *not* in git: the parquet itself. A teammate runs `dvc pull` to fetch the bytes from S3 at the version recorded in the current commit.

```bash
# Daily collaboration
git pull && dvc pull                               # sync code + data
git checkout v1.3 && dvc checkout                  # historical state
dvc diff HEAD~3 HEAD                               # what data changed in last 3 commits
```

## DVC Pipelines (lineage)

```yaml
# dvc.yaml
stages:
  preprocess:
    cmd: python src/preprocess.py data/raw data/clean
    deps: [data/raw, src/preprocess.py]
    outs: [data/clean]
  train:
    cmd: python src/train.py data/clean models/model.joblib
    deps: [data/clean, src/train.py]
    outs: [models/model.joblib]
    metrics: [metrics.json]
```

`dvc repro` re-runs only the stages whose dependencies changed — content-addressed by hash, not timestamp. The DAG is the lineage record: a model built today and a model built next quarter are bit-equivalent if the inputs are.

## Git LFS — When DVC Is Overkill

```bash
git lfs install
git lfs track "*.parquet" "*.h5" "*.bin" "*.safetensors"
git add .gitattributes
git add data/train.parquet
git commit -m "chore(data): add training data (LFS)"
git push
```

LFS is right when: you don't need pipelines, you don't need branchable data state, and the team is already comfortable with git. It is wrong when: you have multiple datasets, want lineage, or have files >2GB (LFS storage gets expensive fast).

## Hashing as a Cheap Pin (tracker-friendly)

If you use a tracker (MLflow, W&B), you don't always need a separate versioning tool — you can record a content hash:

```python
import hashlib
from pathlib import Path

def file_sha256(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()

data_hash = file_sha256(Path("data/train.parquet"))
# log this with the run, e.g., mlflow.set_tag("data_sha256", data_hash)
```

For multi-file datasets, hash a sorted manifest of `(relpath, hash, size)`. Two runs with the same manifest hash are using identical data — provable, no tool required.

## Logging Datasets to MLflow (real API)

MLflow has a real dataset-logging API as of MLflow 2.4+. The pattern is `mlflow.data.from_pandas` (or `from_numpy` / `from_huggingface`) → `log_input`:

```python
import mlflow
import mlflow.data
import pandas as pd

df = pd.read_parquet("data/train.parquet")
ds = mlflow.data.from_pandas(
    df,
    source="s3://my-org-ml-data/v1.4/train.parquet",
    name="fraud_training_v1.4",
    targets="label",
)
with mlflow.start_run():
    mlflow.log_input(ds, context="training")
    mlflow.set_tag("data_version", "v1.4")
    mlflow.set_tag("data_sha256", file_sha256(Path("data/train.parquet")))
    # ... rest of training
```

`mlflow.log_input` records dataset name, source URI, schema, and a profile (row count, column stats). It does *not* upload the bytes — that's DVC / lakeFS / your warehouse's job. MLflow stores the metadata; the actual data lives where it lives.

(Earlier versions of this skill referenced a `mlflow.log_dataset` function that does not exist. Use `mlflow.data.from_pandas` + `mlflow.log_input` instead.)

## lakeFS — Git-Like Branching at Lake Scale

```bash
# Branch the dataset for an experiment without copying bytes
lakectl branch create lakefs://ml-lake/exp-fraud-augmentation \
    --source lakefs://ml-lake/main

# Make changes on the branch
aws s3 cp augmented_train.parquet s3://ml-lake/exp-fraud-augmentation/data/

# Train against the branch URI
DATA_URI=s3://ml-lake/exp-fraud-augmentation/data/train.parquet python train.py

# Merge if it works, discard if it doesn't — no copies, just metadata
lakectl merge lakefs://ml-lake/exp-fraud-augmentation lakefs://ml-lake/main
```

lakeFS shines for parquet lakes where copying for experimentation would be prohibitive. The mental model is git — branch, commit, merge — applied to object storage.

## Versioning Schema Changes

A schema change is a version bump. Encode this explicitly:

```yaml
# data/schema.yaml
version: "1.4"
columns:
  - { name: user_id, type: string, nullable: false }
  - { name: amount,  type: float64, nullable: false }
  - { name: country, type: string, nullable: true }
breaking_changes_from_1_3:
  - "Removed column `legacy_id` (deprecated since v1.1)"
  - "country now nullable (was empty string)"
```

Pair this with a `pandera` schema that runs in CI. A pull request that changes the schema requires a schema version bump in the same commit.

## Dataset Registry Pattern

For >5 datasets, formalize:

```
datasets/
  fraud_training/
    DATASET_CARD.md
    schema.yaml
    versions/
      v1.4.dvc          → s3 pointer
      v1.3.dvc
    CHANGELOG.md
```

The `DATASET_CARD.md` (see `skill-data-collection`) describes provenance, license, biases. The `CHANGELOG.md` describes what changed between versions and why. Without these, datasets become folklore.

## Versioning at Inference Time

Production inference must record which model AND which dataset version produced predictions, so post-mortem audits are possible:

```python
# inside inference handler
log({
    "request_id": req_id,
    "model_version": MODEL_VERSION,
    "trained_on_data_version": MODEL_DATA_VERSION,
    "feature_set_version": FEATURE_SET_VERSION,
    "ts": now,
})
```

When something looks wrong in prod six months later, you'll want to be able to say "this model was trained on data v1.4, the schema was X, here's the validation report at the time."

## Common Failure Modes

| Pattern | Consequence |
|---|---|
| Putting a 5GB parquet in git directly | Repo clone takes 20 minutes forever; everyone hates the project |
| Hashing only the file path, not content | "Same dataset" with different content; reproducibility lies |
| Renaming files as versioning (`train_final.csv`) | Drift, ambiguity, "is this the one Sarah used in March?" |
| No schema check in CI | Silent breakage when a column is renamed upstream |
| DVC tracking notebooks that change every run | Pipeline reruns nothing useful; track outputs and inputs only |
| Pinning a model to "latest" data version | Today's prod model trained on different bytes than yesterday's |
| Storing PII in versioned data without encryption | Old versions retain PII forever; coordinate with `shared/skill-security` |
| Calling fabricated APIs (e.g., `mlflow.log_dataset`) | Code looks plausible, raises `AttributeError` at runtime |
| Versioning tool added but no team standard | Half the team uses DVC, half uses LFS, neither is consistent |
| Branching data with cp instead of lakeFS at lake scale | Doubling storage cost per experiment |

## Integration

- `skill-reproducibility` — code/env/seeds; this skill is the data half of the same problem
- `skill-experiment-tracking` — runs reference the data version; tracker stores the metadata
- `skill-data-preprocessing` — outputs of preprocessing should also be versioned
- `skill-data-collection` — DATASET_CARD lives here too; it's the human-readable companion
- `skill-mlops` — DVC pipelines and lakeFS branches plug into orchestrators
- `skill-monitoring` — drift is "data drift from version v1.4"; needs the version pinned
- `shared/skill-security` — large versioned datasets often contain PII; lifecycle management matters

## Resources

- [DVC docs](https://dvc.org/doc) — start with "Get Started"; the pipelines guide is essential
- [lakeFS docs](https://docs.lakefs.io/) — git-like branching for object stores
- [Git LFS docs](https://git-lfs.com/)
- [MLflow Datasets API](https://mlflow.org/docs/latest/python_api/mlflow.data.html) — the real `mlflow.data.*` interface
- [Hugging Face Datasets versioning](https://huggingface.co/docs/datasets/main/en/loading#hugging-face-hub) — `revision=` parameter
- [Datasheets for Datasets — Gebru et al.](https://arxiv.org/abs/1803.09010) — the dataset-card framework
- [Delta Lake / Iceberg comparison](https://lakefs.io/blog/delta-lake-vs-iceberg/) — for warehouse-scale time travel
