---
name: skill-model-selection
description: Picking a model family for a problem and tuning its hyperparameters — baselines first, decision trees by data type and size, principled hyperparameter search (grid / random / Bayesian / ASHA), and apples-to-apples comparison with proper CV and statistical tests. Use when starting a new ML problem, choosing between candidate algorithms, or deciding between hyperparameter values. For deep-learning architecture decisions specifically, see `skill-model-architecture`. For the metrics used during comparison, see `skill-ml-evaluation`.
---

# Model Selection & Hyperparameter Tuning

The model you reach for first sets a ceiling on how fast you'll learn. Pick something simple, fast, and well-understood — then earn complexity with evidence.

## When to Activate

Use when:
- Starting any new supervised learning problem
- Asked "should we try XGBoost or a neural net?"
- Comparing two or more candidate models on the same task
- Tuning hyperparameters and unsure whether to use grid / random / Bayesian / ASHA
- Submitting a leaderboard entry and need a principled sweep
- A teammate proposes a complex model — you need to defend or replace the baseline

**Trigger phrases:** "which model should I try", "logistic regression vs random forest", "should we deep learn this", "tune hyperparameters", "Optuna", "GridSearchCV", "set up a sweep", "what's a reasonable baseline".

## When NOT to Use

| Situation | Use instead |
|---|---|
| Designing a *new* neural architecture | `skill-model-architecture` |
| Adapting a pre-trained model to a new task | `skill-finetuning` |
| Deciding which evaluation metric to use | `skill-ml-evaluation` |
| Choosing a vector store / retriever | `skill-rag` |
| Picking which prompt to use with an LLM | `skill-prompt-engineering` |

## Iron Laws

1. **Always ship a baseline before tuning.** A `DummyClassifier` or majority-class baseline anchors what "0.85 accuracy" means. Tuning before baselines is theater.
2. **Compare on identical splits.** Different `random_state`, different scaler fit, different fold = invalid comparison. Use a fixed pipeline and a fixed CV object.
3. **Tune the metric you ship on.** If you ship recall@95% precision, don't tune for accuracy and check recall later — that's overfitting to the wrong objective.

## Decision Tree by Data Type and Size

```
What kind of data?
├── Tabular (rows × features)
│   ├── n < 1k → Logistic / linear regression, or shallow tree
│   ├── 1k ≤ n < 1M → Gradient-boosted trees (XGBoost, LightGBM, CatBoost) ← default
│   ├── n ≥ 1M, structured numerical → GBDT still competitive; try TabNet/FT-Transformer only with reason
│   └── Heavy categorical / mixed → CatBoost (native categorical handling)
├── Image
│   ├── < 10k labeled → Fine-tune a pretrained ConvNet/ViT (skill-finetuning)
│   ├── ≥ 10k → ResNet / EfficientNet / ViT trained from scratch is feasible
│   └── Object detection / segmentation → YOLO / DETR / Mask R-CNN family
├── Text
│   ├── Classification, < 10k labels → Fine-tune DistilBERT / RoBERTa
│   ├── Generation / chat → Use an instruction-tuned LLM, see skill-prompt-engineering
│   └── Embeddings / search → SentenceTransformers, see skill-rag
├── Time series
│   ├── Classical (ARIMA, ETS) → statsmodels; great baseline
│   ├── Many series, exogenous features → LightGBM with lag features
│   └── Long-range, high frequency → Temporal Fusion Transformer, N-BEATS
└── Audio / video / graph → domain-specific; not in this skill's scope
```

For 90% of tabular problems, your first model is gradient-boosted trees. Anything more complex needs a written justification.

## Baselines (mandatory)

```python
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, mean_absolute_error

# Classification
trivial = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
linear  = LogisticRegression(max_iter=1000).fit(X_train, y_train)

print("Trivial AUC :", roc_auc_score(y_test, trivial.predict_proba(X_test)[:, 1]))
print("Linear  AUC :", roc_auc_score(y_test, linear.predict_proba(X_test)[:, 1]))
```

If your fancy model can't beat `DummyClassifier(strategy="stratified")`, you have a data or labeling problem, not a model problem.

## Apples-to-Apples Comparison

```python
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

candidates = {
    "logreg": Pipeline([("sc", StandardScaler()),
                        ("clf", LogisticRegression(max_iter=1000))]),
    "xgb":    Pipeline([("clf", XGBClassifier(n_estimators=300, max_depth=5,
                                              eval_metric="logloss",
                                              random_state=42))]),
}

for name, est in candidates.items():
    scores = cross_val_score(est, X, y, cv=cv, scoring="roc_auc", n_jobs=-1)
    print(f"{name:8s} AUC = {scores.mean():.4f} ± {scores.std():.4f}")
```

The pipeline is critical — it ensures the scaler is `fit` on each fold's training data only. Fitting the scaler on `X` before CV leaks test info into training (see `skill-data-preprocessing`).

### Multiclass Metrics — Get the Averaging Right

```python
from sklearn.metrics import f1_score, roc_auc_score

# Multiclass: choose averaging deliberately
f1_score(y_true, y_pred, average="macro")     # equal weight per class — use when all classes matter equally
f1_score(y_true, y_pred, average="weighted")  # weighted by support — masks minority class regressions
f1_score(y_true, y_pred, average="micro")     # = accuracy for multiclass; rarely the right answer

# AUC for multiclass requires probabilities and explicit strategy
roc_auc_score(y_true, model.predict_proba(X), multi_class="ovr", average="macro")
```

Defaulting to `average="binary"` on multiclass data raises an error in modern sklearn but used to silently misbehave; never trust the default — declare what you mean.

## Hyperparameter Search Strategy

