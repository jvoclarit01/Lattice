---
name: skill-data-preprocessing
description: Cleaning and transforming raw tabular data for ML — handling missing values, outliers, duplicates, scaling, encoding, and avoiding train/test leakage. Use when preparing a dataset for modeling, when fixing a notebook that's mutating dataframes inconsistently, or when a model trained great offline but tanked in production. For creating new features from cleaned data see `skill-feature-engineering`; for collecting raw data in the first place see `skill-data-collection`.
---

# Data Preprocessing

Preprocessing is where ML projects die quietly. A misplaced `fit_transform` on the test set, a `dropna()` that silently doesn't mutate, an imputed mean from the full dataset — none crash; all corrupt the result. The discipline is to make every transformation reproducible, leak-free, and saved alongside the model.

## When to Activate

Use when:
- Cleaning a freshly collected dataset before modeling
- Building the preprocessing layer for a training pipeline
- Diagnosing a "model great offline, terrible in production" bug
- Writing inference-time preprocessing that must match training-time
- Reviewing a notebook for hidden mutations (`df.dropna()` without assignment)
- Choosing imputation strategies (mean, median, model-based)

**Trigger phrases:** "missing values", "outliers", "drop duplicates", "fit_transform", "data leakage", "scaling", "imputation", "preprocessing pipeline", "production prediction differs from offline".

## When NOT to Use

| Situation | Use instead |
|---|---|
| Designing new features (interactions, encodings, target stats) | `skill-feature-engineering` |
| Sourcing the data in the first place | `skill-data-collection` |
| Versioning the cleaned dataset | `skill-data-versioning` |
| Choosing the model that will consume this data | `skill-model-selection` |
| Auditing fairness implications of cleaning choices | `skill-bias-and-fairness` |
| Big-data ETL at warehouse scale (Spark, dbt) | `webdev/skill-database` (with this skill for ML-specific concerns) |

## Iron Laws

1. **Fit on train, transform on everything.** Every fitted statistic — mean, median, scale, vocabulary, IQR cutoffs — comes from the training set. Computing it on `train + test` or on the full dataframe before splitting is leakage. Always.
2. **Pandas operations are not in-place by default.** `df.dropna()` returns a new dataframe and discards it. Either reassign (`df = df.dropna()`) or use `inplace=True`. Reading a notebook that does neither is reading a bug.
3. **Save the fitted preprocessor with the model.** Inference-time preprocessing must apply the same fitted transformer (same scaler, same encoder, same imputer) the model was trained with. Recomputing at inference = silent skew.

## The Leakage Trap (Iron Law #1, with code)

```python
# DEFECT — DO NOT DO THIS
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)               # FIT on full data — leaks test info
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2)
# By the time you split, the scaler has seen test means and stds. Metrics inflated.
```

```python
# CORRECT — fit on train only
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)        # fit + transform on train
X_test_s  = scaler.transform(X_test)             # transform only on test

# At inference: load the same scaler, call .transform()
import joblib
joblib.dump(scaler, "scaler.joblib")
```

The seemingly-tiny difference between `fit_transform` and `transform` is the difference between a leak-free pipeline and a deployment-time disaster. Wrapping everything in a `Pipeline` (below) makes this impossible to forget.

## The Mutation Trap (Iron Law #2, with code)

```python
# DEFECT — these do nothing to df
df.dropna()                                       # returns new df, discarded
df.fillna(0)                                      # returns new df, discarded
df.drop_duplicates()                              # returns new df, discarded
```

```python
# CORRECT — pick one of these, consistently
df = df.dropna()
df = df.fillna({"age": df["age"].median()})
df = df.drop_duplicates(subset=["user_id", "ts"])

# OR (less idiomatic, harder to chain):
df.dropna(inplace=True)
df.fillna({"age": df["age"].median()}, inplace=True)
df.drop_duplicates(subset=["user_id", "ts"], inplace=True)
```

