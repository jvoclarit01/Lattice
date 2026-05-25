---
name: skill-citation-management
description: Citation and reference management — choosing a tool (Zotero / Mendeley / EndNote / BibTeX / CSL), curating a personal library, generating accurate in-text citations and reference lists in the chosen style, DOI / identifier hygiene, and building the citation graph that feeds the literature review. Use when setting up a reference manager, importing or fixing BibTeX, managing identifiers and metadata, or auditing the reference list before submission. For the *style* decision (APA vs IEEE vs Chicago) and document layout, route to `skill-formatting`; for the prose work of synthesizing prior work, route to `skill-literature-review`.
---

# Citation Management

A thesis is a citation graph wrapped in prose. This skill governs how the graph is built, maintained, and rendered: which tool, which identifiers, which metadata, and how to keep all of it in sync with the prose. The decision of *which style* (APA / IEEE / Chicago / Vancouver) and the *layout of the page* belong to `skill-formatting`. The argumentative work of synthesizing prior work belongs to `skill-literature-review`.

## When to Activate

Use when:
- Setting up a reference manager at the start of a thesis project
- Importing references from databases (Google Scholar, Semantic Scholar, Web of Science, PubMed, arXiv)
- Fixing broken or inconsistent BibTeX entries
- Auditing in-text citations against the reference list
- Resolving DOIs, ISBNs, ORCIDs, ArXiv IDs, or correcting metadata
- Building the citation graph that informs the literature review
- Pre-submission reference-list audit
- Switching citation styles late in the project (last resort)

**Trigger phrases:** "Zotero", "Mendeley", "EndNote", "BibTeX", "CSL", "DOI", "reference manager", "fix references", "missing citations", "import references", "citation graph", "reference audit"

## When NOT to Use

| Situation | Use instead |
|---|---|
| Choosing *which* citation style to adopt (APA / IEEE / etc.) | `skill-formatting` |
| Page layout, fonts, margins, headings | `skill-formatting` |
| Synthesizing prior work into a literature review narrative | `skill-literature-review` |
| Verifying that a contribution claim is supported by the cited prior work | `skill-argument-validator` |
| Polishing prose register | `skill-academic-writing` |
| Final terminology / notation consistency | `skill-consistency-checker` |
| Detecting AI-style citation stuffing or vague attributions | `skill-avoid-ai-writing` (with `related-work` profile) |

The cleanest test: if the question is *what tool, what entry, what identifier*, this skill answers. If the question is *what style or how the page looks*, route to `skill-formatting`. If the question is *what the cited body of work actually says*, route to `skill-literature-review`.

## Iron Laws

1. **One library, one tool, one source of truth.** Mixing two reference managers, or maintaining a "manual" `.bib` alongside a managed one, guarantees drift and broken citations.
2. **Every entry has a stable identifier.** DOI for journal articles; ArXiv ID for preprints; ISBN for books; URL with retrieval date as last resort. Entries without identifiers cannot be verified.
3. **The reference list is generated, not typed.** Hand-typed references introduce errors that survive proofreading. Use the manager's export.
4. **Every in-text citation has a reference; every reference is cited in text.** Orphan citations and orphan references are both defects.
5. **Cite the work you actually read.** "As cited in" is acceptable for unobtainable primary sources; routine "as cited in" use signals the author has not read the cited work.

## Tool Decision Rubric

Pick once at the start. Switching mid-thesis is recoverable but costly.

| Tool | Strengths | Limitations | Best when |
|---|---|---|---|
| **Zotero** | Free, open-source, browser connector excellent, strong PDF management, group libraries, plugins (Better BibTeX, Zotero LibreOffice / Word integration) | Sync limited to 300 MB on free tier (storage upgrade is cheap) | Most users; default recommendation. Especially strong for LaTeX users via Better BibTeX |
| **Mendeley** | Free, decent PDF reader, social network for discovery, Word plugin | Owned by Elsevier (privacy concerns), reduced development | Existing Mendeley users with established libraries; otherwise prefer Zotero |
| **EndNote** | Mature Word integration, large institutional installs, strong search across many databases | Commercial; clunky modern UI | When your institution mandates it or your collaborators all use it |
| **BibTeX / BibLaTeX (manual)** | Maximum control, plain-text under version control | No PDF management, no metadata fetching, manual maintenance | Math / theory theses with small bibliographies (< 100 entries) and LaTeX fluency |
| **JabRef** | BibTeX-native GUI, free, open-source, good for editing `.bib` files | Less polished than Zotero for general use | LaTeX-only workflow with heavy `.bib` editing |
| **Paperpile** | Strong Google Docs integration, web-first | Subscription; less LaTeX-native | Google Docs-based collaborative workflows |

**Decision shortcut:** Zotero + Better BibTeX for LaTeX users. Zotero alone for Word users. EndNote only when institutionally mandated. Pure BibTeX only for small (< 100 entry) math theses.

## Library Setup — First Hour Investment

The first hour spent configuring the manager pays back across the whole thesis. Skipping it produces the chaos most theses end up rebuilding from in week 30.

