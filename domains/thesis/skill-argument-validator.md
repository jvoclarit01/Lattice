---
name: skill-argument-validator
description: Auditing the logical structure of thesis claims — checking that conclusions follow from evidence, that warrants connecting data to claims are explicit, and that the most common ML/empirical argument flaws (overgeneralization from one dataset, post-hoc reasoning, p-hacking framing) are not present. Use when defending a contribution, anticipating reviewer objections, or auditing the argument chain in Discussion or Conclusion. For sentence-level prose polish see `skill-academic-writing`; for terminology consistency see `skill-consistency-checker`.
---

# Argument Validator

A thesis is an argument. The data, methods, and results are evidence; the contribution is the conclusion that the evidence supports. This skill checks that the chain holds.

## When to Activate

Use when:
- Reviewing the Discussion or Conclusion before submission
- A claim in the thesis seems stronger than the evidence supports
- Anticipating reviewer objections at defense or peer review
- An advisor says "are you sure about this claim?"
- Comparing your contribution claim against your actual results
- Auditing whether RQs are answered (not merely addressed)

**Trigger phrases:** "validate this argument", "is this claim supported", "logical fallacy check", "reviewer-proof", "stress test the contribution", "does the evidence support…"

## When NOT to Use

| Situation | Use instead |
|---|---|
| Polishing prose at sentence level | `skill-academic-writing` |
| Confirming results are reported correctly | `skill-results-writing` |
| Verifying terminology consistency | `skill-consistency-checker` |
| Checking citation accuracy | `skill-citation-management` |
| Verifying the contribution is genuinely novel | `skill-contribution-checker` |
| Auditing methodology rigor | `skill-research-methodology` |

## Iron Laws

1. **Every claim has data, a warrant, and an explicit scope.** A claim with no data is rhetoric; a claim with no warrant is a leap; a claim with no scope is overgeneralization.
2. **Generalization beyond the evaluated domain requires explicit justification.** If you tested only on English news articles, you cannot conclude the model "generalizes to NLP."
3. **Statistical significance is not effect size, and effect size is not practical importance.** Each requires a separate argument.
4. **Limitations and counterarguments are surfaced, not buried.** If a reviewer can think of a confound in 30 seconds and it isn't acknowledged, the argument fails on credibility before substance.

## The Claim → Data → Warrant Test (Toulmin)

Every load-bearing claim in the thesis must pass this test:

| Component | Question to ask |
|---|---|
| **Claim** | What is being asserted? Stated as a single declarative sentence? |
| **Data** | What concrete evidence (numbers, table, figure, citation) supports the claim? |
| **Warrant** | What rule or principle licenses inferring the claim from the data? Is it stated or hidden? |
| **Backing** | What supports the warrant itself — prior literature, theory, established benchmark? |
| **Qualifier** | What scope, sample, or condition limits the claim? |
| **Rebuttal** | What evidence would falsify it, and is that evidence absent? |

If you can't fill in all six for a claim in your contribution chapter, the claim is under-defended.

### Worked Example

**Claim:** "Our domain-adapted transformer outperforms BERT on medical NLP."

| Component | Audit |
|---|---|
| Data | F1 = 0.94 vs 0.82 on MedNLI; F1 = 0.91 vs 0.79 on i2b2-NER |
| Warrant | Higher F1 on the same test sets indicates better task performance |
| Backing | F1 is the standard metric in both benchmarks (citations) |
| Qualifier | On these two benchmarks, English clinical text only |
| Rebuttal | Possible: BERT was not retrained on the same compute budget. Addressed in §5.2 |
| Claim, revised | "On MedNLI and i2b2-NER, our domain-adapted transformer outperforms BERT by 8–12 F1 points (Table 4); generalization to other medical NLP tasks remains an open question." |

The qualifier ("on these benchmarks") and the explicit rebuttal handling are what make the revised claim defensible.

## ML- and Empirical-Specific Argument Flaws

These are the argument failures most common in empirical and ML theses. Patch them before defense.

| Flaw | What it looks like | Fix |
|---|---|---|
| **Single-dataset overgeneralization** | "Our method outperforms baselines" after testing on one dataset | Either run on ≥3 datasets or scope the claim to the dataset |
| **Cherry-picked baselines** | Comparing only to weak or outdated baselines | Include current SOTA; if missing, justify explicitly |
| **Significance without effect size** | "p < .001" with no Cohen's d, F1 delta, or CI | Report effect; large N can make tiny effects significant |
| **Effect size without practical importance** | "0.3 F1 improvement" framed as a major contribution | Argue for practical relevance (compute, deployment cost) |
| **Train-test contamination unaddressed** | Reporting test scores without a leakage audit | Document data split provenance and run a leakage probe |
| **HARKing (Hypothesizing After Results Known)** | Hypotheses in the intro that match results suspiciously well | Pre-registration trail or Methodology timestamp; or label as exploratory |
| **p-hacking framing** | Reporting only the significant runs, no mention of seeds tried | Report mean ± std over ≥3 seeds; full run table in appendix |
| **Post-hoc rationalization** | Discussion explains "why" results came out this way without testing the explanation | Either test the explanation or label as speculation |
| **Causal language from correlational data** | "X causes improved performance" from observational comparison | Replace "causes" with "is associated with"; design an interventional study for causal claims |
| **Conflated levels of evaluation** | Mixing per-instance, per-class, and aggregate metrics without flagging | Separate the evaluation tiers; primary metric named explicitly |
| **Generalization across tasks claimed from one task** | Section title: "X for NLP"; experiments: one classification benchmark | Rescope title and abstract; add multi-task experiments or label as exploratory |

