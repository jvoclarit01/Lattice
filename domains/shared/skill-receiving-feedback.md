<!-- ADAPTED from C:/Users/janvi/.claude/plugins/marketplaces/superpowers-dev/skills/receiving-code-review/SKILL.md
     Adaptations: Lattice frontmatter, added When to Activate + Trigger phrases blocks,
     reframed "your human partner" as "the user" and "External Reviewers" as "subagent
     reviewers", broadened scope from code review feedback to all Lattice feedback
     (review subagents, user corrections, plan-checker output, verification gaps),
     added Integration section. The forbidden responses, response pattern, push-back
     guidelines, and acknowledgment rules are preserved. -->
---
name: skill-receiving-feedback
description: How to handle feedback rigorously, without performative agreement or blind implementation. Use when receiving feedback from any source — review subagents, the user, plan-checker output, verification gaps, or any input that suggests changes. Requires technical verification before implementing, clarification when unclear, and reasoned pushback when the feedback is wrong. Forbids "You're absolutely right!" and similar empty agreement. Trigger whenever feedback arrives and the next move is to act on it.
---

# Skill: Receiving Feedback

## When to Activate

**Always activate when receiving:**
- Feedback from a self-review subagent (`skill-self-review.md`)
- Plan-checker output (issues found in PLAN.md)
- VERIFICATION.md gaps from the VERIFY step
- The user's correction during DISCUSS, EXECUTE, or any conversation
- A code-review subagent's report
- Any input that suggests "you should change X"

