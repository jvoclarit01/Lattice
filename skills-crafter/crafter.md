<!-- ENRICHED with C:/Users/janvi/.claude/plugins/marketplaces/superpowers-dev/skills/writing-skills/SKILL.md
     Adaptations: absorbed TDD-for-docs methodology (RED-GREEN-REFACTOR for skills),
     CSO description rules, token efficiency targets, rationalization tracking,
     bulletproofing patterns, skill type taxonomy. The original five-dimension
     evaluation, eight-phase workflow, and behavior rules are preserved. Marked
     enriched sections with "NEW" comments to make the audit clear. -->
---
name: skills-crafter
description: Create, evaluate, test, and bulletproof AI skills using TDD-for-documentation methodology. Use whenever the user wants to write a new skill, turn documentation/GitHub repos/PDFs into skills, adapt community skills, evaluate or improve existing skills, or audit a skill for quality. Applies the Iron Law NO SKILL WITHOUT A FAILING TEST FIRST — every skill is built RED-GREEN-REFACTOR style with baseline pressure scenarios, rationalization tracking, and loophole closing. Also covers description-as-trigger-only authoring (CSO), token efficiency budgets, and bulletproofing against pressure.
---

# Skills Crafter

Create AI skills with TDD-for-documentation methodology. Combines the strengths of skill-creator (process-oriented), skill-seekers (reference-oriented), and writing-skills (TDD discipline) — with built-in quality evaluation for all sourced skills.

## The Iron Law

```
NO SKILL WITHOUT A FAILING TEST FIRST
```

Wrote a skill before testing the baseline behavior? Delete it. Start over.

This applies to NEW skills AND EDITS to existing skills.

**No exceptions:**
- Not for "simple additions"
- Not for "just adding a section"
- Not for "documentation updates"
- Don't keep untested changes as "reference"
- Delete means delete

**Violating the letter of this rule is violating the spirit of this rule.**

## Core Principle

Writing skills IS test-driven development applied to process documentation.

You write test cases (pressure scenarios with subagents), watch them fail (baseline behavior without the skill), write the skill (documentation), watch tests pass (agents comply), and refactor (close loopholes).

If you didn't watch an agent fail without the skill, you don't know if the skill teaches the right thing.

## When to Use This Skill

- Create a skill from documentation, a GitHub repo, a PDF, or another existing skill
- Adapt a community skill for Lattice (always evaluate first)
- Improve an existing skill with testing and iteration
- Optimize a skill's description for triggering accuracy
- Audit an existing skill against the quality dimensions
- Package and install skills

## TDD Mapping for Skills

| TDD Concept | Skill Authoring |
|---|---|
| **Test case** | Pressure scenario with subagent |
| **Production code** | Skill document (SKILL.md) |
| **Test fails (RED)** | Agent violates rule without skill (baseline) |
| **Test passes (GREEN)** | Agent complies with skill present |
| **Refactor** | Close loopholes while maintaining compliance |
| **Write test first** | Run baseline scenario BEFORE writing skill |
| **Watch it fail** | Document exact rationalizations agent uses |
| **Minimal code** | Write skill addressing those specific violations |
| **Watch it pass** | Verify agent now complies |
| **Refactor cycle** | Find new rationalizations → plug → re-verify |

The entire skill creation process follows RED-GREEN-REFACTOR.

## Skill Type Taxonomy

Different skill types need different testing approaches.

### Discipline-enforcing skills

Examples in Lattice: `verification-protocol`, `skill-tdd`, `brainstorming-protocol`, `skill-receiving-feedback`.

**Test with:**
- Academic questions: do agents understand the rules?
- Pressure scenarios: do they comply under stress?
- Multiple pressures combined: time + sunk cost + exhaustion + authority
- Identify rationalizations and add explicit counters

**Success criteria:** agent follows the rule under maximum pressure.

### Technique skills

Examples in Lattice: `skill-debugging`, `skill-self-review`, `skill-finishing-branch`.

**Test with:**
- Application scenarios: can agents apply the technique correctly?
- Variation scenarios: do they handle edge cases?
- Missing-information tests: do instructions have gaps?

**Success criteria:** agent successfully applies technique to a new scenario.

### Pattern skills

Examples in Lattice: `phase-artifacts-protocol`, `dpev-loop-protocol`.

**Test with:**
- Recognition scenarios: do they recognize when the pattern applies?
- Application scenarios: can they use the mental model?
- Counter-examples: do they know when NOT to apply?

**Success criteria:** agent correctly identifies when and how to apply the pattern.

### Reference skills

Examples in Lattice: `gates-reference`, `anti-patterns-reference`.

**Test with:**
- Retrieval scenarios: can agents find the right information?
- Application scenarios: can they use what they found correctly?
- Gap testing: are common use cases covered?

