---
name: thesis-lattice
description: Mode orchestrator for academic research writing — theses, journal papers, dissertations, conference papers. Activated automatically by Lattice.md when the user describes academic-writing work. Coordinates the DPEV loop with phase artifacts where each phase is typically a chapter or major section. Orchestrates eligible domain skills from domains/thesis/ and domains/shared/.
---

# thesis-lattice Mode

Academic research writing orchestrator. Coordinates the DPEV loop across chapters, sections, or research milestones.

## When This Mode Activates

The user is producing scholarly written work:

- **Theses and dissertations:** undergraduate, master's, PhD
- **Journal papers:** original research, review papers
- **Conference papers:** workshop, conference, journal submissions
- **Other academic outputs:** technical reports, white papers, grant proposals

Trigger phrases (caught by `Lattice.md` mode detection):
- "thesis", "dissertation", "research paper", "journal article"
- "academic writing", "literature review", "methodology section"
- "abstract", "discussion", "conclusion"
- "write a paper", "submit to [conference/journal]"

If the project also includes building an ML/AI system, hybrid mode activates both `model-lattice` and `thesis-lattice`.

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

1. Apply `questioning-protocol.md` to gather the brief. Thesis-specific items:
   - Research domain and sub-area
   - Research question (specific enough to be falsifiable)
   - Contribution / gap in the literature
   - Audience (committee, journal, conference, defense)
   - Type (empirical / theoretical / review / mixed)
   - Methodology direction
   - Style guide and citation format (APA / IEEE / ACM / etc.)
   - Hard constraints (page limit, deadline, advisor preferences)
2. Confirm the brief
3. Decide structure (apply Unsure Protocol if uncertain — IMRaD, narrative, by-paper-collection)
4. Initialize `.lattice-plan.md`
5. Decompose into phases (chapters or major sections). Common thesis sequence:
   - `01-introduction/` — research question, motivation, contribution
   - `02-literature-review/` — survey of related work
   - `03-methodology/` — methods and design
   - `04-results/` — findings (or per-experiment if multiple studies)
   - `05-discussion/` — interpretation
   - `06-conclusion/` — synthesis and future work
6. Get user approval on the chapter roadmap

### 2. Per-phase DPEV loop

For the next pending chapter or section:

**During DISCUSS:** lock the chapter's scope and argument in `CONTEXT.md`. Common thesis decisions:
- Chapter goal — what argument does it make?
- Section structure
- Key claims and the evidence each requires
- What's in scope vs out of scope (out-of-scope is critical to prevent chapter sprawl)
- Citation density expected
- Figures/tables to include
- Argument flow — how does this chapter connect to previous and next

**During PLAN:** apply `writing-plans-protocol.md`. Tasks are section-by-section drafts with citations to gather, figures to insert, evidence to weave in. Verify with `plan-checker-protocol.md`.

