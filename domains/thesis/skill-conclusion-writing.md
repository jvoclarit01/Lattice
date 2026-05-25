---
name: skill-conclusion-writing
description: Writing the Conclusion chapter — restating the problem, synthesizing the contributions, sketching long-horizon research directions unbounded by this thesis's specific limitations, and closing with a one-paragraph reflection on broader significance. Use when drafting or revising the Conclusion, deciding what is "future work" vs Discussion's narrower next-experiments, or finalizing the contribution restatement that mirrors the Introduction. For limitations-driven next experiments and prior-work comparison, route to `skill-discussion-writing`.
---

# Conclusion Writing

The Conclusion is the synthesis chapter. Its job is to remind the reader of the problem, state the contributions cleanly, point forward to long-horizon research directions, and close with a single paragraph of reflection. It is *not* a recap of Discussion, *not* a re-listing of Results, and *not* the place for limitation-specific next experiments — those live in the Discussion.

## When to Activate

Use when:
- Drafting or revising the Conclusion chapter
- Writing the contribution restatement that mirrors the Introduction's preview
- Sketching long-horizon directions that go *beyond* this thesis's specific limitations
- Writing the closing reflection on broader significance
- An advisor flags Conclusion as "redundant with Discussion" or "abrupt"
- Final pass before submission, after Discussion is stable

**Trigger phrases:** "conclusion chapter", "wrap up the thesis", "final chapter", "broader significance", "long-term future work", "closing", "synthesis"

## When NOT to Use

| Situation | Use instead |
|---|---|
| Limitation-specific next experiments | `skill-discussion-writing` |
| Comparing findings to specific prior studies | `skill-discussion-writing` |
| Reporting numbers, tests, effect sizes | `skill-results-writing` |
| Verifying a contribution claim is novel | `skill-contribution-checker` |
| Auditing whether a claim is supported | `skill-argument-validator` |
| Drafting the Introduction's contribution preview | `skill-introduction-writing` |
| Sentence-level prose register | `skill-academic-writing` |
| Detecting AI-style "future looks bright" closures | `skill-avoid-ai-writing` |

The cleanest test: if a paragraph could be moved into the Discussion without rewriting it, it does not belong here. The Conclusion synthesizes; the Discussion interprets.

## Iron Laws

1. **No new results, no new interpretations, no new comparisons to prior work.** All three were the Discussion's job. The Conclusion only synthesizes.
2. **The contribution restatement must match the Introduction's preview verbatim or be a clear superset.** Drift between Introduction and Conclusion contributions is a defense liability.
3. **Future Work in the Conclusion is broad and unbounded by this thesis's limitations.** Specific next experiments tied to this study's limits live in the Discussion. Mixing the two creates redundancy.
4. **One closing paragraph, not three.** A long, ornate reflection inflates routine work. Earn the closing through specificity, not flourish.
5. **No "the future looks bright."** Generic closings ("only time will tell," "as we move forward," "exciting times ahead") are AI-style filler. Cut on sight.

## The Conclusion Skeleton

A defense-grade Conclusion has four components in this order. Total length: 5-8% of the thesis word budget — typically 3,000-5,000 words for a PhD, 800-1,500 for a master's.

| # | Component | Purpose | Length guide |
|---|---|---|---|
| 1 | **Restate the problem** | One paragraph: what motivated the work, in plain terms | 1 paragraph |
| 2 | **Summarize contributions** | Mirror the Introduction's contributions list, now with evidence | 2-4 paragraphs |
| 3 | **Long-horizon future directions** | Broad research questions opened by — not constrained by — the thesis | 2-4 paragraphs |
| 4 | **Closing reflection** | One paragraph on what the work means in a broader context | 1 paragraph |

The skeleton is rigid on purpose. Conclusions that drift add Discussion content and reviewers notice.

## Component 1: Restate the Problem

One paragraph. Remind the reader what motivated the thesis and what specific question it took on. This paragraph *links back* to the Introduction's hook without copying it.

| Pattern | Example |
|---|---|
| **Plain restatement** | "This thesis began with a practical question: can clinical NLP systems be deployed in non-English settings without retraining? Existing work largely answered this in English." |
| **Stake restatement** | "The cost of training large language models on biomedical corpora — both in compute and in expert annotation — has limited their adoption outside well-resourced labs. This thesis asked whether the same gains could be obtained at one-tenth the data scale." |

