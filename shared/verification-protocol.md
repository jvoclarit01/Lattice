<!-- ADAPTED from C:/Users/janvi/.claude/plugins/marketplaces/superpowers-dev/skills/verification-before-completion/SKILL.md
     Adaptations: dropped frontmatter (this is a shared protocol, not a triggerable skill —
     loaded by other skills), reframed "your human partner" as "the user", kept the
     Iron Law, gate function, common failures table, and red flags verbatim. -->

# The Verification Protocol — Evidence Before Claims

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle:** Evidence before claims, always.

**Violating the letter of this rule is violating the spirit of this rule.**

## When to Apply

Apply this protocol whenever any Lattice skill or protocol is about to claim:
- A test passes
- The build succeeds
- A bug is fixed
- A requirement is met
- A phase is complete (DPEV VERIFY step)
- A plan task is done
- An agent's work succeeded

It is invoked from: `skill-tdd.md` (verify GREEN), `skill-debugging.md` (Phase 4 step 3), `dpev-loop-protocol.md` (VERIFY step), `skill-finishing-branch.md` (Step 1 test verification), and any place where success is about to be asserted.

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this turn, you cannot claim it passes.

## The Gate Function

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: state actual status with evidence
   - If YES: state claim WITH evidence
5. ONLY THEN: make the claim

Skip any step = lying, not verifying
```

## Common Failures

| Claim | Requires | Not Sufficient |
|---|---|---|
| Tests pass | Test command output: 0 failures | Previous run, "should pass", "looks like" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command exit code 0 | Linter passing, logs look good |
| Bug fixed | Test for original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Line-by-line checklist with evidence | Tests passing |
| Phase complete | VERIFICATION.md per success criterion with evidence | SUMMARY.md says "all done" |
| Decision honored | Decision visible in shipped code, tested | Plan said it would be |

## Red Flags — STOP

If you catch yourself doing any of these, STOP and run verification first:

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!")
- About to commit/push/PR without running tests
- Trusting an agent's success report
- Relying on partial verification
- Thinking "just this once"
- Tired and wanting work over
- ANY wording implying success without having run verification

## Rationalization Prevention

| Excuse | Reality |
|---|---|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter ≠ compiler |
| "Agent said success" | Verify independently |
| "I'm tired" | Exhaustion ≠ excuse |
| "Partial check is enough" | Partial proves nothing |
| "Different words so the rule doesn't apply" | Spirit over letter |

## Key Patterns

**Tests:**
```
✅ [Run test command] [See: 34/34 pass] "All tests pass"
❌ "Should pass now" / "Looks correct"
```

**Regression tests (TDD red-green):**
```
✅ Write → Run (pass) → Revert fix → Run (MUST FAIL) → Restore → Run (pass)
❌ "I've written a regression test" (without red-green verification)
```

**Build:**
```
✅ [Run build] [See: exit 0] "Build passes"
❌ "Linter passed" (linter doesn't check compilation)
```

**Requirements (Lattice phase):**
```
✅ Re-read PLAN.md success criteria → write VERIFICATION.md per criterion → quote evidence → report gaps or completion
❌ "Tests pass, phase complete"
```

**Decision coverage (Lattice phase):**
```
✅ For each CONTEXT.md decision: locate it in shipped code, run a test or check, mark verified in VERIFICATION.md
❌ "I implemented all the decisions"
```

**Agent delegation:**
```
✅ Agent reports success → check VCS diff → verify changes → report actual state
❌ Trust agent's report
```

## When To Apply

**ALWAYS before:**
- ANY variation of success/completion claims
- ANY expression of satisfaction
- ANY positive statement about work state
- Committing, PR creation, task completion
- Moving to the next task
- Delegating to agents (verify their output before continuing)
- Marking a TodoWrite task complete
- Marking a phase Done in `.lattice-plan.md`
- Writing a phase's SUMMARY.md "Self-Check: PASSED"

**Rule applies to:**
- Exact phrases ("done", "fixed", "passing")
- Paraphrases and synonyms ("good", "working", "looks right")
- Implications of success ("ready to ship", "moving on")
- ANY communication suggesting completion or correctness

## Why This Matters

Claiming completion without verification:
- Erodes trust ("I don't believe you" is unrecoverable)
- Ships broken work that crashes downstream
- Misses requirements that the user thinks are done
- Wastes time on rework after the false completion is caught
- Violates the basic honesty contract between Claude and the user

## The Bottom Line

**No shortcuts for verification.**

Run the command. Read the output. THEN claim the result.

This is non-negotiable.