**During EXECUTE:**
- Produce the draft section by section
- Apply `domains/thesis/skill-academic-writing.md` for general scholarly prose
- Apply `domains/thesis/skill-avoid-ai-writing.md` to keep prose natural
- Apply `domains/thesis/skill-citation-management.md` to handle references
- Apply chapter-specific skills (e.g., `skill-results-writing` for results, `skill-discussion-writing` for discussion)
- Update SUMMARY.md as you go
- For surveying multiple sub-areas in a literature review, apply `parallel-agents-protocol.md`
- If a bug in the argument appears (claim doesn't follow from evidence), apply `skill-debugging.md`'s scientific method to the argument

**During VERIFY:**
- Apply `verification-protocol.md` — every claim cited or supported by evidence in the text
- Apply `skill-argument-validator.md` — does the argument actually hold?
- Apply `skill-consistency-checker.md` — terminology and notation consistent across chapters?
- Apply `skill-contribution-checker.md` — is the contribution clear and supported?
- Run a final `skill-avoid-ai-writing.md` pass with the appropriate context profile (`thesis-chapter`, `journal-paper`, etc.)
- Confirm decision coverage end-to-end
- Apply `skill-self-review.md` for major sections — fresh-context review catches argument gaps
- Write VERIFICATION.md

### 3. Phase completion

After VERIFY passes:
1. Update `.lattice-plan.md` phase status to Done
2. Move to next phase
3. If the chapter changes how earlier chapters should be framed, route back to those phases' DISCUSS

### 4. Project completion

When all phases are Done:
1. Cross-chapter consistency check (notation, terminology, argument flow)
2. Final formatting pass (`skill-formatting`)
3. Abstract pass (`skill-abstract-writing`) — usually written or revised last
4. Citation final check (`skill-citation-management`)
5. Hand back to `Lattice.md`

## Eligible Domain Skills

### Thesis domains (`domains/thesis/`)

| Skill | Activate when |
|---|---|
| `skill-thesis-structure` | Setting up the overall thesis structure |
| `skill-academic-writing` | General scholarly prose and conventions |
| `skill-avoid-ai-writing` | Reviewing prose for AI-isms; final-pass quality |
| `skill-abstract-writing` | Writing or revising the abstract |
| `skill-literature-review` | Survey, gap identification, related work |
| `skill-research-methodology` | Methodology chapter / methods section |
| `skill-results-writing` | Reporting results without inflation |
| `skill-discussion-writing` | Interpreting results, calibrated hedging |
| `skill-conclusion-writing` | Synthesis and future work |
| `skill-argument-validator` | Checking that arguments actually hold |
| `skill-consistency-checker` | Cross-chapter consistency |
| `skill-contribution-checker` | Verifying the contribution is clear |
| `skill-citation-management` | Reference management, citation style |
| `skill-figures-and-tables` | Visual asset design and captioning |
| `skill-formatting` | Style guide compliance |
| `skill-dataset-documentation` | Dataset descriptions for empirical work |
| `skill-ml-experiment-design` | Experiment design for empirical thesis chapters |
| `skill-model-description` | Describing models in academic style |

### Shared domains (`domains/shared/`)

Same as other modes — but `skill-tdd` typically does NOT apply (no code being shipped). Active ones: `skill-debugging` (for argument bugs), `skill-self-review` (for chapter review), `skill-receiving-feedback` (for advisor feedback), `skill-docs`, `skill-ethics`, `skill-reproducibility` (for empirical chapters).

For empirical theses, `domains/ml/*` is also eligible — apply hybrid mode.

## Per-Mode Quality Notes

- **Citations are non-negotiable.** Apply `skill-citation-management` from day one. Never fabricate a citation — flag missing sources as `[CITATION NEEDED]`.
- **Calibrated hedging.** Apply `skill-avoid-ai-writing.md` with `discussion-section` profile when writing discussions — calibrated hedging is allowed; reflexive AI hedging is not.
- **Argument before prose.** A chapter's CONTEXT.md must lock the argument before drafting. "Beautiful prose for a wrong argument" is the worst failure mode.
- **Abstract written last.** The abstract reflects what was actually written, not what was planned. Revise it after the final chapter is done.
- **Cross-chapter consistency.** `skill-consistency-checker` runs at project completion at minimum. Notation, terminology, and definitions must align across chapters.
- **Decision coverage matters even more.** A locked decision in chapter 03 ("we use X notation") must show up in all later chapters. Apply decision coverage end-to-end across the entire thesis.
- **Avoid-AI-writing as final pass.** Run it on every section before declaring it done. Use the appropriate context profile (`thesis-chapter`, `journal-paper`, `abstract`, `discussion-section`, etc.).

## Handoff Back to Lattice

When the thesis (or paper) is complete:
1. Update `.lattice-plan.md` with final status
2. Run cross-chapter consistency one more time
3. Hand back to `Lattice.md` for status check or new-milestone flow
