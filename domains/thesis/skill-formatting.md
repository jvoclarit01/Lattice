---
name: skill-formatting
description: Document layout for theses and academic papers — page setup, margins, fonts, heading hierarchy, lists, code blocks, equation typesetting, figure/table placement, and the choice between LaTeX and Word. Use when configuring a thesis template, enforcing department style, choosing a citation *style* (not generating citations), or auditing layout consistency before submission. For citation generation, BibTeX management, and reference-list mechanics, route to `skill-citation-management`; for figure/table content design, route to `skill-figures-and-tables`.
---

# Formatting

Formatting is the layer of the thesis that lives below the prose: how the document is set, what fonts it uses, how headings cascade, where figures sit, and which toolchain produces it. Citation *mechanics* — generating an entry, formatting a reference list — belong to `skill-citation-management`. This skill governs the layout the citations appear in.

## When to Activate

Use when:
- Setting up a thesis or paper template at the start of a project
- Choosing between LaTeX and Word
- Configuring page size, margins, line spacing, font, and heading hierarchy
- Enforcing a department template that supersedes general guidance
- Choosing a citation *style* (APA / IEEE / Chicago / Vancouver) — the style decision, not the entries
- Placing figures and tables on the page (float positioning, captions, sizing)
- Typesetting equations, code listings, algorithm blocks
- Final pre-submission layout pass
- An advisor flags "doesn't match the template"

**Trigger phrases:** "thesis template", "LaTeX vs Word", "department template", "page layout", "margins", "font", "heading hierarchy", "citation style", "code listing", "equation formatting", "submission requirements"

## When NOT to Use

| Situation | Use instead |
|---|---|
| Generating BibTeX entries, managing references, fixing in-text citation mechanics | `skill-citation-management` |
| Designing what goes inside a figure or table | `skill-figures-and-tables` |
| Polishing prose register, tense, voice | `skill-academic-writing` |
| Detecting AI-style writing patterns | `skill-avoid-ai-writing` |
| Final terminology and notation pass | `skill-consistency-checker` |
| Deciding chapter ordering and word budgets | `skill-thesis-structure` |
| Designing the figures themselves | `skill-figures-and-tables` |
| Drafting any specific section's content | the section-specific writing skill |

The cleanest test: if the question is *how the page looks*, this skill answers. If the question is *what the citation says or which sources are cited*, route to `skill-citation-management`. If the question is *what the figure shows*, route to `skill-figures-and-tables`.

## Iron Laws

1. **The department template supersedes all general guidance.** If your department mandates a font, margin, or style, use it — even when this skill or a general style guide says otherwise. Read the template before the first draft.
2. **One toolchain for the whole document.** Mixing LaTeX and Word for different chapters creates inconsistency that no amount of polish recovers. Pick once, commit.
3. **Consistency over preference.** Whatever font, spacing, heading style, and citation *style* you pick, apply it identically across all chapters. Inconsistent layout reads as carelessness.
4. **Figures and tables are referenced before they appear, captioned below figures and above tables.** This is the dominant convention; some department templates invert it — follow the template.
5. **No formatting decisions in the final week.** Layout drift in the last days before submission breaks cross-references and pagination. Lock formatting once the document is structurally complete.

## LaTeX vs Word — The Decision Rubric

The choice is load-bearing for the rest of the thesis. Pick once, at the start.

| Factor | LaTeX | Word |
|---|---|---|
| Heavy mathematics or equations | Strongly preferred — equation typesetting is a class apart | Workable but visibly inferior |
| Code listings, algorithm blocks | `listings`, `algorithm2e`, `minted` are mature | Workable; less control |
| Long documents (PhD thesis, > 200 pages) | Cross-references and bibliography scale; recompiles cleanly | Cross-reference rot is real at scale |
| Department provides a LaTeX class file | Use it — saves weeks | If only `.docx` template, use Word |
| Department provides a Word template only | Forcing LaTeX usually fails the format check | Use it |
| Co-authoring with non-LaTeX users | Friction; consider Overleaf with `git` | Track changes is mature |
| Complex tables (multi-row, multi-col, rotation) | `booktabs`, `longtable`, `tabularx` are excellent | Workable but tedious |
| First-time user, tight deadline, no math | Learning curve may not be worth it | Use Word |
| Scientific publishing pipeline downstream (CTAN, arXiv, conference templates) | Native | Often requires conversion |

**Decision shortcut:** If the department provides a LaTeX class, you write math, and you have time to learn the toolchain — LaTeX. Otherwise, Word with the department template.

**Markdown / Pandoc / Quarto:** Reasonable for a master's thesis with light formatting needs and good Pandoc fluency. For PhD theses with department-mandated typesetting, the round-trip risk is usually not worth it.

## Page Setup — Defaults Worth Knowing

Use the department template if one exists. These defaults apply when none does, or when sanity-checking a template.