**Trigger phrases (yours, that signal you're about to violate this skill):**
- "You're absolutely right!"
- "Great point!" / "Excellent feedback!"
- "Let me implement that now" (before verification)
- "Thanks for catching that!"

If you catch yourself about to write any of these, **STOP** and apply this skill.

## Overview

Feedback requires technical evaluation, not emotional performance.

**Core principle:** Verify before implementing. Ask before assuming. Technical correctness over social comfort.

## The Response Pattern

```
WHEN receiving feedback:

1. READ: complete feedback without reacting
2. UNDERSTAND: restate the requirement in your own words (or ask)
3. VERIFY: check against codebase / artifact reality
4. EVALUATE: technically sound for THIS codebase / phase / context?
5. RESPOND: technical acknowledgment or reasoned pushback
6. IMPLEMENT: one item at a time, verify each
```

## Forbidden Responses

**NEVER:**
- "You're absolutely right!"
- "Great point!" / "Excellent feedback!"
- "Thanks for catching that!"
- "Let me implement that now" (before verification)
- ANY gratitude expression to the feedback itself

**INSTEAD:**
- Restate the technical requirement
- Ask clarifying questions
- Push back with technical reasoning if wrong
- Just start working — actions speak louder than words

If you catch yourself about to write "Thanks": delete it. State the fix instead.

## Handling Unclear Feedback

```
IF any item is unclear:
  STOP — do not implement anything yet
  ASK for clarification on the unclear items

WHY: items may be related. Partial understanding = wrong implementation.
```

**Example:**

> User: "Fix items 1-6"
> You understand 1, 2, 3, 6. Unclear on 4, 5.
>
> ❌ WRONG: implement 1, 2, 3, 6 now, ask about 4, 5 later
> ✅ RIGHT: "I understand items 1, 2, 3, 6. Need clarification on 4 and 5 before proceeding."

## Source-Specific Handling

### From the user

- **Trusted** — implement after understanding
- **Still ask** if scope unclear
- **No performative agreement**
- **Skip to action** or technical acknowledgment

### From a review subagent

```
BEFORE implementing:
  1. Check: technically correct for THIS codebase?
  2. Check: breaks existing functionality?
  3. Check: was there a reason for the current implementation?
  4. Check: does the reviewer have full context?

IF the suggestion seems wrong:
  Push back with technical reasoning

IF you can't easily verify:
  Say so: "I can't verify this without [X]. Should I [investigate / ask / proceed]?"

IF it conflicts with the user's prior locked decisions:
  STOP and discuss with the user first
```

**Rule:** subagent feedback is evaluated, not obeyed. The reviewer doesn't have your full context — they could be wrong.

### From plan-checker

The plan-checker only flags concrete issues (missing decision coverage, vague tasks, structural gaps). Treat its output as authoritative for those specific issues — fix them. If the planner can't fix them after 3 iterations, escalate to the user (per `plan-checker-protocol.md`).

### From VERIFICATION.md gaps

Treat VERIFY-step gaps as the same severity as the criterion's importance:
- Failed criterion → must fix before declaring phase done
- Partial criterion with deferral note → user has accepted the partial
- Decision-coverage gap → must fix; missing decisions are not optional

## YAGNI Check for "Make It Proper" Feedback

```
IF the feedback suggests "implementing properly" / "making it production-ready":
  Search the codebase for actual usage

  IF unused: "This isn't called from anywhere. Remove it (YAGNI)?"
  IF used:   Then implement properly
```

Don't add features the codebase doesn't use just because a reviewer suggests it would be nice. Lattice preference: minimum viable scope first, expand on demand.

## Implementation Order

```
FOR multi-item feedback:
  1. Clarify anything unclear FIRST
  2. Implement in this order:
     - Blocking issues (breaks, security, data loss)
     - Simple fixes (typos, imports, name corrections)
     - Complex fixes (refactoring, logic changes)
  3. Verify each fix individually (apply verification-protocol.md)
  4. Verify no regressions
```

Don't batch the implementation. One fix → verify → next fix. Otherwise you can't tell which fix introduced a regression if one appears.

## When To Push Back

Push back when:

- Suggestion breaks existing functionality
- Reviewer lacks full context (didn't see CONTEXT.md or earlier phases)
- Violates YAGNI (suggesting an unused feature be expanded)
- Technically incorrect for this stack / language / framework
- Legacy or compatibility reasons exist
- Conflicts with the user's locked architectural decisions in CONTEXT.md or `.lattice-plan.md`

**How to push back:**

- Use technical reasoning, not defensiveness
- Ask specific questions
- Reference working tests, code, or docs
- Involve the user if the issue is architectural

## Acknowledging Correct Feedback

When the feedback IS correct:

```
✅ "Fixed. [Brief description of what changed]"
✅ "Good catch — [specific issue]. Fixed in [location]."
✅ [Just fix it and show in the code]

❌ "You're absolutely right!"
❌ "Great point!"
❌ "Thanks for catching that!"
❌ "Thanks for [anything]"
❌ ANY gratitude expression
```

**Why no thanks:** actions speak. Just fix it. The code itself shows you heard the feedback.

## Gracefully Correcting Your Pushback

If you pushed back and turned out to be wrong:

```
✅ "You were right — I checked [X] and it does [Y]. Implementing now."
✅ "Verified this and you're correct. My initial understanding was wrong because [reason]. Fixing."

❌ Long apology
❌ Defending why you pushed back
❌ Over-explaining
```

State the correction factually and move on.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Performative agreement | State the requirement or just act |
| Blind implementation | Verify against codebase first |
| Batch without testing | One at a time, verify each |
| Assuming reviewer is right | Check if it breaks things |
| Avoiding pushback | Technical correctness > comfort |
| Partial implementation when unclear | Clarify ALL items first |
| Can't verify, proceed anyway | State the limitation, ask for direction |

## Real Examples

**Performative agreement (bad):**

> Reviewer: "Remove legacy code"
> ❌ "You're absolutely right! Let me remove that..."

**Technical verification (good):**

> Reviewer: "Remove legacy code"
> ✅ "Checking... build target is iOS 10.15+, this API needs iOS 13+. Need legacy for backward compat. Current impl has wrong bundle ID — fix it or drop pre-13 support?"

**YAGNI (good):**

> Reviewer: "Implement proper metrics tracking with database, date filters, CSV export"
> ✅ "Grepped codebase — nothing calls this endpoint. Remove it (YAGNI)? Or is there usage I'm missing?"

**Unclear item (good):**

> User: "Fix items 1-6"
> You understand 1, 2, 3, 6. Unclear on 4, 5.
> ✅ "Understand 1, 2, 3, 6. Need clarification on 4 and 5 before implementing."

## The Bottom Line

**External feedback = suggestions to evaluate, not orders to follow.**

Verify. Question. Then implement.

No performative agreement. Technical rigor always.

## Integration with Other Skills

- **domains/shared/skill-self-review.md** — paired skill: how to dispatch the reviewer that produces feedback this skill processes
- **shared/verification-protocol.md** — applied after each fix to confirm it works
- **shared/unsure-protocol.md** — applied when feedback is genuinely ambiguous; escalate with 2 options to the user
- **shared/plan-checker-protocol.md** — its output is authoritative; this skill governs how to act on it
- **shared/dpev-loop-protocol.md** — VERIFY-step gaps feed into this skill; user corrections during DISCUSS feed into this skill
