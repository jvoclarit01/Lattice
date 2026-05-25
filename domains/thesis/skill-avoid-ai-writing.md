<!-- ADAPTED from D:/skills/community/writing/avoid-ai-writing/SKILL.md (v3.3.1, MIT, by Conor Bronsdon)
     Adaptations: Lattice frontmatter (dropped version/license/compatibility/metadata),
     added When to Activate + Trigger phrases blocks, replaced context profiles
     (linkedin/blog/technical-blog/investor-email/docs/casual) with academic profiles
     (thesis-chapter/journal-paper/conference-abstract/dissertation-abstract/working-draft),
     adjusted "social posts may use emoji" anti-pattern to "academic prose forbids emoji",
     added Integration with Other Skills section. Tier 1/2/3 word tables, severity tiers,
     pattern catalog, output format, and tone calibration preserved verbatim — these are
     the load-bearing value of the skill. -->
---
name: skill-avoid-ai-writing
description: Detect and remove AI writing patterns (AI-isms) from thesis chapters, journal papers, abstracts, and any academic prose. Use whenever the user asks to "remove AI-isms", "clean up AI writing", "make this sound less like AI", "audit this writing", "edit for tone", or whenever you suspect a draft sounds machine-generated (em-dash overuse, hollow intensifiers like "robust" and "comprehensive", formulaic openings, copula avoidance, hedging). Has detect mode (flag without rewriting) and rewrite mode (flag and fix). Tiered word lists reduce false positives. Context profiles adjust strictness for thesis chapters, journal papers, conference abstracts, dissertation abstracts, and working drafts.
---

# Avoid AI Writing — Audit & Rewrite

You are editing academic content to remove AI writing patterns ("AI-isms") that make text sound machine-generated.

## When to Activate

**Always activate for:**
- Reviewing thesis chapters, journal papers, conference papers, dissertation drafts
- Reviewing abstracts, conclusions, discussion sections, related work
- Polishing prose before submission, defense, or peer review
- Any time the user mentions AI-sounding writing or generic tone

**Trigger phrases:**
- "remove AI-isms", "clean up AI writing", "make this sound less like AI"
- "audit this writing", "scan this", "what AI patterns are in this"
- "tone check", "polish this", "edit for voice"
- "sounds generic", "sounds robotic", "feels machine-generated"
- "too wordy", "trim the fluff", "cut the filler"

## Modes

This skill operates in one of two modes:

**`rewrite`** (default) — Flag AI-isms and rewrite the text to fix them.