| Element | Common default | Notes |
|---|---|---|
| Page size | US Letter (8.5×11 in) or A4 (210×297 mm) | A4 is standard outside North America; check |
| Margins | 1 in (2.54 cm) on all sides | Some department templates require wider binding margin (e.g., 1.5 in inner) |
| Line spacing | 1.5 or double (body); single (block quotes, code, references) | Department template usually mandates |
| Body font | Times New Roman 12, Computer Modern Roman 11/12, Garamond 11 | LaTeX defaults to Computer Modern; many departments allow Latin Modern, Palatino, Charter |
| Heading font | Same family as body, scaled and bold; sans-serif (Helvetica/Arial) headings acceptable in some templates | Avoid pairing more than two font families |
| Page numbers | Bottom center or bottom right; Roman lowercase for front matter, Arabic from Chapter 1 | Standard across most templates |
| Chapter start | Recto page (right-hand) in printed theses | LaTeX `\cleardoublepage` |

## Heading Hierarchy

A typical thesis uses three levels of heading inside a chapter; rarely more.

| Level | Typical render | LaTeX | Sentence vs title case |
|---|---|---|---|
| Chapter | Centered, bold, large (16-22 pt) | `\chapter{}` | Title case typical; sentence case in some humanities templates |
| Section | Left-aligned, bold (14 pt) | `\section{}` | Sentence case typical for IEEE/ACM; title case for APA |
| Subsection | Left-aligned, bold or italic (12-13 pt) | `\subsection{}` | Match section choice |
| Subsubsection | Indented, bold or italic | `\subsubsection{}` | Use sparingly; > 4 levels signals over-structure |

**Rules:**
- Same level → identical formatting everywhere
- Don't skip levels (no `\subsection` directly under `\chapter`)
- > 3 levels of nesting in one chapter usually indicates the chapter should split
- Heading numbering scheme (1, 1.1, 1.1.1 vs unnumbered) is a single decision applied throughout

## Lists, Code Blocks, and Algorithm Blocks

Academic prose should be prose. Bullets and numbered lists are for *list-like content*: variable definitions, hyperparameters, step-by-step procedures, decision criteria.

| Content | Format |
|---|---|
| Continuous reasoning | Prose, not bullets |
| Variable / hyperparameter table | Table or itemized list with definitions |
| Step-by-step procedure | Numbered list |
| Pseudocode for an algorithm | `algorithm` / `algorithmic` (LaTeX) or fenced block (Word) |
| Source code | `listings` / `minted` (LaTeX) or fixed-width font block (Word); cite the language |
| Inline code reference | Monospace font (`\texttt{}` / Courier) |
| Equations | `equation` / `align` (LaTeX); MathType / native equation editor (Word) |

Code listings need: language label, line numbers if > 10 lines, monospace font, a caption, and a `\label` for cross-reference. Walls of code without these read as appendix material misplaced in the body.

## Figures and Tables — Layout Only

This skill governs *placement*; figure / table *design* belongs to `skill-figures-and-tables`.

| Convention | Detail |
|---|---|
| Caption position | Below figures, above tables (dominant convention; check template) |
| Caption format | "Figure 4.2: …" or "Fig. 4.2." (style-dependent) — match throughout |
| Numbering | Per-chapter ("Figure 4.2") or sequential ("Figure 12") — match throughout |
| First reference | Every figure / table must be referenced *before* it appears |
| Float placement (LaTeX) | `[htbp]` is a reasonable default; `[h!]` only when ordering matters |
| Sizing | Single-column figures fit text width; full-page or rotated figures should be rare |
| Resolution | 300 DPI or vector; raster screenshots in vector PDFs are a defect |
| Color | Verify the figure is readable in greyscale (printing) — never encode by color alone |

## Equations and Mathematical Notation

LaTeX is the standard. If you are using Word, the native equation editor is preferable to MathType for most submissions in 2024+.

- Display equations are numbered when referenced; unnumbered when standalone
- One numbering scheme across the document
- Use `\eqref` (LaTeX) for in-text references; "Equation 4.2" or "Eq. 4.2" in prose
- Define every symbol on first use; maintain a notation table in the front matter for dense theses
- Match notation to field convention (e.g., bold for vectors in CS / ML; arrows in physics)
- Coordinate notation choices with `skill-consistency-checker` for the final pass

## Citation Style — Choosing It (Not Generating It)

This skill chooses *which* citation style the document uses. `skill-citation-management` handles the mechanics of generating entries in that style.

| Style | Common in | In-text format |
|---|---|---|
| APA 7 | Social sciences, education, parts of CS | (Smith, 2020) |
| IEEE | Engineering, signal processing, parts of CS | [12] |
| ACM (numeric or author-year) | Computing, depending on venue | [12] or (Smith, 2020) |
| Chicago author-date | Humanities, some social sciences | (Smith 2020) |
| Chicago notes-bibliography | Humanities (especially history) | Footnote / endnote |
| Vancouver | Medicine, biomedical sciences | [12] or superscript |
| MLA | English literature, humanities | (Smith 45) |

**Decision drivers, in order:**
1. **Department mandate** — overrides everything
2. **Target venue** if applying for a journal-format thesis
3. **Field convention** — IEEE for ECE; APA for psychology; Vancouver for medicine
4. **Tooling** — match what your reference manager exports cleanly

