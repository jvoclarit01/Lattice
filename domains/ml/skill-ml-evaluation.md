---
name: skill-ml-evaluation
description: Rigorous offline ML evaluation — picking metrics that match the business cost, computing bootstrap confidence intervals, comparing models with statistical tests, and assessing calibration (Brier, ECE, reliability diagrams). Use when measuring model quality, comparing two candidate models, or producing numbers a stakeholder will defend in review. For production-time monitoring of these metrics see `skill-monitoring`; for fairness-stratified evaluation see `skill-bias-and-fairness`.
---

# ML Evaluation

A point estimate of accuracy is a guess. Without a confidence interval, a calibration check, and a statistical comparison to the alternative, you have a number on a slide — not evidence.

## When to Activate

Use when:
- Reporting model performance to stakeholders or in a paper
- Comparing two candidate models (champion vs challenger)
- Picking a threshold for a binary classifier
- Auditing whether a probabilistic model's probabilities are meaningful
- A reviewer asks "is that improvement statistically significant?"
- Designing an evaluation harness for a new project
- Multi-class problem and you don't know which average to use

**Trigger phrases:** "is this improvement real", "confidence interval", "bootstrap", "calibration", "Brier score", "ECE", "AUC", "macro vs micro F1", "model A vs model B", "statistical test", "evaluation pipeline".

## When NOT to Use

| Situation | Use instead |
|---|---|
| Production-time drift / quality monitoring | `skill-monitoring` |
| Choosing the model architecture | `skill-model-architecture` |
| Choosing the model class (RF vs XGB vs NN) | `skill-model-selection` |
| Hyperparameter optimization loop | `skill-training` |
| Fairness-stratified evaluation across groups | `skill-bias-and-fairness` |
| LLM/RAG evaluation (Ragas, LM-as-judge) | `skill-rag` or `skill-prompt-engineering` |
| Explaining individual predictions (SHAP, LIME) | `skill-explainability` |

## Iron Laws

1. **No point estimate without an interval.** Every reported metric gets a 95% CI. A model that's 0.82 ± 0.03 AUC and one that's 0.84 ± 0.04 AUC are not distinguishable; pretending otherwise is dishonest.
2. **Choose the metric before you see the test set.** Picking the metric that makes your model look best is `p-hacking`. The metric is part of the problem definition, not the result.
3. **Calibration matters whenever probabilities are used.** If downstream code uses `p > 0.5` or expects "70% means 70 out of 100", a model can be high-AUC and dangerously miscalibrated. Always check.

## Metric Selection by Problem

| Problem | Default metric | When to switch |
|---|---|---|
| Balanced binary classification | AUC-ROC + accuracy | If costs asymmetric → cost-weighted error |
| Imbalanced binary (≤10% positive) | AUC-PR (avg precision) | AUC-ROC over-promises on imbalanced data |
| Multi-class, balanced | Macro-F1, balanced accuracy | — |
| Multi-class, imbalanced | Macro-F1 (weights all classes equally) | Use weighted-F1 only if rare classes truly matter less |
| Probabilistic predictions consumed downstream | Brier score + ECE | AUC alone says nothing about probability quality |
| Regression, symmetric errors | RMSE | — |
| Regression, robust to outliers | MAE / median AE | When a few large errors shouldn't dominate |
| Regression on percentages / counts | MAPE / MASE | But MAPE breaks at y=0; check first |
| Ranking / search | NDCG@k, MAP@k | k = the number of items users actually see |
| Forecasting | sMAPE / MASE / pinball loss (quantile) | Pinball when quantile forecasts are required |

`accuracy` alone is almost always the wrong default. For a 99% imbalanced dataset, predicting the majority class gets 99% accuracy and zero value.

## Bootstrap Confidence Intervals

```python
import numpy as np
from sklearn.metrics import roc_auc_score

def bootstrap_ci(
    y_true: np.ndarray,
    y_score: np.ndarray,
    metric_fn=roc_auc_score,
    n_boot: int = 2000,
    alpha: float = 0.05,
    seed: int = 42,
) -> dict:
    """Percentile bootstrap CI for any metric_fn(y_true, y_score)."""
    rng = np.random.default_rng(seed)
    n = len(y_true)
    boot = np.empty(n_boot)
    for i in range(n_boot):
        idx = rng.integers(0, n, n)
        # Resample preserves the joint (y_true, y_score) distribution
        boot[i] = metric_fn(y_true[idx], y_score[idx])
    lo, hi = np.quantile(boot, [alpha / 2, 1 - alpha / 2])
    return {
        "estimate": float(metric_fn(y_true, y_score)),
        "ci_low": float(lo),
        "ci_high": float(hi),
        "n_boot": n_boot,
    }

# Usage
result = bootstrap_ci(y_test, y_proba, metric_fn=roc_auc_score)
print(f"AUC = {result['estimate']:.3f} (95% CI {result['ci_low']:.3f}–{result['ci_high']:.3f})")
```

