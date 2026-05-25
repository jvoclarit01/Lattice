---
name: skill-research-methodology
description: Designing and writing the Methodology chapter of a thesis — choosing among experimental, observational, ML training/evaluation, and qualitative designs; reporting at the level of detail required for replication; documenting data, materials, procedures, analysis plan, and ethics. Use when planning a study, writing the Methods chapter, or auditing methodological rigor before defense. For ML-specific evaluation procedure see `domains/ml/skill-ml-evaluation`; for dataset documentation specifically see `skill-dataset-documentation`.
---

# Research Methodology

The Methodology chapter has one job: enable a competent peer to replicate the study. Everything else — elegance, rationale, completeness — serves that job.

## When to Activate

Use when:
- Designing a thesis study before data collection or training
- Writing or revising the Methodology / Methods chapter
- A reviewer flags methodology as insufficiently described
- Choosing between experimental, observational, mixed, or ML evaluation designs
- Justifying a methodological choice to an advisor or committee
- Auditing reproducibility before submission

**Trigger phrases:** "methodology", "methods chapter", "research design", "how do I justify…", "is this rigorous enough", "replication detail", "study design"

## When NOT to Use

| Situation | Use instead |
|---|---|
| Reporting the actual results | `skill-results-writing` |
| Documenting a specific dataset's provenance | `skill-dataset-documentation` |
| Writing the ML model architecture description | `skill-model-description` |
| ML evaluation methodology specifically (metrics, splits) | `domains/ml/skill-ml-evaluation` |
| ML experiment design specifically | `skill-ml-experiment-design` |
| Discussing what the results mean | `skill-discussion-writing` |
| Reviewing prior methodology in literature | `skill-literature-review` |
| Sentence-level prose polish | `skill-academic-writing` |

## Iron Laws

1. **Replicability is the standard.** A peer with your Methods chapter, the artifacts cited, and standard tooling should be able to reproduce your study without contacting you.
2. **Justify every design choice in one sentence.** "We used X because Y" beats "We used X." Implicit choices invite reviewer challenge.
3. **State what you did, not what you should have done.** Methodology is descriptive of the actual study, not aspirational. Limitations belong in Discussion.
4. **Pre-register or label exploratory.** Analyses planned before data inspection are confirmatory; analyses developed after are exploratory. Mixing these without labels is HARKing.

## Methodology Selection Rubric

Pick the design that fits the research question. Mismatched design is the largest source of methodological objections.

| Research question shape | Likely design | Notes |
|---|---|---|
| "Does X cause Y?" — controllable X | Randomized experiment | Gold standard for causal claims; required for clinical, often required for HCI |
| "Does X cause Y?" — uncontrollable X | Quasi-experiment / natural experiment / IV | Requires identification strategy; weaker causal claim |
| "Does method M outperform baseline B on task T?" | ML benchmark evaluation | Multiple datasets, multiple seeds, statistical test |
| "How does method M behave under condition C?" | Ablation / controlled empirical study | Vary C, hold everything else constant |
| "What is the prevalence / distribution of phenomenon P?" | Observational / survey | Sampling strategy is load-bearing |
| "What does it feel like to / how do practitioners think about Q?" | Qualitative (interviews, ethnography) | Saturation, thematic analysis, reflexivity |
| "Does the literature converge on conclusion C?" | Systematic review / meta-analysis | PRISMA reporting; search protocol pre-registered |
| "Is theorem T true?" | Mathematical proof | Methods chapter is short; proof technique discussion belongs in body |
| Multiple of the above | Mixed methods | Justify integration design (sequential vs concurrent) |

If your RQ does not fit any row, the RQ is too vague — sharpen it before designing the study.

## The Standard Methodology Chapter Skeleton

Most empirical theses use this structure. Adapt section depth to the dominant design.