Mixing styles inside one notebook ("sometimes I assign, sometimes inplace") is the bug pattern. Pick assignment and stick to it — `inplace=True` is being deprecated in newer pandas anyway.

## Missing Values

| Strategy | When | Watch for |
|---|---|---|
| Drop rows | <5% missing, missingness is random | Drops can introduce selection bias |
| Drop column | >50% missing or feature unavailable at inference | Lose the signal in the remaining data |
| Constant fill (0, "Unknown") | Domain meaning of "absent" is real | Distorts statistics if many rows |
| Mean / median impute | Numeric, MAR (missing at random) | Median > mean for skewed data; fit on train only |
| Mode impute | Categorical | Inflates the mode count |
| KNN / iterative impute | Few features, MNAR plausible | Slow; can overfit; needs scaling first |
| Indicator + impute | Missingness is informative | Adds `is_missing_x` column; usually beats impute alone |

```python
import pandas as pd
from sklearn.impute import SimpleImputer

# Indicator + impute pattern (recommended default)
def impute_with_indicator(train: pd.DataFrame, test: pd.DataFrame,
                          col: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    train = train.copy()
    test = test.copy()
    train[f"{col}_was_missing"] = train[col].isna().astype(int)
    test[f"{col}_was_missing"]  = test[col].isna().astype(int)
    imp = SimpleImputer(strategy="median")
    train[[col]] = imp.fit_transform(train[[col]])
    test[[col]]  = imp.transform(test[[col]])
    return train, test, imp                       # save imp for inference
```

## Outliers

```python
import numpy as np

def iqr_clip(df: pd.DataFrame, col: str, k: float = 1.5) -> pd.DataFrame:
    """Clip (don't drop) outliers using IQR fences. Compute on TRAIN data only;
    pass the bounds in for test data."""
    q1, q3 = df[col].quantile([0.25, 0.75])
    iqr = q3 - q1
    lo, hi = q1 - k * iqr, q3 + k * iqr
    return df.assign(**{col: df[col].clip(lo, hi)}), (lo, hi)

train, bounds = iqr_clip(train, "income")
test = test.assign(income=test["income"].clip(*bounds))
```

Clip rather than drop — dropping shrinks the dataset and biases evaluation. The bounds come from training data only; applying them to test is just clipping, not leakage.

For high-dimensional data, `IsolationForest` or `LocalOutlierFactor` find multivariate outliers a univariate IQR misses. Treat them as `is_outlier` indicators, not as rows to remove.

## Duplicates

```python
# Exact duplicates
df = df.drop_duplicates()

# Logical duplicates: same entity, possibly different irrelevant columns
df = df.drop_duplicates(subset=["user_id", "transaction_ts"], keep="last")

# Near-duplicates (text): use minhash or hash buckets
# Production: datasketch.MinHash + LSH for >1M strings
```

For text datasets, near-duplicate removal (cosine similarity > 0.95 on embeddings, or MinHash) prevents the same article appearing in train and test under slightly different titles — a stealthy form of leakage.

## Scaling and Standardization

| Scaler | Use when |
|---|---|
| `StandardScaler` | Features approximately normal; default for linear / NN |
| `MinMaxScaler` | Bounded range needed (e.g., neural-net inputs in [0,1]) |
| `RobustScaler` | Heavy-tailed data; uses median + IQR |
| `Normalizer` | Per-row L2 norm (text TF-IDF rows often) |
| None | Tree models — they don't need scaling |

```python
from sklearn.preprocessing import RobustScaler
scaler = RobustScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)
```

## Encoding

```python
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder

# One-hot — low cardinality, no order
ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
ohe.fit(X_train[["region"]])
X_train_oh = ohe.transform(X_train[["region"]])
X_test_oh  = ohe.transform(X_test[["region"]])

# Ordinal — true order exists; otherwise use one-hot
ord_enc = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1,
                         categories=[["S", "M", "L", "XL"]])
```

