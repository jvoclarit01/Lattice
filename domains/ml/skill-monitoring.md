---
name: skill-monitoring
description: Production ML monitoring — detecting feature/label/prediction drift, alerting on quality regressions, and instrumenting model services with metrics that catch silent failures. Use when a model is in production, when designing the observability layer for an ML service, or when a model "stopped working" and you can't tell why. For the orchestrated retraining loop that drift triggers see `skill-mlops`; for offline evaluation methodology see `skill-ml-evaluation`.
---

# ML Monitoring

A model that isn't monitored isn't deployed — it's abandoned. Software-style uptime checks tell you the API is up; they tell you nothing about whether the predictions are still correct. Monitoring ML means watching three layers at once: system health, data distribution, and prediction quality.

## When to Activate

Use when:
- A model is going to production for the first time
- A model is "behaving weirdly" but the API is healthy and CPU is fine
- You need to decide when to retrain (drift-triggered vs scheduled)
- Designing the dashboard / alerts for an ML service
- A regulator or auditor asks how you'd know if the model is failing
- Adding feature, label, or prediction drift detection

**Trigger phrases:** "data drift", "concept drift", "model degraded", "PSI", "KS test", "model is stale", "prediction distribution changed", "Grafana dashboard for ML", "alert when accuracy drops".

## When NOT to Use

| Situation | Use instead |
|---|---|
| Pre-deployment evaluation methodology | `skill-ml-evaluation` |
| Pipeline orchestration / retraining triggers | `skill-mlops` |
| Inference latency / throughput tuning | `skill-model-serving` |
| Tracking offline experiments | `skill-experiment-tracking` |
| Web app observability without an ML model | `webdev/skill-deployment` |
| Auditing fairness drift across groups | `skill-bias-and-fairness` (with metrics from this skill) |

## Iron Laws

1. **Three layers or it's incomplete.** System (latency/errors), data (input distributions), and prediction (output + ground-truth lag). Missing one of these means a class of failures is invisible.
2. **An alert without a runbook is noise.** Every alert must point to (a) what likely broke, (b) what to check first, (c) who owns it. Otherwise it gets snoozed and ignored.
3. **Ground truth lags reality; design for it.** Labels arrive hours/days/weeks after predictions. Monitoring must use proxies (drift, prediction distribution, business metrics) that are observable in real time.

## The Three Layers

| Layer | Examples | Detectable in real time? |
|---|---|---|
| System | Latency p50/p95/p99, QPS, error rate, GPU memory | Yes |
| Data | Feature distributions, missing-rate, schema, PSI, KS | Yes |
| Prediction | Output distribution, confidence histogram, business KPIs, accuracy vs ground truth | Distribution: yes. Accuracy: lagged |

A common mistake is monitoring only system + accuracy. The data layer is where most production failures originate (upstream pipeline change, schema drift, traffic shift) and it's the most diagnostic.

## Drift Detection — KS Test (continuous features)

```python
import numpy as np
from scipy import stats

def ks_drift(reference: np.ndarray, current: np.ndarray,
             alpha: float = 0.01) -> dict:
    """Two-sample Kolmogorov-Smirnov test for distribution shift.
    Returns the statistic, p-value, and a drift flag."""
    stat, p = stats.ks_2samp(reference, current)
    return {
        "statistic": float(stat),
        "p_value": float(p),
        "drift": bool(p < alpha),
        "n_ref": len(reference),
        "n_cur": len(current),
    }

# Practical usage: compare last 7 days of a feature to the training distribution
ref = train_df["feature_x"].dropna().to_numpy()
cur = recent_df["feature_x"].dropna().to_numpy()
result = ks_drift(ref, cur)
```

KS works well for continuous numeric features. For categorical features, use chi-squared or PSI (below). At very large sample sizes any tiny shift becomes "significant" by p-value alone — pair p-value with an effect-size threshold (e.g., `statistic > 0.1`).

## Drift Detection — PSI (Population Stability Index)

PSI is the industry-standard drift metric for credit/risk and is widely understood by stakeholders. Rule of thumb: PSI < 0.1 stable, 0.1–0.25 moderate shift, > 0.25 significant.

