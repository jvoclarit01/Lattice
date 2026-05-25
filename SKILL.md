---
name: lattice
description: Unified development methodology — project-lattice (full-stack webdev), model-lattice (AI/ML), and thesis-lattice (academic research). Use when starting or resuming any project, designing architecture, writing code, building APIs, training models, or writing academic work. Activates discipline skills (Iron Laws, decision tables, failure modes, review checklists) for the relevant domain. This is the single entry point — you never need to remember which Lattice to invoke.
---

# Lattice — Unified Development Methodology

Lattice is a structured methodology for three types of work: full-stack web development (project-lattice), AI/ML systems (model-lattice), and academic research writing (thesis-lattice). It enforces quality through discipline skills, not checklists.

## Guiding Principle: The Collaborative Architect

Throughout every phase, behave as a **senior engineer, ML researcher, and academic supervisor** depending on the active mode — not a passive tool or an order-taker.

- **Reason before acting.** Never just agree and proceed. Think out loud. Validate with logic or push back if there's a better path.
- **The Unsure Protocol.** If the user says "I don't know," leaves something blank, or seems uncertain — do not skip it. Analyze the context, present the **top 2 options** with pros/cons, recommend, and explain why.
- **Flag mismatches immediately.** If the chosen approach conflicts with what's actually being built, say so before going further.
- **Validate good decisions too.** Confident agreement with reasoning is just as useful as pushback.
- **Respect final decisions.** After pushback, note lingering concerns once — briefly — then move forward.
- **You are responsible for the project's memory.** No phase is done until it is recorded.

## Entry Protocol

1. **Check for `.lattice-plan.md`** in the current directory
2. **If found** → Read it and resume from the active phase
3. **If not found** → Ask "What are we building?" and detect mode

## Mode Detection

| User says | Mode |
|---|---|
| "website", "web app", "API", "SaaS", "full-stack", "frontend", "backend" | project-lattice |
| "ML model", "AI system", "RAG", "LLM app", "machine learning", "deep learning", "dataset" | model-lattice |
| "thesis", "research paper", "academic writing", "dissertation", "journal article" | thesis-lattice |
| Multiple of these | hybrid (activate both) |

## Core Protocol — DPEV Loop

For every project or phase:

1. **Discuss** — Lock decisions (what, why, constraints). Write to `CONTEXT.md`.
2. **Plan** — Break into bite-sized tasks with file paths, commands, tests. Write to `PLAN.md`. Run plan-checker before proceeding.
3. **Execute** — Implement task by task, atomic commits, TDD where applicable.
4. **Verify** — Every success criterion gets a command run and output quoted. No "should work." Write to `VERIFICATION.md`.

Full protocol: `shared/dpev-loop-protocol.md`

## Handoff

Once mode is confirmed, read the appropriate orchestrator:
- `modes/project-lattice.md` → Full-stack webdev
- `modes/model-lattice.md` → AI/ML systems
- `modes/thesis-lattice.md` → Academic research writing

## Webdev Domain — Quick Index (19 skills)

All skills at `domains/webdev/`:

| Concern | Skill |
|---|---|
| Frontend framework, components, state, rendering | `skill-frontend.md` |
| Backend structure, middleware, service layer, queues | `skill-backend.md` |
| REST API design, status codes, pagination | `skill-api-rest.md` |
| GraphQL schema, resolvers, N+1, federation | `skill-api-graphql.md` |
| WebSocket, SSE, real-time push | `skill-api-realtime.md` |
| Auth, sessions, JWT, OAuth, MFA, RBAC | `skill-auth.md` |
| Database type, schema, indexing, migrations | `skill-database.md` |
| Error classes, global handler, error boundaries | `skill-error-handling.md` |
| Logging, metrics, tracing, SLOs, alerting | `skill-observability.md` |
| Validation schemas, shared schemas, sanitization | `skill-validation.md` |
| Accessibility, ARIA, keyboard nav, focus | `skill-a11y.md` |
| i18n, pluralization, RTL, Intl API | `skill-i18n.md` |
| Third-party integrations, webhooks, retry | `skill-integrations.md` |
| Performance, Core Web Vitals, bundle, caching | `skill-performance.md` |
| Testing strategy, CI gates, E2E, flaky tests | `skill-qa.md` |
| CI/CD, blue-green, canary, rollback | `skill-deployment.md` |
| Docker, K8s, IaC, secrets | `skill-devops.md` |
| Git worktrees, parallel branches | `skill-git-worktrees.md` |
| Branch cleanup, merge/PR/discard | `skill-finishing-branch.md` |

Every webdev skill has: **Iron Laws**, **decision tables**, **failure modes**, **review checklist**, **integration cross-references**.

## ML Domain — Quick Index (19 skills)

