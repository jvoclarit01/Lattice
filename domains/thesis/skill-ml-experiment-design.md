---
name: skill-ml-experiment-design
description: ML experiment design best practices for academic research. Use when designing ML experiments, planning empirical studies, or conducting ML research. Covers experimental design, evaluation metrics, and reproducibility.
---

# ML Experiment Design Domain

ML experiment design best practices for academic research.

## When to Activate

Activate when designing ML experiments, planning empirical studies, or conducting ML research.

## Core Principles

1. **Design Rigorously** — Design experiments rigorously
2. **Evaluate Appropriately** — Use appropriate evaluation
3. **Ensure Reproducibility** — Ensure reproducibility completely
4. **Report Honestly** — Report results honestly

## Experimental Design

### Baselines

**Establish strong baselines:**
- Use established baselines
- Include simple baselines
- Compare with state-of-the-art
- Report baseline results

**Compare with state-of-the-art:**
- Identify relevant SOTA methods
- Use recent SOTA methods
- Ensure fair comparison
- Report differences

**Use standard datasets:**
- Well-established benchmarks
- Publicly available datasets
- Community-accepted datasets
- Document dataset characteristics

**Report baseline results:**
- All baselines evaluated
- Same conditions for all
- Statistical significance
- Clear presentation

**Example:**
> **Baseline Selection:**
> - Simple baseline: Logistic regression
> - Standard baseline: BERT-base
> - SOTA baseline: BioBERT
> - Our method: Domain-adapted BERT
> - All evaluated on same dataset splits

### Datasets

**Use standard datasets:**
- Community benchmarks
- Publicly available
- Well-documented
- Widely used

**Describe data preprocessing:**
- Preprocessing steps
- Feature extraction
- Data cleaning
- Normalization

**Report data statistics:**
- Dataset size
- Class distribution
- Feature statistics
- Data quality metrics

**Make data available:**
- Public repository
- Clear documentation
- Appropriate license
- Reproducible preprocessing

**Example:**
> **Dataset Description:**
> - Name: Medical-Text-Classification
> - Size: 50,000 documents
> - Classes: 12 balanced categories
> - Splits: 40K train, 5K val, 5K test
> - Preprocessing: Tokenization, lowercasing, stopword removal

### Evaluation

**Use appropriate metrics:**
- Task-appropriate metrics
- Multiple metrics
- Metric justification
- Metric limitations

**Use cross-validation:**
- K-fold cross-validation
- Stratified sampling
- Repeated runs
- Report variance

**Report statistical significance:**
- Statistical tests
- Confidence intervals
- P-values
- Effect sizes

**Use multiple metrics:**
- Complementary metrics
- Different aspects of performance
- Metric trade-offs
- Comprehensive evaluation

**Example:**
> **Evaluation Setup:**
> - Metrics: Accuracy, F1, Precision, Recall, AUC
> - Validation: 5-fold stratified cross-validation
> - Significance: Paired t-test, p < 0.05
> - Reporting: Mean ± std over 5 folds

## Evaluation Metrics

### Classification

**Accuracy:**
- Overall correctness
- Formula: (TP + TN) / (TP + TN + FP + FN)
- Use when: Balanced classes
- Limitation: Sensitive to class imbalance

**Precision:**
- Positive predictive value
- Formula: TP / (TP + FP)
- Use when: False positives costly
- Limitation: Doesn't consider false negatives

**Recall:**
- Sensitivity, true positive rate
- Formula: TP / (TP + FN)
- Use when: False negatives costly
- Limitation: Doesn't consider false positives

**F1 score:**
- Harmonic mean of precision and recall
- Formula: 2 × (Precision × Recall) / (Precision + Recall)
- Use when: Balance between precision and recall
- Limitation: Doesn't consider true negatives

**AUC-ROC:**
- Area under ROC curve
- Use when: Threshold-independent evaluation
- Limitation: Doesn't reflect actual performance at threshold

**Example:**
> **Classification Metrics:**
> - Accuracy: 94.2% (balanced classes)
> - Precision: 93.8% (few false positives)
> - Recall: 94.5% (few false negatives)
> - F1: 94.2% (balanced performance)
> - AUC: 0.98 (excellent discrimination)

### Regression

**MSE (Mean Squared Error):**
- Average squared difference
- Formula: (1/n) Σ(yi - ŷi)²
- Use when: Large errors penalized heavily
- Limitation: Sensitive to outliers

**MAE (Mean Absolute Error):**
- Average absolute difference
- Formula: (1/n) Σ|yi - ŷi|
- Use when: Linear penalty for errors
- Limitation: Doesn't penalize large errors more

**R² (R-squared):**
- Proportion of variance explained
- Formula: 1 - (SSres / SStot)
- Use when: Comparing models
- Limitation: Can be misleading with non-linear relationships

**RMSE (Root Mean Squared Error):**
- Square root of MSE
- Formula: √MSE
- Use when: Same units as target
- Limitation: Sensitive to outliers

**Example:**
> **Regression Metrics:**
> - MSE: 0.023 (low squared error)
> - MAE: 0.12 (low absolute error)
> - R²: 0.94 (high explained variance)
> - RMSE: 0.15 (low error in target units)

### Ranking

**NDCG (Normalized Discounted Cumulative Gain):**
- Ranking quality measure
- Use when: Relevance-graded rankings
- Limitation: Requires relevance scores

**MRR (Mean Reciprocal Rank):**
- Reciprocal of first relevant item rank
- Use when: First relevant item matters
- Limitation: Doesn't consider full ranking