```python
import numpy as np
import pandas as pd

def psi(reference: np.ndarray, current: np.ndarray,
        n_bins: int = 10) -> float:
    """Population Stability Index using equal-frequency bins from reference."""
    # Bin edges from reference quantiles; clip current to avoid NaN bins
    edges = np.unique(np.quantile(reference, np.linspace(0, 1, n_bins + 1)))
    if len(edges) < 3:
        return 0.0  # degenerate; near-constant feature
    ref_counts, _ = np.histogram(reference, bins=edges)
    cur_counts, _ = np.histogram(current, bins=edges)
    eps = 1e-6
    ref_pct = ref_counts / max(ref_counts.sum(), 1) + eps
    cur_pct = cur_counts / max(cur_counts.sum(), 1) + eps
    return float(np.sum((cur_pct - ref_pct) * np.log(cur_pct / ref_pct)))

def psi_categorical(reference: pd.Series, current: pd.Series) -> float:
    cats = sorted(set(reference.unique()) | set(current.unique()))
    eps = 1e-6
    ref_pct = (reference.value_counts(normalize=True).reindex(cats).fillna(0) + eps)
    cur_pct = (current.value_counts(normalize=True).reindex(cats).fillna(0) + eps)
    return float(((cur_pct - ref_pct) * np.log(cur_pct / ref_pct)).sum())
```

The `eps` term prevents `log(0)` when a bin is empty in either window; without it PSI returns `inf` for any new category and your dashboard breaks.

## Prediction & Concept Drift

When ground truth is delayed, watch the prediction distribution itself:

```python
def prediction_drift(ref_preds: np.ndarray, cur_preds: np.ndarray) -> dict:
    """For classifiers: compare class-probability distribution shift."""
    return {
        "ks_score_class1": ks_drift(ref_preds, cur_preds),
        "ref_mean": float(ref_preds.mean()),
        "cur_mean": float(cur_preds.mean()),
        "delta_mean": float(cur_preds.mean() - ref_preds.mean()),
    }
```

A 5pp shift in predicted positive rate without a corresponding feature drift is a smoking gun for concept drift (the relationship between X and y changed). Trigger investigation; don't auto-retrain blindly.

## Prometheus Instrumentation

```python
from prometheus_client import Counter, Gauge, Histogram, start_http_server

# Counters / gauges / histograms — never re-create them per request
PREDICTION_TOTAL = Counter(
    "ml_predictions_total", "Total predictions served",
    ["model_name", "model_version", "outcome"],
)
PREDICTION_LATENCY = Histogram(
    "ml_prediction_latency_seconds", "Inference latency",
    ["model_name", "model_version"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5),
)
FEATURE_PSI = Gauge(
    "ml_feature_psi", "Population stability index per feature",
    ["model_name", "feature"],
)
PREDICTION_MEAN = Gauge(
    "ml_prediction_mean", "Mean predicted probability over rolling window",
    ["model_name", "model_version"],
)

def serve_predict(features, model):
    with PREDICTION_LATENCY.labels(model.name, model.version).time():
        proba = model.predict_proba(features)[:, 1]
    PREDICTION_TOTAL.labels(model.name, model.version, "success").inc(len(proba))
    return proba

start_http_server(9100)  # /metrics on :9100
```

Histogram buckets matter — pick them so your p95 SLO falls inside a bucket boundary, not on it. Default buckets are tuned for HTTP services and miss the action for ms-scale model latency.

## Grafana Alert Rules (Prometheus)

```yaml
# alerts.yml
groups:
- name: ml-model
  rules:
  - alert: MLPredictionLatencyHigh
    expr: histogram_quantile(0.95, sum by (le) (rate(ml_prediction_latency_seconds_bucket[5m]))) > 0.5
    for: 5m
    labels: { severity: warning, team: ml-platform }
    annotations:
      summary: "p95 inference latency > 500ms for 5 min"
      runbook: "https://wiki/ml/runbooks/latency-spike"

  - alert: MLFeatureDriftHigh
    expr: ml_feature_psi > 0.25
    for: 30m
    labels: { severity: warning, team: ml-platform }
    annotations:
      summary: "Feature {{ $labels.feature }} PSI > 0.25 for 30 min"
      runbook: "https://wiki/ml/runbooks/feature-drift"

  - alert: MLPredictionDistributionShift
    expr: |
      abs(
        ml_prediction_mean - ml_prediction_mean offset 7d
      ) > 0.05
    for: 1h
    labels: { severity: page, team: ml-platform }
    annotations:
      summary: "Prediction mean drifted >5pp vs same time last week"
      runbook: "https://wiki/ml/runbooks/prediction-drift"
```

