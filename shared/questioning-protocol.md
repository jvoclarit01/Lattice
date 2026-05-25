<!-- ADAPTED from D:/GSD/get-shit-done/references/questioning.md.
     Adaptations: stripped XML tag wrapping (Lattice protocols use markdown
     headings), reframed "PROJECT.md" references to "the brief / `.lattice-plan.md`",
     added per-mode adaptation for the three Lattice modes, kept the dream-extraction
     philosophy and anti-patterns verbatim. -->

# The Questioning Protocol — Dream Extraction

Project initialization and brief-gathering are **dream extraction**, not requirements gathering. You're helping the user discover and articulate what they want to build. This isn't a contract negotiation — it's collaborative thinking.

## Philosophy

**You are a thinking partner, not an interviewer.**

The user often has a fuzzy idea. Your job is to help them sharpen it. Ask questions that make them think "oh, I hadn't considered that" or "yes, that's exactly what I mean."

Don't interrogate. Collaborate. Don't follow a script. Follow the thread.

## When to Apply

- During mode detection in `Lattice.md` ("What are we building?")
- During brainstorming for any new phase (`brainstorming-protocol.md`)
- During discuss step of the DPEV loop (`dpev-loop-protocol.md`)
- Any time the user's intent is fuzzy and needs to be sharpened before action

## The Goal

By the end of questioning, you need enough clarity that downstream steps don't have to guess:

- **For mode detection:** which Lattice mode applies (project / model / thesis / hybrid)
- **For brief-gathering:** what they're building, why, who it's for, what done looks like
- **For per-phase discuss:** what specific decisions this phase needs locked

A vague brief or vague CONTEXT.md forces every downstream step to guess. The cost compounds.

## How to Question

**Start open.** Let them dump their mental model. Don't interrupt with structure.

**Follow energy.** Whatever they emphasized, dig into that. What excited them? What problem sparked this?

**Challenge vagueness.** Never accept fuzzy answers. "Good" means what? "Users" means who? "Simple" means how?

**Make the abstract concrete.** "Walk me through using this." "What does that actually look like?"

**Clarify ambiguity.** "When you say Z, do you mean A or B?" "You mentioned X — tell me more."

**Know when to stop.** When you understand what they want, why they want it, who it's for, and what done looks like — offer to proceed.

## Question Types

Use these as inspiration, not a checklist. Pick what's relevant to the thread.

**Motivation — why this exists:**
- "What prompted this?"
- "What are you doing today that this replaces?"
- "What would you do if this existed?"

**Concreteness — what it actually is:**
- "Walk me through using this."
- "You said X — what does that actually look like?"
- "Give me an example."

**Clarification — what they mean:**
- "When you say Z, do you mean A or B?"
- "You mentioned X — tell me more about that."

**Success — how you'll know it's working:**
- "How will you know this is working?"
- "What does done look like?"

## Using AskUserQuestion

Use the AskUserQuestion tool to help users think by presenting concrete options to react to.

**Good options:**
- Interpretations of what they might mean
- Specific examples to confirm or deny
- Concrete choices that reveal priorities

**Bad options:**
- Generic categories ("Technical", "Business", "Other")
- Leading options that presume an answer
- Too many options (2-4 is ideal)
- Headers longer than 12 characters (hard limit)

**Example — vague answer:**

User says "it should be fast"

- header: "Fast"
- question: "Fast how?"
- options: ["Sub-second response", "Handles large datasets", "Quick to build", "Let me explain"]

**Example — following a thread:**

User mentions "frustrated with current tools"

- header: "Frustration"
- question: "What specifically frustrates you?"
- options: ["Too many clicks", "Missing features", "Unreliable", "Let me explain"]

## The Freeform Rule

**When the user wants to explain freely, STOP using AskUserQuestion.**

If a user selects "Other" or signals they want to describe something in their own words ("let me describe it", "I'll explain", "something else"), you MUST:

1. **Ask your follow-up as plain text** — NOT via AskUserQuestion
2. **Wait for them to type at the normal prompt**
3. **Resume AskUserQuestion** only after processing their freeform response

**Wrong:** User says "let me describe it" → AskUserQuestion("What feature?", ["A", "B", "Describe in detail"])

**Right:** User says "let me describe it" → "Go ahead — what are you thinking?"

## Per-Mode Adaptation

<!-- ADAPTED: original questioning.md only handled project initialization;
     Lattice has three modes that each need slightly different question framings. -->

### project-lattice — building a webdev project

Background checklist (don't walk through it; weave naturally):
- [ ] What they're building (concrete enough to explain to a stranger)
- [ ] Who it's for (even if just themselves)
- [ ] Why it needs to exist
- [ ] What "done" looks like (deployable, has feature X, has N users, etc.)
- [ ] Hard constraints (must use stack X, must integrate with Y, must ship by Z)

### model-lattice — building an ML/AI system

Background checklist:
- [ ] What problem the model solves (the underlying task)
- [ ] How "good" will be measured (metrics, baselines)
- [ ] What data is available
- [ ] Deployment target (notebook, API, edge device, batch job)
- [ ] Hard constraints (latency, cost, interpretability, privacy)

### thesis-lattice — academic research / writing

Background checklist:
- [ ] Research question (concrete enough to be falsifiable)
- [ ] What contribution it makes (gap in the literature it fills)
- [ ] Audience (committee, journal, conference, defense)
- [ ] What "done" looks like (chapter draft, full thesis, journal submission)
- [ ] Hard constraints (style guide, deadline, page limit, advisor preferences)

## Decision Gate

When you could write a clear brief or CONTEXT.md, offer to proceed:

- header: "Ready?"
- question: "I think I understand what you're after. Ready to proceed?"
- options:
  - "Proceed" — Let's move forward
  - "Keep exploring" — I want to share more

If "Keep exploring" — ask what they want to add, or identify gaps and probe naturally.

Loop until "Proceed" is selected.

## Anti-Patterns

- **Checklist walking** — Going through domains regardless of what they said
- **Canned questions** — "What's your core value?" "What's out of scope?" regardless of context
- **Corporate speak** — "What are your success criteria?" "Who are your stakeholders?"
- **Interrogation** — Firing questions without building on answers
- **Rushing** — Minimizing questions to get to "the work"
- **Shallow acceptance** — Taking vague answers without probing
- **Premature constraints** — Asking about tech stack before understanding the idea
- **User skills** — NEVER ask about the user's technical experience. Lattice builds.

## The Principle

Dream extraction is the front-loaded investment that pays off across every downstream step. Skipping it doesn't save time — it just defers the questions to a later step where they're more expensive (often after work has already been wasted on the wrong thing).
