<!-- ADAPTED from C:/Users/janvi/.claude/plugins/marketplaces/superpowers-dev/skills/systematic-debugging/SKILL.md
     Adaptations: Lattice frontmatter (description with explicit when-to-use), added
     When to Activate + Trigger phrases, replaced superpowers:test-driven-development
     reference with skill-tdd, replaced superpowers:verification-before-completion with
     verification-protocol, removed external file references (root-cause-tracing.md,
     defense-in-depth.md, condition-based-waiting.md) — those would be separate files
     Lattice does not bundle. Inlined the key idea from each. The four-phase scientific
     method, Iron Law, and architecture-questioning at fix #3+ are preserved verbatim. -->
---
name: skill-debugging
description: Systematic debugging using the scientific method. Use when encountering ANY bug, test failure, build failure, integration issue, performance problem, or unexpected behavior — before proposing any fix. Iron Law: NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST. Catches "guess and check" thrashing, prevents symptom fixes, escalates to architectural questioning after 3 failed fix attempts. Trigger especially when under time pressure, when "just one quick fix" feels obvious, or when previous fixes didn't work.
---

# Skill: Systematic Debugging

## When to Activate

**Always activate for:**
- Test failures (unit, integration, e2e)
- Bugs in production or development
- Unexpected behavior (output mismatch, crash, hang)
- Build failures, compilation errors, dependency issues
- Performance regressions
- Integration issues across services or layers

**Trigger phrases:**
- "this is broken", "doesn't work", "failing test"
- "I'm getting an error", "weird behavior", "intermittent"
- "let me try fixing", "quick fix", "I'll just"
- "can't figure out why", "I'm stuck"

**Use this ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

**Don't skip when:**
- Issue seems simple (simple bugs have root causes too)
- You're in a hurry (rushing guarantees rework)
- The user wants it fixed NOW (systematic is faster than thrashing)

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of debugging.**

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## The Four Phases

You MUST complete each phase before proceeding to the next.

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read error messages carefully**
   - Don't skip past errors or warnings
   - They often contain the exact solution
   - Read stack traces completely
   - Note line numbers, file paths, error codes

2. **Reproduce consistently**
   - Can you trigger it reliably?
   - What are the exact steps?
   - Does it happen every time?
   - If not reproducible → gather more data, don't guess

3. **Check recent changes**
   - What changed that could cause this?
   - `git diff`, recent commits
   - New dependencies, config changes
   - Environmental differences

4. **Gather evidence in multi-component systems**

   **WHEN system has multiple components (CI → build → deploy, API → service → database):**

   **BEFORE proposing fixes, add diagnostic instrumentation:**

   ```
   For EACH component boundary:
     - Log what data enters component
     - Log what data exits component
     - Verify environment/config propagation
     - Check state at each layer

   Run once to gather evidence showing WHERE it breaks
   THEN analyze evidence to identify failing component
   THEN investigate that specific component
   ```

   **Example (multi-layer system):**

   ```bash
   # Layer 1: Request entry
   echo "=== Headers received: ==="; printenv | grep ^HTTP_
   # Layer 2: Auth middleware
   echo "=== Token decoded: ==="; echo "$DECODED_JWT" | jq .
   # Layer 3: Service handler
   echo "=== Service input: ==="; cat /tmp/service-in.json
   # Layer 4: DB query
   echo "=== DB result: ==="; psql -c "SELECT count(*) FROM ..."
   ```

   **This reveals:** Which layer fails (request → auth ✓, auth → service ✗).

5. **Trace data flow**

   **WHEN error is deep in call stack:**

   - Where does the bad value originate?
   - What called this with the bad value?
   - Keep tracing up until you find the source
   - Fix at source, not at symptom

   This is **backward tracing**: start from the symptom and walk up the call stack until you find the moment the bad value first existed. Fix there.

### Phase 2: Pattern Analysis

**Find the pattern before fixing:**

1. **Find working examples**
   - Locate similar working code in the same codebase
   - What works that's similar to what's broken?

2. **Compare against references**
   - If implementing a known pattern, read the reference implementation COMPLETELY
   - Don't skim — read every line
   - Understand the pattern fully before applying

3. **Identify differences**
   - What's different between working and broken?
   - List every difference, however small
   - Don't assume "that can't matter"

4. **Understand dependencies**
   - What other components does this need?
   - What settings, config, environment?
   - What assumptions does it make?

### Phase 3: Hypothesis and Testing

**Scientific method:**

1. **Form a single hypothesis**
   - State clearly: "I think X is the root cause because Y"
   - Write it down
   - Be specific, not vague