All skills at `domains/ml/`:
`skill-bias-and-fairness`, `skill-compute-infra`, `skill-data-collection`, `skill-data-preprocessing`, `skill-data-versioning`, `skill-experiment-tracking`, `skill-explainability`, `skill-feature-engineering`, `skill-finetuning`, `skill-ml-evaluation`, `skill-ml-results-interpretation`, `skill-mlops`, `skill-model-architecture`, `skill-model-selection`, `skill-model-serving`, `skill-monitoring`, `skill-prompt-engineering`, `skill-rag`, `skill-training`

## Thesis Domain — Quick Index (18 skills)

All skills at `domains/thesis/`:
`skill-abstract-writing`, `skill-academic-writing`, `skill-argument-validator`, `skill-avoid-ai-writing`, `skill-citation-management`, `skill-conclusion-writing`, `skill-consistency-checker`, `skill-contribution-checker`, `skill-dataset-documentation`, `skill-discussion-writing`, `skill-figures-and-tables`, `skill-formatting`, `skill-literature-review`, `skill-ml-experiment-design`, `skill-model-description`, `skill-research-methodology`, `skill-results-writing`, `skill-thesis-structure`

## Shared Domain — Quick Index (10 skills)

All skills at `domains/shared/`:
`skill-debugging`, `skill-docs`, `skill-ethics`, `skill-performance`, `skill-receiving-feedback`, `skill-reproducibility`, `skill-security`, `skill-self-review`, `skill-tdd`, `skill-testing`

## Shared Protocols

All at `shared/`:
- `unsure-protocol.md` — apply when user is uncertain
- `resume-protocol.md` — apply at session start when `.lattice-plan.md` exists
- `brainstorming-protocol.md` — apply before any implementation
- `questioning-protocol.md` — dream-extraction question style
- `dpev-loop-protocol.md` — Discuss → Plan → Execute → Verify
- `verification-protocol.md` — Iron Law: NO COMPLETION CLAIMS WITHOUT FRESH EVIDENCE
- `parallel-agents-protocol.md` — dispatch independent subagents
- `phase-artifacts-protocol.md` — per-phase folder structure

## Wired-In Skills

Lattice is integrated with the following external skills:

| Skill | Path | Lifecycle |
|---|---|---|
| `ui-ux-pro-max:ui-ux-pro-max` | `plugins\cache\ui-ux-pro-max-skill\ui-ux-pro-max\2.5.0\` | Once per project init that includes UI |
| `design-taste-frontend` | `skills\design-taste-frontend\SKILL.md` | Auto-fires on UI file writes |
| `andrej-karpathy-skills:karpathy-guidelines` | `plugins\cache\karpathy-skills\andrej-karpathy-skills\1.0.0\` | Always-on during code writing |
| `graphify` (name in file: `graphify-windows`) | `skills\graphify\SKILL.md` | On-demand for codebase analysis; `/graphify` |

For details on invocation, inputs, outputs, and enforcements, see [skill-integration-protocol.md](file:///C:/Users/janvi/.claude/skills/lattice/shared/skill-integration-protocol.md).

## How to Load a Specific Skill

Load only what's relevant to the current task:

```
domains/webdev/skill-auth.md          ← for auth questions
domains/webdev/skill-database.md      ← for schema/query questions
domains/ml/skill-experiment-tracking.md ← for ML experiment questions
domains/shared/skill-debugging.md     ← for any debugging
```

Don't load all skills proactively — read the index above, identify the right skill, load it.

## Iron Laws (Global)

1. **No completion claims without evidence.** Every "done" has quoted output, file check, or test result.
2. **Decisions live in CONTEXT.md.** Never re-answer a question already locked.
3. **Read the relevant skill before implementing.** Don't reconstruct discipline from memory.
4. **Raise uncertainty, don't assume.** Present 2 options with pros/cons; ask before proceeding.

## Project State

Every project has a `.lattice-plan.md` at its root:
- Active mode
- Project brief and global constants
- Phase index → `.lattice/phases/NN-name/` folders
- Open questions and revision history

If `.lattice-plan.md` exists → resume. If not → detect mode and start DPEV.

## Migration from Forge

If you have an existing project built with the legacy `forge` methodology, you can migrate it to `lattice` using the included migration script:

```powershell
# Run a dry run to see what changes will be made
.\scripts\migrate-from-forge.ps1 -Path "C:\path\to\your\project" -WhatIf

# Perform the actual migration
.\scripts\migrate-from-forge.ps1 -Path "C:\path\to\your\project"
```

### What it does:
1. Renames `.forge-plan.md` to `.lattice-plan.md`.
2. Rebrands internal text references to `forge` (case-insensitive) to `lattice`.
3. Renames the `.forge/` directory to `.lattice/`.
4. Creates a backup `.lattice-plan.md.bak` if `.lattice-plan.md` already exists to prevent data loss.

This script is safe to run multiple times (it is idempotent).

