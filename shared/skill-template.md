# Canonical Skill Template (Lattice)

This is the template every Lattice domain skill should follow. Skills that score 22+/25 in the audit (`skill-tdd`, `skill-database`, `skill-avoid-ai-writing`, `skill-git-worktrees`, `skill-finishing-branch`) all match this structure. Skills that scored ≤14 mostly didn't.

A skill is an *activation contract*. Its sections answer four questions in order:
1. **When does this fire?** (frontmatter description + When to Activate + trigger phrases)
2. **When does this NOT fire?** (When NOT to Use — points at the right neighbor instead)
3. **What discipline does it impose?** (Iron Laws + decision rubrics)
4. **How do I act on it?** (concrete patterns, code, checklists, failure modes)

Skip any of the four and the skill is anemic.

---

## Required Frontmatter

```yaml
---
name: skill-<noun-or-verb-noun>
description: <One sentence on what this skill is. Then a sentence on WHEN to use it — concrete situations, not "when working on X". Then a sentence pointing readers to the closest neighbor skill so they don't load the wrong one.>
---
```

The description is the routing signal. Three sentences:
1. **What** — one sentence
2. **When** — concrete triggers, not tautological ("Activate when doing X" where X is the skill name)
3. **What this is NOT** — the neighbor skill they should consider instead

Bad: `description: Authentication best practices. Use when implementing authentication.` (tautological, no boundary)

Good: `description: Authentication implementation patterns for web apps — sessions, JWT, OAuth, MFA, password handling. Use when adding sign-in, building an auth flow, or reviewing an auth PR. For broader threat-model and OWASP defenses across the SDLC, see shared/skill-security.`

---

## Required Body Sections (in order)

### 1. Title + One-line Premise

```markdown
# <Skill Name>

<One sentence stating the central premise of the skill. Not the description rephrased — the *thesis*.>
```

Example: "Security is not a step in the lifecycle — it's a constraint at every step."

### 2. When to Activate

```markdown
## When to Activate

Use when:
- <Concrete trigger 1>
- <Concrete trigger 2>
- <Concrete trigger N — usually 4–8 bullets>

**Trigger phrases:** "<phrase a user actually says>", "<another>", …
```

The trigger bullets describe situations, not categories. "When implementing auth" is a category; "When adding a sign-in page" or "When a teammate asks 'should this endpoint be public?'" are situations.

### 3. When NOT to Use

```markdown
## When NOT to Use

| Situation | Use instead |
|---|---|
| <Adjacent task> | `<sibling-skill>` |
| <Adjacent task> | `<sibling-skill>` |
```

Mandatory. If you can't name three adjacent things this skill is NOT for, the boundary isn't sharp enough. This is the section homegrown skills almost always lack.

### 4. Iron Laws

```markdown
## Iron Laws

1. **<Imperative rule>.** <One-sentence justification.>
2. **<Imperative rule>.** <One-sentence justification.>
3. **<Imperative rule>.** <One-sentence justification.>
```

Three to five inviolable rules. Phrase them as prohibitions or as positive requirements that take precedence over convenience. Without Iron Laws, the skill is suggestions.

### 5. Decision Rubric (if the skill governs choices)

```markdown
## <Choice Type>

| <Question> | <Use this> | Notes |
|---|---|---|
| … | … | … |
```

Use when the skill helps the agent pick between options (which database, which release strategy, which fairness metric). Not every skill needs one — but if the skill is "best practices for X" with multiple Xs, you need a rubric.

### 6. Concrete Patterns / Code

```markdown
## <Pattern Name>

<One sentence on what this pattern is for.>

```<language>
<runnable code, with imports, no placeholder gibberish>
```

<One paragraph on what this enforces, what the common mistake is, when not to use this.>
```

Code must:
- Run as written (or be clearly labeled `# DEFECT — do NOT do this`)
- Include imports
- Use real APIs (the audit found multiple hallucinated APIs in the ml domain)
- Be accompanied by prose explaining *why*

### 7. Common Failure Modes

```markdown
## Common Failure Modes

| Pattern | Why it fails / consequence |
|---|---|
| <Pattern> | <Consequence> |
```

This is the "if you skip this skill, here's what bites you" section. Stronger than vague "best practices" bullets.

### 8. Checklist (optional, for review-gate skills)

```markdown
## <Stage> Checklist

- [ ] <Concrete check>
- [ ] <Concrete check>
```

For skills that govern a gate (security review, pre-merge, pre-defense), include the checklist. For skills that govern an activity (debugging, design), checklists are usually noise.

### 9. Integration

```markdown
## Integration

- `<sibling-skill>` — <one phrase on how they interact>
- `<sibling-skill>` — <one phrase>
```

Mandatory. List every skill this one collaborates with. Use real file paths within `domains/`. References to skills that don't exist must be pruned (the audit found broken references in multiple skills).

### 10. Resources

```markdown
## Resources

- [<Title>](<URL>) — <one phrase on why this is useful>
```

Curated, not boilerplate. The audit found that many skills append the same 3–4 GitHub links regardless of topic. Don't.

---

## Length Targets

| Skill type | Target lines | Maximum |
|---|---|---|
| Discipline / process (debugging, TDD) | 200–350 | 500 |
| Domain reference (database, deployment) | 300–500 | 700 |
| Specialist (single technique) | 150–250 | 400 |

If you're at 800+ lines, the skill is a tutorial; split it.

---

## Forbidden Patterns

These appeared in low-scoring skills. Do not reproduce them.

| Pattern | Why it's banned |
|---|---|
| "Activate when [verb-ing X]" where X is the skill name | Tautological; gives the agent no routing signal |
| "Core Principles: 1. **Be Accurate** — Be accurate" | Repeats the bold phrase as the explanation; zero information |
| Section titled "Best Practices" with no specifics | Almost always vague filler — replace with concrete patterns + Common Failure Modes |
| Resources block with the same 4 GitHub repos every skill links to | Non-curated; signals a template wasn't customized |
| Code that doesn't run (missing imports, undefined vars, hallucinated APIs) | Worse than no code — actively misleads |
| Re-explaining a sibling skill's content "for completeness" | Creates duplication; reference instead |
| No "When NOT to use" section | Highest-leverage missing element across the audit |

---

## Adapting an Existing Skill

When rewriting a low-scoring skill against this template:

1. **Keep the original's intent.** Don't change *what* the skill does — change *how clearly* it communicates and gates.
2. **Mark non-obvious changes** with `<!-- ADAPTED: <reason> -->` if you want provenance traceable.
3. **Verify code runs** — missing imports, hallucinated APIs, deprecated calls are defects.
4. **Cross-link to siblings** — the most common deficiency is treating each skill as an island.
5. **Cut "Resources" boilerplate** — keep links the user would actually click for this specific skill.

---

## Reference Skills (use as concrete examples)

These five Lattice skills already match this template. When unsure how to render a section, look at one of these:

- `domains/shared/skill-tdd.md` — discipline / process; Iron Laws done well
- `domains/shared/skill-debugging.md` — process; "User Signals You're Doing It Wrong" pattern
- `domains/shared/skill-self-review.md` — process with subagent prompt template
- `domains/webdev/skill-database.md` — domain reference with trigger phrases
- `domains/thesis/skill-avoid-ai-writing.md` — specialist with severity tiers and profiles