**Success criteria:** agent finds and correctly applies reference information.

## Core Workflow

### Phase 1: Source & Requirements

1. **Understand the goal:** what should this skill enable Claude to do?
2. **Determine the type:** discipline / technique / pattern / reference (drives testing approach)
3. **Determine the source:** new from scratch / from documentation / from a repo / from a PDF / from an existing skill
4. **Gather requirements:**
   - Skill name (lowercase, hyphens, no reserved words)
   - Brief description (when-to-use, third person)
   - Output location (default: `~/.claude/skills/Lattice/`)
   - Success criteria

### Phase 2: Skill Evaluation (for sourced skills)

**ALWAYS evaluate sourced skills before copying or adapting.**

1. **Read the source** — fetch URL, read file, or use pasted content
2. **Score across 5 dimensions** (1–5 each):
   - **Clarity** — is the trigger condition clearly defined?
   - **Completeness** — does it cover the full workflow including edge cases?
   - **Actionability** — concrete and specific, not vague?
   - **Structure** — well organized, consistent, appropriately concise?
   - **Integration** — fits the existing Lattice ecosystem without conflict?
3. **Verdict:** PASS (18+), NEEDS WORK (12–17), REJECT (<12)
4. **Handle:**
   - **PASS:** produce adapted version, mark every change with `<!-- ADAPTED: reason -->`, ask user where to save
   - **NEEDS WORK:** show report, ask "improve anyway or find a better source?"
   - **REJECT:** show report, suggest what to look for in a replacement, do not adapt

### Phase 3: Baseline Testing (RED — Watch It Fail)

**This is the test-first step. You cannot skip it.**

For NEW skills (no source):
1. Construct 2-3 pressure scenarios that the skill should govern
2. Dispatch subagents WITHOUT the skill loaded
3. Document exact behavior verbatim:
   - What choices did they make?
   - What rationalizations did they use?
   - Which pressures triggered violations?
4. Save the baseline transcript

For ADAPTED skills (from a source):
1. The source IS the GREEN-phase artifact — but you still need RED to know what changes
2. Construct scenarios that test the source's rules
3. Run baseline WITHOUT the skill — confirm agents fail without it
4. This proves the skill is needed; if agents pass without it, the skill might be unnecessary