Bootstrap is the right default because it works for any metric (AUC, F1, NDCG, MAPE) without requiring a closed-form variance. For very small test sets (n < 100), the bootstrap underestimates uncertainty; use stratified bootstrap and report sample size.

## Comparing Two Models — Paired Bootstrap

A common error: bootstrap CI of model A and bootstrap CI of model B, then check if they overlap. Non-overlapping CIs ⇒ different. *Overlapping CIs do not imply equivalence.* The correct test is paired:

```python
def paired_bootstrap(
    y_true: np.ndarray,
    score_a: np.ndarray,
    score_b: np.ndarray,
    metric_fn=roc_auc_score,
    n_boot: int = 2000,
    seed: int = 42,
) -> dict:
    """Test the paired difference metric_fn(B) - metric_fn(A) on the same resamples."""
    rng = np.random.default_rng(seed)
    n = len(y_true)
    diffs = np.empty(n_boot)
    for i in range(n_boot):
        idx = rng.integers(0, n, n)
        diffs[i] = metric_fn(y_true[idx], score_b[idx]) - metric_fn(y_true[idx], score_a[idx])
    lo, hi = np.quantile(diffs, [0.025, 0.975])
    p_b_better = float((diffs > 0).mean())
    return {
        "delta_estimate": float(metric_fn(y_true, score_b) - metric_fn(y_true, score_a)),
        "delta_ci": (float(lo), float(hi)),
        "prob_b_better": p_b_better,
    }
```

Significance check: the CI for the *difference* excludes 0. For paired classification accuracy specifically, McNemar's test is the textbook choice and is exact for small samples (`scipy.stats.contingency.mcnemar`).

## Calibration

A model is calibrated if among predictions of `0.7`, about 70% are positives. This is independent of AUC — a perfect AUC model can be wildly miscalibrated.

### Brier Score (proper scoring rule)

```python
from sklearn.metrics import brier_score_loss
brier = brier_score_loss(y_true, y_proba)
# Lower is better. Ranges 0 (perfect) to 1; for balanced data baseline = 0.25
```

### Expected Calibration Error (ECE)

```python
import numpy as np

def expected_calibration_error(y_true: np.ndarray, y_proba: np.ndarray,
                               n_bins: int = 10) -> float:
    bins = np.linspace(0, 1, n_bins + 1)
    bin_idx = np.digitize(y_proba, bins) - 1
    bin_idx = np.clip(bin_idx, 0, n_bins - 1)
    ece = 0.0
    for b in range(n_bins):
        mask = bin_idx == b
        if not mask.any():
            continue
        avg_pred = y_proba[mask].mean()
        true_rate = y_true[mask].mean()
        ece += (mask.sum() / len(y_true)) * abs(avg_pred - true_rate)
    return float(ece)
```

ECE < 0.05 is "well calibrated" for most consumer applications; medical/financial may demand < 0.02.

### Reliability Diagram

```python
import matplotlib.pyplot as plt

def reliability_diagram(y_true, y_proba, n_bins=10, ax=None):
    bins = np.linspace(0, 1, n_bins + 1)
    bin_idx = np.clip(np.digitize(y_proba, bins) - 1, 0, n_bins - 1)
    xs, ys, ns = [], [], []
    for b in range(n_bins):
        mask = bin_idx == b
        if mask.sum() < 5:        # skip near-empty bins
            continue
        xs.append(y_proba[mask].mean())
        ys.append(y_true[mask].mean())
        ns.append(mask.sum())
    ax = ax or plt.gca()
    ax.plot([0, 1], [0, 1], "--", color="gray", label="perfect")
    ax.plot(xs, ys, "o-", label="model")
    ax.set_xlabel("predicted probability")
    ax.set_ylabel("observed positive rate")
    ax.legend()
    return ax
```

If the curve sags below the diagonal, the model is overconfident; above, under-confident. Apply Platt scaling or isotonic regression (`sklearn.calibration.CalibratedClassifierCV`) on a held-out calibration set.

## Multi-Class Handling

```python
from sklearn.metrics import f1_score, roc_auc_score, classification_report

# Macro: simple average over classes — treats all classes equally
f1_macro = f1_score(y_true, y_pred, average="macro")
# Weighted: weighted by class support — biased toward majority class
f1_weighted = f1_score(y_true, y_pred, average="weighted")
# Micro: treats every prediction as one outcome — equals accuracy in single-label
f1_micro = f1_score(y_true, y_pred, average="micro")

# AUC for multi-class needs an explicit scheme
auc_ovr = roc_auc_score(y_true, y_proba, multi_class="ovr", average="macro")
auc_ovo = roc_auc_score(y_true, y_proba, multi_class="ovo", average="macro")

print(classification_report(y_true, y_pred, digits=3))
```

