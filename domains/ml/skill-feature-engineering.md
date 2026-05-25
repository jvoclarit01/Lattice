---
name: skill-feature-engineering
description: Building, transforming, and selecting features without leaking information from the future or the test set. Covers numerical/categorical/temporal/text features, target/frequency encoding done leak-free, interaction terms, and feature stores. Use when designing features, when accuracy on training is dramatically better than on validation, or when reviewing a notebook for hidden leakage. For raw cleaning before features see `skill-data-preprocessing`; for feature stores at production scale see `skill-mlops`.
---

# Feature Engineering

The most expensive bug in ML is a feature that reads the future. It boosts every offline metric, ships, and then degrades the moment it meets data it didn't train on. This skill is about building features that survive deployment.

## When to Activate

Use when:
- Designing the feature set for a new model
- Encoding high-cardinality categorical columns
- Creating temporal features (lags, rolling windows, seasonality)
- Reviewing a notebook for leakage (offline metric ≫ deployed metric)
- Adding a feature store or moving feature logic out of training notebooks
- Deciding which of 200 candidate features to keep

**Trigger phrases:** "target encoding", "leakage", "offline metric is too good", "rolling features", "feature store", "high cardinality", "train and test got different columns", "interaction features".

## When NOT to Use

| Situation | Use instead |
|---|---|
| Cleaning raw data (missing, outliers, duplicates) | `skill-data-preprocessing` |
| Picking the model that consumes these features | `skill-model-selection` |
| Versioning the feature set itself | `skill-data-versioning` |
| Feature attribution / SHAP for an existing model | `skill-explainability` |
| Production feature store ops (Feast, Tecton) | `skill-mlops` |
| Auditing fairness implications of a feature | `skill-bias-and-fairness` |

## Iron Laws

1. **Fit on train, transform on test.** Every fitted statistic — mean, scale, target mean, vocabulary, PCA components — comes from training data only. Anything else is leakage.
2. **Time-aware features must respect time.** Lag, rolling, and target-aggregate features computed across the full series leak the future into training rows. Use `expanding`, `rolling` with proper offsets, or `groupby(...).shift()`.
3. **A feature that requires the target to compute belongs in a cross-fold pipeline.** Naive target encoding = leakage. There is no "I'll be careful" exception; encode it correctly or pick a different encoding.

## Numerical Features

```python
import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import Pipeline

# Polynomial (interactions only avoids the squared explosion)
poly = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)

# Domain-driven interactions are usually better than blind PolynomialFeatures
def add_interactions(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["price_per_sqft"] = df["price"] / df["sqft"].clip(lower=1)
    df["log_income"] = np.log1p(df["income"])
    return df

# Wrap in a Pipeline so fitting on train only is enforced
num_pipe = Pipeline([
    ("scale", StandardScaler()),
])
```

`clip(lower=1)` prevents division-by-zero from polluting `inf` into the feature; `log1p` handles zeros gracefully.

## Categorical Features — Leak-Free Target Encoding

This is the section most projects get wrong. The naive form below **leaks the label** because each row's encoded value contains its own target.

```python
# DEFECT — DO NOT DO THIS
df["category_encoded"] = df.groupby("category")["target"].transform("mean")
# Each row's value is computed including its own target, so a model can
# trivially recover the label. Validation looks great; production tanks.
```

The leak-free form uses out-of-fold encoding: for each row in fold k, the encoded value is computed from rows in folds ≠ k.

