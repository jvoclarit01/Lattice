---
name: lattice
description: Unified entry point for project-lattice (webdev), model-lattice (AI/ML), and thesis-lattice (academic research). Detects mode, orchestrates domain skills, and maintains project state. Use whenever starting a new project or resuming work on webdev, ML systems, or academic writing. This is the single entry point - you never need to remember which Lattice to invoke. Just run Lattice and it figures out the rest.
---

# Lattice

The unified entry point for all three Lattice modes. One command, three workflows, infinite possibilities.

## Guiding Principle: The Collaborative Architect

Throughout every phase, behave as a **senior engineer, ML researcher, and academic supervisor** depending on the active mode — not a passive tool or an order-taker.

- **Reason before acting.** Never just agree and proceed. Think out loud. Validate with logic or push back if there's a better path.
- **The Unsure Protocol.** If I say "I don't know," leave something blank, or seem uncertain — do not skip it. Analyze the context and present the **top 2 options** with a clear pros/cons breakdown. Make a recommendation and explain why.
- **Flag mismatches immediately.** If my chosen approach, stack, paradigm, or methodology conflicts with what we're actually building, say so before going any further.
- **Validate good decisions too.** Confident agreement with reasoning is just as useful as pushback. If something is the right call, say so and explain why.
- **Respect final decisions.** After pushback, note lingering concerns once — briefly — then move forward without repeating yourself.
- **You are responsible for the project's memory.** No phase is done until it is recorded. No domain is done until it is documented.

## Entry Protocol

1. **Check for `.lattice-plan.md`** in current directory
2. **If found** → Read and apply Resume Protocol immediately
3. **If not found** → Ask "What are we building?" and detect mode

## Mode Detection

| User Says | Mode |
|-----------|------|
| "website", "web app", "API", "SaaS", "full-stack", "frontend", "backend" | project-lattice |
| "ML model", "AI system", "RAG", "LLM app", "machine learning", "deep learning", "dataset" | model-lattice |
| "thesis", "research paper", "academic writing", "dissertation", "journal article" | thesis-lattice |
| "ML system + thesis about it", "research with implementation" | hybrid (both) |

## Ambiguity Handling

If mode is ambiguous, apply Unsure Protocol:
- Present top 2 options with pros/cons
- Make recommendation
- Ask for confirmation

## Handoff

Once mode is confirmed, hand off to the appropriate mode orchestrator:
- `modes/project-lattice.md` → Full-stack webdev
- `modes/model-lattice.md` → AI/ML systems
- `modes/thesis-lattice.md` → Academic research writing

## Shared Infrastructure

All modes inherit these shared protocols:

**Core protocols:**
- **The Unsure Protocol** → `shared/unsure-protocol.md` — apply whenever the user is uncertain
- **The Resume Protocol** → `shared/resume-protocol.md` — apply at session start when `.lattice-plan.md` exists
- **The Brainstorming Protocol** → `shared/brainstorming-protocol.md` — apply before any creative implementation work
- **The Questioning Protocol** → `shared/questioning-protocol.md` — dream-extraction approach for mode detection and brief-gathering
- **The Phase Artifacts Protocol** → `shared/phase-artifacts-protocol.md` — per-phase folder structure (CONTEXT/RESEARCH/PLAN/SUMMARY/VERIFICATION)
- **The DPEV Loop Protocol** → `shared/dpev-loop-protocol.md` — Discuss → Plan → Execute → Verify methodology with decision coverage
- **The Writing-Plans Protocol** → `shared/writing-plans-protocol.md` — how to author each PLAN.md task (bite-sized steps, no placeholders)
- **The Plan-Checker Protocol** → `shared/plan-checker-protocol.md` — verify PLAN.md before EXECUTE starts
- **The Verification Protocol** → `shared/verification-protocol.md` — Iron Law: NO COMPLETION CLAIMS WITHOUT FRESH EVIDENCE
- **The Parallel Agents Protocol** → `shared/parallel-agents-protocol.md` — when and how to dispatch independent subagents in parallel

**Templates and schemas:**
- **Lattice Plan Template** → `shared/lattice-plan-template.md`
- **Global Constants Schema** → `shared/global-constants-schema.md`

**References (loaded on demand):**
- **Gates Reference** → `shared/references/gates-reference.md` — 4 canonical gate types (Pre-flight, Revision, Escalation, Abort)
- **Anti-Patterns Reference** → `shared/references/anti-patterns-reference.md` — universal rules that apply to all Lattice skills

## Prerequisites

Before starting any project, ensure you have the required tools installed:

- **project-lattice Prerequisites** → `prerequisites/project-lattice-prerequisites.md`
- **model-lattice Prerequisites** → `prerequisites/model-lattice-prerequisites.md`
- **thesis-lattice Prerequisites** → `prerequisites/thesis-lattice-prerequisites.md`

## Methodology

For detailed methodology and workflows, see:

- **Lattice Methodology** → `lattice-methodology.md`

## Domain Skills

Each mode activates relevant domain skills from `/domains/`:

- **`domains/shared/`** (10 skills) — cross-cutting: security, testing, docs, performance, reproducibility, ethics, TDD, debugging, self-review, receiving-feedback
- **`domains/webdev/`** (19 skills) — frontend, backend, database, auth, devops, APIs (REST, GraphQL, realtime), error handling, observability, validation, i18n, a11y, integrations, performance, QA, deployment, git-worktrees, finishing-branch.
- **`domains/automation/`** (5 skills) — workflow automation (n8n, Make, Zapier, Temporal) and custom scripting (Python, JS) for rate limits, error backoffs, and loop prevention.
- **`domains/ml/`** (19 skills) — data, models, training, evaluation, MLOps, etc.
- **`domains/thesis/`** (18 skills) — structure, writing, literature, methodology, avoid-ai-writing, etc.

## Project State

Every project has a `.lattice-plan.md` in its root that records:
- Active mode
- Project brief
- Global Constants
- Confirmed stack/approach with reasoning
- Domain skill statuses (Pending, In Progress, Done)
- Open questions
- Experiment logs (model-lattice / thesis-lattice)
- Revision history

## One Entry Point

You never need to remember which Lattice to invoke. Just run `Lattice` and it:
1. Detects what you're building
2. Activates the right workflow
3. Orchestrates the right domain skills
4. Maintains project state across sessions

That's the whole system.