The point is to re-anchor the reader, not to re-litigate motivation. One paragraph; move on.

## Component 2: Summarize Contributions

This section answers "what is new because of this work?" It must mirror the contribution list previewed in the Introduction. Mismatch between the two — claims appearing here that were not foreshadowed, or vice versa — is a defense red flag.

For each contribution:

1. **Name the type** (method / empirical / theoretical / artifact — see `skill-contribution-checker`)
2. **State the contribution** in one sentence
3. **Cite the chapter or section** where the supporting evidence lives
4. **Calibrate language** to the evidence tier

**Pattern:**
> This thesis makes three contributions: (1) **Method.** We propose [METHOD], described in Chapter 4 and evaluated in §5.3. (2) **Empirical.** We show that [FINDING] holds across [SCOPE], reported in §5.4 and §5.6. (3) **Artifact.** We release [ARTIFACT], described in Appendix B.

**Bad (drifts from Introduction, mistypes contributions, no pointers):**
> This thesis introduced a novel framework for medical NLP, achieved state-of-the-art results, and provided new theoretical insights into transformer behavior.

**Good (typed, evidenced, mirrors the Introduction):**
> This thesis makes three contributions, foreshadowed in §1.4 and now evidenced in the body. (1) **Method.** Hierarchical Sparse Attention (HSA), an attention variant that reduces FLOPs by 38% on long-context inputs (Chapter 4, §4.3). (2) **Empirical.** HSA matches dense-attention performance on five long-context benchmarks (Table 5.1) while degrading gracefully beyond training length (§5.4) — a behavior not observed in prior sparse-attention work. (3) **Artifact.** HSA-Bench, 12K naturally-long-context examples drawn from legal and scientific corpora (Appendix B).

The good version is auditable, typed, and pointer-anchored.

## Component 3: Long-Horizon Future Directions

This is the section where the Discussion / Conclusion boundary matters most. **Keep it sharp.**

| Belongs in Conclusion (broad, long-horizon) | Belongs in Discussion (limitations-driven, narrow) |
|---|---|
| "Sparse attention may eventually replace dense attention for long-context inference, contingent on advances in custom kernels." | "An ablation isolating positional encoding under matched compute would test the §5.6 explanation for the contradiction with Liu et al." |
| "The methodological tension between data scale and domain specificity is a long-running open question in NLP." | "A multi-language replication on the Spanish ClinicalBERT benchmark would establish whether the F1 gains observed here transfer beyond English." |
| "If clinical NLP is to be deployable globally, the field will need shared, multilingual evaluation infrastructure that does not yet exist." | "Re-running the user study with N ≥ 600 and broader demographic recruitment would license population-scale claims." |

**Boundary test for each future-work paragraph:**
- Is it tied to a specific limitation that appeared in the Discussion? → Move to Discussion.
- Is it a long-horizon direction that would still be relevant if this thesis had different limitations? → Keep in Conclusion.

Two to four broad directions is plenty. A list of ten signals that the author has not chosen.

**Patterns:**

| Direction type | Pattern |
|---|---|
| **Open theoretical question** | "Whether [phenomenon] arises from [property A] or [property B] remains open. Resolving it would require [methodology], which is beyond the scope of this thesis." |
| **Methodological frontier** | "The methods developed here assume [assumption]. Relaxing it for [setting] is a long-term direction; current tooling is not yet adequate." |
| **Cross-domain transfer** | "Whether the patterns observed in [our domain] hold in [adjacent domain] is a natural next question for the field." |
| **Societal / policy frontier** | "The deployability of [system] depends on [non-technical factor], which sits outside the empirical scope of this thesis but is the natural next frontier." |

## Component 4: Closing Reflection

One paragraph. Connects the contribution to the broader significance promised in the Introduction. This is the only paragraph in the thesis where slightly elevated register is forgiven — but earn it.

**What to write:**
- One claim about why the contribution matters in a broader context
- A specific link back to the motivation in the Introduction
- A close that *does not* over-promise

**What to cut:**
- "The future looks bright"
- "Only time will tell"
- "As we move forward"
- "One thing is certain"
- Rhetorical questions ("What does this mean for AI?")
- Anything that survives in another paper unchanged

**Bad (generic, inflated, slot-fill):**
> In conclusion, this work represents a significant step forward for the field. The future of medical AI looks bright, and only time will tell what new horizons await. As we move forward, one thing is certain: the journey is just beginning.

