---
name: skill-model-architecture
description: Designing neural network architectures — picking and composing layers for tabular, vision, sequence, and text/audio inputs. Covers the architecture decision rubric, residual/normalization/regularization patterns, and the common bug patterns that make models fail to learn at all. Use when designing a new model from scratch or replacing a component (e.g., swapping an LSTM for a Transformer block). For picking among existing model families (XGBoost vs MLP vs ConvNet) at the high level, see `skill-model-selection`. For adapting pretrained models, see `skill-finetuning`.
---

# Model Architecture Design

Most "we tried a deep model and it didn't work" stories trace to architecture errors made before training started: wrong inductive bias for the data, missing normalization, broken residuals, mismatched output dim. Design first, train second.

## When to Activate

Use when:
- Sketching a new model from scratch (not reusing a pretrained backbone)
- Picking the right architectural primitive for a data modality (tabular, image, sequence, text, graph)
- Replacing a component in an existing model (e.g., swap GRU for Transformer block)
- Diagnosing "loss won't go down" on a model you wrote yourself
- Designing the head for a fine-tuned backbone
- Asked "should we add another layer / wider hidden / dropout?"

**Trigger phrases:** "design a model for", "what kind of network", "should we add a layer", "wider or deeper", "swap out the encoder", "loss isn't decreasing", "stack a transformer on top".

## When NOT to Use

| Situation | Use instead |
|---|---|
| Choosing between model *families* (linear vs trees vs neural) | `skill-model-selection` |
| Adapting a pretrained model (BERT, ResNet, Llama) | `skill-finetuning` |
| Designing a serving system around a model | `skill-model-serving` |
| Training-loop / optimizer choices | `skill-training` |
| LLM prompt design | `skill-prompt-engineering` |

## Iron Laws

1. **The architecture's inductive bias must match the data structure.** Convolutions encode translation invariance. Recurrences encode temporal order. Self-attention encodes pairwise relations. Picking the wrong primitive can't be fixed by "more layers."
2. **Every block has normalization, residual, and a nonlinearity — in that order, debated.** Skipping any of the three is a bug ~95% of the time. Modern transformers use Pre-LN (`norm → attn/mlp → +residual`); CNNs since ResNet use Post-LN-ish variants. Pick one and stay consistent.
3. **Sanity-check shapes and overfit a tiny batch before any real training.** If the model can't drive loss to ~0 on 16 examples, it's broken. No amount of compute will fix a bug; debug now.

## Architecture Decision Rubric

| Data | Default architecture | When to escalate |
|---|---|---|
| Tabular | Don't. Use GBDT. | Only consider TabNet / FT-Transformer if you have >1M rows AND need representation learning for downstream tasks |
| Image (classification, detection) | ResNet / EfficientNet / ViT | ConvNeXt or DINOv2 features for SOTA at modest scale |
| Image (small dataset, < 50k) | Pretrained backbone + linear head, see `skill-finetuning` | — |
| Text classification, < 100k docs | Pretrained BERT/RoBERTa + classifier head | Train from scratch only with strong reason |
| Long-context sequence (genomics, time-series with thousands of steps) | Transformer + RoPE / ALiBi, or Mamba/SSM | LSTM only as a baseline |
| Tabular time-series with exogenous features | LightGBM with lag features | TFT or N-BEATS for many parallel series |
| Graph data | GCN, GAT, GraphSAGE | Don't try to flatten into tabular |
| Audio (waveforms) | Conv1D + spectrogram preprocessing, or Wav2Vec2 / Whisper backbone | — |

When in doubt: take a known-good architecture for the domain and modify the head. Inventing layers from scratch is a research project.

## Building Blocks (PyTorch, runnable)

### Feedforward / MLP — the right default for tabular post-embedding

```python
import torch
import torch.nn as nn

class MLPBlock(nn.Module):
    """Pre-norm MLP block with residual and dropout."""
    def __init__(self, dim: int, hidden: int, dropout: float = 0.1):
        super().__init__()
        self.norm = nn.LayerNorm(dim)
        self.net = nn.Sequential(
            nn.Linear(dim, hidden),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden, dim),
            nn.Dropout(dropout),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x + self.net(self.norm(x))   # residual
```

