---
name: skill-bias-and-fairness
description: Bias and fairness best practices for ML systems. Use when detecting bias, ensuring fairness, or mitigating unfair outcomes. Covers bias detection, fairness metrics, and mitigation strategies.
---

# Bias and Fairness Domain

Bias and fairness best practices for ML systems.

## When to Activate

Activate when detecting bias, ensuring fairness, or mitigating unfair outcomes.

## Core Principles

1. **Detect Bias** — Detect bias in data and models
2. **Measure Fairness** — Measure fairness metrics
3. **Mitigate Bias** — Mitigate unfair outcomes
4. **Monitor Continuously** — Monitor for bias over time

## Bias Detection

### Data Bias
```python
import pandas as pd

# Check for class imbalance
class_counts = df['target'].value_counts()
print(class_counts)

# Check for demographic parity
demographic_counts = df.groupby(['protected_attribute', 'target']).size()
print(demographic_counts)
```

### Model Bias
```python
from fairlearn.metrics import demographic_parity_difference

# Calculate demographic parity difference
dpd = demographic_parity_difference(
    y_true, y_pred, sensitive_features=df['protected_attribute']
)
print(f"Demographic Parity Difference: {dpd:.3f}")
```

## Fairness Metrics

### Individual Fairness
- Similar individuals should receive similar outcomes
- Consistency across similar cases
- No discrimination based on protected attributes

### Group Fairness
- Demographic parity
- Equal opportunity
- Equalized odds
- Calibration

### Fairlearn Metrics
```python
from fairlearn.metrics import (
    demographic_parity_difference,
    equalized_odds_difference,
    selection_rate
)

# Demographic parity difference
dpd = demographic_parity_difference(
    y_true, y_pred, sensitive_features=sensitive_features
)

# Equalized odds difference
eod = equalized_odds_difference(
    y_true, y_pred, sensitive_features=sensitive_features
)

# Selection rate
sr = selection_rate(y_pred, sensitive_features=sensitive_features)
```

## Mitigation Strategies

### Pre-processing
```python
from fairlearn.preprocessing import CorrelationRemover

# Remove sensitive attribute correlations
remover = CorrelationRemover(sensitive_feature_names=['protected_attribute'])
X_transformed = remover.fit_transform(X)
```

### In-processing
```python
from fairlearn.reductions import DemographicParity

# Train with fairness constraint
mitigator = ExponentiatedGradient(
    estimator=model,
    constraints=DemographicParity()
)

mitigator.fit(X_train, y_train, sensitive_features=sensitive_features)
```

### Post-processing
```python
from fairlearn.postprocessing import ThresholdOptimizer

# Adjust thresholds for fairness
postprocessor = ThresholdOptimizer(
    estimator=model,
    constraints='demographic_parity',
    prefit=True
)

postprocessor.fit(X_train, y_train, sensitive_features=sensitive_features)
```

## Best Practices

### Bias Detection
- Analyze data for bias
- Test models for bias
- Use fairness metrics
- Document findings

### Fairness Mitigation
- Choose appropriate strategy
- Evaluate trade-offs
- Monitor continuously
- Document decisions

### Documentation
- Document bias analysis
- Record fairness metrics
- Note limitations
- Track changes over time

## Resources

- [Fairlearn](https://fairlearn.org/)
- [AI Fairness 360](https://aif360.res.ibm.com/)
- [claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills)
