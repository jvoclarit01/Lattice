<!-- ADAPTED from C:/Users/janvi/.claude/plugins/marketplaces/superpowers-dev/skills/requesting-code-review/SKILL.md
     Adaptations: Lattice frontmatter, added When to Activate + Trigger phrases blocks,
     replaced superpowers:code-reviewer subagent dependency with a simpler "fresh-context
     subagent with explicit prompt" pattern that works without bundled prompt templates,
     added Lattice-mode adaptation, added Integration section. The when-to-request,
     git-SHA pattern, feedback-handling rules, and red flags are preserved. -->
---
name: skill-self-review
description: Solo-developer self-review pattern. Dispatch a fresh-context subagent to review your own work before declaring it done or merging. Use when completing a task in subagent-driven development, after implementing a major feature, before merging to main, or whenever a fresh perspective would help. Catches issues your own context can no longer see. Particularly valuable for solo devs who have no team review. Trigger when work feels complete and the next step is "ship it" or "move on."
---

# Skill: Self-Review (Solo-Dev Code Review Pattern)

## When to Activate

**Mandatory:**
- After each task in subagent-driven or DPEV-loop execution
- After completing a major feature
- Before merging to main / before `skill-finishing-branch`
- Before declaring a phase Done in `.lattice-plan.md`

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing a complex bug
- After applying a sequence of fixes that touched many files

**Trigger phrases:**
- "ready to merge", "ready to ship", "I think it's done"
- "let me review this", "code review", "self-review"
- "I'm not sure if this is right"
- "any issues with this?"

## Overview

Solo developers don't have a team to review their work. Self-review via a fresh-context subagent is the substitute: it catches issues your own context can no longer see — patterns you internalized halfway through writing, edge cases you stopped considering, dead code you didn't notice.

**Core principle:** Review early, review often. The subagent gets precisely-crafted context for evaluation — never your session's history. This keeps the reviewer focused on the work product, not your thought process.

## How to Request a Review

### 1. Get the git SHAs

Define the change range you want reviewed:

```bash
# If you're reviewing the latest commit
BASE_SHA=$(git rev-parse HEAD~1)
HEAD_SHA=$(git rev-parse HEAD)

# If you're reviewing the entire current branch vs main
BASE_SHA=$(git merge-base HEAD main)
HEAD_SHA=$(git rev-parse HEAD)

# If you want to review uncommitted changes too
HEAD_SHA="working-tree"
```

### 2. Dispatch a fresh-context subagent

Use the Task tool with a focused prompt. The subagent does NOT inherit your session — give it everything it needs:

```markdown
You are reviewing code changes for quality, correctness, and adherence to spec.

**What was implemented:**
[Brief summary, e.g., "Verification and repair functions for the conversation index"]

**Spec / requirements:**
[Paste relevant parts of CONTEXT.md, PLAN.md, or the task description]

**Change range:**
- BASE_SHA: <base sha>
- HEAD_SHA: <head sha>
- Diff: run `git diff <base>..<head>` (you have Bash access)

**Your task:**
1. Read the diff
2. Read the spec and verify the code matches it
3. Look for:
   - Critical issues: bugs, security holes, data loss
   - Important issues: spec violations, missing test coverage, broken patterns
   - Minor issues: naming, comments, small cleanups
4. Apply the Lattice anti-patterns reference (shared/references/anti-patterns-reference.md) — flag any violations
5. Push back if anything is wrong; quote specific lines

**Output format:**

## Strengths
[What was done well]

## Issues

### Critical
[Issues that block ship]

### Important
[Issues to fix before proceeding]

### Minor
[Optional cleanups]

## Spec compliance
[Does the code match every locked decision in CONTEXT.md? List any gaps]

## Recommendation
[READY / NEEDS FIXES / BLOCKED]
```

### 3. Act on the feedback

- **Critical issues:** fix immediately, do not proceed
- **Important issues:** fix before declaring done
- **Minor issues:** note in SUMMARY.md for follow-up
- **Push back if reviewer is wrong:** use `skill-receiving-feedback.md` discipline — verify against codebase, then push back with technical reasoning
- **Re-review** after fixing critical/important issues — the loop closes when the reviewer returns READY

## Per-Mode Adaptation

### project-lattice — code review

The standard case. Reviewer reads diff, checks spec compliance, looks for bugs/security/coverage gaps. Output drives fixes before merge.

### model-lattice — experiment / pipeline review

Reviewer reads:
- The training script or pipeline diff
- The metrics/loss curves (if reproducible)
- The eval results vs baseline
- The hyperparameter changes

Looks for: data leakage, incorrect metric computation, train/test contamination, hidden hyperparameter dependencies, broken reproducibility.

### thesis-lattice — chapter / section review

Reviewer reads:
- The chapter or section diff
- The argument flow
- Citations
- The figures and tables

Looks for: argument gaps, missing citations, contradictions with earlier chapters, AI-isms (run `skill-avoid-ai-writing` mentally or as a follow-up), unsupported claims.

## Common Mistakes

| Mistake | Fix |
|---|---|
| ❌ "Trust me, it's fine" — skip review | ✅ Solo devs especially need self-review; no one else is checking |
| ❌ Argue with valid feedback | ✅ Verify against the codebase first; push back only with evidence |
| ❌ Skip review because "it's simple" | ✅ Simple changes have bugs too. Review takes 1 minute. |
| ❌ Ignore Critical issues | ✅ Fix before proceeding, no exceptions |
| ❌ Reviewer reads your session history | ✅ Fresh-context subagent — paste only what they need |
| ❌ Vague review prompt: "review this" | ✅ Specific prompt with spec, range, and expected output format |

## Red Flags

**Never:**
- Skip review because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Important issues
- Argue with valid technical feedback without verification
- Mark a phase Done before review passes

**If reviewer is wrong:**
- Apply `skill-receiving-feedback.md`
- Push back with technical reasoning
- Show code or tests that prove it works
- Request clarification

## Integration with Other Skills

- **domains/shared/skill-receiving-feedback.md** — paired skill: how to handle feedback the reviewer returns (no performative agreement, verify before implementing)
- **shared/parallel-agents-protocol.md** — for large changes, dispatch multiple reviewers in parallel each scoped to one subsystem
- **shared/verification-protocol.md** — applied before declaring fixes from review actually work
- **shared/dpev-loop-protocol.md** — review fits into the VERIFY step or as a sub-step within EXECUTE between tasks
- **domains/webdev/skill-finishing-branch.md** — invoked AFTER self-review passes; review is the gate before "ready to merge"