Once chosen, apply uniformly. Do not mix in-text styles within a thesis.

## Department Template Adherence

A department template is a contract. Read it before the first draft and re-read it before submission.

| Element typically mandated | Audit |
|---|---|
| Title page exact wording, position, capitalization | Verbatim — names, dates, departmental phrases |
| Declaration / authorship statement page | Some departments mandate exact text |
| Abstract length and placement | Word limit usually capped (250-500) |
| Table of contents formatting | Auto-generated; spot-check against template |
| Front matter ordering | Title → declaration → abstract → acknowledgments → ToC → list of figures → list of tables → nomenclature |
| Margins (especially binding margin) | 1.5 in inner is common; print test recommended |
| Line spacing in body | Often 1.5 or 2.0 mandated |
| Chapter start position | Often recto-only |
| Page numbering scheme | Roman lowercase for front matter, Arabic from Chapter 1 |
| File format | PDF/A may be required for archival |

If the template is silent on a detail, follow the dominant field convention (or this skill's defaults). Do not invent a third option.

## Pre-Submission Layout Audit

- [ ] Department template requirements verified against current draft
- [ ] One toolchain throughout (no mixed LaTeX / Word chapters)
- [ ] Body font, size, and line spacing identical across chapters
- [ ] Heading hierarchy consistent; no skipped levels; no level deeper than the template allows
- [ ] All figures and tables referenced before they appear
- [ ] Caption position correct (figures below, tables above, or per template)
- [ ] Figure / table numbering scheme consistent (per-chapter or sequential, not mixed)
- [ ] All cross-references resolve (no `??` in PDF; no broken `\ref`)
- [ ] All figures readable in greyscale
- [ ] Code listings have language, monospace font, caption
- [ ] Equations numbered consistently; symbols defined on first use
- [ ] Front matter complete and in correct order
- [ ] Page numbers: Roman lowercase for front matter, Arabic from Chapter 1
- [ ] PDF generated; spot-checked for missing fonts, broken figures, off-margin content
- [ ] Print test: at least one chapter printed on the binding paper to catch margin issues
- [ ] Citation style choice locked; mechanics handed to `skill-citation-management`
- [ ] `skill-consistency-checker` run for final terminology / notation pass

## Common Failure Modes

| Pattern | Consequence |
|---|---|
| Mixed LaTeX and Word chapters | Inconsistent fonts, spacing, cross-references; usually fails department format check |
| Inconsistent heading hierarchy across chapters | Reads as careless; reviewers and committees notice |
| Figure caption above and below in different chapters | Format check failure |
| Figures referenced after they appear | Reader has to flip back; reviewer flag |
| Walls of bullet points inside body chapters | Should be prose; reads as AI-generated |
| Department template ignored ("the default looks fine") | Format check failure; rebinding cost |
| LaTeX cross-references broken (`Section ??`) | Final compile pass missed; visible at submission |
| Color-only figure encoding | Inaccessible; fails on greyscale printing |
| Five+ levels of nesting in one chapter | Structural defect; chapter usually needs splitting |
| Notation notation drift between chapters | `skill-consistency-checker` should catch; this skill establishes the system |
| Citation style mixed (APA in Chapter 2, IEEE in Chapter 3) | Format check failure; usually a tooling artifact |
| 300+ DPI raster screenshots in a vector PDF | Bloated file size, pixelated under zoom |

## Integration

- `domains/thesis/skill-citation-management` — supplies the *entries* in the *style* this skill selects; mechanics live there
- `domains/thesis/skill-figures-and-tables` — designs the figure / table content this skill places on the page
- `domains/thesis/skill-thesis-structure` — chapter ordering and word budgets feed the layout
- `domains/thesis/skill-consistency-checker` — final pass for notation, terminology, formatting drift
- `domains/thesis/skill-academic-writing` — register and tense rules apply to prose; this skill handles its container
- `domains/thesis/skill-avoid-ai-writing` — em-dash, bold overuse, list-overuse rules align with this skill's guidance
- `domains/thesis/skill-results-writing` — anchors prose to figures and tables; placement rules apply

## Resources

- [LaTeX Project — Documentation](https://www.latex-project.org/help/documentation/) — canonical LaTeX reference
- [Overleaf — Knowledge Base](https://www.overleaf.com/learn) — practical LaTeX recipes
- [APA Publication Manual (7th ed.)](https://apastyle.apa.org/products/publication-manual-7th-edition) — layout in addition to citations
- [IEEE Author Center — Manuscript Templates](https://ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/authoring-tools-and-templates/) — IEEE class files and templates
- [Chicago Manual of Style](https://www.chicagomanualofstyle.org/) — definitive on layout for humanities theses
- [Memoir / Classic Thesis (LaTeX)](https://ctan.org/pkg/classicthesis) — frequently-used thesis classes; check department compatibility
- [Bringhurst, *The Elements of Typographic Style*](https://www.indiebound.org/book/9780881792126) — typography reference behind most thesis style choices
