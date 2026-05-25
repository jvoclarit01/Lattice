---
name: skill-explainability
description: Model explainability and ML results interpretation. Use when explaining model decisions, computing feature attributions (SHAP, LIME), running error analysis, or communicating ML outputs to stakeholders. Covers technical explanation methods AND interpreting/communicating the results those methods produce.
---

# Explainability & Results Interpretation

Two activities, one skill: (1) explaining how a model reaches a decision, and (2) interpreting what those explanations mean for stakeholders.

## When to Activate

Use when:
- Computing feature attributions (SHAP, LIME, permutation importance)
- Diagnosing why a specific prediction was made
- Running error analysis on misclassifications or large residuals
- Producing a model card, audit report, or stakeholder-facing explanation
- Comparing global vs local explanations
- Validating that a model's decisions are defensible (regulatory, ethical, scientific)

## When NOT to Use

- Pure model evaluation (accuracy, AUC, calibration) — use `skill-ml-evaluation`
- Fairness audits across protected groups — use `skill-bias-and-fairness`
- Writing the "Results" section of a thesis or paper — use `thesis/skill-results-writing`
- Deciding which model to ship — use `skill-model-selection`

## Iron Laws

1. **Correlation in an explanation is not causation in the world.** SHAP tells you what the model relied on, not what actually causes the outcome. Never present feature importance as a causal claim.
2. **Local ≠ global.** A feature with low global importance can dominate a single prediction; a globally important feature can be irrelevant for a given case. Pick the right scope for the question being asked.
3. **Validate every explanation against held-out behavior.** A SHAP value that contradicts test-set patterns is a bug, not an insight.

## Method Selection

| Question | Method | Notes |
|---|---|---|
| "Why did the model predict X for *this* row?" | LIME, SHAP local, counterfactuals | Local methods |
| "Which features matter overall?" | SHAP summary, permutation importance | Global methods |
| "Does feature F have a monotonic effect?" | PDP, ICE plots, SHAP dependence | Direction & shape |
| "What change to the input flips the prediction?" | Counterfactuals, anchors | Actionable insight |
| "Where does the model fail systematically?" | Error analysis (below) | Diagnostic |

## Core Methods

### SHAP — Global + Local

```python
import shap

explainer = shap.TreeExplainer(model)            # use Explainer() for non-tree models
shap_values = explainer.shap_values(X_test)

shap.summary_plot(shap_values, X_test)            # global feature impact
shap.dependence_plot('feature', shap_values, X_test)  # marginal effect
shap.force_plot(explainer.expected_value, shap_values[0], X_test.iloc[0])  # local
```

For deep models use `shap.DeepExplainer` or `shap.GradientExplainer`. For arbitrary models use the model-agnostic `shap.KernelExplainer` (slow but works on anything).

### LIME — Local Surrogates

```python
import lime.lime_tabular

explainer = lime.lime_tabular.LimeTabularExplainer(
    X_train.values,
    feature_names=feature_names,
    class_names=class_names,
    mode='classification',
)

explanation = explainer.explain_instance(
    X_test.iloc[0].values,
    model.predict_proba,
    num_features=5,
)
explanation.show_in_notebook(show_table=True)
```

LIME fits a local linear surrogate. It is fast and intuitive but unstable across runs — average over multiple seeds before presenting.

### Permutation Importance — Model-Agnostic Global

```python
from sklearn.inspection import permutation_importance

result = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=0)
sorted_idx = result.importances_mean.argsort()[::-1]
```

Robust to model type. Slower than tree-based importance but does not suffer from the cardinality bias of impurity-based importances.

### Built-In Feature Importance

```python
import matplotlib.pyplot as plt
import numpy as np

importances = model.feature_importances_
indices = np.argsort(importances)[::-1]

plt.figure(figsize=(10, 6))
plt.title('Feature Importance')
plt.bar(range(len(importances)), importances[indices])
plt.xticks(range(len(importances)), np.array(feature_names)[indices], rotation=90)
plt.tight_layout()
plt.show()
```

Tree-based `feature_importances_` is biased toward high-cardinality features. Prefer permutation importance for honest comparisons.

## Error Analysis

Don't stop at aggregate metrics — inspect the failures.

```python
import pandas as pd

errors = pd.DataFrame({
    'true': y_test[y_test != y_pred],
    'predicted': y_pred[y_test != y_pred],
}).join(X_test.loc[y_test != y_pred])

# Where do errors concentrate?
errors.groupby(['true', 'predicted']).size().unstack(fill_value=0)

# Are there feature ranges with disproportionate failure?
for col in X_test.columns:
    err_rate = (y_test != y_pred).groupby(pd.qcut(X_test[col], 10, duplicates='drop')).mean()
    print(col, err_rate.max() - err_rate.min())  # large gap = leverage point
```

What to look for:
- **Cluster failures**: do errors concentrate in a region of feature space, a class pair, or a time slice? That's a model gap, not noise.
- **Confidence-vs-correctness**: are wrong predictions also high-confidence? Calibration is broken.
- **Slice underperformance**: does accuracy drop below acceptable for any subgroup? Hand off to `skill-bias-and-fairness`.
- **Label noise**: are some "errors" actually mislabeled ground truth? Spot-check 20 manually.

## Communicating Results to Stakeholders

Explanations for ML practitioners and explanations for non-technical audiences are different artifacts.

| Audience | Format | What to emphasize |
|---|---|---|
| ML team | SHAP/LIME plots, error analysis tables | Model mechanics, failure modes |
| Domain experts | Top-N drivers in plain language, counterfactuals | "If X had been Y, prediction would change to Z" |
| Executives / regulators | Summary card, decision-impact framing, limitations | Risk, accountability, what the model will NOT decide |
| End users affected by a decision | Single-row local explanation, recourse options | Actionable steps to change the outcome |

Always include:
1. **Confidence/uncertainty** of the prediction (calibrated probability, prediction interval)
2. **Limitations** — what the model does NOT account for
3. **Recourse** — what the affected party can do about it
4. **Distribution caveat** — these explanations apply to in-distribution inputs; flag OOD cases

## Common Pitfalls

- **Reporting feature importance as causation.** Always qualify: "the model relied on feature X" not "X causes the outcome".
- **Cherry-picking the local explanation that supports a story.** Pre-commit to the rows you'll explain (random sample, then worst errors, then borderline cases) before looking.
- **Using one method only.** SHAP and permutation importance often disagree; investigate the disagreement instead of picking the one you like.
- **Explaining a model that hasn't been validated yet.** Explain a working model, not a broken one — interpretability cannot rescue poor performance.
- **Ignoring the deployed-model gap.** Explanations on the training set don't generalize if the production distribution has drifted; pair with `skill-monitoring`.

## Integration

- `skill-ml-evaluation` — establishes the metrics whose patterns this skill explains
- `skill-bias-and-fairness` — fairness audits build on the slice analysis here
- `skill-monitoring` — drift detection in production triggers re-running these explanations
- `skill-model-description` (thesis) — the model card is where these results live in a thesis or report
- `shared/skill-docs` — for the audit-trail document an explanation produces

## Resources

- [SHAP documentation](https://shap.readthedocs.io/)
- [LIME repository](https://github.com/marcotcr/lime)
- [scikit-learn inspection module](https://scikit-learn.org/stable/inspection.html)
- [Interpretable ML Book (Molnar)](https://christophm.github.io/interpretable-ml-book/)
