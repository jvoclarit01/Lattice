---
name: skill-finetuning
description: Adapting a pretrained model to a downstream task — full fine-tuning, parameter-efficient methods (LoRA, QLoRA, adapters, prefix-tuning), instruction tuning, and the discipline that prevents catastrophic forgetting and overfitting on small datasets. Use when adapting a foundation model to your data, choosing between full FT and PEFT, debugging a fine-tune that lost the base model's capabilities, or preparing a deployable adapter. For training from scratch see `skill-training`; for prompting an unmodified model see `skill-prompt-engineering`.
---

# Fine-tuning

Fine-tuning is not "training, but with weights pre-loaded." Pretrained models bring fragile, expensive-to-restore capabilities that aggressive fine-tuning destroys. The discipline is to change as little of the model as possible while teaching the task — which is why parameter-efficient methods are now the default, not the exception.

## When to Activate

Use when:
- Adapting an LLM, vision model, or audio model to a new task / domain / format
- Deciding between full fine-tuning and PEFT (LoRA, QLoRA, adapters, prefix-tuning)
- Instruction-tuning or RLHF/DPO-style preference fine-tuning
- The base model "knows" the topic but produces the wrong style/format
- Targeting a deploy-time constraint (one model, many adapters)
- A fine-tune is overfitting, catastrophically forgetting, or losing safety properties

**Trigger phrases:** "fine-tune", "LoRA", "QLoRA", "PEFT", "adapter", "instruction tuning", "DPO", "SFT", "catastrophic forgetting", "frozen backbone", "trainer.train()", "PeftConfig".

## When NOT to Use

| Situation | Use instead |
|---|---|
| Training a model from random initialization | `skill-training` |
| Steering an unmodified base model with prompts | `skill-prompt-engineering` |
| Adding retrieval to ground a base model in your data | `skill-rag` |
| Choosing which base model to start from | `skill-model-selection` |
| Picking metrics to evaluate the fine-tuned model | `skill-ml-evaluation` |
| Hosting / batching the fine-tuned model | `skill-model-serving` |
| Catching bias introduced by the fine-tune dataset | `skill-bias-and-fairness` |

## Iron Laws

1. **Try prompts and RAG first.** Fine-tuning is the heaviest, most expensive, hardest-to-revert lever. If a well-engineered prompt or retrieval augmentation hits your bar, ship that.
2. **PEFT before full fine-tuning.** A LoRA adapter trained at 1-5% of the parameters reaches near-full-FT quality on most adaptation tasks at a fraction of the cost and with no catastrophic forgetting. Reach for full FT only when PEFT demonstrably underperforms.
3. **Hold out a "general capability" eval.** Fine-tuning silently degrades unrelated abilities. Always measure on the original benchmarks (or a small slice of them) AS WELL as your task metric — see "Catastrophic Forgetting" below.
4. **Lower the LR by 10-100× from training-from-scratch.** The base model is in a delicate basin; large updates ruin what's already there.

## Decision Rubric — Which Method?

| Goal | Method | Trainable params | Notes |
|---|---|---|---|
| New domain knowledge in a small format | **LoRA** | ~0.1-1% | Default. Composable, swappable adapters at inference. |
| Same as above but VRAM is tight | **QLoRA** | ~0.1-1%, 4-bit base | Train 70B on a single 80 GB GPU. Slight quality cost vs LoRA. |
| Adjust output style / format only | **Prefix tuning / IA³** | <0.1% | Cheapest. Limited expressive power. |
| Adapt vision encoder for new domain | **Adapter modules** | ~1-5% | Standard for vision; well-trodden for transformers. |
| Need to truly absorb new knowledge at scale | **Full fine-tuning** | 100% | Expensive. Highest quality ceiling. Catastrophic forgetting risk. |
| Align outputs to human preference | **DPO / KTO** | LoRA or full | Pairs of (chosen, rejected). Simpler than RLHF. |
| Continue pretraining on a corpus | **Continued pretraining** | 100% | Big domain shifts. Use very small LR. Effectively a separate phase before any task FT. |

For most LLM use cases in 2026, **start with LoRA via Hugging Face PEFT**. Move to QLoRA if VRAM-bound. Move to full FT only with strong evidence PEFT is the bottleneck.

## LoRA — The Default Recipe

