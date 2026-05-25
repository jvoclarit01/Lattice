<!-- ADAPTED from D:/GSD/docs/ARCHITECTURE.md (File System Layout section) and the
     phase-folder convention used across .planning/ in GSD. Adaptations: replaced
     .planning/ with the Lattice-equivalent path (project root or `.lattice/`),
     replaced GSD-specific naming (REQUIREMENTS.md, MILESTONES.md) with Lattice-mode
     equivalents, and dropped artifacts that don't apply to Lattice (UAT, UI-REVIEW,
     gsd-tools.cjs-managed indices). The CONTEXT/RESEARCH/PLAN/SUMMARY/VERIFICATION
     five-artifact pattern and per-phase folder structure are preserved. -->

# The Phase Artifacts Protocol

How to organize per-phase work so each phase has its own context, decisions, plan, and outcomes — without polluting the project-level `.lattice-plan.md` or contaminating later phases.

## When to Apply

Use the phase artifacts pattern when:
- A project has multiple distinct phases (typical for `project-lattice` and `model-lattice`)
- A thesis has multiple chapters or experiment runs (typical for `thesis-lattice`)
- A phase is large enough to deserve its own design discussion, research, plan, and review

For trivial single-step work, a single section in `.lattice-plan.md` is enough — don't create empty phase folders.

## Folder Layout

Each phase lives in its own folder under `.lattice/phases/`:

```
project-root/
├── .lattice-plan.md              ← Project-level state and phase index
└── .lattice/
    └── phases/
        ├── 01-foundation/
        │   ├── CONTEXT.md      ← Decisions captured during discuss step
        │   ├── RESEARCH.md     ← Findings from plan step research
        │   ├── PLAN.md         ← Tasks, dependencies, acceptance criteria
        │   ├── SUMMARY.md      ← Outcomes after execute step
        │   └── VERIFICATION.md ← Review against success criteria
        ├── 02-auth-system/
        │   ├── CONTEXT.md
        │   ├── PLAN.md
        │   └── SUMMARY.md
        └── 03-payment-flow/
            └── CONTEXT.md
```

**Naming:** `NN-kebab-case-name/` where `NN` is a zero-padded two-digit phase number reflecting the order in `.lattice-plan.md`.

**Backward compatibility:** `.lattice-plan.md` remains the project-level index and state. Phase folders are additive — they hold detail that doesn't belong at the project level.

## Artifact Types

Each phase produces up to five artifacts. Not every phase needs all five — small phases can skip RESEARCH or VERIFICATION.

### CONTEXT.md — Decisions captured during the discuss step

Purpose: record the user's intent, constraints, and choices for this specific phase before any planning happens.

Sections:
- **Goal** — One sentence describing what this phase delivers
- **Why now** — Why this phase exists in the order it does
- **Decisions locked** — User-confirmed choices (UI patterns, API shapes, data formats, approaches)
- **Out of scope** — What this phase explicitly does not do
- **Dependencies** — What earlier phases this builds on, and what assets it needs

CONTEXT.md is the user's voice. Once written, decisions in CONTEXT.md are not re-litigated unless the user explicitly revisits them.

### RESEARCH.md — Findings from the plan step

Purpose: record any external research needed to write a sound plan.

Sections:
- **Open questions before research** — what was unclear at start
- **Findings** — concrete answers, with sources/citations
- **Open questions after research** — what's still unclear (blocks planning if unresolved)
- **Recommendations** — what the research implies for the plan

For phases without external unknowns (e.g., a straightforward refactor), RESEARCH.md can be skipped or replaced with a one-line "No research needed" note.

### PLAN.md — Tasks, dependencies, acceptance criteria

Purpose: a concrete, executable breakdown of the work.

Sections:
- **Objective** — restate the phase goal in implementation terms
- **Tasks** — ordered list, each with: what to do, files affected, verification step, acceptance criteria
- **Dependencies between tasks** — explicit ordering or parallel groups
- **Decision coverage** — checklist confirming every decision in CONTEXT.md maps to at least one task
- **Verification** — how to confirm the whole phase is done (commands, files, behaviors)
- **Success criteria** — measurable outcomes that signal completion