```python
from sklearn.model_selection import KFold
import numpy as np
import pandas as pd

def kfold_target_encode(
    df: pd.DataFrame,
    cat_col: str,
    target_col: str,
    n_splits: int = 5,
    smoothing: float = 10.0,
    seed: int = 42,
) -> pd.Series:
    """Out-of-fold target encoding. Safe to use on training data."""
    encoded = pd.Series(np.nan, index=df.index, dtype=float)
    global_mean = df[target_col].mean()
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=seed)
    for tr_idx, val_idx in kf.split(df):
        tr, val = df.iloc[tr_idx], df.iloc[val_idx]
        agg = tr.groupby(cat_col)[target_col].agg(["mean", "count"])
        # Bayesian smoothing: pull rare categories toward the global mean
        agg["smoothed"] = (
            agg["count"] * agg["mean"] + smoothing * global_mean
        ) / (agg["count"] + smoothing)
        encoded.iloc[val_idx] = val[cat_col].map(agg["smoothed"]).fillna(global_mean)
    return encoded

# For test data: fit ONE encoding on the full training set, apply to test
def fit_target_encoder(train: pd.DataFrame, cat_col: str, target_col: str,
                      smoothing: float = 10.0) -> dict:
    global_mean = train[target_col].mean()
    agg = train.groupby(cat_col)[target_col].agg(["mean", "count"])
    smoothed = (agg["count"] * agg["mean"] + smoothing * global_mean) / (agg["count"] + smoothing)
    return {"map": smoothed.to_dict(), "global_mean": global_mean}

def apply_target_encoder(s: pd.Series, encoder: dict) -> pd.Series:
    return s.map(encoder["map"]).fillna(encoder["global_mean"])
```

**Use `kfold_target_encode` for the training set, `fit_target_encoder` + `apply_target_encoder` for test/inference.** Never call `groupby(...).transform("mean")` on the target. If you remember one thing from this skill, remember that.

For most cases, `category_encoders.TargetEncoder` from the `category_encoders` package implements this correctly out of the box and is the recommended default.

## Other Categorical Encodings

| Encoding | When | Watch for |
|---|---|---|
| **One-hot** | Low cardinality (<~20), no order | Memory blow-up at high cardinality |
| **Ordinal** | True order exists (S < M < L) | Don't use for nominal categories |
| **Frequency** | High cardinality, frequency is informative | Leakage if computed on full set; fit on train only |
| **Target / mean** | High cardinality, target signal | Use OOF or hold-out; never naive `.transform("mean")` |
| **Hashing** | Very high cardinality, online learning | Collisions; less interpretable |
| **Embedding** | Deep models, very high cardinality | Needs enough data; treat as a learned layer |

## Temporal Features (Time-Series Leakage Trap)

```python
def add_lag_features(df: pd.DataFrame, group: str, target: str,
                     lags: list[int]) -> pd.DataFrame:
    df = df.sort_values([group, "date"]).copy()
    for k in lags:
        df[f"{target}_lag_{k}"] = df.groupby(group)[target].shift(k)
    return df

def add_rolling_features(df: pd.DataFrame, group: str, target: str,
                         windows: list[int]) -> pd.DataFrame:
    df = df.sort_values([group, "date"]).copy()
    for w in windows:
        # shift(1) BEFORE rolling — prevents the current row leaking into its own window
        df[f"{target}_roll_mean_{w}"] = (
            df.groupby(group)[target]
              .shift(1)
              .rolling(w, min_periods=1)
              .mean()
              .reset_index(level=0, drop=True)
        )
    return df
```

The `shift(1)` before `rolling` is what makes this not-leakage. A rolling window that *includes* the current row reads the target during inference, which won't be available in production.

For seasonality:

```python
df["dow"] = df["date"].dt.dayofweek
df["month"] = df["date"].dt.month
# Cyclic encoding for tree-models is unnecessary; for linear/NN models:
df["dow_sin"] = np.sin(2 * np.pi * df["dow"] / 7)
df["dow_cos"] = np.cos(2 * np.pi * df["dow"] / 7)
```

## Text Features

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

text_pipe = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=50_000, ngram_range=(1, 2),
                              min_df=2, sublinear_tf=True)),
    ("clf", LogisticRegression(max_iter=1000, C=1.0)),
])
text_pipe.fit(X_train_text, y_train)
# IMPORTANT: never call vectorizer.fit on the full dataset, only on X_train
```

For modern NLP, sentence-transformer embeddings (e.g., `sentence-transformers/all-MiniLM-L6-v2`) usually beat TF-IDF as features for downstream classifiers. Cache embeddings — recomputing them per training run is the most common feature-engineering cost-sink.

## Feature Selection

```python
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.ensemble import RandomForestClassifier

