---
name: skill-consistency-checker
description: Surface-level consistency audit across a complete thesis — terminology, notation, capitalization, hyphenation, abbreviation expansion, cross-reference resolution, citation-key uniqueness, and figure/table numbering. Use as the final pass before submission, after writing has stabilized and the document is structurally complete. For deeper logical / argument auditing, route to `skill-argument-validator`; for AI-style writing patterns and reflexive hedging, route to `skill-avoid-ai-writing`; for layout / fonts / page setup, route to `skill-formatting`.
---

# Consistency Checker

The consistency pass is a surface-level audit run after the thesis is written and before it is submitted. It catches the small drifts that accumulate across months of writing: a term spelled two ways, an abbreviation introduced in Chapter 4 and expanded again in Chapter 6, a symbol that means one thing in §3 and another in §5, a figure referenced as "Fig. 4.2" in one chapter and "Figure 4.2" in another. Logical depth — does the argument hold? — belongs to other skills.

## When to Activate

Use when:
- Final pre-submission pass, after writing has stabilized
- Merging chapter drafts written weeks or months apart
- Adopting a department template late and re-running uniformity checks
- An advisor flags "this reads like several different documents stitched together"
- A reviewer comments on inconsistent terminology or notation
- Returning to a thesis after a break and verifying the document is internally aligned

**Trigger phrases:** "consistency check", "final pass", "terminology audit", "notation audit", "cross-reference check", "abbreviations", "fix typos and consistency", "pre-submission check"

## When NOT to Use

| Situation | Use instead |
|---|---|
| Auditing logical structure of an argument (does evidence support claim?) | `skill-argument-validator` |
| Detecting AI-style writing patterns or reflexive hedging | `skill-avoid-ai-writing` |
| Page layout, font, margins, heading hierarchy | `skill-formatting` |
| Citation entries, BibTeX, DOIs, reference list mechanics | `skill-citation-management` |
| Verifying contributions are novel and supported | `skill-contribution-checker` |
| Sentence-level prose register, tense, voice | `skill-academic-writing` |
| Auditing methodology rigor | `skill-research-methodology` |

The cleanest test: if the question is *do these two passages refer to the same thing the same way*, this skill answers. If the question is *does this claim follow from the evidence*, route to `skill-argument-validator`. If the question is *does this prose sound machine-generated*, route to `skill-avoid-ai-writing`.

## Iron Laws

1. **One concept, one term — across the entire document.** If you named a thing "the embedding layer" in Chapter 3, it stays "the embedding layer" in every later chapter. Synonyms are noise.
2. **One symbol, one meaning — across the entire document.** Reusing `λ` for a regularization weight in Chapter 4 and a learning-rate decay in Chapter 5 is a defect. Disambiguate or rename.
3. **Abbreviations expanded once, on first use, in the front matter and the body.** Re-expanding an abbreviation in every chapter is noise; failing to expand it on first use is a defect.
4. **Every cross-reference resolves.** No `Section ??`, no `[?]`, no "see Section X" where Section X was renumbered.
5. **Run this pass last, after structural and prose passes have stabilized.** Re-running consistency after major revisions is fine; running it *before* prose stabilization wastes effort because edits will reintroduce drift.

## Boundary with `skill-argument-validator`

These two skills sound similar; they are not. Drawing the boundary cleanly avoids redundancy.

| `skill-consistency-checker` (this skill) | `skill-argument-validator` |
|---|---|
| Surface: same term, same symbol, same format | Depth: claim → data → warrant chain |
| "The model is called HSA in Chapter 4 and HSAtt in Chapter 5 — fix" | "The claim 'method generalizes' is licensed by single-dataset evidence — scope the claim" |
| "Abbreviation MoE expanded twice" | "The Methods chapter promised 5 seeds; Results report 1 — fix Methods or run more seeds" |
| Cross-reference resolution, figure numbering | Causal claims unsupported by interventional design |
| Citation-key uniqueness | Whether the cited paper actually says what you claim it does |
| Find/replace-friendly | Requires reading and judgment |

If the issue can be fixed mechanically (find/replace, regex), it is this skill's. If the issue requires re-thinking the argument or the design, route to `skill-argument-validator`.

## The 4-Phase Consistency Pass

Run the phases in order. Earlier phases are mostly automatable; later phases require human reading.

### Phase 1: Automated Lexical Pass

Tooling does most of the work. Use a search tool (ripgrep, grep, find/replace).

