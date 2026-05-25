---
name: skill-discussion-writing
description: Writing the Discussion chapter — interpreting results, comparing to prior work, surfacing limitations, and proposing the narrow next experiments those limitations imply. Use when drafting or revising Discussion, deciding what counts as interpretation vs reporting, or framing limitations honestly without deflating the contribution. For broad long-horizon research directions and the closing synthesis, route to `skill-conclusion-writing`; for the logical audit of the claims this chapter makes, route to `skill-argument-validator`.
---

# Discussion Writing

The Discussion is where you earn the right to your contribution. Results show *what happened*; Discussion explains *what it means*, *how it relates to prior work*, *what it does not yet support*, and *which next experiments would close the gaps*. Everything else — broad future horizons, closing reflection — belongs in the Conclusion.

## When to Activate

Use when:
- Drafting or revising the Discussion chapter or section
- Deciding whether a sentence is reporting (Results) or interpreting (Discussion)
- Comparing your findings to a specific prior paper
- Writing the Limitations subsection
- Proposing the *next* experiment that would address a specific limitation
- An advisor flags Discussion as "thin," "evasive," or "just a recap of Results"
- Anticipating reviewer pushback on interpretation

**Trigger phrases:** "interpret these results", "discussion section", "what do the results mean", "compare to prior work", "limitations section", "next experiment", "discussion vs conclusion"

## When NOT to Use

| Situation | Use instead |
|---|---|
| Reporting numbers, tests, effect sizes | `skill-results-writing` |
| Broad long-horizon research directions, closing synthesis | `skill-conclusion-writing` |
| Auditing whether a claim is supported by the evidence | `skill-argument-validator` |
| Verifying a contribution claim is novel | `skill-contribution-checker` |
| Surveying prior work to identify the gap | `skill-literature-review` |
| Designing or describing the Methods | `skill-research-methodology` |
| Sentence-level prose register, tense, voice | `skill-academic-writing` |
| Detecting AI-style filler in interpretation prose | `skill-avoid-ai-writing` |

The cleanest test: if the sentence is *narrow and tied to a specific limitation of the work just reported*, it belongs here. If it is *broad and forward-looking* ("future systems should…"), it belongs in the Conclusion.

## Iron Laws

1. **No new results.** A number, table, or figure introduced for the first time in the Discussion is a Results-section defect. If a result is load-bearing for the interpretation, it must already exist in Results.
2. **Every interpretive claim points at a Results subsection or table.** "These findings suggest X" without "(see §4.3, Table 5)" is rhetoric.
3. **Limitations are surfaced, not buried.** A reviewer who can identify a confound in 30 seconds will reject any limitations section that fails to mention it.
4. **Future Work in Discussion is limitations-driven and narrow.** Each entry maps 1:1 to a specific limitation in this chapter and proposes the next experiment to address it. Long-horizon directions live in the Conclusion.
5. **Calibrate language to the evidence tier.** Single dataset → "in this setting…"; multiple datasets and seeds → "our method outperforms…"; theoretical guarantee + empirics → strongest claims permitted.

## The Discussion Skeleton

A defense-grade Discussion has five components in this order. Skipping or merging them is the most common structural defect.

| # | Component | Purpose | Length guide |
|---|---|---|---|
| 1 | **Brief recap** | One paragraph reminding the reader what was found — *not* a re-listing of every number | 1 paragraph |
| 2 | **Interpretation** (RQ by RQ) | What each finding means, scoped to the evidence | 2-4 paragraphs per RQ |
| 3 | **Comparison to prior work** | Confirms / extends / contradicts named prior studies | 1 paragraph per relevant comparison |
| 4 | **Limitations** | Honest enumeration of what the work does *not* support | substantive — not 2 sentences |
| 5 | **Future Work (limitations-driven)** | Next experiments that would address the limitations above | 1 paragraph per limitation |

**Boundary with Conclusion:** Discussion future work is *bounded by this study's limits*. Conclusion future work is *unbounded by them*. They should not be near-duplicates.

## Interpretation Rubric

Every interpretive claim must answer four questions. If any answer is "no" or "unsure," the interpretation needs revision.

| # | Question | Failure mode if "no" |
|---|---|---|
| 1 | **What** is being claimed, in one sentence? | Diffuse interpretation; reader cannot pin the claim down |
| 2 | **Which result** (table / figure / §) supports it? | Floating interpretation; reads as opinion |
| 3 | **What scope** does the evidence license? | Single-dataset overgeneralization (the most common reviewer flag) |
| 4 | **What alternative explanation** has been considered and ruled out? | Post-hoc rationalization; reviewer suggests the alternative |