2. **Test minimally**
   - Make the SMALLEST possible change to test the hypothesis
   - One variable at a time
   - Don't fix multiple things at once

3. **Verify before continuing**
   - Did it work? Yes → Phase 4
   - Didn't work? Form NEW hypothesis
   - DON'T add more fixes on top

4. **When you don't know**
   - Say "I don't understand X"
   - Don't pretend to know
   - Ask the user for help
   - Research more

### Phase 4: Implementation

**Fix the root cause, not the symptom:**

1. **Create a failing test case**
   - Simplest possible reproduction
   - Automated test if possible
   - One-off test script if no framework
   - MUST exist before fixing
   - Use `skill-tdd.md` for writing the failing test

2. **Implement a single fix**
   - Address the root cause identified
   - ONE change at a time
   - No "while I'm here" improvements
   - No bundled refactoring

3. **Verify the fix**
   - Test passes now?
   - No other tests broken?
   - Issue actually resolved?
   - Apply `verification-protocol.md` — run the verification command and quote the output before claiming it works

4. **If the fix doesn't work**
   - STOP
   - Count: how many fixes have you tried?
   - If < 3: return to Phase 1, re-analyze with new information
   - **If ≥ 3: STOP and question the architecture (step 5 below)**
   - DON'T attempt fix #4 without architectural discussion

5. **If 3+ fixes failed: question the architecture**

   **Pattern indicating an architectural problem:**
   - Each fix reveals new shared state / coupling / problem in a different place
   - Fixes require "massive refactoring" to implement
   - Each fix creates new symptoms elsewhere

   **STOP and question fundamentals:**
   - Is this pattern fundamentally sound?
   - Are we sticking with it through inertia?
   - Should we refactor architecture vs. continue fixing symptoms?

   **Discuss with the user before attempting more fixes.**

   This is NOT a failed hypothesis — this is wrong architecture.

## Red Flags — STOP and Follow Process

If you catch yourself thinking:

- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems: [lists fixes without investigation]"
- "One more fix attempt" (when already tried 2+)
- Each fix reveals a new problem in a different place

**ALL of these mean: STOP. Return to Phase 1.**

If 3+ fixes failed: question the architecture (see Phase 4.5).

## User Signals You're Doing It Wrong

**Watch for these redirections from the user:**
- "Is that not happening?" — you assumed without verifying
- "Will it show us...?" — you should have added evidence gathering
- "Stop guessing" — you're proposing fixes without understanding
- "Ultrathink this" — question fundamentals, not just symptoms
- "We're stuck?" (frustrated) — your approach isn't working

**When you see these:** STOP. Return to Phase 1.

## Common Rationalizations

| Excuse | Reality |
|---|---|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I'll write the test after confirming the fix works" | Untested fixes don't stick. Test first proves it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "Reference too long, I'll adapt the pattern" | Partial understanding guarantees bugs. Read it completely. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question pattern, don't fix again. |

## Quick Reference

| Phase | Key Activities | Success Criteria |
|---|---|---|
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence, trace data flow | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare, identify differences | Know the differences |
| **3. Hypothesis** | Form theory, test minimally, verify | Confirmed or new hypothesis |
| **4. Implementation** | Failing test, single fix, verify with `verification-protocol` | Bug resolved, tests pass |

## When Process Reveals "No Root Cause"

If systematic investigation reveals the issue is truly environmental, timing-dependent, or external:

1. You've completed the process
2. Document what you investigated in `.lattice-plan.md` or the active phase's SUMMARY.md
3. Implement appropriate handling (retry with backoff, timeout with fallback, error message with diagnostic info)
4. Add monitoring/logging for future investigation

**But:** 95% of "no root cause" cases are incomplete investigation.

## Real-World Impact

From debugging sessions across many projects:
- Systematic approach: 15–30 minutes to fix
- Random fixes approach: 2–3 hours of thrashing
- First-time fix rate: 95% vs 40%
- New bugs introduced: near zero vs common

## Integration with Other Skills

- **domains/shared/skill-tdd.md** — Phase 4 step 1 uses TDD to write the failing test for the bug
- **shared/verification-protocol.md** — Phase 4 step 3 uses verification-protocol to confirm the fix actually works
- **shared/parallel-agents-protocol.md** — when there are 3+ unrelated bugs, dispatch parallel agents instead of investigating sequentially
- **shared/dpev-loop-protocol.md** — debugging often happens during EXECUTE; document findings in SUMMARY.md and verify in VERIFICATION.md
- **shared/references/anti-patterns-reference.md** — anti-patterns 12-15 (questioning anti-patterns) apply when investigating bugs