| Setup step | Why it matters |
|---|---|
| Install browser connector | One-click capture from Google Scholar / journal pages avoids manual entry errors |
| Install word processor / LaTeX integration (Better BibTeX for LaTeX) | Citation insertion becomes one keystroke |
| Create a project-level collection (e.g., "PhD Thesis") | Keeps unrelated reading separate |
| Create sub-collections per chapter / RQ | Maps directly onto the literature-review architecture |
| Choose citation key format (e.g., `Smith2020SparseAttention`) | Stable, human-readable, version-control-friendly |
| Set sync (Zotero account, OneDrive for Word users) | Library survives laptop loss |
| Backup `.bib` to git if LaTeX | Recoverable history of every citation change |
| Configure auto-fetch DOI metadata | Prevents typos in author names and titles |

## Identifier Hygiene

The single biggest cause of broken references is bad metadata at import time. Fix it once, and the rest of the thesis benefits.

| Identifier | When to use | How to verify |
|---|---|---|
| **DOI** | Any journal article from 1995 onward; many books and conference papers | Resolve at https://doi.org/<DOI> — should hit the publisher page |
| **ArXiv ID** | Preprints; cite the published version when available | Resolve at https://arxiv.org/abs/<ID> |
| **ISBN** | Books, edited volumes | Verify on WorldCat or publisher site |
| **PMID** | Biomedical | Resolve at https://pubmed.ncbi.nlm.nih.gov/<ID> |
| **Semantic Scholar Corpus ID** | Useful as a backup identifier | Less stable than DOI; do not rely on alone |
| **URL + access date** | Web pages, software, datasets without DOIs | Last resort; expect link rot — archive via web.archive.org |
| **OSF / Zenodo** | Datasets, preregistrations, code releases | These DOIs are durable; preferred for reproducibility |

**Common metadata defects to fix at import:**
- Author names truncated ("Smith J" → "Smith, John A.")
- Title in ALL CAPS or sentence case where title case is required (style-dependent)
- Journal abbreviations vs full names (style-dependent — pick one and apply)
- Missing volume / issue / pages
- Wrong year (preprint year vs published year — cite the published version)
- "et al." baked into the author field (each author should be a separate entry)

## Importing References — Source Hierarchy

Not all import sources produce equal-quality metadata. Prefer high-quality sources and verify the rest.

| Source | Metadata quality | Notes |
|---|---|---|
| Crossref / DOI metadata | Highest | Fetch directly via DOI when possible |
| Publisher page | High | Use the "Cite" / "Export Citation" button |
| Semantic Scholar | High | Strong for CS / ML preprints; use for citation-graph queries |
| PubMed | High | Biomedical default |
| Google Scholar | Mixed | Convenient but noisy; verify author names and dates |
| Author's personal site | Variable | Trust the publisher version more |
| BibTeX from random author's repo | Low | Audit before importing; common source of typos |

When importing in bulk (e.g., from a literature-review search), spot-check 5-10% of entries against the original source. Errors at import compound.

## Citation Graph for the Literature Review

A thesis library is not a flat list — it is a directed graph. Building the graph deliberately accelerates the literature review.

| Step | Tool support |
|---|---|
| 1. Seed with the 5-10 most central papers in your area | Manual; advisor input |
| 2. Backward chain (their references) for foundational work | Zotero / Mendeley import; or Connected Papers |
| 3. Forward chain (papers citing them) for recent developments | Google Scholar "Cited by"; Semantic Scholar; Inciteful |
| 4. Concurrent search by topic for last 24 months | arXiv, Semantic Scholar Recommendations |
| 5. Tag each entry: foundational / methodological / empirical / adjacent | Zotero tags; consistent vocabulary |
| 6. Identify the gap — papers that should exist but don't | Map the cluster; missing region is the contribution opportunity |

This graph feeds `skill-literature-review` directly. The graph also informs `skill-contribution-checker`'s novelty audit — concurrent work in the last 12 months must be visible in the graph.

## In-Text Citation Patterns (Style-Agnostic)

The mechanics here apply across styles; the surface format depends on the style chosen via `skill-formatting`.

| Pattern | Use when |
|---|---|
| **Narrative** ("Smith (2020) demonstrated…") | The author is the subject of the sentence; emphasizes the source |
| **Parenthetical** ("recent work has demonstrated… (Smith, 2020)") | The finding is the subject; citation is supporting |
| **Multiple sources** ("(Smith, 2020; Jones, 2021; Park, 2023)") | Reading is converging; pick the strongest 2-3, not 8 |
| **Page-specific** ("(Smith, 2020, p. 47)") | Direct quotes; specific claims |
| **Et al.** | When 3+ authors; first author + et al. (style-dependent on first vs subsequent use) |
| **Secondary** ("Johnson (1985), as cited in Smith, 2020") | When primary source is unavailable; should be rare |

**Citation stuffing** — five papers behind a single uncontroversial claim — is an AI-style anti-pattern. Cite the foundational work and one recent example.

**Vague attribution** — "studies have shown," "experts believe" — is not citation. Either name the studies or cut the claim.

## Style Choice — Where This Skill Hands Off to `skill-formatting`