| Check | How |
|---|---|
| Spelling and grammar | Built-in checker; review every flag manually (no auto-accept) |
| Inconsistent capitalization of key terms | Search variants: "Machine Learning" / "machine learning" / "ML" |
| Hyphenation drift | Search "long context" vs "long-context"; "state of the art" vs "state-of-the-art" |
| Abbreviation expansion on first use | Search every abbreviation; verify first-use is expanded |
| Repeat expansions | Same abbreviation expanded in two different chapters → cut later expansions |
| Figure / table label format | "Figure 4.2" vs "Fig. 4.2" vs "figure 4.2" |
| Citation key duplicates | Search the `.bib` file for keys with the same DOI |
| US vs UK spelling | Pick one ("organize" vs "organise"; "color" vs "colour"); apply throughout |
| Smart vs straight quotes | Pick one; apply throughout |
| Em vs en vs hyphen | "—" vs "–" vs "-"; em-dash overuse is also flagged by `skill-avoid-ai-writing` |

Build a *terminology table* during this phase — one row per concept, with the chosen term, common drift variants, and the find/replace pattern.

### Phase 2: Notation Audit

For mathematical / formal sections, build a notation table in the front matter (or audit an existing one).

| Check | How |
|---|---|
| Each symbol defined on first use | Read every chapter's first use of each symbol |
| Each symbol has one meaning across the document | Search the symbol; verify every use refers to the same concept |
| Vector / matrix / scalar conventions consistent | Bold for vectors? Italic for scalars? Pick once |
| Subscript / superscript conventions | $w_i^t$ vs $w^t_i$ — pick one ordering |
| Function vs random-variable typography | $f(x)$ vs $\hat f(x)$ vs $\mathbf{F}(x)$ — pick conventions |
| Greek letters reused for different concepts | If $\lambda$ means two things, rename one |
| Notation table in front matter matches body usage | Compile the table; every body symbol must appear |

A notation table that is generated and never audited against the body is decorative.

### Phase 3: Cross-Reference and Numbering Audit

After the document compiles, every `\ref`, `\cite`, `\eqref` and figure / table reference must resolve.

| Check | How |
|---|---|
| `\ref{}` and `\eqref{}` resolve | Search PDF for "??" |
| `\cite{}` resolves | Search PDF for "[?]" |
| Figure references precede the figure (or are in the same float region) | Read every "see Figure X" — does X appear later? |
| Numbering scheme consistent (per-chapter vs sequential) | "Figure 4.2" requires per-chapter; "Figure 12" requires sequential — match throughout |
| Equation numbering consistent | All numbered or only those referenced; pick one convention |
| Section number scheme uniform | "1.2.1" vs "1.2.A" — pick one |
| Page numbers in front matter (Roman lowercase) vs body (Arabic) | Standard; verify front matter switches at Chapter 1 |
| Table of contents matches actual headings | Regenerate ToC after final edits |
| List of figures / list of tables match captions | Regenerate after final edits |

This is the most common phase to break in the last week. Re-run after every set of edits in the final two weeks.

### Phase 4: Cross-Chapter Coherence

The final phase requires reading. Walk the document chapter by chapter, asking:

| Check | How |
|---|---|
| Hypothesis stated in Introduction matches the one tested in Results | Read Introduction §X.X, then Results §X.X — same wording? |
| Contributions in Introduction match Conclusion | Lists should be verbatim or clear superset |
| Methodology promises match Results delivery (5 seeds, 5 datasets, etc.) | Read Methods, then Results, line by line |
| Discussion limitations match what Results actually shows | Limitation must be a real bound on the actual evidence |
| Future Work in Discussion (limitations-driven) does not duplicate Conclusion (broad horizon) | Cross-check the two sections |
| Abstract claims supported by the body | Every abstract sentence must have a chapter pointer |
| Terminology in Abstract matches body | Abstract often drifts; final pass critical |
| Acknowledgments don't change the contribution typing | "Co-developed with X" matters for typing |

This is where authorial judgment is required and where automation cannot help.

## Worked Example — Drift Across Chapters

**Bad (drift accumulated from months of writing):**

| Chapter | Phrasing |
|---|---|
| 1 | "Our proposed model, Hierarchical Sparse Attention (HSA)…" |
| 3 | "We introduce a sparse attention variant (the HSAtt model)…" |
| 4 | "The HSA-attention mechanism…" |
| 5 | "Hierarchical Sparse-Attention (HSA) outperforms…" |

The model has four names, two hyphenations, and a re-expansion. Reviewers infer carelessness.

