---
name: skill-model-description
description: Model description best practices for academic research. Use when describing ML models, documenting architectures, or reporting model details. Covers model documentation, architecture description, and hyperparameter reporting.
---

# Model Description Domain

Model description best practices for academic research.

## When to Activate

Activate when describing ML models, documenting architectures, or reporting model details.

## Core Principles

1. **Describe Clearly** — Describe models clearly and completely
2. **Document Architecture** — Document architecture thoroughly
3. **Report Hyperparameters** — Report all hyperparameters
4. **Ensure Reproducibility** — Ensure reproducibility completely

## Model Documentation

### Model Overview

**Model name:**
- Clear, descriptive name
- Include version number
- Use consistent naming
- Avoid abbreviations

**Model type:**
- Architecture type (CNN, RNN, Transformer, etc.)
- Learning paradigm (supervised, unsupervised, etc.)
- Task type (classification, regression, etc.)
- Domain specialization

**Model purpose:**
- Intended use cases
- Target applications
- Problem addressed
- Design goals

**Model architecture:**
- High-level structure
- Main components
- Component relationships
- Key innovations

**Example:**
> **Model Overview:**
> - Name: MedBERT-Adapter-v1.0
> - Type: Transformer-based encoder with adapter modules
> - Purpose: Medical text classification
> - Architecture: 12-layer BERT with domain-specific adapter

### Architecture Description

**Layer types:**
- Input layer
- Hidden layers
- Output layer
- Special layers (attention, pooling, etc.)

**Layer sizes:**
- Input dimensions
- Hidden dimensions
- Output dimensions
- Parameter counts

**Connections:**
- Layer connections
- Skip connections
- Attention patterns
- Information flow

**Activation functions:**
- ReLU, GELU, sigmoid, etc.
- Placement in network
- Justification for choice
- Alternative options considered

**Example:**
> **Architecture Details:**
> - Input: Token embeddings (768-dim)
> - Encoder: 12 transformer layers
> - Hidden size: 768
> - Attention heads: 12 per layer
> - Feed-forward: 3072-dim
> - Activation: GELU
> - Output: Classification head (12 classes)

### Hyperparameters

**Learning rate:**
- Initial learning rate
- Learning rate schedule
- Warmup strategy
- Decay rate

**Batch size:**
- Training batch size
- Evaluation batch size
- Gradient accumulation
- Memory considerations

**Number of epochs:**
- Total epochs
- Early stopping criteria
- Validation frequency
- Checkpoint strategy

**Regularization parameters:**
- Dropout rates
- Weight decay
- Label smoothing
- Data augmentation

**Example:**
> **Hyperparameters:**
> - Learning rate: 2e-5 with linear warmup (1000 steps)
> - Batch size: 32
> - Epochs: 10 with early stopping (patience=3)
> - Dropout: 0.1
> - Weight decay: 0.01
> - Label smoothing: 0.1

### Training Details

**Training data:**
- Dataset name and source
- Training set size
- Validation set size
- Test set size

**Training time:**
- Total training time
- Time per epoch
- Hardware used
- Parallelization strategy

**Training hardware:**
- GPU specifications
- CPU specifications
- Memory requirements
- Storage requirements

**Training procedure:**
- Preprocessing steps
- Optimization algorithm
- Loss function
- Evaluation frequency

**Example:**
> **Training Details:**
> - Data: Medical-Text-Classification (50K train, 5K val, 5K test)
> - Time: ~6 hours on 4x NVIDIA V100
> - Hardware: 4x V100 32GB, 32GB RAM
> - Procedure: AdamW optimizer, cross-entropy loss, validation every epoch

## Model Cards

### Model Card Template

