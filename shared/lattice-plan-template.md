# Lattice Plan Template

Every project has a `.lattice-plan.md` in its root that tracks state, decisions, and progress.

## Template

```yaml
---
lattice_version: "1.0.0"
created: "YYYY-MM-DD"
last_updated: "YYYY-MM-DD"
---

# Lattice Plan

## Active Mode
- **Mode**: project-lattice | model-lattice | thesis-lattice | hybrid
- **Status**: brainstorming | planning | executing | documenting | complete

## Project Brief
- **What we're building**: ...
- **Who it's for**: ...
- **What problem it solves**: ...
- **Success criteria**: ...

## Global Constants
```yaml
global_constants:
  # Mode-specific constants
  ...
  reasoning: "..."
```

## Stack / Approach
- **Chosen approach**: ...
- **Reasoning**: ...
- **Alternatives considered**: ...

## Domain Status
| Domain | Status | Notes |
|--------|--------|-------|
| skill-frontend | Pending | |
| skill-backend | In Progress | |
| skill-database | Done | |

## Open Questions
- [ ] Question 1
- [ ] Question 2

## Experiment Log (model-lattice / thesis-lattice only)
| ID | Hypothesis | Config | Results | Interpretation |
|----|------------|--------|---------|----------------|
| 1 | ... | ... | ... | ... |

## Revision History
| Date | Change |
|------|--------|
| YYYY-MM-DD | Initial plan created |
```

## Status Values

- **Pending** → Not started
- **In Progress** → Currently working on
- **Done** → Completed and documented

## Mode Values

- **brainstorming** → Gathering ideas and requirements
- **planning** → Creating detailed plans
- **executing** → Implementing the plan
- **documenting** → Writing documentation
- **complete** → All phases done

## Per-Phase Folders (Optional Extension)

For projects with multiple distinct phases, augment `.lattice-plan.md` with a per-phase folder structure under `.lattice/phases/`. Each phase folder holds CONTEXT.md, RESEARCH.md, PLAN.md, SUMMARY.md, and VERIFICATION.md.

`.lattice-plan.md` becomes the project-level **index**, with one row per phase pointing into its folder:

```markdown
## Phases
| # | Name | Folder | Status |
|---|------|--------|--------|
| 01 | Foundation | `.lattice/phases/01-foundation/` | Done |
| 02 | Auth System | `.lattice/phases/02-auth-system/` | Executing |
| 03 | Payment Flow | (not started) | Pending |
```

Single-phase or trivial projects can keep all detail in `.lattice-plan.md` itself — phase folders are additive, not required. See `phase-artifacts-protocol.md` for the full structure.

## The Principle

The `.lattice-plan.md` is the **project's memory**. It tracks everything important about the project so you can resume work at any time without losing context. Update it after every meaningful decision or completed domain. For multi-phase projects, scope detail to per-phase folders so the project-level memory stays browsable.