**Good (consistent — this skill's pass):**

| Chapter | Phrasing |
|---|---|
| 1 | "Our proposed model, Hierarchical Sparse Attention (HSA)…" |
| 3 | "HSA introduces …" |
| 4 | "The HSA mechanism…" |
| 5 | "HSA outperforms…" |

One name, expanded once, used consistently. Build the terminology table early in writing; audit at the end.

## Common Failure Modes

| Pattern | Consequence |
|---|---|
| Same concept named three ways across chapters | Reads as careless; reviewers flag |
| Abbreviation introduced and never expanded | Reader has to guess; defect |
| Abbreviation expanded multiple times | Noise; signals chapters were written independently |
| `\ref{}` to a renumbered section appears as "Section ??" | Visible at submission |
| Figure caption format changes between chapters | "Figure 4.2:" in one chapter, "Fig. 4.2." in another |
| Citation key reused for two different papers | Reference list contains the wrong paper for some citations |
| US / UK spelling mixed | Pick "organize" or "organise" — inconsistency reads as careless |
| `λ` means two things in different chapters | Notation collision; rename or scope |
| Hypothesis in Introduction differs from one in Results | Suggests outline drift; structurally bad |
| Hyphenation drift ("state-of-the-art" vs "state of the art") | Find/replace fix |
| Em-dash overuse (also flagged by `skill-avoid-ai-writing`) | Both skills flag; cross-check |
| ToC out of sync with actual headings | Regenerate at final |
| List of abbreviations missing entries used in body | Decorative front matter; audit |
| Notation table claims `\mathbf{x}` but body uses `\vec{x}` | Front matter doesn't match body |

## Pre-Submission Consistency Audit

- [ ] Phase 1 lexical pass complete; terminology table maintained
- [ ] Phase 2 notation audit complete; notation table matches body usage
- [ ] Phase 3 cross-reference pass complete; PDF has no "??" or "[?]"
- [ ] Phase 4 cross-chapter coherence pass complete (manual reading)
- [ ] Abstract terminology matches body terminology
- [ ] Contributions in Introduction match Conclusion's restatement
- [ ] Hypotheses in Introduction match what is tested in Results
- [ ] Limitations in Discussion match real bounds of the evidence
- [ ] Future Work in Discussion (narrow) does not duplicate Conclusion (broad)
- [ ] Citation keys unique; reference list has no duplicates
- [ ] All figures / tables referenced before they appear
- [ ] ToC, list of figures, list of tables regenerated
- [ ] US / UK spelling, smart / straight quotes, em / en dash all uniform
- [ ] Run `skill-argument-validator` on logic-level concerns surfaced during Phase 4
- [ ] Run `skill-avoid-ai-writing` for AI-style and emphasis-stacking patterns this skill does not cover
- [ ] Run `skill-formatting` final layout pass after all consistency edits

## Integration

- `domains/thesis/skill-argument-validator` — handles logical / argument-level consistency that this skill explicitly excludes
- `domains/thesis/skill-avoid-ai-writing` — handles AI-style writing patterns, em-dash overuse, reflexive hedging
- `domains/thesis/skill-formatting` — layout-level consistency (fonts, margins, heading hierarchy); runs alongside this skill in the final pass
- `domains/thesis/skill-citation-management` — citation key uniqueness and reference-list mechanics; this skill audits, that skill maintains
- `domains/thesis/skill-thesis-structure` — provides the chapter contracts that Phase 4 audits against
- `domains/thesis/skill-academic-writing` — sentence-level register; this skill is the document-level pass
- `domains/thesis/skill-contribution-checker` — Introduction / Conclusion contribution alignment is a Phase 4 check
- `domains/thesis/skill-results-writing` — Results / Methodology alignment (promised seeds vs delivered) is a Phase 4 check
- `domains/thesis/skill-research-methodology` — Methodology promises feed Phase 4 cross-check

## Resources

- [PerfectIt](https://www.intelligentediting.com/) — commercial consistency checker; especially strong on terminology and abbreviation expansion
- [LanguageTool](https://languagetool.org/) — free grammar / style with consistency rules
- [latexmk](https://ctan.org/pkg/latexmk) — automated LaTeX recompiles to ensure cross-references resolve
- [Better BibTeX for Zotero](https://retorque.re/zotero-better-bibtex/) — stable citation keys, prevents duplicate-key drift
- [GNU `aspell` / `hunspell`](http://aspell.net/) — scriptable spell-checking against custom term lists
- [ripgrep](https://github.com/BurntSushi/ripgrep) — fast searches across the thesis source for terminology drift
- [Pinker, *The Sense of Style*](https://www.penguinrandomhouse.com/books/202023/the-sense-of-style-by-steven-pinker/) — the chapter on consistency and reader cognition is foundational
