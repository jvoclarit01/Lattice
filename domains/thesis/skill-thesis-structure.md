---
name: skill-thesis-structure
description: Architecting a thesis or dissertation — chapter ordering, length budgets per chapter, what each chapter must accomplish, and explicit handoff to the section-specific writing skills. Use when planning a thesis outline, deciding chapter boundaries, allocating word counts, or routing a writing task to the right specialist skill.
---

# Thesis Structure

This skill is the *architecture* skill — it decides what goes where, how long, and which specialist skill writes it. It does NOT do the writing itself.

## When to Activate

Use when:
- Planning a thesis outline or proposal
- Deciding what counts as Methodology vs Results vs Discussion
- Allocating word counts across chapters
- A chapter has bloated and you need to move content elsewhere
- Routing a writing task to a specific skill (e.g., abstract → `skill-abstract-writing`)

**Trigger phrases:** "thesis structure", "outline", "chapter plan", "word budget", "where does this belong", "thesis proposal", "TOC"

## When NOT to Use

This skill never produces section drafts. It only routes. If you find yourself drafting prose, switch to the relevant specialist:

| Task | Skill |
|---|---|
| Write the abstract | `skill-abstract-writing` |
| Write Results | `skill-results-writing` |
| Write Discussion | `skill-discussion-writing` |
| Write Conclusion | `skill-conclusion-writing` |
| Write Introduction | (gap — no skill exists yet; route to `skill-academic-writing` for tone) |
| Write Methodology | `skill-research-methodology` |
| Write Literature Review | `skill-literature-review` |
| Write Model description for ML thesis | `skill-model-description` |
| Format figures/tables | `skill-figures-and-tables` |
| Citations | `skill-citation-management` |
| Final consistency pass | `skill-consistency-checker` |
| Detect AI-style writing | `skill-avoid-ai-writing` |

## Iron Laws

1. **One claim, one place.** If your hypothesis appears in Introduction, Methodology, and Discussion, only the Introduction should *state* it; Methodology *operationalizes* it; Discussion *evaluates* it. No re-statements of the same claim across chapters.
2. **Results contains no interpretation; Discussion contains no new results.** This is the most-violated rule. Police it.
3. **Every chapter has a job.** If you can't say in one sentence what a chapter accomplishes that no other chapter does, the chapter is misallocated.

## The Standard IMRaD-Plus Structure

For empirical/ML/quantitative theses (most common):

| # | Chapter | Job | Word % |
|---|---|---|---|
| 1 | Introduction | Frame the problem, state RQs, preview contributions | 8–12% |
| 2 | Literature Review | Position the work in prior research; identify the gap | 15–20% |
| 3 | Methodology | Describe how you did it — replicable detail | 15–20% |
| 4 | Results | What you found — neutral reporting | 15–20% |
| 5 | Discussion | What it means; how it relates to prior work; limits | 15–20% |
| 6 | Conclusion | Synthesis + future directions | 5–8% |

For a 60,000-word thesis: ~6,000 / ~10,500 / ~10,500 / ~10,500 / ~10,500 / ~3,500.

For longer empirical theses, Methodology + Results + Discussion may split into multiple chapters (one per study or major experiment) — the proportions stay roughly the same in aggregate.

## Variants

| Thesis type | Structural variant |
|---|---|
| Empirical / ML / Quantitative | IMRaD-Plus (above) — default |
| Theoretical / Mathematical | Intro → Background → Theorem chapters → Applications → Conclusion |
| Multi-study (PhD) | Intro → Lit Review → Study 1 (M+R+D) → Study 2 → Study N → General Discussion → Conclusion |
| Engineering / Systems | Intro → Background → Requirements → Design → Implementation → Evaluation → Discussion → Conclusion |
| Three-paper / Article-based | Intro → Paper 1 → Paper 2 → Paper 3 → Synthesis chapter |
| Humanities | Intro → Theoretical Framework → Argument chapters → Conclusion |

Pick the variant that matches your work; don't force IMRaD onto a theoretical or three-paper thesis.

## Front Matter (in order)

1. Title page
2. Declaration / approval (department-specific)
3. Acknowledgments
4. Abstract — see `skill-abstract-writing`
5. Table of contents
6. List of figures
7. List of tables
8. List of abbreviations / nomenclature

## Back Matter

1. References — see `skill-citation-management`
2. Appendices (raw data, supplementary tables, code listings, IRB documents)
3. Glossary (if dense terminology)
4. Index (rare in modern theses)

## Chapter Templates

### 1. Introduction

**Job:** Convince the reader that the problem is worth your time and theirs.

Components (in order):
- **Hook / motivation** (1-2 paragraphs) — why this matters, in plain language
- **Problem statement** — the specific thing you address
- **Research questions / hypotheses** — numbered, falsifiable, addressed in order through the thesis
- **Contributions** — bulleted; what's new because of this work
- **Thesis outline** — one paragraph mapping RQs to chapters

End the chapter with a forward pointer ("Chapter 2 reviews prior work…"). Don't summarize what you haven't done yet.

### 2. Literature Review

**Job:** Position the thesis in the field and identify the gap that the rest of the thesis fills.