Pattern: `LayerNorm → Linear → GELU → Dropout → Linear → Dropout`, plus a residual. Skipping the norm is the most common silent bug — training works at small scale and diverges past 8 layers.

### Convolutional Block (CNN)

```python
import torch.nn as nn
import torch.nn.functional as F

class ConvBlock(nn.Module):
    """Conv-BN-ReLU, with optional pooling and proper shape arithmetic."""
    def __init__(self, in_ch: int, out_ch: int, kernel: int = 3, pool: bool = True):
        super().__init__()
        self.conv = nn.Conv2d(in_ch, out_ch, kernel_size=kernel, padding=kernel // 2)
        self.bn = nn.BatchNorm2d(out_ch)
        self.pool = nn.MaxPool2d(2) if pool else nn.Identity()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.pool(F.relu(self.bn(self.conv(x))))


class TinyCNN(nn.Module):
    """Image classifier for 32x32 RGB → num_classes. Computes the flatten size."""
    def __init__(self, num_classes: int = 10, in_size: int = 32):
        super().__init__()
        self.features = nn.Sequential(
            ConvBlock(3, 32),       # 32 → 16
            ConvBlock(32, 64),      # 16 → 8
            ConvBlock(64, 128),     # 8  → 4
        )
        # Compute the flatten dim ONCE from a dummy forward — never hardcode it.
        with torch.no_grad():
            flat = self.features(torch.zeros(1, 3, in_size, in_size)).flatten(1).shape[1]
        self.head = nn.Sequential(
            nn.Flatten(),
            nn.Linear(flat, 256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.head(self.features(x))
```

The hardcoded `64 * 6 * 6` in the original version of this skill was a defect — the math only works for one specific input size and one specific pool/conv/pad combination. Compute it from a dummy tensor instead.

### Sequence Models — Transformer vs RNN

```python
class TransformerEncoderBlock(nn.Module):
    """Pre-LN Transformer block. The modern default for sequences."""
    def __init__(self, d_model: int, n_heads: int, ff: int, dropout: float = 0.1):
        super().__init__()
        self.norm1 = nn.LayerNorm(d_model)
        self.attn  = nn.MultiheadAttention(d_model, n_heads,
                                           dropout=dropout, batch_first=True)
        self.norm2 = nn.LayerNorm(d_model)
        self.ff = nn.Sequential(
            nn.Linear(d_model, ff), nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(ff, d_model),
        )
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, attn_mask=None, key_padding_mask=None):
        h = self.norm1(x)
        a, _ = self.attn(h, h, h, attn_mask=attn_mask,
                         key_padding_mask=key_padding_mask, need_weights=False)
        x = x + self.dropout(a)
        x = x + self.ff(self.norm2(x))
        return x
```

Use Pre-LN (norm before attention/MLP) — it's far more stable than the original Post-LN at >6 layers. Always pass `key_padding_mask` if your batches have variable-length sequences; padded tokens that aren't masked will leak into attention.

### When to use RNNs/LSTMs

LSTMs are still the right choice when:
- Sequence length is short (< 100) and a tiny model is desired (mobile, low-latency)
- Data is genuinely sequential and small in volume; transformers overfit
- You need streaming inference with bounded state

For everything else, prefer transformers (or Mamba / SSMs at very long context).

## Output Heads (where most bugs live)

| Task | Final layer | Loss | Common mistake |
|---|---|---|---|
| Binary classification | `nn.Linear(d, 1)` then sigmoid only at inference | `BCEWithLogitsLoss` | Applying sigmoid before the loss → numerical instability |
| Multiclass classification | `nn.Linear(d, num_classes)` | `CrossEntropyLoss` (expects logits, not softmax) | Applying softmax before CE → silently wrong gradient |
| Multilabel classification | `nn.Linear(d, num_labels)` | `BCEWithLogitsLoss` per label | Using `CrossEntropyLoss` (which assumes single class) |
| Regression | `nn.Linear(d, 1)` | `MSELoss` or `HuberLoss` | Forgetting to scale targets; large targets explode gradients |
| Regression w/ heteroscedastic noise | Predict `(mu, log_sigma)` | Gaussian NLL | Predicting `sigma` directly (must be positive) |
| Ranking / metric learning | Embedding head | Triplet / InfoNCE | Not L2-normalizing embeddings before cosine sim |