1. **Research Design and Rationale** — overall approach; why this design fits the RQs.
2. **Data and Sample** — population, sampling, IRB/ethics, dataset provenance.
3. **Materials / Instruments / Models** — survey instruments, lab equipment, ML model architecture; cite or attach the artifact.
4. **Procedure** — what was done, in chronological order, at the level of detail a peer needs to replicate.
5. **Analysis Plan** — for each RQ, the statistical test or evaluation procedure that addresses it; significance threshold; effect size measure.
6. **Reproducibility** — code, data, hardware, software versions, random seeds; pointer to repository.
7. **Ethics and Limitations of Method** — IRB, consent, anonymization, conflicts of interest. (Substantive limitations live in Discussion.)

## Depth: Quantitative / Experimental

The most common shape in CS, ML, and engineering theses.

**Required reporting:**
- Sample size justification — power analysis or pre-registration of N
- Random assignment procedure — RNG seed, allocation method
- Manipulation specification — exactly what differed between conditions
- Outcome measure — operational definition, validity citation
- Analysis plan — primary test, correction for multiple comparisons, significance threshold

**Worked example (ML benchmark eval):**
> We evaluate Method M against three baselines (B1, B2, B3) on five public benchmarks (D1–D5; Table 3.1). For each method × dataset combination, we run training with 5 random seeds (42, 1337, 2024, 7, 11) and report mean ± standard deviation of the primary metric (macro-F1) and 95% bootstrap confidence intervals (10,000 resamples). The primary statistical test is a paired permutation test (n = 10,000 permutations) on per-instance scores, with Holm-Bonferroni correction across the five datasets. Hyperparameters are selected on a held-out validation split via random search with budget B = 50 (search space in Appendix A).

This passage tells a reader (a) what was compared, (b) at what statistical scale, (c) with what randomness control, (d) under what hyperparameter budget — i.e., what they need to replicate.

## Depth: Qualitative / Interview-Based

Less common in CS theses but standard in HCI and information systems.

**Required reporting:**
- Sampling strategy (purposive, snowball, theoretical) and saturation criterion
- Recruitment and consent procedure
- Interview guide (attached as appendix)
- Recording and transcription procedure
- Coding protocol — initial codebook, inter-rater reliability if multiple coders, refinement procedure
- Reflexivity statement — researcher's relationship to participants and topic