| Average | Use when |
|---|---|
| `macro` | All classes equally important (default for imbalanced) |
| `weighted` | Class importance scales with frequency (rarely a real requirement) |
| `micro` | Multi-label setting, or you really mean accuracy |

For very rare classes, `support` per class in `classification_report` is the most useful column — small support ⇒ huge variance in F1.

## Threshold Selection

Default 0.5 is rarely right. Pick the threshold that optimizes the business metric on a *validation* set, then evaluate on test:

```python
from sklearn.metrics import precision_recall_curve

p, r, thr = precision_recall_curve(y_val, y_proba_val)
# Suppose minimum precision = 0.8 is required
ok = p[:-1] >= 0.8
best_thr = thr[ok][np.argmax(r[:-1][ok])] if ok.any() else 1.0
```

Then **lock the threshold** before touching test data. Tuning the threshold on test inflates every reported metric.

## Validation Strategy by Data Type

| Data | Use |
|---|---|
| IID, single timepoint | Stratified k-fold |
| Time series | `TimeSeriesSplit` (forward chaining); never random splits |
| Grouped (patient, user, store) | `GroupKFold` so a group never spans train/val |
| Stratified time + group | Custom: time-cutoff per group |
| Tiny dataset (< 1000) | Repeated stratified k-fold + report mean ± std |

## Common Failure Modes

| Pattern | Consequence |
|---|---|
| Reporting accuracy on imbalanced data | Hides catastrophic minority-class failure |
| Comparing models with overlapping CIs and concluding "tied" | Statistical error; use paired test on the difference |
| Tuning threshold on test set | Inflates precision/recall by 1–5pp |
| AUC-ROC on highly imbalanced data | Looks great because TNR dominates; use AUC-PR |
| `classification_report` without inspecting per-class support | Macro-F1 dominated by classes with n=3 in test |
| Reporting one seed | Result is noise; report mean across ≥5 seeds with std |
| Ignoring calibration | Threshold-based decisions miscalibrated; downstream costs wrong |
| Bootstrap on a non-IID test set | CIs underestimated; use block bootstrap for time series |
| Comparing model trained on v1 data to model trained on v2 data | Apples to oranges; pin the dataset version |
| `train_test_split` on time-series data | Future leaks into past; metrics are unrealistic |

## Reporting Template

For every model in a report:

```
Model: <name + git_sha>
Dataset: <dataset_name v1.4>
Test n: 12,431 | Eval seed: 42

Primary metric:
  AUC-PR = 0.741  (95% CI 0.728–0.755, paired bootstrap n=2000)

Secondary:
  AUC-ROC = 0.892  (CI 0.884–0.901)
  F1 @ thr=0.32 = 0.621  (CI 0.611–0.631)

Calibration:
  Brier = 0.142
  ECE   = 0.038 (10 bins)

Vs baseline (logistic regression):
  ΔAUC-PR = +0.084  (CI +0.069 – +0.099, prob_better = 0.999)

Subgroups (see skill-bias-and-fairness): … (separately reported)
```

## Integration

- `skill-monitoring` — runs these metrics live on production traffic
- `skill-model-selection` — uses these metrics to pick a model class
- `skill-bias-and-fairness` — same metrics, stratified by protected attributes
- `skill-rag` — RAG-specific eval (faithfulness, context relevance) builds on this
- `skill-explainability` — when stakeholders need to understand *why* the metric moved
- `skill-experiment-tracking` — log eval metrics + CIs alongside hyperparams
- `skill-mlops` — eval gate in CI/CD uses thresholds from this skill
- `shared/skill-tdd` — fixture-based eval suites are TDD for models

## Resources

- [scikit-learn model evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html) — exhaustive metric reference
- [On Calibration of Modern Neural Networks — Guo et al.](https://arxiv.org/abs/1706.04599) — the canonical ECE / temperature-scaling paper
- [Statistical Comparisons of Classifiers — Demšar](https://www.jmlr.org/papers/v7/demsar06a.html) — the textbook reference for multi-model comparison
- [`sklearn.calibration` docs](https://scikit-learn.org/stable/modules/calibration.html)
- [Bootstrap methods — Efron & Tibshirani](https://www.crcpress.com/An-Introduction-to-the-Bootstrap/Efron-Tibshirani/p/book/9780412042317) (book)
- [Cleverhans on data leakage in eval](https://www.cleverhans.io/) — common eval pitfalls