For each load-bearing interpretive claim, run all four. If the alternative explanation cannot be ruled out, *say so* and either run the experiment that would or scope the claim accordingly.

## Comparison to Prior Work — Patterns

Comparison is not "we differ from Smith." It is one of three relations: **confirms**, **extends**, or **contradicts**. Pick the right one.

| Relation | Pattern | Example |
|---|---|---|
| **Confirms** | "Consistent with [prior, year], who reported X in [setting], we observe X in [our setting]. Our work [adds what?]." | "Consistent with Wei et al. (2022), who reported diminishing returns past 8M tokens on English news, we observe a similar plateau at 10M tokens on biomedical abstracts. Our work extends the finding to a different domain." |
| **Extends** | "[Prior, year] established X in [their setting]. We extend this to [our setting] / [larger N] / [more conditions], finding [specific delta]." | "Park et al. (2023) showed that domain pretraining helps clinical NLP. We extend this to legal NLP and find the effect halves (4.1 vs 8.4 F1)." |
| **Contradicts** | "[Prior, year] reported X. We instead observe Y. The discrepancy may be due to [specific design difference]: [evidence for that explanation]." | "Liu et al. (2021) reported that sparse attention loses 3-5 F1 on long-context QA. We instead observe parity (Table 5). The discrepancy likely reflects our use of bucketed positional encoding (§3.4); ablation in §5.6 supports this." |

A Discussion that compares to "the literature" without naming a study is doing zero comparison. Cite specific work, with the year, and state the relation explicitly.

## Limitations: Honesty Calibrated

A reviewer-proof Limitations section names the things the work cannot defend, in their strongest form. Anything weaker reads as performative.

For each limitation, write one short paragraph that:
1. **States** the limitation specifically — what scope, sample, or condition the work does not cover.
2. **Concedes** the implication — what claim it weakens.
3. **Bounds** the rest — which claims are *not* affected.

| Limitation type | Example phrasing |
|---|---|
| Scope | "Our experiments cover English clinical text. Generalization to non-English clinical NLP is not established by this work." |
| Sample | "The 247 participants were recruited from a single university; demographic diversity is limited (Appendix C). Population-scale claims require broader sampling." |
| Method | "Effect sizes were estimated with 5 random seeds. While CIs are reported, smaller effects observed here may not survive larger-scale replication." |
| Confounds | "Compute budget differed between baseline and proposed method (§3.5). The contribution is the architecture under matched FLOPs; absolute wall-clock comparisons are not licensed." |
| External validity | "All evaluations are offline. In-the-wild deployment introduces distribution shift not modeled in this study." |

A limitations section without at least one *substantive* concession ("we cannot conclude…") is decorative.

## Future Work (Limitations-Driven) — The Critical Boundary

This is the single most-overlapped section between Discussion and Conclusion. Keep it sharp.

**Rule:** Each future-work entry in the Discussion maps 1:1 to a limitation in the same chapter and proposes the *next experiment* that would address it. Nothing broader.

| Allowed in Discussion future work | Belongs in Conclusion future work |
|---|---|
| "A multi-language replication with 5 additional clinical corpora would establish whether our F1 gains transfer beyond English." | "Long-term, fully multilingual clinical NLP requires standardized cross-lingual benchmarks." |
| "An ablation isolating positional encoding under matched compute would test the §5.6 explanation for the contradiction with Liu et al." | "Sparse attention may eventually replace dense attention for long-context inference." |
| "Re-running the user study with a larger and more demographically diverse sample (target N ≥ 600) would license population-scale claims." | "Future HCI research should examine cross-cultural variation in tooling adoption." |

If a future-work entry could be in either column, force it into the Discussion column by attaching a specific limitation. If it cannot be attached, it belongs in the Conclusion.

## Worked Example

**Bad (recap, no interpretation, no scope, future work generic):**
> Our results show that domain-adapted transformers significantly outperform general models. This is interesting and aligns with the literature. There are some limitations to our study. Future research could explore many directions including transfer learning, multimodal data, longitudinal studies, and ethical implications.

Audit: re-states Results without interpreting; "the literature" is unnamed; limitations are unspecified; future work is a thesaurus dump unattached to any limitation.