```python
from transformers import (AutoModelForCausalLM, AutoTokenizer,
                          TrainingArguments, Trainer, DataCollatorForLanguageModeling)
from peft import LoraConfig, get_peft_model, TaskType
from datasets import load_dataset

base = "meta-llama/Llama-3.1-8B"
tokenizer = AutoTokenizer.from_pretrained(base)
model = AutoModelForCausalLM.from_pretrained(base, torch_dtype="bfloat16")

# Adapter config — these target attention projections; targets vary by architecture
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=16,                                                       # rank — 8-64 typical
    lora_alpha=32,                                              # scaling — usually 2*r
    lora_dropout=0.05,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],    # check model card
    bias="none",
)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# trainable params: 41,943,040 || all params: 8,072,204,288 || trainable%: 0.52

# ... tokenize a dataset ...

args = TrainingArguments(
    output_dir="./lora-out",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,                              # effective batch = 16
    learning_rate=2e-4,                                         # higher than full FT (~10×)
    lr_scheduler_type="cosine",
    warmup_ratio=0.03,
    bf16=True,
    logging_steps=10,
    eval_strategy="steps",
    eval_steps=200,
    save_strategy="steps",
    save_steps=200,
    save_total_limit=3,
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    report_to="wandb",                                          # or "mlflow", "tensorboard"
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=train_ds,
    eval_dataset=eval_ds,
    tokenizer=tokenizer,
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
)
trainer.train()
model.save_pretrained("./lora-adapter")                         # adapter only — small file
```

Two facts that surprise new users:
- The saved adapter is tens of MB, not gigabytes — only the LoRA matrices, not the base model.
- LoRA's effective LR is ~10× what you'd use for full FT. The default of 2e-4 is roughly right.

## QLoRA — When VRAM Is the Constraint

```python
from transformers import BitsAndBytesConfig, AutoModelForCausalLM
from peft import prepare_model_for_kbit_training, LoraConfig, get_peft_model

bnb = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",                                  # NormalFloat4 — paper default
    bnb_4bit_compute_dtype="bfloat16",
    bnb_4bit_use_double_quant=True,
)
model = AutoModelForCausalLM.from_pretrained(base, quantization_config=bnb,
                                             device_map="auto")
model = prepare_model_for_kbit_training(model)
model = get_peft_model(model, lora_config)                      # same lora_config as above
```

QLoRA quantizes the frozen base to 4-bit and trains LoRA adapters in bf16 on top. Quality difference vs LoRA is typically <1% on most benchmarks; memory savings are 2-3×. The main cost is slower per-step throughput.

## Inference With an Adapter

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

base = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-8B", torch_dtype="bfloat16")
model = PeftModel.from_pretrained(base, "./lora-adapter")

# Optional: merge adapter into base weights for faster inference (loses swappability)
merged = model.merge_and_unload()
merged.save_pretrained("./merged-model")
```

Two deployment shapes:
- **Adapter mode** — keep base + adapter separate; serve many adapters from one base. Best for multi-tenant / multi-task.
- **Merged mode** — fuse adapter into base for ~10% faster inference. Best for single-task production.

## Catastrophic Forgetting

Aggressive fine-tuning can erase capabilities that came with the base model. Defenses:

1. **Use PEFT.** Most catastrophic-forgetting failures happen with full FT and large LR. LoRA's structural sparsity is a strong protector.
2. **Hold-out general eval.** Run a small slice of the original benchmarks (e.g., 200 MMLU questions) before and after fine-tuning. If general scores drop more than your task scores rise, the trade is bad.
3. **Mix in pretraining-style data.** Adding 5-10% generic instruction-following or pretraining-distribution data to the SFT mix preserves general capability.
4. **Lower the LR or fewer epochs.** If general eval drops, halve the LR or stop training earlier.

```python
def general_capability_check(model, eval_questions: list[dict]) -> float:
    """Run a held-out general-capability slice and return accuracy."""
    correct = 0
    for q in eval_questions:
        out = model.generate(...)
        if out.strip() == q["answer"].strip():
            correct += 1
    return correct / len(eval_questions)
```

Track this metric in `skill-experiment-tracking` like any other. Treat a regression here as seriously as a regression on the task metric.

## Instruction / Chat Fine-Tuning

If the base is a *base* model (not Instruct), apply the chat template the deploy stack expects:

```python
def format_example(example: dict) -> dict:
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user",   "content": example["question"]},
        {"role": "assistant", "content": example["answer"]},
    ]
    text = tokenizer.apply_chat_template(messages, tokenize=False)
    return {"text": text}

train_ds = train_ds.map(format_example)
```

Mismatched chat templates between training and serving are the #1 silent SFT bug — the model trains fine but produces garbled outputs at inference because the format is different.

## DPO — Preference Fine-Tuning

For aligning outputs to (chosen, rejected) pairs without RL machinery:

```python
from trl import DPOTrainer, DPOConfig
from peft import LoraConfig