| Search | Use when | Why |
|---|---|---|
| **Grid** | ≤ 3 hyperparameters, all categorical / few values | Exhaustive, reproducible, embarrassingly parallel |
| **Random** | More than 3 hyperparameters, continuous spaces | Bergstra & Bengio (2012) showed random beats grid in high-D |
| **Bayesian (Optuna, HyperOpt)** | Each trial is expensive (>1 min), search is well-defined | Adapts after each trial; converges in fewer evaluations |
| **ASHA / Hyperband** | Training is iterative (epochs) and you can early-stop bad trials | Massive parallelism; throws away losers fast |
| **Population-based (PBT)** | RL or large training jobs with non-stationary best LR | Rare in practice; complex setup |

Default for tabular: random search over 30–60 trials. Default for deep learning sweeps: Optuna + ASHA pruner.

### Optuna Example (works for any model)

```python
import optuna
from sklearn.model_selection import cross_val_score
from xgboost import XGBClassifier

def objective(trial: optuna.Trial) -> float:
    params = {
        "n_estimators":     trial.suggest_int("n_estimators", 100, 1000, step=50),
        "max_depth":        trial.suggest_int("max_depth", 3, 10),
        "learning_rate":    trial.suggest_float("learning_rate", 1e-3, 0.3, log=True),
        "subsample":        trial.suggest_float("subsample", 0.5, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.5, 1.0),
        "reg_lambda":       trial.suggest_float("reg_lambda", 1e-3, 10.0, log=True),
    }
    model = XGBClassifier(**params, eval_metric="logloss", random_state=42)
    scores = cross_val_score(model, X_train, y_train, cv=5,
                             scoring="roc_auc", n_jobs=-1)
    return scores.mean()

study = optuna.create_study(direction="maximize",
                            sampler=optuna.samplers.TPESampler(seed=42),
                            pruner=optuna.pruners.MedianPruner())
study.optimize(objective, n_trials=60, show_progress_bar=True)

print("Best AUC :", study.best_value)
print("Params   :", study.best_params)
```

Use `log=True` for parameters that vary by orders of magnitude (LR, regularization). Without it, the sampler wastes most trials in a narrow range.

### Avoiding Hyperparameter Overfitting

Tuning on the same set you evaluate on is leakage. Use **nested CV** for honest estimates:

```python
from sklearn.model_selection import GridSearchCV, cross_val_score, StratifiedKFold

inner_cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=1)
outer_cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=2)

search = GridSearchCV(XGBClassifier(eval_metric="logloss"),
                      param_grid={"max_depth": [3, 5, 7], "n_estimators": [200, 500]},
                      cv=inner_cv, scoring="roc_auc", n_jobs=-1)

honest_scores = cross_val_score(search, X, y, cv=outer_cv, scoring="roc_auc")
print(f"Generalization AUC = {honest_scores.mean():.4f} ± {honest_scores.std():.4f}")
```

The reported number is what you'd see on truly unseen data, not the inflated "best" score from a single tuning sweep.

## Statistical Comparison

When two models are close, the question is whether the difference is noise. For paired CV folds:

```python
from scipy.stats import wilcoxon
# scores_a, scores_b are per-fold AUCs from the SAME folds (not new shuffles)
stat, p = wilcoxon(scores_a, scores_b)
print(f"Wilcoxon p = {p:.3f}")
```

A p > 0.05 means "I can't distinguish these models with this CV setup". Pick the simpler one.

## Common Failure Modes

| Pattern | Consequence |
|---|---|
| Tuning without a fixed CV seed | Each "best" model wins on a different split; not reproducible |
| Comparing models with different preprocessing inside the pipeline | You're comparing pipelines, not models |
| Early stopping on the test set | The test set is now part of training; reported metric is optimistic |
| Picking the model with highest CV mean, ignoring variance | A model with mean=0.83 ± 0.08 is worse than one with 0.81 ± 0.01 in production |
| Using `accuracy` on imbalanced data | 99% accuracy on a 1% positive class = predicting all negative |
| Skipping the baseline | Can't tell if "AUC 0.72" is good or terrible |
| Tuning 20 hyperparameters with grid search | Combinatorial explosion; switch to random or Bayesian |
| Reporting the best CV fold instead of the mean | Cherry-picked; not a real estimate of generalization |

## Integration

- `skill-ml-evaluation` — the metrics used in cross-validation and gating
- `skill-data-preprocessing` — preprocessing must live inside the CV pipeline
- `skill-feature-engineering` — feature design happens before model selection but interacts with it
- `skill-model-architecture` — when "which model" means "which deep architecture"
- `skill-finetuning` — when the answer is "use a pretrained model"
- `skill-experiment-tracking` — log every trial; sweeps generate a lot of runs
- `skill-reproducibility` — fix seeds across CV / search / model
- `shared/skill-tdd` — preprocessing and evaluation utilities are TDD candidates

## Resources

- [scikit-learn model selection guide](https://scikit-learn.org/stable/model_selection.html)
- [Optuna docs](https://optuna.readthedocs.io/) — practical Bayesian optimization
- [Bergstra & Bengio, "Random Search for Hyper-Parameter Optimization" (2012)](https://www.jmlr.org/papers/v13/bergstra12a.html) — why random ≥ grid
- [Asha paper, Li et al. 2020](https://arxiv.org/abs/1810.05934) — early-stopping bandit
- [LightGBM tuning guide](https://lightgbm.readthedocs.io/en/latest/Parameters-Tuning.html) — the canonical "what dial does what"
- [Probabilistic ML — Murphy, ch. 4 (model selection)](https://probml.github.io/pml-book/book1.html)
