---
name: project-lattice
description: Mode orchestrator for full-stack web development — websites, web apps, APIs, SaaS products, frontend, backend, devops. Activated automatically by Lattice.md when the user describes a webdev project. Coordinates the DPEV loop with phase artifacts, applies Lattice protocols, and orchestrates eligible domain skills from domains/webdev/ and domains/shared/.
---

# project-lattice Mode

Full-stack webdev orchestrator. Coordinates the DPEV loop across one or more feature phases.

## When This Mode Activates

The user is building any web-based system:

- **Frontend:** websites, dashboards, web apps, design system
- **Backend:** APIs, services, microservices, server-side logic
- **Full-stack:** SaaS products, internal tools, marketplaces
- **Infrastructure:** deployment, CI/CD, observability

Trigger phrases (caught by `Lattice.md` mode detection):
- "website", "web app", "API", "SaaS", "full-stack"
- "frontend", "backend", "REST", "GraphQL", "WebSocket"
- "build a [user-facing system]", "deploy a service"

## Required Protocols on Entry

Load these from `shared/` at session start (Lattice.md handles this):

- `unsure-protocol.md` — apply on any uncertainty
- `resume-protocol.md` — apply if `.lattice-plan.md` exists
- `brainstorming-protocol.md` — apply before any phase begins
- `phase-artifacts-protocol.md` — defines per-phase folder structure
- `dpev-loop-protocol.md` — the operational backbone
- `verification-protocol.md` — Iron Law for completion claims
- `references/anti-patterns-reference.md` — universal rules

## The Workflow

### 1. Project initialization

If no `.lattice-plan.md` exists:

1. Apply `questioning-protocol.md` to gather the brief (what / why / who / done-look-like / constraints)
2. Confirm the brief with the user
3. Decide stack (apply Unsure Protocol if user is undecided)
4. Initialize `.lattice-plan.md` from `shared/lattice-plan-template.md`
5. Run codebase discovery using `understand-anything` (via `/understand`) to map files and architecture.
6. Decompose into phases — each is a feature milestone or deployable increment
7. Get user approval on the phase roadmap

If `.lattice-plan.md` exists, skip to step 2 (resume).

### 2. Per-phase DPEV loop

For the next pending phase in `.lattice-plan.md`:

```
DISCUSS  →  PLAN  →  EXECUTE  →  VERIFY  →  Done
```

Apply `dpev-loop-protocol.md` rigorously. Each step produces an artifact in `.lattice/phases/NN-name/`.

**During DISCUSS:** invoke `brainstorming-protocol.md`. Lock decisions in `CONTEXT.md`. Common webdev decisions:
- UI patterns and design system choices
- API shapes and contracts
- Data models and persistence
- Auth flow
- Error handling strategy
- Performance budget
- Deployment target

**During PLAN:** apply `writing-plans-protocol.md` for task authoring. Verify with `plan-checker-protocol.md` before EXECUTE.

**During EXECUTE:**
- Use `domains/webdev/skill-git-worktrees.md` for isolated workspace
- Apply `domains/shared/skill-tdd.md` for testable behavior
- Update SUMMARY.md as you go
- If multiple unrelated tasks/failures arise, apply `parallel-agents-protocol.md`
- If a bug appears, apply `domains/shared/skill-debugging.md`

**During VERIFY:**
- Apply `verification-protocol.md` — quote test output, don't claim success without evidence
- Run `domains/shared/skill-self-review.md` for major changes
- Confirm decision coverage end-to-end
- Write VERIFICATION.md

### 3. Phase completion

After VERIFY passes:
1. Update `.lattice-plan.md` phase status to Done
2. Apply `domains/webdev/skill-finishing-branch.md` to handle merge / PR / keep / discard
3. Move to next phase

### 4. Project completion

When all phases are Done:
1. Final project-level review
2. Generate or update root-level documentation (README, CONTRIBUTING, ADRs)
3. Hand back to `Lattice.md` for final status check

## Eligible Domain Skills

### Webdev domains (`domains/webdev/`)

| Skill | Activate when |
|---|---|
| `skill-frontend` | Building UI components, pages, or interfaces |
| `skill-backend` | Building server-side logic or services |
| `skill-database` | Designing or implementing database schemas |
| `skill-auth` | Implementing authentication or authorization |
| `skill-api-rest` | Building REST APIs |
| `skill-api-graphql` | Building GraphQL APIs |
| `skill-api-realtime` | Building WebSockets, SSE, or other real-time APIs |
| `skill-devops` | Setting up CI/CD or infrastructure |
| `skill-deployment` | Deploying to production |
| `skill-observability` | Logging, monitoring, metrics, tracing |
| `skill-error-handling` | Error strategy and graceful degradation |
| `skill-validation` | Input validation and schema enforcement |
| `skill-integrations` | Third-party service integration |
| `skill-a11y` | Accessibility compliance |
| `skill-i18n` | Internationalization |
| `skill-code-review` | Reviewing code quality |
| `skill-qa` | Quality assurance processes |
| `skill-git-worktrees` | Isolated workspace setup |
| `skill-finishing-branch` | Completing development work |

### Shared domains (`domains/shared/`)

| Skill | Activate when |
|---|---|
| `skill-tdd` | Implementing any feature or bugfix (always) |
| `skill-testing` | Setting up test infrastructure |
| `skill-debugging` | Encountering bugs or unexpected behavior |
| `skill-self-review` | Before declaring a phase done |
| `skill-receiving-feedback` | When processing review or correction feedback |
| `skill-security` | Always for production systems |
| `skill-docs` | Always for production systems |
| `skill-performance` | Performance-critical systems |
| `skill-reproducibility` | Complex systems with multiple environments |
| `skill-ethics` | User-facing systems with personal data |

## Per-Mode Quality Notes

- **TDD by default.** All testable behavior gets a failing test first. Glue code and visual styling are fair exceptions.
- **Atomic commits.** One commit per task using the convention `{type}({phase}-{task}): description` (e.g., `feat(02-auth-03): add JWT validation`).
- **Worktrees for non-trivial features.** Use `skill-git-worktrees` to isolate from main; `skill-finishing-branch` to integrate.
- **No silent decision changes.** If EXECUTE reveals a CONTEXT decision is wrong, route back to DISCUSS — don't change it inline.
- **Verification before merge.** Apply `verification-protocol.md` before `skill-finishing-branch` — quote the test output.

## Handoff Back to Lattice

When the project (or a substantial milestone) is complete:
1. Update `.lattice-plan.md` with final status
2. Hand back to `Lattice.md` for status check or new-project flow