**Worked example:**
> We conducted semi-structured interviews with 18 software engineers from three organizations (selected via theoretical sampling per Charmaz, 2014; saturation reached at interview 16). The interview guide (Appendix C) covered three topics: prior tooling, current workflow, and unmet needs. Interviews lasted 45–60 minutes, were audio-recorded with consent (IRB protocol 2023-104) and transcribed verbatim. Two researchers independently coded the first six transcripts using open coding; the codebook was reconciled and applied to remaining transcripts (Cohen's κ = 0.79 across three random checks).

## Depth: Mixed Methods

Justify *why* mixed and how the components integrate. The most common defect is two unrelated studies stapled together.

| Integration design | When to use |
|---|---|
| Sequential explanatory (quant → qual) | Quant identifies a pattern; qual explains it |
| Sequential exploratory (qual → quant) | Qual generates hypotheses; quant tests them |
| Concurrent triangulation | Both methods address same RQ; convergence strengthens claim |
| Concurrent embedded | One method is primary; the other supports a secondary RQ |

State the design explicitly. Without that label, reviewers infer it themselves and often disagree.

## Reproducibility Requirements (CS / ML focus)

Modern CS conferences and most CS PhD committees expect:

- [ ] Code released (or available on request) — repository link in the chapter
- [ ] Data released, or instructions for accessing the original source
- [ ] Hardware specification — GPU model, RAM, CPU
- [ ] Software environment — frozen `requirements.txt`, `environment.yml`, or container image
- [ ] All random seeds reported
- [ ] Hyperparameters reported, including those for baselines
- [ ] Compute budget reported (GPU-hours)
- [ ] License under which artifacts are released

The NeurIPS / ACL / EMNLP "reproducibility checklist" is a useful template even for non-ML theses.

## Pre-Registration and Exploratory Labeling

A defense-grade Methodology chapter distinguishes:

- **Confirmatory analyses** — pre-registered or stated before data inspection. These get the strong language ("we test the hypothesis…").
- **Exploratory analyses** — discovered during analysis. These get hedged language ("we additionally observe…") and are flagged as exploratory in Results.

The convention protects against HARKing. Mixing the two without labels is the most common methodological objection in 2024-era ML theses.

## Common Failure Modes

| Pattern | Consequence |
|---|---|
| Methodology chapter < 5 pages in an empirical thesis | Cannot be replicated; almost always rejected |
| "We used standard techniques" with no citation or detail | Standard ≠ self-evident; reviewers will probe |
| Hyperparameters reported for the proposed method but not the baseline | Suggests unfair comparison |
| One random seed, no seed disclosure | Reviewer demands seed analysis; result may not survive |
| No power analysis for a study claiming a null result | Insufficient power, not absence of effect |
| Qualitative coding by one researcher with no reliability check | Standard threshold for qualitative rigor not met |
| Pre-registration absent in a confirmatory framing | Cannot distinguish from HARKing |
| Limitations buried in Methodology rather than Discussion | Discussion has nothing to say; reader confused about scope |
| Ethics / IRB unmentioned in human-subjects work | Hard rejection at most departments |

## Pre-Submission Methodology Audit

- [ ] Research design name stated and justified
- [ ] Sample / dataset described including size justification
- [ ] Materials / instruments / model attached or cited
- [ ] Procedure described in chronological order
- [ ] Analysis plan maps each RQ to a specific test or evaluation
- [ ] Reproducibility artifacts referenced
- [ ] Pre-registration status disclosed (or "exploratory" labels applied)
- [ ] Ethics / IRB statement present where applicable
- [ ] Each design choice has a one-sentence justification
- [ ] Domain-specific reporting standard followed (CONSORT, STROBE, PRISMA, NeurIPS checklist, etc.)
- [ ] `skill-academic-writing` and `skill-avoid-ai-writing` have been run on the chapter

## Integration

- `domains/thesis/skill-results-writing` — Methodology specifies what; Results report the outcome
- `domains/thesis/skill-discussion-writing` — substantive limitations of method belong here, not in Methodology
- `domains/thesis/skill-dataset-documentation` — for datasets contributed by the thesis itself
- `domains/thesis/skill-model-description` — for ML model architecture detail
- `domains/thesis/skill-ml-experiment-design` — design of the experiments referenced in Methodology
- `domains/ml/skill-ml-evaluation` — choice of metrics and splits
- `domains/ml/skill-reproducibility` — checklist-grade reproducibility detail
- `domains/thesis/skill-thesis-structure` — chapter ordering and length budget
- `domains/thesis/skill-argument-validator` — methodology validity is a precondition for argument validity
- `domains/thesis/skill-academic-writing` — register and tense rules

## Resources

- [NeurIPS / ML Reproducibility Checklist](https://www.cs.mcgill.ca/~jpineau/ReproducibilityChecklist.pdf) — by Joelle Pineau; canonical for ML
- [PRISMA 2020 Statement](https://www.prisma-statement.org/) — for systematic reviews and meta-analyses
- [CONSORT 2010 Statement](https://www.equator-network.org/reporting-guidelines/consort/) — for randomized clinical and HCI experiments
- [STROBE Statement](https://www.strobe-statement.org/) — for observational studies
- [Open Science Framework — Pre-registration](https://osf.io/prereg/) — pre-registration templates and rationale
- [Charmaz, *Constructing Grounded Theory* (2nd ed.)](https://us.sagepub.com/en-us/nam/constructing-grounded-theory/book235960) — qualitative analysis standard
- [Field & Hole, *How to Design and Report Experiments*](https://uk.sagepub.com/en-gb/eur/how-to-design-and-report-experiments/book207175) — pragmatic reference for experimental design and reporting