Use `skill-literature-review` for the writing. Structurally:
- **Organization:** thematic > methodological > chronological. Choose one and stick with it.
- **End with the gap:** the last subsection must clearly state what is missing in prior work, which the thesis addresses.

Common defect: a "list of studies." A literature review *argues*, not just summarizes.

### 3. Methodology

**Job:** Provide enough detail that a competent peer could replicate the study.

Use `skill-research-methodology`. Components:
- **Research design** (overall approach: experimental, observational, ML training/eval, etc.)
- **Data** — collection, sample, sampling strategy, ethics/IRB
- **Materials / instruments / models** — see `skill-model-description` for ML
- **Procedure** — what was done, in order
- **Analysis plan** — what statistical or evaluation methods address each RQ
- **Reproducibility** — see `ml/skill-reproducibility` or `shared/skill-reproducibility`

Pre-registration (if any) is mentioned here.

### 4. Results

**Job:** Report what was found, neutrally and exhaustively for planned analyses.

Use `skill-results-writing`. Iron law: no interpretation. Every claim cites a number, table, or figure. See that skill for statistical reporting templates.

### 5. Discussion

**Job:** Interpret. Compare to prior work. State limitations. Recommend.

Use `skill-discussion-writing`. Components:
- **Summary of findings** (1-2 paragraphs — not a re-listing of every result)
- **Interpretation** — what the results mean, RQ by RQ
- **Comparison to prior work** — confirms? extends? contradicts?
- **Theoretical / practical implications**
- **Limitations** (be honest; reviewers will find them otherwise)
- **Future work** — see overlap with Conclusion below

### 6. Conclusion

**Job:** Synthesize, state the contribution clearly, point forward.

Use `skill-conclusion-writing`. Components:
- **Restate the problem** (1 paragraph)
- **Summarize contributions** (this is the answer to "what's new")
- **Future directions** (the most promising next questions, NOT a recap of Discussion limitations)
- **Closing reflection** (one paragraph; what the work means in a broader context)

**Future Work boundary:** Discussion treats future work narrowly (next experiments to address THIS thesis's limitations). Conclusion treats it broadly (longer-horizon directions). They should not be near-duplicates.

## Where Does This Belong? — Quick Routing

| Sentence-level content | Goes in |
|---|---|
| "We hypothesized that…" | Introduction |
| "Smith (2021) found…" | Literature Review or Discussion |
| "We trained the model with…" | Methodology |
| "Accuracy was 84.2%…" | Results |
| "This suggests…" / "This contradicts…" | Discussion |
| "An important limitation is…" | Discussion |
| "Future work could…" | Discussion (specific) or Conclusion (broad) |
| "Our main contribution is…" | Introduction (preview) + Conclusion (full statement) |

If a paragraph contains content from two of these rows, it belongs in two different chapters.

## Length Budget Workflow

1. Decide your total word count target (department/regulation; usually 50,000–100,000 for a PhD, 15,000–30,000 for a master's)
2. Apply the percentages above to get per-chapter budgets
3. Track word counts as you write — when a chapter hits 120% of budget, audit for content that belongs elsewhere
4. The Introduction and Conclusion should be the *last* chapters finalized — they reference the rest

## Common Failure Modes

| Pattern | Consequence |
|---|---|
| Lit review absent or buried in Introduction | Reviewers cannot evaluate the contribution |
| Results section interprets findings | Discussion has nothing left to say; reviewer flag |
| Discussion introduces new results | Reviewer red flag; weakens Methodology and Results |
| Conclusion repeats Discussion verbatim | Wasted chapter; signals lack of synthesis |
| Same hypothesis stated five times | Indicates outline drift; consolidate |
| 40-page Introduction | Lit review hiding inside Intro — split it |
| One-page Methodology | Not replicable; reviewers will reject |

## Pre-Defense Structure Audit

- [ ] Each chapter's job statement (one sentence) is distinct
- [ ] No overlap between Discussion and Conclusion future work
- [ ] No interpretation in Results
- [ ] Word counts roughly match the budget; outliers explained
- [ ] Every research question stated in Intro is answered in Discussion
- [ ] Every contribution claimed in Intro is supported by a Results section
- [ ] Front matter and back matter are complete per department template
- [ ] `skill-consistency-checker` and `skill-avoid-ai-writing` have been run on the full document

## Integration

- **All thesis writing skills** — this skill routes to them; it doesn't replace them
- `skill-consistency-checker` — final pass on the assembled document
- `skill-formatting` — citations, headings, page layout
- `skill-academic-writing` — sentence/paragraph-level discipline that applies everywhere
- `skill-avoid-ai-writing` — run on every chapter pre-submission

## Resources

- [Patrick Dunleavy — *Authoring a PhD*](https://www.macmillanihe.com/page/detail/Authoring-a-PhD/?K=9781403905840)
- [Joan Bolker — *Writing Your Dissertation in Fifteen Minutes a Day*](https://us.macmillan.com/books/9780805048919/writingyourdissertationinfifteenminutesaday)
- [Chicago Manual of Style — Dissertation/Thesis chapter](https://www.chicagomanualofstyle.org/)
- Department-specific template (always supersedes general guidance)