dpo_config = DPOConfig(
    output_dir="./dpo-out",
    beta=0.1,                                                   # KL strength — 0.1 is standard
    learning_rate=5e-6,                                         # lower than SFT
    num_train_epochs=1,                                         # often enough; watch overfit
    bf16=True,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
)

trainer = DPOTrainer(
    model=model,
    ref_model=None,                                             # uses model itself if PEFT
    args=dpo_config,
    train_dataset=preference_ds,                                # needs prompt/chosen/rejected
    tokenizer=tokenizer,
    peft_config=LoraConfig(r=16, lora_alpha=32, ...),
)
trainer.train()
```

DPO is sensitive to data quality. A few hundred high-quality preference pairs often beat tens of thousands of noisy ones.

## Vision / Multimodal Fine-Tuning

```python
import torch
import torchvision.models as models
import torch.nn as nn

backbone = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)

# Freeze all backbone params, replace head, train head only — feature extraction
for p in backbone.parameters():
    p.requires_grad = False
backbone.fc = nn.Linear(backbone.fc.in_features, num_classes)

# Stage 2: unfreeze the last block, lower LR, fine-tune
for p in backbone.layer4.parameters():
    p.requires_grad = True

optimizer = torch.optim.AdamW([
    {"params": backbone.fc.parameters(),     "lr": 1e-3},
    {"params": backbone.layer4.parameters(), "lr": 1e-4},       # 10× lower for backbone
])
```

Two-stage fine-tuning (head-only → unfreeze top blocks) is the safest pattern when data is small.

## Common Failure Modes

| Pattern | Consequence |
|---|---|
| Full fine-tuning a 70B model on 1k examples | Massive overfitting; ruins base model quality; just use LoRA |
| Same LR as training-from-scratch | Catastrophic forgetting; base model destroyed |
| No general-capability eval | Model "improves" on task metric but fails on everything else; you don't notice until users do |
| Mismatched chat template train vs deploy | Garbled outputs in production |
| LoRA targets wrong modules | Adapter trains but doesn't generalize; check model architecture's actual projection names |
| Saving the merged model when you wanted the adapter | Adapter swappability lost; multi-tenant deploy breaks |
| QLoRA without `prepare_model_for_kbit_training` | Subtle gradient issues; loss looks OK but quality regresses |
| Training many epochs on tiny preference data | DPO overfits; stick to 1-2 epochs and watch eval |
| Not freezing the base in PEFT | All params trainable; you've accidentally done full FT |
| Loading adapter onto a different base than it was trained on | Silent quality collapse; pin and verify the base model hash |
| Using fp16 instead of bf16 with PEFT | More NaN-loss issues; bf16 is the modern default for FT |

## Pre-Commit Checklist

- [ ] Started with prompt engineering and/or RAG; fine-tuning is justified
- [ ] Picked PEFT (LoRA/QLoRA) unless full FT is empirically needed
- [ ] LR is 10-100× smaller than training-from-scratch (1e-4 to 5e-6 range)
- [ ] Eval includes both task metric AND general-capability slice
- [ ] Chat template matches deploy-time template
- [ ] Adapter saved separately for multi-tenant; merged for single-task production
- [ ] Run logged with base model hash, dataset version, adapter config — see `skill-reproducibility`
- [ ] Eval set is held-out, not seen during training (look for accidental contamination if data is large)

## Integration

- `skill-training` — provides the loop discipline this skill builds on
- `skill-prompt-engineering` — try this first; cheaper, faster, often enough
- `skill-rag` — the other "first try this" alternative for adding knowledge
- `skill-model-selection` — picking the right base model is upstream of everything here
- `skill-ml-evaluation` — task metrics + general-capability metrics
- `skill-experiment-tracking` — log every run with base model + dataset + config
- `skill-reproducibility` — adapter weights + tokenizer + base model hash all version-pinned together
- `skill-model-serving` — adapter-mode vs merged-mode deploy decisions
- `skill-bias-and-fairness` — fine-tuning data introduces new bias surfaces
- `shared/skill-tdd` — golden-output regression tests catch silent quality drops

## Resources

- [Hugging Face PEFT documentation](https://huggingface.co/docs/peft) — definitive reference
- [QLoRA paper](https://arxiv.org/abs/2305.14314)
- [LoRA paper](https://arxiv.org/abs/2106.09685)
- [DPO paper](https://arxiv.org/abs/2305.18290)
- [TRL library](https://huggingface.co/docs/trl) — DPO, SFT, PPO, KTO trainers
- [Sebastian Raschka — *Practical Tips for Finetuning LLMs*](https://magazine.sebastianraschka.com/p/practical-tips-for-finetuning-llms)