Plans are reviewed by the plan-checker (see `plan-checker-protocol.md`) before execution.

### SUMMARY.md — Outcomes after the execute step

Purpose: record what was actually built, what deviated from the plan, and what the next phase needs to know.

Sections:
- **What was built** — link to commits or file paths
- **Deviations from plan** — anything the executor changed during implementation, and why
- **Open issues** — bugs found, deferred work, follow-ups
- **What downstream phases need to know** — interfaces, conventions, gotchas

SUMMARY.md is what gets read by the next phase's discuss step — it's the bridge between phases.

### VERIFICATION.md — Review against success criteria

Purpose: explicit verification that the phase met its success criteria, written by an independent pass (the verifier role) before user UAT.

Sections:
- **Success criteria from PLAN.md** — copied verbatim
- **Per-criterion verification** — for each criterion: PASSED / FAILED / PARTIAL with evidence
- **Decision coverage check** — confirm every CONTEXT.md decision appears in shipped work
- **Gaps surfaced** — anything missing or broken
- **Recommendation** — ready for user review / needs fixes / blocked

For modes where formal verification is overkill (early `thesis-lattice` brainstorming, exploratory `model-lattice` spikes), this can be a 3-line note rather than a full review.

## Per-Mode Adaptation

### project-lattice

Phases are feature milestones. Typical sequence:
- `01-foundation/` — repo setup, base stack, core models
- `02-auth/` — authentication system
- `03-feature-X/` — first user-facing feature
- `04-feature-Y/` — second feature

A phase usually maps to a sprint or a deployable increment.

### model-lattice

Phases are experiment runs or system stages. Typical sequence:
- `01-data-pipeline/` — collection, preprocessing, versioning
- `02-baseline-model/` — first end-to-end working model
- `03-experiment-A/` — first hypothesis test
- `04-experiment-B/` — second hypothesis test
- `05-deployment/` — serving and monitoring

CONTEXT.md captures the experimental hypothesis. PLAN.md is the experiment design. SUMMARY.md is the results.

### thesis-lattice

Phases are chapters or major sections. Typical sequence:
- `01-introduction/` — research question, motivation, contribution
- `02-literature-review/` — survey
- `03-methodology/` — methods and design
- `04-results/` — findings
- `05-discussion/` — interpretation
- `06-conclusion/` — synthesis and future work

CONTEXT.md captures the chapter's scope and argument. PLAN.md is the section breakdown. SUMMARY.md is the draft outcome.

## .lattice-plan.md as the Phase Index

The project-level `.lattice-plan.md` keeps a phase index — one row per phase, with status pointing to the phase folder:

```markdown
## Phases
| # | Name | Folder | Status |
|---|------|--------|--------|
| 01 | Foundation | `.lattice/phases/01-foundation/` | Done |
| 02 | Auth System | `.lattice/phases/02-auth-system/` | Executing |
| 03 | Payment Flow | `.lattice/phases/03-payment-flow/` | Planning |
| 04 | Admin Dashboard | (not started) | Pending |
```

**Read order during a session:**
1. `.lattice-plan.md` — get the project state and find which phase is active
2. Active phase's CONTEXT.md, PLAN.md (and SUMMARY.md if mid-execution) — get the operational detail
3. Other phases' SUMMARY.md only if explicitly needed — don't blanket-load

## What NOT to Do

- **Do not** read every phase's full PLAN.md every session. Only the active phase.
- **Do not** duplicate decisions across CONTEXT.md and `.lattice-plan.md`. CONTEXT.md is per-phase; `.lattice-plan.md` indexes phases.
- **Do not** skip CONTEXT.md and jump to PLAN.md. Decisions get lost; downstream phases re-litigate.
- **Do not** write VERIFICATION.md before SUMMARY.md exists. Verification needs something to verify.
- **Do not** create phase folders for trivial work. A single-paragraph entry in `.lattice-plan.md` is fine for one-off changes.

## The Principle

Phase artifacts give each phase its own scoped memory. The project remembers via `.lattice-plan.md`; the phase remembers via its folder. This separation is what keeps a long-running project's context budget bounded — the orchestrator only loads what the current phase needs, not the entire history.