**Precision@k:**
- Precision in top k results
- Use when: Top results matter
- Limitation: Doesn't consider ranking beyond k

**Recall@k:**
- Recall in top k results
- Use when: Coverage matters
- Limitation: Doesn't consider ranking quality

**Example:**
> **Ranking Metrics:**
> - NDCG@10: 0.87 (high ranking quality)
> - MRR: 0.92 (relevant items near top)
> - Precision@5: 0.84 (high precision in top 5)
> - Recall@10: 0.78 (good coverage in top 10)

## Best Practices

### Design

**Define clear hypotheses:**
- Specific, testable hypotheses
- Null and alternative hypotheses
- Expected outcomes
- Significance criteria

**Use appropriate baselines:**
- Strong baselines
- Fair comparison
- Same conditions
- Clear reporting

**Control variables:**
- Identify confounding factors
- Control for important variables
- Randomize when possible
- Document all conditions

**Plan for contingencies:**
- Alternative approaches
- Backup plans
- Resource requirements
- Timeline considerations

### Evaluation

**Use appropriate metrics:**
- Task-appropriate metrics
- Multiple metrics
- Metric justification
- Metric limitations

**Use cross-validation:**
- K-fold cross-validation
- Stratified sampling
- Repeated runs
- Report variance

**Report statistical significance:**
- Statistical tests
- Confidence intervals
- P-values
- Effect sizes

**Use multiple metrics:**
- Complementary metrics
- Different aspects of performance
- Metric trade-offs
- Comprehensive evaluation

### Reproducibility

**Document all settings:**
- Hyperparameters
- Random seeds
- Software versions
- Hardware specifications

**Share code and data:**
- Public repository
- Clear documentation
- Appropriate license
- Reproducible setup

**Use version control:**
- Git for code
- Data versioning
- Experiment tracking
- Clear commit messages

**Report random seeds:**
- All random seeds
- Reproducibility notes
- Sources of randomness
- Variability assessment

### Reporting

**Report all results:**
- All metrics
- All baselines
- All conditions
- All runs

**Discuss limitations:**
- Methodological limitations
- Dataset limitations
- Evaluation limitations
- Generalizability concerns

**Provide code:**
- Public repository
- Clear documentation
- Installation instructions
- Usage examples

**Share data:**
- Public repository
- Clear documentation
- Appropriate license
- Data preprocessing code

## Common Mistakes to Avoid

1. **Weak baselines** — Use strong baselines
2. **Inappropriate metrics** — Use task-appropriate metrics
3. **No statistical testing** — Report statistical significance
4. **Data leakage** — Prevent data leakage
5. **Overfitting** — Use proper validation
6. **Cherry-picking** — Report all results
7. **No reproducibility** — Ensure reproducibility
8. **Unclear reporting** — Report clearly

## Experiment Design Template

### Template

```
## Experimental Setup

### Datasets
- Dataset name and source
- Dataset size and characteristics
- Train/validation/test splits
- Preprocessing steps

### Baselines
- Baseline 1: [Description]
- Baseline 2: [Description]
- Baseline 3: [Description]
- Our method: [Description]

### Evaluation Metrics
- Metric 1: [Justification]
- Metric 2: [Justification]
- Metric 3: [Justification]

### Experimental Protocol
- Cross-validation strategy
- Number of runs
- Random seeds
- Statistical testing

## Results

### Overall Performance
- Table of results
- Statistical significance
- Comparison with baselines

### Ablation Studies
- Component ablation
- Hyperparameter sensitivity
- Design choices

### Analysis
- Error analysis
- Success cases
- Failure cases
- Qualitative analysis

## Discussion

### Key Findings
- Main results
- Statistical significance
- Practical significance

### Limitations
- Methodological limitations
- Dataset limitations
- Evaluation limitations

### Future Work
- Promising directions
- Methodological improvements
- Additional studies
```

## Evaluation Checklist

Before finalizing your experiment design:

- [ ] Clear hypotheses defined
- [ ] Strong baselines selected
- [ ] Appropriate metrics chosen
- [ ] Evaluation protocol specified
- [ ] Statistical testing planned
- [ ] Reproducibility ensured
- [ ] Code and data documented
- [ ] Random seeds specified
- [ ] Limitations acknowledged
- [ ] Results reported honestly

## Resources

### Machine Learning Resources
- [machine-learning](https://github.com/anthropics/skills/tree/main/skills/machine-learning) — Machine learning skills
- [scikit-learn](https://scikit-learn.org/) — Machine learning library
- [PyTorch](https://pytorch.org/) — Deep learning framework
- [TensorFlow](https://www.tensorflow.org/) — Deep learning framework

### Experiment Tracking
- [MLflow](https://mlflow.org/) — Machine learning lifecycle management
- [Weights & Biases](https://wandb.ai/) — Experiment tracking
- [TensorBoard](https://www.tensorflow.org/tensorboard) — Visualization toolkit
- [Comet ML](https://www.comet.ml/) — Experiment tracking

### Academic Writing Guides
- [claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) — Scientific writing best practices
- [AlterLab-Academic-Skills](https://github.com/AlterLab-IEU/AlterLab-Academic-Skills) — Comprehensive academic writing resources

### Evaluation Resources
- [scikit-learn Metrics](https://scikit-learn.org/stable/modules/model_evaluation.html) — Evaluation metrics
- [Metrics for ML](https://www.kaggle.com/learn/metrics) — Kaggle metrics course
- [Evaluation Metrics Guide](https://towardsdatascience.com/the-5-classification-evaluation-metrics-you-must-know-aa8d9f6b939c) — Comprehensive guide
