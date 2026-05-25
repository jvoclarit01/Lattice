<!-- ADAPTED from D:/GSD/get-shit-done/references/gates.md.
     Adaptations: replaced GSD workflow names (plan-phase, execute-phase, verify-work)
     with Lattice DPEV step names (DISCUSS, PLAN, EXECUTE, VERIFY), kept the four
     canonical gate types verbatim, kept the selection heuristic. -->

# Gates Reference

Canonical gate types used across Lattice protocols. Every checkpoint maps to one of these four types.

## Gate Types

### Pre-flight Gate

**Purpose:** Validates preconditions before starting an operation.

**Behavior:** Blocks entry if conditions unmet. No partial work created.

**Recovery:** Fix the missing precondition, then retry.

**Examples in Lattice:**
- DPEV PLAN step checks that CONTEXT.md exists before starting research
- DPEV EXECUTE step checks that PLAN.md exists and plan-checker passed
- DPEV VERIFY step checks that SUMMARY.md exists
- Resume protocol checks `.lattice-plan.md` exists before resuming
- skill-finishing-branch checks tests pass before offering merge options

### Revision Gate

**Purpose:** Evaluates output quality and routes to revision if insufficient.

**Behavior:** Loops back to producer with specific feedback. Bounded by an iteration cap.

**Recovery:** Producer addresses feedback; checker re-evaluates. The loop also escalates early if issue count does not decrease between consecutive iterations (stall detection). After max iterations, escalates unconditionally.

**Examples in Lattice:**
- plan-checker-protocol reviewing PLAN.md (max 3 iterations)
- VERIFY step routing gaps back to EXECUTE as a fix list
- skill-avoid-ai-writing's second-pass audit catching surviving AI tells

### Escalation Gate

**Purpose:** Surfaces unresolvable issues to the user for a decision.

**Behavior:** Pauses workflow, presents options, waits for human input.

**Recovery:** User chooses an action; workflow resumes on the selected path.

**Examples in Lattice:**
- plan-checker revision loop exhausted after 3 iterations
- DISCUSS reveals a decision conflicts with an earlier locked decision
- EXECUTE finds that a CONTEXT.md decision can no longer be honored as written
- Unsure Protocol: every "I don't know" is implicitly an escalation that needs the user

### Abort Gate

**Purpose:** Terminates the operation to prevent damage or waste.

**Behavior:** Stops immediately, preserves state, reports reason.

**Recovery:** User investigates root cause, fixes, restarts from a checkpoint.

**Examples in Lattice:**
- Critical error during EXECUTE that corrupts an artifact (`.lattice-plan.md` write failed mid-update)
- Pre-existing tests fail during skill-git-worktrees baseline verification
- Lattice detects mode conflict (active mode in `.lattice-plan.md` doesn't match what user is asking for)

## Gate Matrix

| Step | Phase | Gate Type | Artifacts Checked | Failure Behavior |
|---|---|---|---|---|
| Resume | Entry | Pre-flight | `.lattice-plan.md` | Skip resume, start fresh mode detection |
| DISCUSS | Entry | Pre-flight | Phase row in `.lattice-plan.md` | Block; ask user which phase |
| DISCUSS | Exit | Escalation | CONTEXT.md decisions | Surface conflicts to user |
| PLAN | Entry | Pre-flight | CONTEXT.md | Block; route back to DISCUSS |
| PLAN | Mid | Revision | RESEARCH.md open questions | Loop research or escalate to DISCUSS |
| PLAN | Exit | Revision | PLAN.md (plan-checker) | Loop to planner (max 3) |
| PLAN | Post-revision | Escalation | Unresolved issues after 3 iterations | Surface to user |
| EXECUTE | Entry | Pre-flight | PLAN.md present, plan-checker passed | Block; route back to PLAN |
| EXECUTE | Per-task | Escalation | Decision conflict mid-execute | Surface to user; route back to DISCUSS |
| EXECUTE | Exit | Revision | SUMMARY.md completeness | Re-run incomplete tasks |
| VERIFY | Entry | Pre-flight | SUMMARY.md | Block with missing-summary message |
| VERIFY | Evaluation | Revision | Failed criteria | Route gaps back to EXECUTE |
| VERIFY | Persistent | Escalation | Criteria still failing after re-execute | Surface to user |
| Any step | Critical error | Abort | (operation result) | Stop, preserve state, report |

## Implementing Gates

Use this taxonomy when designing or auditing Lattice protocol checkpoints:

- **Pre-flight gates** belong at step entry points. They are cheap, deterministic checks that prevent wasted work. If you can verify a precondition with a file-existence check or a status read, use a pre-flight gate.

- **Revision gates** belong after a producer step where quality varies. Always pair them with an iteration cap to prevent infinite loops. The cap should reflect the cost of each iteration — expensive operations get fewer retries (max 3 is the Lattice default).

- **Escalation gates** belong wherever automated resolution is impossible or ambiguous. They are the safety valve between revision loops and abort. Present the user with clear options and enough context to decide. The Unsure Protocol is the canonical Lattice escalation pattern.

- **Abort gates** belong at points where continuing would cause damage, waste significant resources, or produce meaningless output. They should preserve state so work can resume after the root cause is fixed.

## Selection Heuristic

```
Is the check happening before any work is produced?
  → Pre-flight gate

Has work been produced that needs quality checking?
  → Revision gate (with iteration cap)

Has the revision loop hit its cap, OR is the issue genuinely ambiguous?
  → Escalation gate

Would continuing cause damage or produce meaningless output?
  → Abort gate
```

## Pairing Gates with Iteration Caps

| Gate Type | Default Cap | When to lower | When to raise |
|---|---|---|---|
| Pre-flight | N/A (one-shot) | — | — |
| Revision | 3 | Expensive operations (re-running long tests) | Cheap iterations on small artifacts |
| Escalation | N/A (one-shot until resolved) | — | — |
| Abort | N/A (immediate) | — | — |

## The Principle

Gates make implicit failure handling explicit. Without a taxonomy, every step invents its own retry/escalate logic and the system becomes inconsistent. With four canonical types, every checkpoint can be classified and reasoned about uniformly.