The choice of *which* style (APA / IEEE / Chicago / Vancouver / MLA) belongs to `skill-formatting`. Once chosen, this skill applies it via the manager's CSL or BibTeX style file.

| Style | CSL file (Zotero / Mendeley) | LaTeX bibliography style |
|---|---|---|
| APA 7 | apa.csl | `natbib` with `apalike` or BibLaTeX `apa` |
| IEEE | ieee.csl | `IEEEtran` |
| ACM | acm-sig-proceedings.csl | `acmart` class |
| Chicago author-date | chicago-author-date.csl | BibLaTeX `chicago-authordate` |
| Chicago notes-bibliography | chicago-note-bibliography.csl | BibLaTeX `chicago-notes` |
| Vancouver | vancouver.csl | `vancouver` |

If the chosen style isn't in the default CSL list, the [Zotero Style Repository](https://www.zotero.org/styles) catalogues most departmental and journal variants.

## Pre-Submission Reference Audit

- [ ] Every in-text citation resolves to a reference list entry
- [ ] Every reference list entry is cited at least once in text
- [ ] DOIs / ArXiv IDs / ISBNs verified for every entry where they should exist
- [ ] All DOIs resolve (no 404s); test a sample
- [ ] Author names — capitalization, initials, accented characters — match the source
- [ ] Year is the *published* year (preprints cited as preprint or as published version, consistently)
- [ ] Page ranges, volume, issue present where the style requires
- [ ] Style applied uniformly (single CSL or single `\bibliographystyle`)
- [ ] No "as cited in" remains where the primary source is obtainable
- [ ] No citation stuffing (> 4 references behind a single uncontroversial claim)
- [ ] No vague attribution ("studies have shown") without a citation
- [ ] Reference list ordering correct (alphabetical or numerical, per style)
- [ ] No duplicate entries (same paper cited twice with different keys — the most common subtle defect)
- [ ] Concurrent / preprint work checked — within 12 months of submission, has it appeared elsewhere with a different DOI?
- [ ] `skill-formatting` confirms style choice is applied; layout-level details are checked there
- [ ] `skill-avoid-ai-writing` with `related-work` profile run on the literature review for citation-stuffing patterns

## Common Failure Modes

| Pattern | Consequence |
|---|---|
| Two reference managers used in parallel | Drift; references missing in one or the other |
| Hand-typed reference list | Typos in author names, dates, page ranges; reference list and library disagree |
| Imported BibTeX never audited | Truncated names, missing DOIs, wrong years; surface only at submission |
| Same paper cited with two different keys | Duplicate references in the list; reviewer flag |
| `(Smith et al., 2020; Smith et al., 2020a; Smith et al., 2020b)` mixed inconsistently | Style not applied uniformly; usually a tool config error |
| URLs as the only identifier when DOIs exist | Link rot; reproducibility loss |
| Cited papers the author has not read | Detected when reviewer asks about specifics; credibility damage |
| Five citations behind every sentence | AI-style citation stuffing; reviewer fatigue |
| "et al." baked into the author field | Each author should be a separate entry; alphabetization breaks |
| Preprint cited when published version exists | Cite the published version; preprint as alternate identifier |
| `\cite` with broken keys at submission (LaTeX) | "[?]" appears in the PDF; visible at submission |
| Reference list export not regenerated after final edits | Reference list lags the in-text citations |

## Integration

- `domains/thesis/skill-formatting` — chooses the style; this skill applies and audits it
- `domains/thesis/skill-literature-review` — citation graph built here feeds the synthesis there
- `domains/thesis/skill-contribution-checker` — novelty audit depends on a complete and recent citation graph
- `domains/thesis/skill-argument-validator` — claim chains depend on accurate citation
- `domains/thesis/skill-thesis-structure` — back matter (References) is part of the architecture
- `domains/thesis/skill-consistency-checker` — terminology and reference consistency are a final pre-submission pass
- `domains/thesis/skill-avoid-ai-writing` — `related-work` profile flags citation stuffing and vague attributions
- `domains/thesis/skill-academic-writing` — narrative vs parenthetical citation choice is partly a register choice

## Resources

- [Zotero](https://www.zotero.org/) — primary recommended tool
- [Better BibTeX for Zotero](https://retorque.re/zotero-better-bibtex/) — stable citation keys, automatic `.bib` export, BibLaTeX support
- [Zotero Style Repository](https://www.zotero.org/styles) — searchable catalogue of CSL styles for departments and journals
- [Crossref](https://www.crossref.org/) — DOI registry; lookup and metadata
- [Semantic Scholar](https://www.semanticscholar.org/) — citation graph, recommendations, identifier resolution
- [Connected Papers](https://www.connectedpapers.com/) — visual citation neighborhood maps; useful for backward / forward chaining
- [arXiv](https://arxiv.org/) — preprint identifiers, especially CS / ML / physics / math
- [BibLaTeX Documentation (CTAN)](https://ctan.org/pkg/biblatex) — modern LaTeX bibliography handling
- [APA Style — DOIs and URLs](https://apastyle.apa.org/style-grammar-guidelines/references/dois-urls)