# Filter (fast, model-agnostic)
sel = SelectKBest(mutual_info_classif, k=20)
sel.fit(X_train, y_train)

# Embedded (uses the model itself)
rf = RandomForestClassifier(n_estimators=200, random_state=42).fit(X_train, y_train)
importances = pd.Series(rf.feature_importances_, index=X_train.columns).sort_values(ascending=False)

# Permutation importance — preferred over `feature_importances_` for trees;
# unbiased toward high-cardinality features
from sklearn.inspection import permutation_importance
perm = permutation_importance(rf, X_val, y_val, n_repeats=10, random_state=42)
```

`feature_importances_` from tree models is biased toward high-cardinality features. Permutation importance on validation data is more honest — and the version to report to stakeholders.

## Feature Pipelines (the production-safe shape)

```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

num_features = ["age", "income", "tenure"]
cat_features = ["region", "plan_type"]

preprocess = ColumnTransformer([
    ("num", Pipeline([("impute", SimpleImputer(strategy="median")),
                      ("scale", StandardScaler())]), num_features),
    ("cat", Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                      ("ohe", OneHotEncoder(handle_unknown="ignore"))]), cat_features),
])

full = Pipeline([("pre", preprocess), ("clf", RandomForestClassifier())])
full.fit(X_train, y_train)            # statistics computed on train only
y_pred = full.predict(X_test)         # test transformed with train statistics
```

Wrapping everything in a `Pipeline` is what enforces "fit on train, transform on test." Manual `df["x"] = ...` outside the pipeline is where leakage sneaks back in.

## Feature Store Decision

| Need | Pick |
|---|---|
| Single notebook, one model | No store; just functions in a module |
| Several models reuse features | Internal Python module + DVC-versioned parquet |
| Online inference + batch scoring need same features | Feast (open source) or Tecton (managed) |
| Heavily streaming, low-latency online features | Tecton, Hopsworks, or warehouse + Redis cache |

Don't reach for Feast on day one. The "online/offline skew" problem it solves only exists once you have an online inference path.

## Common Failure Modes

| Pattern | Consequence |
|---|---|
| `groupby(cat).transform("mean")` on the target | Leakage; offline AUC ~0.99, prod ~0.7 |
| `StandardScaler().fit(X)` then split | Test-set means leak into training |
| Rolling window includes the current row | Future leaks into past at training time |
| One-hot encoding fit on train, test has new categories | KeyError or silent drop; use `handle_unknown="ignore"` |
| Imputing missing values with full-data mean | Test info leaks back through the imputed values |
| Train/test feature lists drift over time | Inference fails with "shape mismatch" in prod |
| Encoding logic in notebook, not in a callable pipeline | Production reimplements it slightly differently — skew |
| Using `feature_importances_` from trees as the importance story | Bias toward high-cardinality features misleads stakeholders |
| TF-IDF / vocabulary fit on train+test combined | Vocabulary leakage; rare on text but devastating |

## Integration

- `skill-data-preprocessing` — produces the cleaned input this skill consumes
- `skill-model-selection` — model class influences which features matter (trees vs linear vs NN)
- `skill-explainability` — SHAP/permutation importance for explaining what features drive predictions
- `skill-bias-and-fairness` — proxy variables (zipcode → race) often hide here; audit features for disparate impact
- `skill-data-versioning` — pin the feature set version with the model
- `skill-mlops` — feature store and offline/online consistency
- `skill-reproducibility` — fitted preprocessors must be saved alongside model weights

## Resources

- [Feature Engineering for Machine Learning — Zheng & Casari](https://www.oreilly.com/library/view/feature-engineering-for/9781491953235/) — the practical reference
- [category_encoders docs](https://contrib.scikit-learn.org/category_encoders/) — production-quality TargetEncoder, CatBoostEncoder, etc.
- [Feast feature store](https://docs.feast.dev/) — open source, when you actually need a store
- [scikit-learn ColumnTransformer guide](https://scikit-learn.org/stable/modules/compose.html#columntransformer-for-heterogeneous-data)
- [Kaggle: target encoding without leakage](https://www.kaggle.com/code/ryanholbrook/target-encoding) — practical walkthrough