**Good (interpretation scoped, comparison named, limitations honest, future work limitations-driven):**
> The 12.3 F1 advantage of our domain-adapted transformer over general-purpose BERT (Table 4) supports the interpretation that lexical overlap with the evaluation domain — not parameter count — drives performance on MedNLI and i2b2-NER. This extends Park et al. (2023), who reported similar gains on radiology reports, to two new clinical sub-domains. Two limitations bound the claim. First, both benchmarks are English; transfer to non-English clinical text is not established. Second, our compute budget was matched on FLOPs, not wall-clock time, so deployment-time comparisons remain open. Two next experiments follow directly. A replication on the Spanish ClinicalBERT benchmark (Pérez et al., 2024) would test the cross-lingual scope of the first limitation. A wall-clock-matched comparison on inference at 4-bit quantization would address the second.

The improved version interprets, scopes, names a comparison, concedes specifically, and ties next experiments to the conceded limitations.

## Common Failure Modes

| Pattern | Why it fails |
|---|---|
| Discussion re-lists every Results number | Discussion has no room for actual interpretation; reviewer flag |
| Comparison to "the literature" without naming a study | Reads as bluffing; reviewers suspect the work has not been read |
| Limitations section is two sentences | Performative; suggests author has not stress-tested the claim |
| Future Work in Discussion duplicates Conclusion | Wasted real estate in both chapters; signals architectural drift |
| Interpretation outruns evidence ("our method generalizes to NLP" from one English benchmark) | Single-dataset overgeneralization; defense reviewer flag |
| Causal language from correlational design | "X causes improved performance" without intervention; replace with "is associated with" |
| New table or figure first appears in Discussion | Results-Discussion boundary violated |
| "Surprisingly," "Interestingly" without explanation | Editorial filler; either explain the surprise or cut |
| Hedging applied uniformly ("may," "might," "could" in every sentence) | Reflexive AI-style hedging; calibrate per evidence tier |
| Claim that "more data would help" with no specifics | Future work entry without an experiment; cut or sharpen |

## Pre-Submission Discussion Audit

- [ ] No new tables, figures, or numerical results appear here for the first time
- [ ] Each interpretive claim points at a Results subsection
- [ ] Each interpretive claim survives the four-question rubric
- [ ] At least three named prior studies are compared, with the relation (confirms / extends / contradicts) explicit
- [ ] Limitations section has ≥ 3 substantive entries with specific concessions
- [ ] Each future-work entry maps to a limitation in this chapter
- [ ] No future-work entry duplicates content that belongs in the Conclusion
- [ ] Causal language only where the design supports it
- [ ] Hedging is calibrated, not reflexive (run `skill-avoid-ai-writing` with `discussion-section` profile)
- [ ] Argument-level audit completed via `skill-argument-validator`

## Integration

- `domains/thesis/skill-results-writing` — supplies the numbers this chapter interprets; nothing new appears here
- `domains/thesis/skill-conclusion-writing` — paired chapter; takes the broad future directions this skill explicitly excludes
- `domains/thesis/skill-argument-validator` — audits the inferential chain inside each interpretive claim
- `domains/thesis/skill-contribution-checker` — Discussion frames significance; this skill verifies the contribution is real
- `domains/thesis/skill-literature-review` — provides the prior-work map this chapter compares against
- `domains/thesis/skill-research-methodology` — design constraints determine which interpretations are licensed
- `domains/thesis/skill-academic-writing` — calibrated hedging and tense rules apply throughout
- `domains/thesis/skill-avoid-ai-writing` — `discussion-section` profile catches reflexive hedging
- `domains/thesis/skill-thesis-structure` — defines the Discussion / Conclusion boundary this skill enforces
- `domains/ml/skill-ml-evaluation` — evidence ladder depends on metric and split choices made there

## Resources

- [Lipton & Steinhardt, *Troubling Trends in Machine Learning Scholarship* (2018)](https://arxiv.org/abs/1807.03341) — the canonical critique of inflated interpretation in empirical ML
- [Academic Phrasebank — Discussing Findings (University of Manchester)](https://www.phrasebank.manchester.ac.uk/discussing-findings/) — register-appropriate phrasing for comparison and limitation language
- [Belcher, *Writing Your Journal Article in Twelve Weeks* — Week 9 (Discussion)](https://us.sagepub.com/en-us/nam/writing-your-journal-article-in-twelve-weeks/book257100) — pragmatic week-by-week guide; Week 9 covers Discussion architecture
- [Annesley, "The Discussion Section: Your Closing Argument" (Clinical Chemistry, 2010)](https://academic.oup.com/clinchem/article/56/11/1671/5621147) — short, classic, structural