## Regularization Toolkit

| Technique | Use when |
|---|---|
| `Dropout(p=0.1–0.3)` | Default, especially in MLPs/transformers post-attention |
| `nn.LayerNorm` / `BatchNorm2d` | Always — but pick the right one for the modality |
| Weight decay (AdamW) | Default for transformers (`weight_decay=0.01–0.1`) |
| Label smoothing | Classification with hard labels and overconfident outputs |
| Stochastic depth (DropPath) | Deep transformers (>12 layers) |
| Gradient clipping | RNN/transformer training, set `max_norm=1.0` |
| Data augmentation | Always cheaper than architectural regularization |

## Sanity Checks Before Training

Run all four. They take seconds.

```python
import torch

model = MyModel().cuda()
x = torch.randn(4, 3, 32, 32, device="cuda")     # adjust shape
y = torch.randint(0, 10, (4,), device="cuda")
loss_fn = torch.nn.CrossEntropyLoss()

# 1. Forward shape check
out = model(x)
assert out.shape == (4, 10), out.shape

# 2. Backward connectivity — every parameter must receive a gradient
loss = loss_fn(out, y)
loss.backward()
no_grad = [n for n, p in model.named_parameters() if p.grad is None]
assert not no_grad, f"No grad for: {no_grad}"

# 3. Overfit a tiny batch — loss should go to ~0
opt = torch.optim.AdamW(model.parameters(), lr=1e-3)
for _ in range(200):
    opt.zero_grad()
    loss = loss_fn(model(x), y)
    loss.backward()
    opt.step()
assert loss.item() < 0.1, f"Couldn't overfit 4 samples: loss={loss.item()}"

# 4. Param count sanity
n = sum(p.numel() for p in model.parameters())
print(f"Total params: {n:,}")
```

If overfitting 4 samples to ~0 loss takes more than a few hundred steps, the model is broken. Don't waste a 10-hour training run finding out.

## Common Failure Modes

| Pattern | Consequence |
|---|---|
| Hardcoded flatten dim that depends on input size | Crashes the moment you change image resolution |
| Softmax applied before `CrossEntropyLoss` | Gradients silently wrong; loss decreases but model doesn't learn |
| Missing residuals in deep stacks | Vanishing gradients; loss plateaus around random performance |
| `BatchNorm` with batch size 1 (or in eval mode forgotten) | NaNs or zero variance; eval looks great, deployment breaks |
| Forgetting `key_padding_mask` in transformers | Padding tokens influence representations |
| Output dim mismatch (predicting `num_classes-1`) | Off-by-one, silent on multiclass with class 0 majority |
| Initializing transformer with default `nn.init` | Diverges in first 100 steps; needs `xavier_uniform_` or scaled init |
| Adding BatchNorm before Dropout | Subtle but degrades — order is `Conv → BN → Activation → Dropout` |

## Integration

- `skill-model-selection` — picks *which* family of architecture to design within
- `skill-finetuning` — usually preferable to designing from scratch when a backbone exists
- `skill-training` — the loop that uses the model designed here
- `skill-compute-infra` — architecture choices interact with memory and parallelism
- `skill-ml-evaluation` — defines what "the model works" means
- `skill-reproducibility` — initialization seeds matter for architecture experiments
- `shared/skill-debugging` — when "loss won't go down" needs systematic investigation

## Resources

- [The Annotated Transformer](http://nlp.seas.harvard.edu/annotated-transformer/) — read this before writing your first transformer
- [Karpathy's "A Recipe for Training Neural Networks"](https://karpathy.github.io/2019/04/25/recipe/) — debugging discipline
- [Deep Learning Tuning Playbook (Google)](https://github.com/google-research/tuning_playbook) — architecture/training interactions
- [PyTorch model zoo (`torchvision.models`, `transformers`)](https://pytorch.org/vision/stable/models.html) — start from these, don't roll your own
- [timm](https://github.com/huggingface/pytorch-image-models) — battle-tested image backbones
- [He et al., "Deep Residual Learning"](https://arxiv.org/abs/1512.03385) — why every deep stack has residuals