The `offset 7d` comparison isolates real drift from day-of-week seasonality. Without it, every Monday morning pages the team.

## Ground-Truth Lag Strategy

| Lag | Strategy |
|---|---|
| Seconds (online clicks) | Real-time accuracy; alert directly |
| Hours (next-session conversion) | Delayed accuracy with rolling window; recompute hourly |
| Days–weeks (refunds, churn) | Use prediction-drift + business KPI proxies; recompute accuracy on a delay |
| Months (loan default) | Proxy metrics + scheduled reviews; expect to retrain on calendar |

For lagged ground truth, the right pattern is a *delayed* dashboard panel labeled "Accuracy as of T-N days" with the lag visible. Don't let stakeholders mistake last week's accuracy for current quality.

## Logging Predictions for Later Audit

```python
import json
from datetime import datetime, timezone

def log_prediction(request_id: str, features: dict, prediction: float,
                   model_version: str, sink) -> None:
    sink.write(json.dumps({
        "request_id": request_id,
        "ts": datetime.now(timezone.utc).isoformat(),
        "model_version": model_version,
        "features": features,
        "prediction": prediction,
        # NOTE: drop / hash any PII before logging
    }) + "\n")
```

Sample if volume is high (1% of requests). Pair the log with eventual ground truth via `request_id` to compute delayed accuracy. This log is also evidence in a post-incident investigation: "did the model see weird inputs that day?"

## Tooling Decision

| Need | Pick |
|---|---|
| Roll-your-own, you have Prometheus already | Prometheus + Grafana + custom drift jobs |
| Want batteries-included open source | Evidently AI (drift reports, dashboards) |
| Heavy regulated environment | WhyLabs, Arize, Fiddler (managed, with audit) |
| LLM-specific monitoring | Langfuse, Helicone, Arize Phoenix |
| Want to log predictions for analysis later | Add a Kafka topic / Parquet sink + dbt models |

Don't reach for a paid platform on day one. Prometheus + Evidently covers most teams until volume / compliance forces an upgrade.

## Common Failure Modes

| Pattern | Consequence |
|---|---|
| Monitoring only "is the API up?" | Model returns garbage for weeks; nobody notices until quarterly review |
| Alert thresholds set from intuition | Either pager fatigue or no signal; tune from historical noise floor |
| KS test alone at high traffic | Every test is significant; pair with effect-size threshold |
| PSI computed without `eps` | `inf` on first new category; alert spams |
| Drift alert with no investigation runbook | Alert fires; on-call clicks "ack"; root cause never found |
| Single model accuracy metric | Misses subgroup regressions (drift only on one segment) |
| Logging full request payloads with PII | Compliance violation; redact at the logger |
| Recomputing reference distribution daily | "Drift" disappears because reference creeps with current; pin reference to training data |
| No proxy metric for delayed labels | Months of degradation invisible; retrain too late |

## Integration

- `skill-mlops` — drift alerts trigger orchestrated retraining; close the loop
- `skill-ml-evaluation` — defines the metrics this skill watches in production
- `skill-model-serving` — instrument the serving layer with metrics from this skill
- `skill-bias-and-fairness` — track fairness metrics per-group with the same drift machinery
- `skill-experiment-tracking` — production metrics flow back to compare against training-time metrics
- `skill-data-versioning` — pin the *reference* distribution to the dataset version that trained the deployed model
- `shared/skill-performance` — system-layer monitoring (latency, throughput) overlaps with general perf

## Resources

- [Evidently AI](https://docs.evidentlyai.com/) — open-source drift / quality reports; the practical default
- [Google's "Rules of ML"](https://developers.google.com/machine-learning/guides/rules-of-ml) — Rules 14-43 cover monitoring
- [Prometheus best practices for histograms](https://prometheus.io/docs/practices/histograms/)
- [PSI explained for risk modeling](https://towardsdatascience.com/psi-and-csi-top-2-model-monitoring-metrics-924a2540bed8)
- [Arize Phoenix (open-source LLM/ML observability)](https://github.com/Arize-ai/phoenix)
- [Monitoring ML in production — Chip Huyen](https://huyenchip.com/2022/01/02/real-time-machine-learning-challenges-and-solutions.html)
