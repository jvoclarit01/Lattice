---
name: model-lattice
description: Mode orchestrator for AI/ML systems — models, training pipelines, evaluation, MLOps, RAG, LLM applications. Activated automatically by Lattice.md when the user describes an ML/AI project. Coordinates the DPEV loop with phase artifacts where each phase is typically an experiment or pipeline stage. Orchestrates eligible domain skills from domains/ml/ and domains/shared/.
---

# model-lattice Mode

AI/ML systems orchestrator. Coordinates the DPEV loop across data, model, training, evaluation, and serving phases.

## When This Mode Activates

The user is building any ML/AI system:

- **Models:** classification, regression, sequence, vision, multimodal
- **LLM apps:** RAG, agents, chatbots, fine-tuned models
- **Pipelines:** data collection → preprocessing → training → evaluation → serving
- **MLOps:** model serving, monitoring, drift detection, retraining

Trigger phrases (caught by `Lattice.md` mode detection):
- "ML model", "AI system", "machine learning", "deep learning"
- "RAG", "LLM app", "fine-tune", "embeddings"
- "train a model", "evaluate", "deploy a model"
- "dataset", "preprocessing", "feature engineering"

## Required Protocols on Entry

Load these from `shared/`:

- `unsure-protocol.md`
- `resume-protocol.md`
- `brainstorming-protocol.md`
- `phase-artifacts-protocol.md`
- `dpev-loop-protocol.md`
- `verification-protocol.md`
- `references/anti-patterns-reference.md`

## The Workflow

### 1. Project initialization

If no `.lattice-plan.md` exists:

1. Apply `questioning-protocol.md` to gather the brief. ML-specific items:
   - Problem domain and ML task type (classification / regression / generation / retrieval / etc.)
   - Data situation (have / need to collect / synthetic / labeled vs unlabeled)
   - Success metrics (the metric(s) and the threshold)
   - Compute budget
   - Latency / cost / interpretability constraints
   - Ethical considerations and bias risks
2. Confirm the brief
3. Decide approach (apply Unsure Protocol — traditional ML vs deep learning vs transfer learning vs fine-tuning, framework choice)
4. Initialize `.lattice-plan.md`
5. Decompose into phases. Common ML phase sequence:
   - `01-data-pipeline/` — collection, preprocessing, versioning, splits
   - `02-baseline-model/` — first end-to-end working model
   - `03-experiment-A/` — first hypothesis test
   - `04-experiment-B/` — second hypothesis test
   - `05-serving/` — deployment infrastructure
   - `06-monitoring/` — drift detection, retraining triggers
6. Get user approval

### 2. Per-phase DPEV loop

For the next pending phase:

**During DISCUSS:** lock the experimental hypothesis or pipeline-stage decisions in `CONTEXT.md`. Common ML decisions:
- Hypothesis (for experiment phases) — what specifically are we testing?
- Dataset version and splits
- Model architecture / family
- Hyperparameters that vary vs are fixed
- Evaluation metric and threshold for "success"
- Reproducibility requirements (seeds, environment, hardware)

**During PLAN:** apply `writing-plans-protocol.md`. Tasks include data loading, model setup, training run, evaluation pass, results write-up. Verify with `plan-checker-protocol.md`.

**During EXECUTE:**
- Apply `domains/shared/skill-tdd.md` for preprocessing functions, evaluation utilities, feature engineering — these are pure functions and ideal TDD candidates
- For training loops, replace strict TDD with smoke tests on toy data + loss-decreases assertions
- Update SUMMARY.md with metrics, configs, observations as runs complete
- For long-running training: configure correctly, start, document; full verification happens when run finishes
- If a bug appears, apply `skill-debugging.md`
- For multiple ablations or research arms, apply `parallel-agents-protocol.md`

**During VERIFY:**
- Apply `verification-protocol.md` — quote actual metric values, not "looks good"
- Confirm metrics meet the threshold defined in CONTEXT.md
- Confirm reproducibility (seed, environment, hardware documented)
- Apply `skill-self-review.md` for major changes (data leakage, train/test contamination, metric correctness)
- Confirm decision coverage end-to-end
- Write VERIFICATION.md with actual numbers, not promises

### 3. Phase completion

After VERIFY passes:
1. Update `.lattice-plan.md` phase status to Done
2. Append the experiment record to the experiment log section
3. Move to next phase or escalate if results suggest changing direction

### 4. Project completion

When all phases are Done:
1. Final reproducibility review
2. Generate model card and README with usage instructions
3. Document evaluation methodology and limitations
4. Hand back to `Lattice.md`

## Eligible Domain Skills

### ML domains (`domains/ml/`)

| Skill | Activate when |
|---|---|
| `skill-data-collection` | Acquiring or generating data |
| `skill-data-preprocessing` | Cleaning, normalizing, transforming |
| `skill-feature-engineering` | Building features for traditional ML |
| `skill-data-versioning` | Tracking dataset versions (DVC, etc.) |
| `skill-model-selection` | Choosing model family/architecture |
| `skill-model-architecture` | Designing custom architectures |
| `skill-training` | Setting up and running training |
| `skill-finetuning` | Fine-tuning pretrained models |
| `skill-ml-evaluation` | Designing eval and metrics |
| `skill-ml-results-interpretation` | Analyzing and reporting results |
| `skill-experiment-tracking` | Tracking runs, hyperparameters (W&B, MLflow) |
| `skill-explainability` | Model interpretability (SHAP, LIME) |
| `skill-bias-and-fairness` | Auditing for bias, ensuring fairness |
| `skill-prompt-engineering` | Designing prompts for LLM applications |
| `skill-rag` | Retrieval-augmented generation systems |
| `skill-model-serving` | Deploying models for inference |
| `skill-mlops` | Pipelines, orchestration, automation |
| `skill-monitoring` | Production monitoring, drift detection |
| `skill-compute-infra` | GPU/TPU setup, distributed training |

### Shared domains (`domains/shared/`)

Same as project-lattice — `skill-tdd`, `skill-testing`, `skill-debugging`, `skill-self-review`, `skill-receiving-feedback`, `skill-security`, `skill-docs`, `skill-performance`, `skill-reproducibility`, `skill-ethics`.

For ML, `skill-reproducibility` and `skill-ethics` are typically always activated.

## Per-Mode Quality Notes

- **Reproducibility is mandatory.** Every experiment phase records seed, environment, hardware, dataset version, and exact configs. Apply `skill-reproducibility`.
- **Metrics are evidence.** Apply `verification-protocol.md` rigorously: claims like "the model improved" require quoted before/after numbers.
- **Beware data leakage and contamination.** `skill-self-review` for ML focuses on this; train/test/val splits stay separate, no future information in features.
- **Document negative results.** Failed experiments still go in `.lattice-plan.md`'s experiment log. Future you (and reviewers) need this to avoid repeating dead ends.
- **Fairness and bias are not optional.** For models with human impact, `skill-bias-and-fairness` is part of every evaluation phase, not a final check.
- **Single-feature TDD.** Preprocessing and evaluation utilities get TDD. Training loops get smoke tests, not full TDD.

## Handoff Back to Lattice

When the project (or a major experiment chain) is complete:
1. Update `.lattice-plan.md` with final status and full experiment log
2. Hand back to `Lattice.md`
