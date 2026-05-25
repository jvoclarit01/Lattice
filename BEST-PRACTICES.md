<!-- REVAMPED: original 500-line generic best-practices doc shrunk to a concise
     index. Substance now lives in the protocols and references; this file is
     a thin pointer so users find them quickly. -->
---
name: lattice-best-practices
description: Index of Lattice best practices. Points to the protocols, references, and skills where each practice is enforced.
---

# Lattice Best Practices — Index

Lattice encodes best practices as **protocols and references** rather than a single document. This is the index. Each entry points to where the practice actually lives.

## General Practices

| Practice | Where it lives |
|---|---|
| Be specific in your project description | [questioning-protocol.md](./shared/questioning-protocol.md) |
| Answer questions thoughtfully (no "whatever you think") | [unsure-protocol.md](./shared/unsure-protocol.md) |
| Review `.lattice-plan.md` regularly | [lattice-plan-template.md](./shared/lattice-plan-template.md) |
| Don't skip phases | [dpev-loop-protocol.md](./shared/dpev-loop-protocol.md) |
| Use version control | covered by `skill-finishing-branch` and `skill-git-worktrees` |
| Document decisions in CONTEXT.md per phase | [phase-artifacts-protocol.md](./shared/phase-artifacts-protocol.md) |
| Ask when uncertain | [unsure-protocol.md](./shared/unsure-protocol.md) |
| Resume cleanly across sessions | [resume-protocol.md](./shared/resume-protocol.md) |

## Universal Anti-Patterns

The complete list of universal anti-patterns (32 rules covering context budget, file reading, delegation, behavioral, error recovery, and Lattice-specific concerns) lives in:

[**`shared/references/anti-patterns-reference.md`**](./shared/references/anti-patterns-reference.md)

Examples of what's in there:
- Don't read every domain skill proactively
- Don't re-litigate decisions locked in CONTEXT.md
- Don't `git add .` or `git add -A`
- Don't include sensitive information (API keys, secrets) in any Lattice artifact
- Don't declare a step done without writing its artifact

## Gates and Checkpoints

Every checkpoint in Lattice maps to one of 4 canonical gate types (Pre-flight, Revision, Escalation, Abort). The full taxonomy with selection heuristic and gate matrix lives in:

[**`shared/references/gates-reference.md`**](./shared/references/gates-reference.md)

## Discipline-Enforcing Protocols

Practices that are too important to leave as "guidance":

| Discipline | Protocol |
|---|---|
| Evidence before completion claims | [verification-protocol.md](./shared/verification-protocol.md) |
| Design before implementation | [brainstorming-protocol.md](./shared/brainstorming-protocol.md) |
| Decisions must show up in plans and shipped work | [dpev-loop-protocol.md](./shared/dpev-loop-protocol.md) (decision coverage) |
| Plans must pass quality checks before EXECUTE | [plan-checker-protocol.md](./shared/plan-checker-protocol.md) |
| Tests before code | [domains/shared/skill-tdd.md](./domains/shared/skill-tdd.md) |
| Root cause before fixes | [domains/shared/skill-debugging.md](./domains/shared/skill-debugging.md) |
| No performative agreement on feedback | [domains/shared/skill-receiving-feedback.md](./domains/shared/skill-receiving-feedback.md) |

## Per-Mode Practices

Mode-specific practices are in the mode orchestrators' "Per-Mode Quality Notes" sections:

- project-lattice: [modes/project-lattice.md](./modes/project-lattice.md) — TDD by default, atomic commits, worktrees for non-trivial features
- model-lattice: [modes/model-lattice.md](./modes/model-lattice.md) — reproducibility mandatory, metrics as evidence, document negative results
- thesis-lattice: [modes/thesis-lattice.md](./modes/thesis-lattice.md) — citations non-negotiable, calibrated hedging, abstract written last

## How to Add a New Best Practice

If you find yourself repeating the same advice across multiple phases or projects:

1. **If it's a hard rule with rationalizations:** add a discipline skill or protocol. Apply [skills-crafter](./skills-crafter/SKILL.md) to author it (RED-GREEN-REFACTOR).
2. **If it's a checklist or rule list:** add it to `anti-patterns-reference.md` or a relevant existing reference.
3. **If it's per-mode:** add it to the mode orchestrator's "Per-Mode Quality Notes" section.
4. **If it's a general principle:** add it to this index pointing at where it's enforced.

Avoid adding generic best-practices prose to this file — it duplicates what's already enforced. Best practices live where they get applied.

## The Bottom Line

Lattice enforces best practices through protocols, references, and discipline skills — not through reading a list. To follow them, follow the protocols. To improve them, update the protocols.