## Classical Logical Fallacies (still apply)

The classics still bite empirical work:

- **Affirming the consequent.** "If H is true, we expect to observe D. We observed D. Therefore H." Other hypotheses also predict D — list them.
- **Circular reasoning.** "The method is fair because it satisfies our fairness metric, which we defined as what the method satisfies." Surface the definition before claiming the property.
- **False dilemma.** "Either deep learning or hand-crafted features." Hybrid approaches usually exist.
- **Appeal to authority alone.** "Hinton (2018) said this, therefore it is true." Authority motivates; evidence justifies.
- **Straw man comparison.** Defining the baseline narrowly so your method automatically wins. Use the strongest baseline you reasonably can.
- **Hasty generalization.** Three case studies extrapolated to a population. Bound the claim to the studied units.

## Counterargument Discipline

A reviewer-proof Discussion explicitly handles the three strongest objections to the contribution.

For each objection, write one paragraph that:
1. **States** the objection in its strongest form (steel-man it; do not straw-man).
2. **Concedes** what is genuinely valid in it.
3. **Refutes or scopes** what the objection implies — with evidence or by limiting the claim.

If the strongest objection has no concession-worthy element and no refutation, your claim is too strong. Weaken it.

## "Strength of Evidence" Ladder

Calibrate language to the evidence tier. Reviewers notice when claims outrun the ladder.

| Evidence | Acceptable language |
|---|---|
| Single experiment, single dataset, single seed | "We observe…" / "In this setting…" |
| Single experiment, multiple seeds with CIs | "Our method achieves…" / "On benchmark X…" |
| Multiple datasets, multiple seeds, controlled comparisons | "Our method outperforms baselines on the studied tasks…" |
| Multiple datasets across domains, replicated by independent groups | "The approach generalizes to…" |
| Theoretical guarantee + matching empirics | "We prove… and confirm empirically that…" |

If your evidence is at tier 1 but your abstract claims tier 4 generality, the gap is the failure point.

## Common Failure Modes

| Pattern | Why it fails |
|---|---|
| Contribution chapter restates Results without defending the inferential leap | Reviewer asks "so what?" and there is no answer |
| Limitations section is two sentences and concedes nothing material | Reads as performative; suggests author has not stress-tested the work |
| "Our method is robust" without ablations or perturbation experiments | Robustness is a claim that needs robustness experiments |
| "This generalizes" after testing on one English benchmark | Single-dataset overgeneralization; defense reviewer flag |
| Claims about *why* a model works ("attention learns syntax") with no probe | Post-hoc rationalization; demand a controlled test |
| Statistical significance reported, effect size omitted | Reviewer asks for effect size, finds it small, contribution shrinks |
| Future work doubles as an admission of unaddressed scope | Use scope qualifier in claim instead — be honest, not decorous |

## Pre-Defense Argument Audit

- [ ] Every load-bearing claim passes the Toulmin six-component check
- [ ] Each ML-specific flaw above has been searched for explicitly
- [ ] Three strongest counterarguments are surfaced and handled
- [ ] Language matches the evidence ladder tier — no upward drift
- [ ] Statistical significance, effect size, and practical importance are separated
- [ ] No causal language survives where the design is correlational
- [ ] Generalization claims are scoped to evaluated domains
- [ ] Limitations section is substantive, not decorative

## Integration

- `domains/thesis/skill-academic-writing` — polishes the prose this skill validates the logic of
- `domains/thesis/skill-discussion-writing` — Discussion is where most argument failures surface
- `domains/thesis/skill-conclusion-writing` — Conclusion's contribution claims must survive this audit
- `domains/thesis/skill-contribution-checker` — novelty audit complements this logical audit
- `domains/thesis/skill-results-writing` — Results provide the data this skill checks claims against
- `domains/thesis/skill-research-methodology` — design rigor is a precondition for argument validity
- `domains/thesis/skill-consistency-checker` — terminology drift inside an argument is its own bug
- `domains/ml/skill-ml-evaluation` — choice of metrics determines what claims are licensed

## Resources

- [Stephen Toulmin, *The Uses of Argument*](https://www.cambridge.org/core/books/uses-of-argument/26CF801BC12004587B66778297D5567C) — original source for the claim/data/warrant model
- [Anders Ericsson — Internet Encyclopedia of Philosophy: Logical Fallacies](https://iep.utm.edu/fallacy/) — fallacy reference
- [Lipton & Steinhardt, *Troubling Trends in Machine Learning Scholarship* (2018)](https://arxiv.org/abs/1807.03341) — the canonical critique of ML argument failures
- [Gencoglu et al., *HARK Side of Deep Learning* (2019)](https://arxiv.org/abs/1904.07633) — survey of HARKing and post-hoc rationalization in ML
- [Stanford Encyclopedia of Philosophy — Scientific Explanation](https://plato.stanford.edu/entries/scientific-explanation/)