**`detect`** — Flag AI-isms only. No rewriting. Use this mode when:
- The writer wants to see what's flagged and decide what to fix themselves
- The flagged patterns might be intentional (AI patterns aren't always bad — they can be effective in small doses)
- You're auditing text you don't want altered (already-published work, an advisor's prose, reference material)
- You want a quick scan without waiting for a full rewrite

Trigger detect mode when the user says "detect," "flag only," "audit only," "just flag," "scan," "what AI patterns are in this," or similar. Default to rewrite mode if not specified.

---

In **rewrite** mode, your job is to:

1. **Audit it**: identify every AI-ism present, citing the specific text
2. **Rewrite it**: return a clean version with all AI-isms removed
3. **Show a diff summary**: briefly list what you changed and why

In **detect** mode, your job is to:

1. **Audit it**: identify every AI-ism present, citing the specific text
2. **Assess it**: note which flags are clear problems vs. patterns that may be intentional or effective in context

---

## What to remove or fix

### Formatting

- **Em dashes (— and --)**: Replace with commas, periods, parentheses, or rewrite as two sentences. Target: zero. Hard max: one per 1,000 words. This applies to headings and section titles too. Catch both the Unicode em dash (—) and the double-hyphen substitute (--).
- **Bold overuse**: Strip bold from most phrases. One bolded phrase per major section at most, or none. If something's important enough to bold, restructure the sentence to lead with it instead.
- **Emoji in headers**: <!-- ADAPTED: original allowed 1-2 emoji on social posts; academic prose forbids emoji entirely. --> Remove entirely. Academic prose does not use emoji in headers, body, or anywhere else. No exceptions.
- **Excessive bullet lists**: Convert bullet-heavy sections into prose paragraphs. Bullets only for genuinely list-like content (variable definitions, hyperparameter tables, step-by-step procedures). Thesis prose should be prose.

### Sentence structure

- **"It's not X — it's Y" / "This isn't about X, it's about Y"**: Rewrite as a direct positive statement. Max one per piece, and only if it serves the argument.
- **Hollow intensifiers**: Cut `genuine`, `real` (as in "a real improvement"), `truly`, `quite frankly`, `to be honest`, `let's be clear`, `it's worth noting that`. Just state the fact.
- **Vague endorsement ("worth [verb]ing")**: Cut or replace `worth reading`, `worth paying attention to`, `worth a look`, `worth exploring`, `worth your time`. Say *why* something matters instead.
- **Hedging**: Cut `perhaps`, `could potentially`, `it's important to note that`, `to be clear`. In academic writing, calibrated hedging (`may`, `suggests`, `indicates`) is legitimate; reflexive AI hedging is not.
- **Missing bridge sentences**: Each paragraph should connect to the last. If paragraphs could be rearranged without the reader noticing, add connective tissue.
- **Compulsive rule of three**: Vary groupings. Use two items, four items, or a full sentence instead of triads. Max one "adjective, adjective, and adjective" pattern per piece.

### Words and phrases to replace

Words are organized into three tiers based on how reliably they signal AI-generated text. This tiered approach reduces false positives on words that are fine in isolation but suspicious in clusters.

- **Tier 1 — Always flag.** These words appear 5–20x more often in AI text than human text. Replace on sight.
- **Tier 2 — Flag in clusters.** Individually fine, but two or more in the same paragraph is a strong AI signal. Flag when they appear together.
- **Tier 3 — Flag by density.** Common words that AI simply overuses. Only flag when they make up a noticeable fraction of the text (roughly 3%+ of total words).

#### Tier 1 — Always replace

| Replace | With |
|---|---|
| delve / delve into | explore, dig into, look at |
| landscape (metaphor) | field, area, literature |
| tapestry | (describe the actual complexity) |
| realm | area, field, domain |
| paradigm | model, approach, framework |
| embark | start, begin |
| beacon | (rewrite entirely) |
| testament to | shows, proves, demonstrates |
| robust | strong, reliable, sound |
| comprehensive | thorough, complete, full |
| cutting-edge | recent, current, state-of-the-art (cite the benchmark) |
| leverage (verb) | use |
| pivotal | important, key, central |
| underscores | highlights, shows |
| meticulous / meticulously | careful, detailed, precise |
| seamless / seamlessly | smooth, without friction |
| game-changer / game-changing | (describe what specifically changed and why) |
| utilize | use |
| watershed moment | turning point, shift |
| nestled | located, sits, is in |
| vibrant | (describe what makes it active, or cut) |
| thriving | growing, active (or cite a number) |
| despite challenges… continues to thrive | (name the challenge and the response, or cut) |
| showcasing | showing, demonstrating (or cut) |
| deep dive / dive into | look at, examine, explore |
| unpack / unpacking | explain, break down |
| bustling | busy, active |
| intricate / intricacies | complex, detailed (or name the specific complexity) |
| complexities | (name the actual complexities) |
| ever-evolving | changing, developing |
| enduring | lasting, long-running |
| daunting | hard, difficult, challenging |
| holistic / holistically | complete, full (or describe what's included) |
| actionable | practical, useful, concrete |
| impactful | effective, significant (or describe the impact) |
| learnings | lessons, findings, takeaways |
| thought leader / thought leadership | expert, authority (or describe their actual contribution) |
| best practices | what works, proven methods |
| at its core | (cut — just state the thing) |
| synergy / synergies | (describe the actual combined effect) |
| interplay | relationship, connection, interaction |
| in order to | to |
| due to the fact that | because |
| serves as | is |
| features (verb) | has, includes |
| boasts | has |
| presents (inflated) | is, shows, gives |
| commence | start, begin |
| ascertain | find out, determine |
| endeavor | effort, attempt, try |
| symphony (metaphor) | (describe the actual coordination) |
| embrace (metaphor) | adopt, accept, use |

#### Tier 2 — Flag when 2+ appear in the same paragraph

These words are legitimate on their own. When two or more show up together, the paragraph likely needs a rewrite.

| Replace | With |
|---|---|
| harness | use, take advantage of |
| navigate / navigating | work through, handle, deal with |
| foster | encourage, support, build |
| elevate | improve, raise, strengthen |
| unleash | release, enable, unlock |
| streamline | simplify, speed up |
| empower | enable, let, allow |
| bolster | support, strengthen |
| spearhead | lead, drive, run |
| resonate / resonates with | connect with, appeal to, matter to |
| revolutionize | change, transform (or describe what changed) |
| facilitate / facilitates | enable, help, allow |
| underpin | support, form the basis of |
| nuanced | specific, subtle, detailed |
| crucial | important, key, necessary |
| multifaceted | (describe the actual facets) |
| ecosystem (metaphor) | system, community, network |
| myriad | many, numerous (or give a number) |
| plethora | many, a lot of (or give a number) |
| encompass | include, cover, span |
| catalyze | start, trigger, accelerate |
| reimagine | rethink, redesign |
| galvanize | motivate, rally |
| augment | add to, expand, supplement |
| cultivate | build, develop, grow |
| illuminate | clarify, explain, show |
| elucidate | explain, clarify |
| juxtapose | compare, contrast |
| paradigm-shifting | (describe what actually shifted) |
| transformative / transformation | (describe what changed and how) |
| cornerstone | foundation, basis |
| paramount | most important, top priority |
| poised (to) | ready, set, about to |
| burgeoning | growing, emerging |
| nascent | new, early-stage, emerging |
| quintessential | typical, classic |
| overarching | main, central, broad |
| underpinning / underpinnings | basis, foundation |

#### Tier 3 — Flag only at high density

These are normal words. Only flag them when the text is saturated with them — a sign that AI filled space with vague praise instead of specifics.

| Word | What to do |
|---|---|
| significant / significantly | Replace some with specifics: numbers, comparisons, examples (in academic writing, "statistically significant" is fine — flag only the rhetorical use) |
| innovative / innovation | Describe what's actually new |
| effective / effectively | Say how or cite a metric |
| dynamic / dynamics | Name the actual forces or changes |
| scalable / scalability | Describe what scales and to what |
| compelling | Say why it compels |
| unprecedented | Name the precedent it breaks (or cut) |
| exceptional / exceptionally | Cite what makes it an exception |
| remarkable / remarkably | Say what's worth remarking on |
| sophisticated | Describe the sophistication |
| instrumental | Say what role it played |
| world-class / state-of-the-art / best-in-class | Cite a benchmark or comparison |

### Template phrases (avoid)

These slot-fill constructions signal that a sentence was generated, not written. If a phrase has a blank where a noun or adjective could go and still sound the same, it's too generic.

- "a [adjective] step towards [adjective] AI infrastructure" → describe the specific capability, benchmark, or outcome
- "a [adjective] step forward for [noun]" → say what actually changed
- "Whether you're [X] or [Y]" → false-breadth construction. Pick the audience you're actually addressing, or cut.
- "I recently had the pleasure of [verb]-ing" → conversational AI pattern. Just say what happened.

### Transition phrases to remove or rewrite

- "Moreover" / "Furthermore" / "Additionally" → restructure so the connection is obvious, or use "and," "also"
- "In today's [X]" / "In an era where" → cut or state specific context
- "It's worth noting that" / "Notably" → just state the fact
- "Here's what's interesting" / "Here's what caught my eye" → reader-steering frame. Let the content signal its own importance.
- "In conclusion" / "In summary" / "To summarize" → your conclusion should be obvious (in thesis writing, an explicit "In summary" once per chapter conclusion is fine; flag overuse)
- "When it comes to" → just talk about the thing directly
- "At the end of the day" → cut
- "That said" / "That being said" → cut or use "but," "yet," "however"

### Structural issues

- **Uniform paragraph length**: Vary deliberately. Include some 1-2 sentence paragraphs and some longer ones. If every paragraph is roughly the same size, fix it.
- **Formulaic openings**: If a chapter or section opens with broad context before getting to the point ("In the rapidly evolving field of machine learning..."), rewrite to lead with the specific contribution or finding. Context can come second.
- **Suspiciously clean grammar**: Don't sand away all personality. Academic prose can still have rhythm. Deliberate fragments are rare in formal writing but a varied sentence cadence is essential.

### Significance inflation

- Phrases like "marking a pivotal moment in the evolution of..." or "a watershed moment for the field" inflate routine results into history-making ones. State what happened and let the reader judge significance.
- If the sentence still works after you delete the inflation clause, delete it.

### Copula avoidance

- AI text avoids "is" and "has" by substituting fancier verbs: "serves as," "features," "boasts," "presents," "represents." These sound like a press release, not a thesis.
- Default to "is" or "has" unless a more specific verb genuinely adds meaning.

### Synonym cycling

- AI rotates synonyms to avoid repeating a word: "researchers… scholars… authors… investigators" in the same paragraph. Human academic writers repeat the clearest word.
- If "researcher" is the right word, use it three times. Forced variation reads as thesaurus abuse.

### Vague attributions

- "Experts believe," "Studies show," "Research suggests," "Recent work has demonstrated" — without naming the experts, studies, or work. Either cite a specific source (which academic writing requires anyway) or drop the attribution.

### Filler phrases

- Strip mechanical padding that adds words without meaning:
  - "It is important to note that" → (just state it)
  - "In terms of" → (rewrite)
  - "The reality is that" → (cut)

### Generic conclusions

- "The future looks bright," "Only time will tell," "One thing is certain," "As we move forward" — these are filler disguised as conclusions. Cut them. Thesis conclusions need specific findings, specific limitations, and specific future-work directions.

### Chatbot artifacts

- "I hope this helps!", "Certainly!", "Absolutely!", "Great question!", "Let me know if you need anything else" — conversational tics from chat interfaces, never appropriate in academic prose. Remove entirely.
- Also watch for: "In this chapter, we will explore…" — fine *once* per chapter as a roadmap sentence; AI-generated meta-narration if it appears multiple times.

### "Let's" constructions

- "Let's explore," "Let's take a look," "Let's break this down," "Let's examine" — AI uses "let's" as a false-collaborative opener. In academic writing, this is almost always wrong tone. Use "We examine," "This section presents," or just start with the point.

### Notability name-dropping

- AI piles on prestigious citations to manufacture credibility. In academic writing, this maps to citation stuffing — citing five papers to make a single uncontroversial claim. Cite the foundational work and one recent example, not the entire field.

### Superficial -ing analyses

- Strings of present participles used as pseudo-analysis: "extending prior work, demonstrating the approach, showcasing the results, opening new avenues." These say nothing. Replace with specific facts or cut entirely.

### Promotional language

- AI defaults to brochure prose. In academic writing, this shows up as overselling: "novel, powerful, robust, comprehensive framework that significantly advances the field." Replace with plain description: "We propose X. On benchmark Y, X improves accuracy by Z."

### Formulaic challenges

- "Despite challenges, [subject] continues to thrive" or "While facing limitations, the approach remains effective." Name the actual limitation and the actual response.

### False ranges

- AI creates false breadth: "from foundational theory to practical applications," "from low-resource languages to multilingual benchmarks." List the actual scope or pick the part that matters.

### Title case headings

- AI over-capitalizes headings: "Strategic Negotiations And Key Partnerships." Use sentence case for subheadings unless your style guide (APA, IEEE, ACM) specifies otherwise.

### Cutoff disclaimers

- "While specific details are limited based on available information," "As of my last update," "I don't have access to real-time data." These are model limitations leaking into prose. Either find the information or remove the hedge. Never publish a sentence that admits the writer didn't look something up.

### Novelty inflation

- AI text treats established concepts as if the speaker invented them: "We introduce a novel concept," "We coin the term." In reality, most ideas are extensions of existing work. Frame contributions accurately: "We extend [existing concept] to [new setting]" rather than "We introduce a new paradigm." Reviewers and committees notice claimed novelty that doesn't hold up.

### Emotional flatline

- AI claims emotions as a structural crutch: "What surprised us most," "We were fascinated to discover." If the result is genuinely surprising, the data should show it. Otherwise cut the claim.

### False concession structure

- "While X is impressive, Y remains a challenge" or "Although X has made strides, Y is still an open question." AI uses this to sound balanced without actually weighing anything. Either make the concession specific or pick a side and argue it.

### Rhetorical question openers

- "But what does this mean for practitioners?" / "So why does this matter?" — AI uses rhetorical questions to stall. Just state the implication.

### Reasoning chain artifacts

- "Let me think step by step," "Breaking this down," "First, let's consider" — artifacts of chain-of-thought reasoning leaking into prose. The reader doesn't need the scaffolding. State the conclusion, then the evidence.

### Sycophantic tone

- "Great question!", "Excellent point!" — sycophancy from chat interfaces. Remove entirely.

### Confidence calibration phrases

- "It's worth noting that," "Interestingly," "Surprisingly," "Importantly," "Notably," "Certainly," "Undoubtedly" — AI signals how the reader should feel instead of letting the result speak. One "notably" in a 5,000-word chapter is fine. Three in 500 words is AI emphasis stacking.

### Excessive structure

- More than 3 headings in under 300 words is almost always AI trying to look organized. Merge sections or use prose transitions.
- 8+ bullet points in under 200 words means the content should be a paragraph.

### Rhythm and uniformity

These aren't individual word problems — they're patterns in how the text flows. AI text is metronomic; human text has varied rhythm.

**Structure is the #1 detection signal.** AI detection tools weight structural regularity higher than vocabulary. Consistent sentence construction, uniform pacing, and symmetrical phrasing are harder to mask than swapping flagged words.

- **Sentence length uniformity**: If most sentences are 15–25 words, the text sounds robotic. Mix short with longer.
- **Paragraph length uniformity**: If every paragraph is 3–5 sentences and roughly the same size, vary deliberately.
- **Vocabulary repetition vs. synonym cycling**: Repeat when the word is right. Vary when it's natural. No formula.
- **Read-aloud test**: If the text could be read by a TTS engine without sounding weird, it's probably too uniform.
- **Over-polishing**: Aggressive editing toward "clean" prose pushes text *toward* AI statistical profiles. Don't sand away all personality.

### When to rewrite from scratch vs. patch

If the text has 5+ flagged vocabulary hits across multiple categories, 3+ distinct pattern categories triggered, and uniform sentence/paragraph length, patching individual phrases won't fix it — the structure itself is AI-generated. Advise a full rewrite: state the core point in one sentence, then rebuild from there.

---

## Severity tiers

When doing a quick pass or triaging a long chapter, prioritize by tier:

### P0 — Credibility killers (fix immediately)
- Cutoff disclaimers ("As of my last update")
- Chatbot artifacts ("I hope this helps!", "Great question!")
- Vague attributions without sources ("Experts believe")
- Significance inflation on routine results
- Novelty inflation that won't survive reviewer scrutiny

### P1 — Obvious AI smell (fix before submission)
- Word-list violations (delve, leverage, harness, robust, etc.)
- Template phrases and slot-fill constructions
- "Let's" transition openers
- Synonym cycling within a paragraph
- Formulaic openings ("In the rapidly evolving field of...")
- Bold overuse
- Em dash frequency (above 1 per 1,000 words)

### P2 — Stylistic polish (fix when time allows)
- Generic conclusions
- Compulsive rule of three
- Uniform paragraph length
- Copula avoidance
- Transition phrases (Moreover, Furthermore, Additionally)

Use P0+P1 for quick passes. Full audit covers all three tiers.

---

## Self-reference escape hatch

When writing *about* AI writing patterns (this skill, related work that critiques AI-generated text), quoted examples are exempt from flagging. Text inside quotation marks, code blocks, or explicitly marked as illustrative ("for example, AI might write...") should not be rewritten. Only flag patterns that appear in the author's own prose.

---

## Context profiles

<!-- ADAPTED: original profiles were linkedin/blog/technical-blog/investor-email/docs/casual.
     Replaced with academic profiles relevant to thesis-lattice work. The strictness pattern
     and tolerance matrix concept are preserved; the labels and tunings are reframed. -->

Pass an optional context hint to adjust rule strictness. If no context is specified, auto-detect from content cues (heading structure with §/numbered sections = thesis-chapter, abstract under 350 words = abstract, conference template formatting = conference-paper, default = thesis-chapter).

### Profile definitions

**`thesis-chapter`** — Default. Long-form scholarly prose. All rules apply at full strength.
**`journal-paper`** — Strict. Word counts matter, every paragraph earns its space.
**`conference-paper`** — Like journal-paper but with tighter page budget; flag bloated phrasing more aggressively.
**`abstract`** — Extra strict. 150-300 words, every word counts. Promotional language and inflation are the biggest risks.
**`dissertation-abstract`** — Like abstract but a bit longer; same extra-strict rules.
**`discussion-section`** — Strict on hedging and significance inflation; calibrated hedging is allowed but reflexive AI hedging is not.
**`related-work`** — Strict on synonym cycling (researchers / scholars / authors / investigators) and citation-stuffing.
**`working-draft`** — Relaxed. Catch only the worst offenders. Use when the author wants encouragement, not surgery.

### Tolerance matrix

Rules not listed in the table apply at full strength across all profiles.

| Rule | thesis-chapter | journal-paper | conference-paper | abstract / dissertation-abstract | discussion | related-work | working-draft |
|------|----------------|---------------|------------------|--------------------------------|------------|--------------|----------------|
| Em dashes | strict | strict | strict | **extra strict** | strict | strict | skip |
| Bold overuse | strict | strict | strict | strict | strict | strict | skip |
| Emoji anywhere | strict (forbid) | strict (forbid) | strict (forbid) | strict (forbid) | strict (forbid) | strict (forbid) | strict (forbid) |
| Excessive bullets | strict | strict | strict | strict | strict | strict | skip |
| Hedging | strict (catch reflexive) | strict (catch reflexive) | strict | strict | relaxed (calibrated hedging is legitimate) | strict | skip |
| Word table (full list) | strict | strict | strict | **extra strict** | strict | strict | P0 only |
| Promotional language | strict | strict | strict | **extra strict** | strict | strict | skip |
| Significance inflation | strict | strict | strict | **extra strict** | **extra strict** | strict | skip |
| Copula avoidance | strict | strict | strict | strict | strict | strict | skip |
| Uniform paragraph length | strict | strict | strict | skip (short-form) | strict | strict | skip |
| Numbered list inflation | strict | strict | strict | strict | strict | strict | skip |
| Rhetorical questions | strict | strict | strict | strict | strict | strict | skip |
| Transition phrases | strict | strict | strict | strict | strict | strict | skip |
| Generic conclusions | strict | strict | strict | **extra strict** | **extra strict** | strict | skip |
| Novelty inflation | strict | **extra strict** | **extra strict** | **extra strict** | strict | strict | strict |
| Synonym cycling | strict | strict | strict | strict | strict | **extra strict** | skip |

**"Extra strict"** means: flag even borderline instances. In an abstract, a single "thriving research community" can sink the framing.

**"Skip"** means: don't audit this category for this profile.

### Auto-detection cues

When no context is specified, infer from these signals:

| Signal | Inferred context |
|--------|-----------------|
| 100-350 words, single paragraph or two, dense | `abstract` |
| 350-600 words, single section, structured | `dissertation-abstract` |
| Numbered sections (§ or 1.1, 1.2), figures/tables, citations dense | `thesis-chapter` |
| LaTeX `\section`, two-column hint, tighter prose | `conference-paper` or `journal-paper` |
| Heavy citations, prose mostly summarizing prior work | `related-work` |
| Limitations / Future work language, hedged claims | `discussion-section` |
| No strong signals | `thesis-chapter` (safest default) |

If auto-detection feels wrong, say which profile you're using and why. The user can override.

---

## Output format

### Rewrite mode (default)

Return your response in four sections:

**1. Issues found**
A bulleted list of every AI-ism identified, with the offending text quoted.

**2. Rewritten version**
The full rewritten content. Preserve the original structure, intent, and all specific technical details. Only change what the guidelines require.

**3. What changed**
A brief summary of the major edits. Not every word — just the meaningful changes.

**4. Second-pass audit**
Re-read the rewritten version. Identify any remaining AI tells — recycled transitions, lingering inflation, copula avoidance, filler. Fix them, return the corrected text inline, and note what changed in this pass. If the rewrite is clean, say so.

### Detect mode

Return your response in two sections:

**1. Issues found**
A bulleted list of every AI-ism identified, with the offending text quoted. Group by severity (P0, P1, P2).

**2. Assessment**
For each flag, note whether it's a clear problem or a judgment call. Some AI-associated patterns are effective writing techniques. Call out which flags the writer should definitely fix vs. which might be fine in context. If the text is clean, say so.

---

## Tone calibration

The goal is academic writing that sounds like a person wrote it. Direct. Specific. Confident through demonstration, not assertion.

Five principles for human-sounding rewrites:

1. **Vary sentence length** — mix short with long. Not fragments (academic prose is usually full sentences), but vary the cadence.
2. **Be concrete** — replace vague claims with numbers, names, dates, citations.
3. **Have a voice** — where appropriate, use first person plural ("we observe," "we propose"), state methodological preferences, show reasoning.
4. **Calibrate hedging** — use hedging where the evidence requires it; cut reflexive hedging that AI adds for safety.
5. **Earn your emphasis** — don't tell the reader something is "significant"; make the result speak for itself.

If the original writing is already strong, say so and make only the necessary cuts. Don't over-edit for the sake of it.

The replacement table provides defaults, not mandates. If a flagged word is clearly the right choice in context (e.g., "robust" when describing a robustness analysis specifically about robustness), preserve it.

## Integration with Other Skills

- **domains/thesis/skill-academic-writing.md** — broader academic writing conventions; this skill is the AI-isms pass run alongside or after
- **domains/thesis/skill-abstract-writing.md** — apply the `abstract` / `dissertation-abstract` profile after drafting
- **domains/thesis/skill-conclusion-writing.md** — generic conclusions ("The future looks bright") are this skill's bread and butter
- **domains/thesis/skill-discussion-writing.md** — apply `discussion-section` profile; calibrated hedging is allowed
- **domains/thesis/skill-results-writing.md** — significance inflation is the biggest risk in results sections
- **domains/thesis/skill-literature-review.md** — apply `related-work` profile to catch synonym cycling and citation-stuffing
- **domains/thesis/skill-formatting.md** — em-dash and bold rules in this skill align with thesis formatting guidance
- **domains/thesis/skill-consistency-checker.md** — terminology consistency complements vocabulary cycling detection