Always set `handle_unknown` — at inference time, a category unseen during training will otherwise raise. For richer encodings (target, frequency, hashing) see `skill-feature-engineering`.

## The Pipeline Pattern (production-safe shape)

This is the form preprocessing should take in any project that ships:

```python
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import GradientBoostingClassifier
import joblib

num_cols = ["age", "income", "tenure"]
cat_cols = ["region", "plan_type"]

preprocess = ColumnTransformer([
    ("num", Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ]), num_cols),
    ("cat", Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("ohe",    OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ]), cat_cols),
])

pipeline = Pipeline([
    ("pre", preprocess),
    ("clf", GradientBoostingClassifier()),
])

pipeline.fit(X_train, y_train)             # statistics fit on train only
y_pred = pipeline.predict(X_test)          # test transformed with train stats
joblib.dump(pipeline, "model.joblib")      # one artifact: preprocessing + model
```

Three properties this enforces:
1. Leakage is structurally impossible (`fit` only sees train).
2. The fitted preprocessor travels with the model — load `model.joblib` at inference and you're done.
3. Schema mismatches at inference fail loudly instead of silently producing garbage.

## Validation

After preprocessing, assert what you expect:

```python
import pandera as pa

schema = pa.DataFrameSchema({
    "age":      pa.Column(float, pa.Check.in_range(0, 120)),
    "income":   pa.Column(float, pa.Check.greater_than_or_equal_to(0)),
    "region":   pa.Column(str, pa.Check.isin(["NA", "EU", "APAC"])),
})
schema.validate(X_train)            # raises if violated
```

Schema validation belongs in CI and at the start of training. Catches drift between data versions before it eats a training run.

## Common Failure Modes

| Pattern | Consequence |
|---|---|
| `df.dropna()` with no reassignment | Silent no-op; rows you "cleaned" still in the data |
| `scaler.fit(X)` before split | Test means leak into training; AUC inflated |
| Different preprocessing in train vs inference scripts | Production scores skewed; classic "works offline" bug |
| `OneHotEncoder` with default `handle_unknown="error"` | Inference crashes on a new category |
| Mean imputation on a long-tail / log-normal feature | Imputed values pull the distribution; use median or model-based |
| Drop outliers from train AND test | Test no longer represents reality; metrics optimistic |
| Computing IQR / bounds on full dataset | Same leakage as scalers |
| Not saving the fitted preprocessor | Can't reproduce inference; reverse-engineering it is painful |
| Treating numeric IDs as features | Model learns spurious patterns; cast to category or drop |
| Forgetting `random_state` on `train_test_split` | Different splits each run; can't reproduce metrics |

## Integration

- `skill-feature-engineering` — operates on the cleaned data this skill produces
- `skill-data-versioning` — every cleaned dataset gets a version pin
- `skill-data-collection` — raw inputs come from here
- `skill-bias-and-fairness` — preprocessing choices (drop missing, impute) can amplify or mask disparate impact
- `skill-mlops` — preprocessing pipelines are first-class steps in orchestrated DAGs
- `skill-reproducibility` — fitted preprocessors are part of the reproducible artifact set
- `shared/skill-tdd` — schema tests on inputs are the TDD form of preprocessing

## Resources

- [scikit-learn preprocessing guide](https://scikit-learn.org/stable/modules/preprocessing.html)
- [scikit-learn ColumnTransformer + Pipeline](https://scikit-learn.org/stable/modules/compose.html)
- [Pandera dataframe schemas](https://pandera.readthedocs.io/) — declarative validation
- [Great Expectations](https://docs.greatexpectations.io/) — heavier-weight data validation suite
- [Pandas Cookbook — handling missing data](https://pandas.pydata.org/docs/user_guide/missing_data.html)
- [Effect of imputation on bias — Schafer & Graham](https://methodology.psu.edu/) — the foundational missingness reference
