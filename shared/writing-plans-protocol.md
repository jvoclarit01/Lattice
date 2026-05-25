<!-- ADAPTED from C:/Users/janvi/.claude/plugins/marketplaces/superpowers-dev/skills/writing-plans/SKILL.md
     Adaptations: dropped frontmatter (this is a shared protocol referenced by
     phase-artifacts-protocol and dpev-loop-protocol), replaced
     docs/superpowers/plans/ path with .lattice/phases/NN-name/PLAN.md, removed
     mandatory subagent-driven-development reference at top of plans (Lattice offers
     this as optional via parallel-agents-protocol), added Lattice-mode adaptation
     section. The bite-sized task structure, no-placeholders rule, and self-review
     section are preserved verbatim. -->

# The Writing-Plans Protocol — How to Write a PLAN.md

How to actually author the PLAN.md file that `phase-artifacts-protocol.md` says belongs in each phase folder. The phase-artifacts protocol says WHAT goes in PLAN.md; this protocol says HOW to write each task so an executor can follow it without guessing.

## When to Apply

Apply this protocol every time you write a `PLAN.md` for a phase, whether the phase is project-lattice, model-lattice, or thesis-lattice. It governs the structure and granularity of tasks inside PLAN.md.

The output target: `.lattice/phases/NN-name/PLAN.md` (per phase-artifacts-protocol).

## Core Principle

Write the plan assuming the executor has zero context for the codebase and questionable taste. Document everything they need: which files to touch, the actual code, tests, what to check. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume the executor is a skilled developer but knows almost nothing about the toolset or the problem domain. Assume they don't know good test design very well.

## Scope Check

If the phase covers multiple independent subsystems, it should have been broken into separate phases during DISCUSS. If it wasn't, route back to DISCUSS — suggest splitting into separate phases, one per subsystem. Each phase should produce working, testable deliverables on its own.

## File Structure Section (write this first)

Before defining tasks, list which files will be created or modified and what each one is responsible for. This is where decomposition decisions get locked in.

- Design units with clear boundaries and well-defined interfaces. Each file should have one clear responsibility.
- Files that change together should live together. Split by responsibility, not by technical layer.
- In existing codebases, follow established patterns. If the codebase uses large files, don't unilaterally restructure — but if a file you're modifying has grown unwieldy, including a split in the plan is reasonable.

This structure informs the task decomposition. Each task should produce self-contained changes that make sense independently.

## Bite-Sized Task Granularity

**Each step is one action (2–5 minutes):**
- "Write the failing test" — step
- "Run it to make sure it fails" — step
- "Implement the minimal code to make the test pass" — step
- "Run the tests and make sure they pass" — step
- "Commit" — step

## Plan Document Header

Every PLAN.md MUST start with this header:

```markdown
---
phase: NN-name
type: plan
created: YYYY-MM-DD
---

# [Phase Name] — Implementation Plan

**Goal:** [One sentence describing what this phase delivers]

**Architecture:** [2-3 sentences about the approach]

**Key files:** [Top-level file paths or modules touched]

---
```

## Task Structure

Use this template for every task. Steps use checkbox `- [ ]` syntax for tracking.

````markdown
### Task N: [Component name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test_file.py`

- [ ] **Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/path/test_file.py::test_specific_behavior -v`
Expected: FAIL with "function not defined"

- [ ] **Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/path/test_file.py::test_specific_behavior -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/path/test_file.py src/path/file.py
git commit -m "feat(NN-N): add specific behavior"
```
````

## Decision Coverage Section (mandatory)

After all tasks, add a decision-coverage checklist mapping each CONTEXT.md decision to one or more tasks. From `dpev-loop-protocol.md`:

```markdown
## Decision coverage

- [x] D1 (PostgreSQL with row-level security) → Task 03
- [x] D2 (JWT auth on all routes except /health) → Task 05, Task 06
- [x] D3 (Rate limit 100 req/min) → Task 07
```

Every line in CONTEXT.md `## Decisions locked` must appear here, mapped to at least one task.

## No Placeholders

Every step must contain the actual content an executor needs. These are **plan failures** — never write them:

- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Write tests for the above" (without actual test code)
- "Similar to Task N" (repeat the code — the executor may be reading tasks out of order)
- Steps that describe what to do without showing how (code blocks required for code steps)
- References to types, functions, or methods not defined in any task

If you find yourself writing a placeholder, stop and write the actual content. If you can't write the actual content, you don't have enough information — route back to RESEARCH or DISCUSS.

## Lattice-Mode Adaptation

### project-lattice — code

Tasks describe code changes. Steps include test code, implementation code, and verify/commit commands. Use TDD steps (write failing test → make it pass) per `skill-tdd.md`.

### model-lattice — experiments and pipelines

Tasks describe data preprocessing steps, training runs, evaluation passes. Steps include the actual command to run (`python train.py --config conf.yaml`), the expected output (loss curve, metric value, file produced), and the verification (`pytest`, manual inspection of plots, comparison to baseline).

For training runs that take hours, the verification step is "training started, monitor with `tensorboard --logdir runs/`" — don't claim done until the run completes and the metric is checked.

### thesis-lattice — chapters and sections

Tasks describe writing or revision passes on specific sections. "Files" lists chapter/section files to create or modify. Steps include the actual prose outline, citations to insert, figures to reference, and the verification ("read aloud, check argument flows" or "run skill-avoid-ai-writing on the section").

For thesis work, "commit" is just the git commit; for shared overleaf or non-git workflows, replace with "save and snapshot."

## Verification Section

After all tasks, define how to verify the whole phase is done:

```markdown
## Verification

- All tasks complete (every checkbox checked)
- Test suite passes: `<test command>`
- Decision coverage verified (see Decision coverage section)
- No regressions in adjacent code: `<broader test command>`
```

## Success Criteria

Define measurable outcomes that signal phase completion:

```markdown
## Success criteria

- [ ] All tests pass (X/X)
- [ ] Feature accessible at `<endpoint or location>`
- [ ] Documented in `<location>`
- [ ] All locked decisions verified in shipped code
```

These are what `dpev-loop-protocol.md` VERIFY step checks against.

## Self-Review

After writing the complete plan, look at the spec/CONTEXT.md with fresh eyes and check the plan against it. This is a checklist you run yourself.

1. **Decision coverage:** Every decision in CONTEXT.md `## Decisions locked` mapped to a task? List any gaps.

2. **Placeholder scan:** Search your plan for red flags — any pattern from the "No placeholders" section above. Fix them.

3. **Type consistency:** Do the types, method signatures, and property names you used in later tasks match what you defined in earlier tasks? A function called `clearLayers()` in Task 3 but `clearFullLayers()` in Task 7 is a bug.

4. **Scope check:** Is this still focused enough for one phase, or did the task list grow to suggest decomposition? > 15 tasks is a smell.

If you find issues, fix them inline. No need to re-review — just fix and move on. If you find a decision with no task, add the task. Then run plan-checker-protocol.md before declaring PLAN.md ready.

## Remember

- Exact file paths always
- Complete code in every step — if a step changes code, show the code
- Exact commands with expected output
- DRY, YAGNI, TDD, frequent commits
- Decision coverage is mandatory, not optional
- No placeholders, no "TBD", no "similar to above"
- Atomic commits with `{type}({phase}-{task}): description` convention

## The Principle

A good PLAN.md eliminates guesswork. The executor doesn't have to interpret intent, search the codebase for the right pattern, or invent edge cases — the plan tells them. The work that goes into writing this much detail is offset many times over by avoiding rework when an executor's interpretation diverges from the user's intent.