**Good (specific, grounded, modest):**
> The motivation in §1.1 was practical: clinical text in low-resource languages remains an under-served setting, and small labs cannot replicate the compute footprints of frontier-lab pretraining. The contributions here do not solve that problem. They establish that domain adaptation at one-tenth the standard data scale recovers most of the F1 of full-scale pretraining on two English benchmarks — a partial, scoped result that nonetheless suggests the broader pattern is worth pursuing systematically.

The good version is honest, specific, and links to a particular Introduction commitment.

## Common Failure Modes

| Pattern | Consequence |
|---|---|
| Conclusion repeats Discussion verbatim | Wasted chapter; signals architectural drift |
| Future Work in Conclusion duplicates Discussion's limitation-driven entries | Two chapters competing for the same content |
| Contributions in Conclusion don't match Introduction | Defense liability; reviewer asks "when did this contribution appear?" |
| New interpretation or new comparison appears here | Reviewer flag; that work belonged in Discussion |
| Closing paragraph is three pages of reflection | Inflates routine work into history-making |
| "The future looks bright" / "exciting times ahead" / "one thing is certain" | AI-style filler; remove |
| Rhetorical question close ("What will the next decade hold?") | Stalling; just state the implication |
| Five+ future directions, each one paragraph | Author has not chosen the most important; pick 2-4 |
| Unscoped grand claims in the close ("This work redefines NLP") | Novelty inflation; reviewers calibrate against |
| Paragraph of meta-commentary on "the writing process" | Out of register; remove |

## Pre-Submission Conclusion Audit

- [ ] Four components present, in order
- [ ] No new results, interpretations, or named-prior-work comparisons
- [ ] Contribution restatement matches Introduction's preview (verbatim or clear superset)
- [ ] Each contribution is typed (method / empirical / theoretical / artifact)
- [ ] Each contribution points at a chapter or section
- [ ] Future Work entries are broad — none duplicates a Discussion limitation-driven next experiment
- [ ] Future Work entries number 2-4, not ten
- [ ] Closing paragraph is one paragraph
- [ ] No "future looks bright," "only time will tell," or rhetorical-question close
- [ ] Run `skill-avoid-ai-writing` with default profile — generic closings are this skill's bread and butter
- [ ] `skill-contribution-checker` confirms contributions are typed and supported
- [ ] `skill-argument-validator` confirms claim language matches the evidence tier

## Integration

- `domains/thesis/skill-discussion-writing` — paired chapter; this skill receives the broad horizon directions Discussion explicitly excludes
- `domains/thesis/skill-introduction-writing` — Introduction's contribution preview must match this chapter's restatement
- `domains/thesis/skill-contribution-checker` — verifies typing and support of every contribution claim
- `domains/thesis/skill-argument-validator` — verifies the contribution claim language matches the evidence
- `domains/thesis/skill-results-writing` — supplies the evidence the contribution claims rest on
- `domains/thesis/skill-thesis-structure` — defines the Conclusion's job and the boundary with Discussion
- `domains/thesis/skill-academic-writing` — register and tense rules apply, with mild relaxation in the closing paragraph
- `domains/thesis/skill-avoid-ai-writing` — generic closings ("the future looks bright") are this skill's high-priority targets
- `domains/thesis/skill-abstract-writing` — abstract and Conclusion contribution restatement must agree

## Resources

- [Patrick Dunleavy, *Authoring a PhD* — Conclusion chapter](https://www.macmillanihe.com/page/detail/Authoring-a-PhD/?K=9781403905840) — disciplined treatment of the synthesis chapter's job
- [Academic Phrasebank — Writing Conclusions (University of Manchester)](https://www.phrasebank.manchester.ac.uk/writing-conclusions/) — register-appropriate phrasing
- [Bunton, "Generic moves in PhD thesis Conclusions" (English for Specific Purposes, 2005)](https://www.sciencedirect.com/science/article/abs/pii/S0889490605000049) — corpus study of what doctoral conclusions actually do
- [Belcher, *Writing Your Journal Article in Twelve Weeks* — Week 11 (Conclusion)](https://us.sagepub.com/en-us/nam/writing-your-journal-article-in-twelve-weeks/book257100) — pragmatic week-by-week with conclusion patterns
