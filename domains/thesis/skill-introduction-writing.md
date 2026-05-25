---
name: skill-introduction-writing
description: Writing the Introduction chapter — hook, problem statement, research questions, contribution preview, thesis outline, and the funnel structure that takes the reader from broad motivation to specific contribution. Use when drafting Chapter 1, restructuring an introduction that has bloated to 40 pages, or aligning the introduction's contributions list with what the thesis actually delivers. For surveying prior work in depth, route to `skill-literature-review`; for the formal contribution audit, route to `skill-contribution-checker`.
---

# Introduction Writing

The Introduction is the chapter the reader judges first. Its job is to convince a thoughtful peer in 8-12% of the thesis word budget that the problem matters, that the questions are well-formed, and that the contributions will be worth their time. Anything beyond that — comprehensive prior-work treatment, methodology details, full results — belongs to later chapters and almost always bloats the Introduction when it leaks in.

## When to Activate

Use when:
- Drafting Chapter 1 of a thesis or paper
- Restructuring an introduction that has grown past its budget (40-page intros are this skill's most common patient)
- Drafting the contribution preview that the Conclusion must mirror
- Writing the research questions or hypotheses
- Producing the thesis outline at the end of Chapter 1
- An advisor flags the introduction as "burying the lede" or "this is a literature review"
- Realigning Introduction contributions with what the thesis actually delivers

**Trigger phrases:** "introduction chapter", "Chapter 1", "draft the intro", "research questions", "hook", "motivation", "problem statement", "thesis outline", "contribution preview", "introduction is too long"

## When NOT to Use

| Situation | Use instead |
|---|---|
| Surveying prior work in depth, identifying the gap | `skill-literature-review` |
| Auditing whether contributions are novel, typed, supported | `skill-contribution-checker` |
| Auditing the logical chain of contribution claims | `skill-argument-validator` |
| Deciding chapter ordering and word budgets | `skill-thesis-structure` |
| Writing the Conclusion's contribution restatement | `skill-conclusion-writing` |
| Writing the Methods, Results, Discussion | the section-specific skill |
| Sentence-level register, tense, voice | `skill-academic-writing` |
| Detecting AI-style "in the rapidly evolving field of…" openers | `skill-avoid-ai-writing` |

The cleanest test: if the section is *framing the problem and previewing the contribution*, this skill answers. If it is *surveying the body of prior work*, route to `skill-literature-review`. If it is *auditing whether the previewed contributions are sound*, route to `skill-contribution-checker`.

## Iron Laws

1. **The introduction is a funnel, not an inverted pyramid.** Open broad enough to motivate; narrow paragraph by paragraph until the contribution sits at the bottom. Reverse funnels (specific opening, broad close) hide the contribution.
2. **No comprehensive literature review.** Cite the 5-10 most central prior works to motivate the gap; the full treatment is Chapter 2's job. If the Introduction is past 15% of the thesis, prior work has leaked in.
3. **Research questions are numbered, falsifiable, and answered chapter-by-chapter.** "How can we improve X?" is not a research question; "Does method M outperform baseline B on tasks T1-T3?" is.
4. **The contribution preview must match the Conclusion's restatement.** Drift between Introduction and Conclusion is a defense liability. Write the Introduction last (or revise it last), once the contributions are stable.
5. **End with a forward pointer, not a summary.** The Introduction does not summarize what you have not yet done. It points at the chapters that will do it.

## The Funnel Structure

A well-formed Introduction has six components in order. Together they should fill 8-12% of the thesis word budget — for a 60,000-word thesis, roughly 5,000-7,000 words.

| # | Component | Purpose | Length guide |
|---|---|---|---|
| 1 | **Hook / motivation** | Why a thoughtful peer should care, in plain language | 1-2 paragraphs |
| 2 | **Problem statement** | The specific thing this thesis addresses | 1-2 paragraphs |
| 3 | **Background (light)** | The minimum prior context needed to understand the gap — not a literature review | 2-4 paragraphs |
| 4 | **Research questions / hypotheses** | Numbered, falsifiable, answered later | List of 2-5 |
| 5 | **Contribution preview** | What is new because of this work — typed and bounded | 1 paragraph or bullet list |
| 6 | **Thesis outline** | How the rest of the document maps onto the RQs | 1 paragraph |

A one-line "thesis statement" — a single declarative sentence that the rest of the thesis defends — sits between components 2 and 5. Some departments require it explicitly; others let it sit implicit at the bottom of the funnel. Make it explicit when in doubt.

## Component 1: Hook / Motivation

One or two paragraphs. Start at the level of motivation a thoughtful peer outside your subfield would care about — not at the level of the abstract problem, and not at the level of "the field of X."

| Pattern | Example |
|---|---|
| **Stake** (consequences if the problem is unsolved) | "Clinical text in low-resource languages remains effectively unsearchable. The cost is borne unevenly: a hospital in a non-English-speaking jurisdiction cannot rely on the NLP infrastructure that anglophone health systems take for granted." |
| **Tension** (something widely believed conflicts with something observed) | "Domain pretraining is widely held to require billions of in-domain tokens. In practice, most clinical institutions can curate at most tens of millions. The gap between what is assumed and what is possible motivates this thesis." |
| **Concrete instance** (one vivid example) | "A radiologist in São Paulo dictates a report in Portuguese. No deployed system reliably extracts findings from it for downstream audit. The reasons are technical, not linguistic." |

**What the hook is not:**
- "In the rapidly evolving field of machine learning, attention mechanisms have become increasingly important…" (AI-style, generic, says nothing — see `skill-avoid-ai-writing`)
- "Machine learning is the study of algorithms that learn from data." (textbook definition; the reader knows)
- "The advent of deep learning has revolutionized…" (significance inflation; cut)

The hook earns the reader's next paragraph. If a competent peer would skim past it, rewrite.

## Component 2: Problem Statement

One or two paragraphs. Move from the broad motivation to the specific problem this thesis addresses. State it as a problem, not a method.

| Bad (method-as-problem) | Good (problem-as-problem) |
|---|---|
| "This thesis develops a sparse attention mechanism for transformers." | "Long-context inference in transformers is bottlenecked by the quadratic cost of dense attention. For inputs beyond 16K tokens, current systems either truncate (losing information) or shard (losing accuracy). This thesis addresses the cost-accuracy tradeoff at long context lengths." |
| "We propose a new prompting strategy." | "Few-shot prompting is sensitive to example order in ways that practitioners cannot predict. The same prompt can vary by 8 F1 points across permutations. The instability blocks production deployment." |

The problem statement is the seed of the thesis statement. If you cannot state the problem in 100 words, the problem is too vague.

## Component 3: Background (Light)

Two to four paragraphs. The reader needs the minimum prior context to understand the gap — definitions of central terms, the canonical formulation of the problem, and a brief acknowledgment that prior work exists. Cite 5-10 papers, no more.

**Boundary with `skill-literature-review`:** The Introduction's background paragraph names the *terrain*; Chapter 2 walks it. If your Introduction is citing 40 papers, you are writing Chapter 2 in Chapter 1.

| Pattern | Example |
|---|---|
| **Define the central term** | "We follow the standard definition of *long context*: input sequences exceeding 8,192 tokens. The threshold is empirically motivated (Press et al., 2022) and aligns with the regime in which dense attention's quadratic cost dominates inference time on commodity GPUs." |
| **Cite the canonical formulation** | "The transformer architecture (Vaswani et al., 2017) and its computational profile (Tay et al., 2022) provide the technical foundation for what follows." |
| **Name the gap (briefly)** | "Existing sparse attention methods (Beltagy et al., 2020; Zaheer et al., 2020) reduce cost but lose accuracy on long-range reasoning benchmarks. Chapter 2 surveys this body of work in detail." |

The last sentence above is a forward pointer to Chapter 2, where the systematic prior-work treatment lives.

## Component 4: Research Questions

Two to five numbered RQs (or hypotheses, if the work is hypothesis-testing). They must be:

1. **Falsifiable** — a coherent answer of "no" must be possible
2. **Bounded** — scope, sample, condition stated
3. **Mapped to a chapter** — each RQ is answered by a specific later chapter

| Bad (vague, unfalsifiable) | Good (specific, falsifiable, bounded) |
|---|---|
| "How can we improve clinical NLP?" | "**RQ1:** Does domain pretraining at 10M tokens recover the F1 of full-scale pretraining at 100M tokens on MedNLI and i2b2-NER?" |
| "What are the implications of long context?" | "**RQ2:** On the LRA benchmark suite, does Hierarchical Sparse Attention match dense-attention F1 within 1 point at 32K tokens, while reducing FLOPs by ≥ 30%?" |
| "Is BERT robust?" | "**RQ3:** Does BERT's classification accuracy on Yelp polarity degrade by more than 5 points under three named distribution shifts (genre, length, domain)?" |

A reader should be able to read your RQ1 alone and identify which chapter answers it. If they cannot, the RQ is too vague.

## Component 5: Contribution Preview

One paragraph or a tight bulleted list. This is the section that the Conclusion will mirror — write it once both are stable, and verify the match.

For each contribution:
- **Type label** (method / empirical / theoretical / artifact — see `skill-contribution-checker`)
- **One-sentence statement**
- **Pointer to the chapter** where the supporting evidence lives
- **Calibrated language** — match the evidence ladder

**Bad (untyped, vague, unbounded — does not survive `skill-contribution-checker`):**
> Our main contributions are: (1) a novel approach to NLP, (2) state-of-the-art results, (3) new insights into transformer behavior.

**Good (typed, scoped, points at chapters):**
> This thesis makes three contributions:
> (1) **Method.** Hierarchical Sparse Attention (HSA), a transformer attention variant that reduces FLOPs on long-context inputs by 38% (Chapter 4).
> (2) **Empirical.** A study showing that HSA matches dense-attention F1 within 1 point on five long-context benchmarks while degrading gracefully on inputs beyond training length — a behavior not observed in prior sparse-attention work (Chapter 5).
> (3) **Artifact.** HSA-Bench, a benchmark of 12K naturally-long-context examples from legal and scientific corpora (Appendix B).

Three to five contributions is the typical range. Seven thin contributions are weaker than three solid ones — reviewers count the strongest, not the most.

## Component 6: Thesis Outline

One paragraph mapping the RQs to chapters.

**Pattern:**
> The remainder of this thesis is organized as follows. Chapter 2 reviews prior work on transformer architectures and sparse attention, identifying the gap that motivates RQ1-RQ2. Chapter 3 develops the methodology used in subsequent experiments. Chapter 4 introduces HSA and addresses RQ1 (architecture and complexity analysis). Chapter 5 reports the experiments addressing RQ2 (empirical performance) and RQ3 (graceful degradation). Chapter 6 discusses the findings, surfaces limitations, and proposes the next experiments those limitations imply. Chapter 7 synthesizes the contributions and points to long-horizon directions.

**What the outline is not:**
- A summary of what each chapter *says* — the reader has not read them yet
- A re-statement of the contributions
- A bullet list with no prose

End with a single forward-pointing sentence, not "in conclusion." The chapter ends; the thesis begins.

## Worked Example — Bad vs Good Opening Paragraph

**Bad (AI-style, generic, no hook, no specificity):**

> In the rapidly evolving field of natural language processing, attention mechanisms have emerged as a transformative paradigm that has revolutionized how we approach a wide variety of tasks. With the advent of large language models, the importance of efficient long-context processing has become increasingly clear, and a comprehensive exploration of this topic is therefore essential. This thesis aims to delve into the intricacies of sparse attention and its myriad applications.

Audit:
- "Rapidly evolving field" — AI-style filler (`skill-avoid-ai-writing`)
- "Transformative paradigm," "revolutionized," "increasingly clear" — significance inflation
- "Comprehensive exploration" — empty calorie
- "Delve into the intricacies" — Tier 1 AI vocabulary
- No stake, no specific problem, no contribution

**Good (concrete, stakes-first, specific):**

> Long-context inference in transformer models is bottlenecked by the quadratic cost of dense attention. At 32K tokens, the attention matrix dominates GPU memory and inference time on commodity hardware; at 128K, even research clusters strain. The cost is uneven: anglophone industrial labs run such models at scale, while smaller groups — including most academic labs — work with truncated inputs and accept the accuracy loss. This thesis addresses the cost-accuracy tradeoff at long context lengths through a new architectural variant, evaluated on five long-context benchmarks and released as an open artifact.

The improved version: hooks with a concrete computational fact, names the stake (uneven access), states the problem in a measurable form, and previews the scope of the work in a single paragraph.

## Common Failure Modes

| Pattern | Consequence |
|---|---|
| 40-page Introduction with embedded literature review | Chapter 2 is hiding inside Chapter 1; split |
| "In the rapidly evolving field of …" opener | AI-style filler; rewrite |
| RQs phrased as "how can we improve X?" | Unfalsifiable; reframe with measurable success criterion |
| Thesis statement absent | No single sentence the rest of the thesis defends; reader cannot anchor |
| Contributions in Introduction don't match Conclusion | Defense liability; revise both together |
| "We propose a method" without naming the problem | Method-as-problem confusion; lead with problem |
| Thesis outline summarizes what each chapter says | Spoils the thesis; replace with mapping to RQs |
| Background paragraph cites 40 papers | Literature review leak; cut to 5-10, route detail to Chapter 2 |
| Hook is a textbook definition | Says nothing the reader doesn't know; rewrite for stake or tension |
| RQs not numbered, not mapped to chapters | Reader cannot find the answers; renumber and map |
| "This thesis will explore many interesting questions" | False breadth; pick the actual scope |
| Inverted funnel (specific opener, broad close) | Hides the contribution; reverse |
| Conclusion contributions silently expanded relative to Introduction | Drift; align in final pass |
| "We coin the term X" for a re-discovery | Novelty inflation; verify with `skill-contribution-checker` |

## Pre-Submission Introduction Audit

- [ ] Introduction is 8-12% of the thesis word budget; not 25% (literature review has leaked)
- [ ] Six funnel components present, in order
- [ ] Hook has a concrete stake or tension; no "rapidly evolving field"
- [ ] Problem stated as a problem, not as a method
- [ ] Background cites no more than ~10 prior works; full treatment routed to Chapter 2
- [ ] RQs numbered, falsifiable, bounded, each mapped to a chapter
- [ ] Contribution preview typed (method / empirical / theoretical / artifact)
- [ ] Each contribution points at a chapter
- [ ] Contribution language matches the evidence ladder
- [ ] Thesis outline maps RQs to chapters; does not summarize chapter content
- [ ] Closes with a forward pointer, not a summary
- [ ] Introduction contributions match Conclusion's restatement (verbatim or clear superset)
- [ ] `skill-contribution-checker` confirms typing, novelty, and support
- [ ] `skill-argument-validator` confirms RQ-to-evidence mapping
- [ ] `skill-avoid-ai-writing` run — formulaic openers and significance inflation are this section's most common defects
- [ ] `skill-academic-writing` run for register, tense, voice

## Integration

- `domains/thesis/skill-thesis-structure` — defines the Introduction's job, length budget, and place in the architecture
- `domains/thesis/skill-literature-review` — Chapter 2 takes the depth this skill explicitly excludes; cite the boundary clearly
- `domains/thesis/skill-contribution-checker` — audits the contribution preview's typing, novelty, and support
- `domains/thesis/skill-argument-validator` — audits the RQ-to-evidence chain promised here
- `domains/thesis/skill-conclusion-writing` — paired chapter; contribution restatement must mirror this skill's preview
- `domains/thesis/skill-academic-writing` — register and hook patterns; reflexive hedging in problem statements is flagged
- `domains/thesis/skill-avoid-ai-writing` — formulaic openers ("rapidly evolving field"), significance inflation, novelty inflation are this section's high-risk patterns
- `domains/thesis/skill-abstract-writing` — abstract is a 200-word funnel of the Introduction; both must agree
- `domains/thesis/skill-research-methodology` — Methods chapter delivers what RQs promise; alignment is a Phase 4 consistency check
- `domains/thesis/skill-results-writing` — Results chapter answers each RQ in order

## Resources

- [Patrick Dunleavy, *Authoring a PhD* — Introduction chapter](https://www.macmillanihe.com/page/detail/Authoring-a-PhD/?K=9781403905840) — disciplined treatment of what the introduction's job is
- [Belcher, *Writing Your Journal Article in Twelve Weeks* — Week 4 (Introduction)](https://us.sagepub.com/en-us/nam/writing-your-journal-article-in-twelve-weeks/book257100) — pragmatic guide; Week 4 covers Introduction structure
- [Swales, *Genre Analysis* — CARS Model](https://www.cambridge.org/9780521338134/) — the canonical "Create A Research Space" model behind most empirical introductions
- [Academic Phrasebank — Writing Introductions (University of Manchester)](https://www.phrasebank.manchester.ac.uk/introducing-work/) — register-appropriate phrasing for hooks, gaps, and contribution previews
- [Lipton & Steinhardt, *Troubling Trends in Machine Learning Scholarship* (2018)](https://arxiv.org/abs/1807.03341) — survey of inflated framing in ML introductions