For IMPROVED skills (editing existing):
1. Identify what triggered the improvement (a real failure observed in use)
2. Reproduce the failure scenario as a baseline
3. The current skill is the baseline (it's what produced the failure)
4. The improvement targets that specific failure

**Output:** baseline transcript + identified rationalization patterns + violation list. This drives Phase 4.

### Phase 4: Skill Authoring (GREEN — Write Minimal Skill)

#### Description authoring (CSO — Claude Search Optimization)

The description is the primary triggering mechanism. Get it right before the body.

**Critical rule: Description = WHEN to use, NOT what the skill does.**

When the description summarizes the skill's workflow, Claude follows the description as a shortcut and skips reading the body. This was observed: a description saying "code review between tasks" caused Claude to do ONE review, even though the skill's flowchart clearly showed TWO reviews. When the description was changed to just "Use when executing implementation plans with independent tasks" (no workflow summary), Claude correctly read the flowchart and followed the two-stage process.

**The trap:** descriptions that summarize workflow create a shortcut Claude takes. The skill body becomes documentation Claude skips.

**Rules:**
- Write in third person ("Use when...", "Detects...", "Generates...")
- Start with concrete triggering conditions and symptoms
- Include keywords future Claude would search for (error messages, symptom phrases, tool names)
- NEVER summarize the skill's process or workflow
- Maximum 1024 characters; aim for under 500
- Be "pushy" enough that Claude triggers when relevant

```yaml
# ❌ BAD: Summarizes workflow — Claude follows this instead of reading skill
description: Use when executing plans — dispatches subagent per task with code review between tasks

# ❌ BAD: Too much process detail
description: Use for TDD — write test first, watch it fail, write minimal code, refactor

# ✅ GOOD: Just triggering conditions, no workflow summary
description: Use when executing implementation plans with independent tasks in the current session

# ✅ GOOD: Triggering conditions + key symptoms, no workflow
description: Use when implementing any feature or bugfix, before writing implementation code
```

#### Body structure

```markdown
---
name: skill-name-with-hyphens
description: [CSO description as above]
---

# Skill Name

## Overview
What is this? Core principle in 1-2 sentences.

## When to Use
[Small inline flowchart IF decision is non-obvious]
Bullet list with SYMPTOMS and use cases. When NOT to use.

## Core Pattern (technique/pattern skills)
Before/after comparison or worked example.

## Quick Reference
Table or bullets for scanning common operations.

## Implementation
Inline code for simple patterns; link to file for heavy reference.

## Common Mistakes / Red Flags
What goes wrong + fixes.

## Real-World Impact (optional)
Concrete results.
```

#### Token efficiency

Skills load into context. Every token competes with conversation history.

**Targets:**
- Getting-started workflows: under 150 words
- Frequently-loaded skills: under 200 words
- Other skills: under 500 words (still be concise; under 500 lines is the SKILL.md ceiling)

**Techniques:**
- Move details to tool `--help` instead of inline documentation
- Cross-reference other skills instead of repeating their content
- Compress examples to the minimum that conveys the pattern
- Eliminate redundancy — don't explain the obvious, don't repeat cross-referenced content

#### Per skill type

- **Discipline:** Iron Law + rationalization table + red flags + spirit-vs-letter rule
- **Technique:** numbered steps with concrete examples + when-not-to-use section
- **Pattern:** worked example + recognition triggers + counter-examples
- **Reference:** table of contents at top + scannable structure + cross-references

### Phase 5: Run Tests (GREEN — Watch It Pass)

Re-run the baseline scenarios from Phase 3, this time WITH the skill loaded.

**Verify:**
- Agent now complies with the rule (discipline skills)
- Agent applies the technique correctly (technique skills)
- Agent recognizes and uses the pattern (pattern skills)
- Agent finds and uses reference information correctly (reference skills)

If agent still fails: the skill body is missing something. Return to Phase 4.

### Phase 6: Bulletproofing (REFACTOR — Close Loopholes)

Skills that enforce discipline need to resist rationalization. Agents are smart and will find loopholes when under pressure.

#### Close every loophole explicitly

Don't just state the rule — forbid specific workarounds.

**Bad:**
```markdown
Write code before test? Delete it.
```

**Good:**
```markdown
Write code before test? Delete it. Start over.

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete
```

#### Address "spirit vs letter" arguments

Add the foundational principle early in the skill body:

```markdown
**Violating the letter of the rules is violating the spirit of the rules.**
```

This cuts off an entire class of "I'm following the spirit" rationalizations.

#### Build a rationalization table

Capture every rationalization observed during baseline testing. Each excuse goes in the table:

```markdown
| Excuse | Reality |
|---|---|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "It's about spirit not ritual" | Spirit IS letter. No exceptions. |
```

#### Create a Red Flags list

Make it easy for agents to self-check when rationalizing:

```markdown
## Red Flags — STOP and Start Over

- Code before test
- "I already manually tested it"
- "Tests after achieve the same purpose"
- "It's about spirit not ritual"
- "This is different because..."

**All of these mean: Delete code. Start over with TDD.**
```

#### Pressure-test cycle

After adding loophole counters, re-run pressure scenarios. Combine multiple pressures:
- Time pressure ("the deadline is in 2 hours")
- Sunk cost ("you've already written 200 lines")
- Authority ("your manager said to skip this")
- Exhaustion ("it's late, just ship it")

If a new rationalization emerges, add a counter, re-test. Continue until bulletproof.

### Phase 7: Description Optimization

After Phases 1-6 produce a working skill, optimize the description for triggering accuracy.

1. Generate 20 eval queries — mix of should-trigger and should-not-trigger
2. The should-not-trigger ones should be near-misses (share keywords but need a different skill)
3. Run each query 3 times to get a reliable trigger rate
4. Iterate the description (max 5 iterations) — refine to maximize correct triggers and minimize false ones
5. Apply the best description

### Phase 8: Finalization

When testing is satisfied:

1. **Confirm the file lives in the right place** — for Lattice skills, follow the layout:
   - Domain skills: `domains/<mode>/skill-X.md`
   - Cross-cutting skills: `domains/shared/skill-X.md`
   - Protocols: `shared/X-protocol.md`
   - References: `shared/references/X-reference.md`
2. **Wire it into discoverability** — if it's a protocol or reference, add it to `Lattice.md`'s Shared Infrastructure section
3. **Run a final pre-flight check** against the Quality Checklist below
4. **Confirm with the user** before declaring done

## Skill Structure

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions (under 500 lines)
├── references/ (optional, for content > 300 lines that loads on demand)
│   └── extra.md
├── scripts/ (optional)
│   └── helper.py
└── assets/ (optional)
    └── template.md
```

For Lattice, single-file skills are the norm. Use `references/` only when SKILL.md would otherwise exceed 500 lines AND the extra content loads on demand.

## Progressive Disclosure

Three loading levels:

1. **Metadata** (name + description) — always in context (~100 words per skill)
2. **SKILL.md body** — in context whenever skill triggers (target under 500 lines)
3. **References / scripts** — loaded only when explicitly read

Reference files at depth > 1 from SKILL.md often get partially read. Keep references one level deep. For files over 100 lines, include a table of contents.

## Common Anti-Patterns

| Anti-pattern | Why bad | Fix |
|---|---|---|
| Description summarizes workflow | Claude follows description, skips body | Description = when-to-use only |
| First-person description ("I help you...") | Inconsistent with system-prompt voice | Third person ("Detects...", "Generates...") |
| No baseline testing | Don't know if skill is needed or works | Run RED phase before writing |
| No rationalization table | Discipline skill gets bypassed under pressure | Capture excuses from baseline, add table |
| Multi-language code examples | Maintenance burden, mediocre quality | One excellent example in the most relevant language |
| Generic flowchart labels (step1, helper2) | Labels lose semantic meaning | Use descriptive node names |
| Code in flowcharts | Can't copy-paste, hard to read | Markdown blocks for code; flowcharts for decisions |
| Narrative storytelling ("In session 2025-10-03...") | Specific to one event, not reusable | Generalize to a reusable pattern |
| Linking Lattice skills with `@` | Force-loads the file, burns context | Reference by path: `domains/shared/skill-tdd.md` |
| 5+ skills in batch without testing each | Untested skills accumulate; bugs compound | Phase 5 must pass per skill before next |

## Quality Checklist

Before declaring a skill done, verify:

**RED phase (testing):**
- [ ] Created baseline pressure scenarios (3+ for discipline skills)
- [ ] Ran scenarios WITHOUT skill — documented baseline failures
- [ ] Identified rationalization patterns

**GREEN phase (authoring):**
- [ ] Name uses only lowercase letters, numbers, hyphens
- [ ] YAML frontmatter has `name` and `description` (description ≤ 1024 chars)
- [ ] Description starts with "Use when..." and includes specific triggers
- [ ] Description does NOT summarize the workflow
- [ ] Description in third person
- [ ] SKILL.md body under 500 lines
- [ ] Token-efficient (under 500 words for general skills, under 200 for frequently-loaded)
- [ ] Cross-references use file paths, not `@` links
- [ ] Code examples in one excellent language (not multi-language dilution)
- [ ] Flowcharts only for non-obvious decisions

**REFACTOR phase (bulletproofing):**
- [ ] Iron Law / spirit-vs-letter rule for discipline skills
- [ ] Rationalization table built from baseline observations
- [ ] Red Flags list for self-check
- [ ] Re-tested under combined pressures (time + sunk cost + exhaustion)

**Integration (Lattice-specific):**
- [ ] Lives in the right folder for its type
- [ ] Cross-references existing Lattice protocols where relevant
- [ ] Wired into `Lattice.md` if it's a protocol or reference
- [ ] No conflict with existing skills

## Evaluation Behavior Rules

- Never silently copy a skill without evaluation first
- Never modify the core logic or intent of a skill — only improve how it communicates and handles edge cases
- Always show the evaluation report before the adapted version
- Always ask for save location before writing any file
- If the skill being evaluated is one of Lattice's own skills, apply the same standard — no homegrown bias
- If the source cannot be read or fetched, report why and stop

## Discovery Workflow (how future Claude finds your skill)

1. Encounters problem ("tests are flaky", "feedback received from review")
2. Sees skill description (matches triggering conditions)
3. Loads SKILL.md body (decides skill is relevant)
4. Scans Quick Reference (finds the right pattern)
5. Reads detail (only the section needed)
6. Loads reference file (only when implementing)

Optimize for this flow:
- Searchable terms early and often
- Quick Reference table for scanning
- Sectioned body for partial reads
- Reference files for deep detail

## STOP: After Writing Any Skill

After writing ANY skill, you MUST STOP and complete the deployment process for THAT skill before starting another.

**Do NOT:**
- Create multiple skills in batch without testing each
- Move to next skill before current one is verified
- Skip testing because "batching is more efficient"

The Quality Checklist is mandatory for EACH skill. Deploying untested skills = deploying untested code.

## Integration with Lattice protocols

- **shared/verification-protocol.md** — apply during Phase 5: don't claim the skill works without showing the test transcript
- **shared/parallel-agents-protocol.md** — Phase 5 testing can dispatch multiple pressure scenarios in parallel
- **shared/dpev-loop-protocol.md** — skill creation IS a phase: DISCUSS the rule, PLAN the skill body, EXECUTE the write, VERIFY against baseline tests
- **shared/references/anti-patterns-reference.md** — apply rules 1-4 (context budget) during Phase 4 authoring: keep skills tight
- **shared/plan-checker-protocol.md** — for major skills (>200 lines), run the equivalent of plan-check before declaring done

## The Bottom Line

**Creating skills IS TDD for process documentation.**

Same Iron Law: NO SKILL WITHOUT A FAILING TEST FIRST.

Same cycle: RED (baseline) → GREEN (write skill) → REFACTOR (close loopholes).

Same benefits: better quality, fewer surprises, bulletproof results.

If you follow TDD for code, follow it for skills. Same discipline, applied to documentation.