```markdown
# Model Card

## Model Details
- **Model name:** [Name and version]
- **Model type:** [Architecture type]
- **Model version:** [Version number]
- **Training date:** [Date]
- **License:** [License information]

## Intended Use
- **Primary use case:** [Main intended application]
- **Secondary use cases:** [Other potential uses]
- **Out-of-scope uses:** [Uses to avoid]
- **Limitations:** [Known limitations]

## Training Data
- **Data sources:** [Source of training data]
- **Data size:** [Number of samples]
- **Data characteristics:** [Key data properties]
- **Data preprocessing:** [Preprocessing steps]
- **Data splits:** [Train/val/test splits]

## Model Architecture
- **Architecture type:** [Type of architecture]
- **Number of parameters:** [Parameter count]
- **Model size:** [Model file size]
- **Key components:** [Main architectural components]

## Training Procedure
- **Training time:** [Total training time]
- **Hardware:** [Hardware specifications]
- **Optimizer:** [Optimization algorithm]
- **Loss function:** [Loss used]
- **Hyperparameters:** [Key hyperparameters]

## Evaluation Results
- **Evaluation metrics:** [Metrics used]
- **Baseline comparison:** [Comparison with baselines]
- **Statistical significance:** [Significance testing]
- **Performance:** [Key results]

## Ethical Considerations
- **Bias analysis:** [Potential biases]
- **Fairness evaluation:** [Fairness assessment]
- **Privacy considerations:** [Privacy issues]
- **Environmental impact:** [Carbon footprint]

## Technical Limitations
- **Known issues:** [Known problems]
- **Failure cases:** [When model fails]
- **Edge cases:** [Problematic inputs]
- **Robustness:** [Robustness assessment]

## Reproducibility
- **Code availability:** [Where to find code]
- **Random seeds:** [Seeds used]
- **Environment:** [Software versions]
- **Data access:** [How to access data]
```

## Best Practices

### Description

**Describe model clearly:**
- Use clear, precise language
- Provide high-level overview
- Include detailed specifications
- Use diagrams when helpful

**Use diagrams:**
- Architecture diagrams
- Component diagrams
- Flow diagrams
- Data flow diagrams

**Provide code:**
- Share implementation code
- Include usage examples
- Document API
- Provide installation instructions

**Document decisions:**
- Explain design choices
- Justify architectural decisions
- Note alternatives considered
- Explain trade-offs

### Hyperparameters

**Report all hyperparameters:**
- Learning rate and schedule
- Batch size
- Number of epochs
- Regularization parameters
- Architecture parameters

**Explain choices:**
- Why specific values chosen
- How values were selected
- Sensitivity analysis
- Alternative values considered

**Report ranges:**
- Values explored
- Best performing values
- Sensitivity to changes
- Recommended ranges

**Note sensitivity:**
- Which parameters are sensitive
- Which are robust
- Interaction effects
- Tuning strategy

### Reproducibility

**Share code:**
- Public repository
- Clear documentation
- Installation instructions
- Usage examples

**Share weights:**
- Model weights
- Checkpoint files
- Loading instructions
- Version information

**Document environment:**
- Software versions
- Hardware specifications
- Dependencies
- Configuration files

**Report random seeds:**
- All random seeds
- Reproducibility notes
- Sources of randomness
- Variability assessment

## Common Mistakes to Avoid

1. **Incomplete description** — Describe all components
2. **Missing hyperparameters** — Report all parameters
3. **No reproducibility** — Ensure reproducibility
4. **Unclear architecture** — Use clear diagrams
5. **Missing code** — Share implementation
6. **No evaluation** — Include evaluation results
7. **No limitations** — Acknowledge limitations
8. **No ethical considerations** — Address ethics

## Evaluation Checklist

Before finalizing your model description:

- [ ] Model name and version specified
- [ ] Model type and purpose described
- [ ] Architecture documented completely
- [ ] All hyperparameters reported
- [ ] Training details provided
- [ ] Evaluation results included
- [ ] Limitations acknowledged
- [ ] Ethical considerations addressed
- [ ] Reproducibility ensured
- [ ] Code shared or described

## Resources

### Model Documentation
- [Model Cards](https://arxiv.org/abs/1810.03993) — Model card paper
- [Datasheets for Datasets](https://arxiv.org/abs/1803.09010) — Dataset documentation
- [Papers With Code](https://paperswithcode.com/) — Model implementations and papers

### Model Management
- [MLflow](https://mlflow.org/) — Machine learning lifecycle management
- [Weights & Biases](https://wandb.ai/) — Experiment tracking
- [TensorBoard](https://www.tensorflow.org/tensorboard) — Visualization toolkit

### Academic Writing Guides
- [claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) — Scientific writing best practices
- [AlterLab-Academic-Skills](https://github.com/AlterLab-IEU/AlterLab-Academic-Skills) — Comprehensive academic writing resources

### Machine Learning Resources
- [Deep Learning Book](https://www.deeplearningbook.org/) — Comprehensive ML textbook
- [Machine Learning Mastery](https://machinelearningmastery.com/) — Practical ML guides
- [Fast.ai](https://www.fast.ai/) — Practical deep learning courses
