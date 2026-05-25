---
name: skill-academic-writing
description: Sentence- and paragraph-level discipline for academic prose — tense, voice, person, hedging calibration, and the formal register. Use when polishing the prose layer of any thesis chapter, deciding whether to use "we" vs passive, choosing a tense for a sentence, or auditing a paragraph for ambiguity and unsupported claims. For section-specific structure (Results, Discussion, etc.) see the dedicated section skills; for AI-style writing patterns see `skill-avoid-ai-writing`.
---

# Academic Writing

Academic writing is not a single skill — it's a register. This skill governs the *how* of every sentence: tense, voice, person, hedging, precision. Section-level structure and content rules live in sibling skills.

## When to Activate

Use when:
- Polishing prose at the sentence or paragraph level in any thesis chapter
- Deciding whether a sentence should be active or passive, present or past
- A paragraph reads as wordy, hedged, or ambiguous and needs surgery
- Translating notes or bullet points into formal academic prose
- Reviewing a co-author or student draft for register issues
- An advisor flags "tone" or "voice" problems

**Trigger phrases:** "academic tone", "make this more formal", "tense check", "voice check", "passive voice", "hedge this", "tighten this paragraph", "is this too informal"

## When NOT to Use

| Situation | Use instead |
|---|---|
| Detecting AI-generated phrasing (delve, leverage, robust) | `skill-avoid-ai-writing` |
| Deciding what content goes in which chapter | `skill-thesis-structure` |
| Writing the Results section's statistical reporting | `skill-results-writing` |
| Writing the Discussion's interpretation | `skill-discussion-writing` |
| Writing an abstract | `skill-abstract-writing` |
| Citation format and reference lists | `skill-citation-management` |
| Page layout, fonts, headings | `skill-formatting` |
| Validating the logic of an argument | `skill-argument-validator` |
| Final terminology and notation consistency | `skill-consistency-checker` |

If the question is "what register should this sentence be in," this skill answers it. If the question is "what should this sentence say," route to a sibling.

## Iron Laws

1. **Past tense for what you did and found; present for what is and what figures show; future only for proposed work.** Mixing tenses within a paragraph is the most common register defect.
2. **Active voice unless the actor is genuinely irrelevant.** "We trained the model" beats "The model was trained." Passive is a tool, not a default.
3. **Every adjective of degree must be earned with a number, citation, or comparison.** "Substantial improvement" without "(from 78% to 84%)" is hand-waving.
4. **No contractions, no second person, no rhetorical questions.** Academic register excludes them. Period.
5. **One concept, one term.** Once you've named a thing "the embedding layer," it stays "the embedding layer" for the rest of the thesis. No synonym cycling.

## Tense Decision Rubric

| What you're describing | Tense | Example |
|---|---|---|
| Your own actions and findings | Past | "We collected data from 247 participants." |
| What a figure, table, or section shows | Present | "Figure 3 shows the loss curves." |
| Established or general fact | Present | "Cross-entropy is a standard classification loss." |
| Specific past work by a cited author | Past | "Smith (2020) demonstrated…" |
| Recent ongoing line of research | Present perfect | "Researchers have explored…" |
| Proposed or planned future work | Future | "Future work will examine…" |

If a paragraph contains all five, you have a tense audit problem. Pick the dominant tense for the section and let it own the paragraph; switch only when the rubric demands it.

## Voice Decision Rubric

| Situation | Voice | Why |
|---|---|---|
| Reporting your method or finding | Active ("We trained…") | Names the agent; clearer; expected in modern science writing |
| Describing a procedure where the agent is irrelevant | Passive ("Data were anonymized.") | The author is not load-bearing |
| Following a field convention that requires passive | Passive | Some medical/biology venues still expect it |
| Sentence is awkward in active form | Active anyway, restructure | If "we" feels wrong, rewrite — don't pad with passive |

Aim for under 25% passive across a chapter. Modern Methods sections that read entirely passive feel anonymized; modern Results sections that read entirely passive feel evasive.

## Person Decision Rubric

| Use | When |
|---|---|
| First person plural ("we") | Reporting your own work, even as a single author in CS/ML |
| Third person ("the author", "this thesis") | Some humanities and older engineering departments still prefer it; check your department template |
| Second person ("you") | **Never.** Replace with "one," restructure, or rewrite |
| First person singular ("I") | Acceptable in some humanities theses, prefaces, and acknowledgments; rare in empirical work |

The "we" of a single-author CS thesis is conventional and not pretentious. The reader and author together: "We see in Figure 2 that…"

## Hedging Calibration

Hedging is a precision tool, not a politeness tool. The defect is reflexive hedging that adds words without adding caution.

**Calibrated (legitimate):**
- "Results suggest that…" — when evidence is correlational
- "May indicate…" — when alternative explanations remain
- "Consistent with…" — when not strictly causal

**Reflexive (cut):**
- "It is perhaps worth noting that…"
- "It could potentially be argued that…"
- "Some might say that…"

A useful test: delete the hedge. If the meaning is unchanged or sharper, the hedge was filler.

## Precision: Vague → Specific

Replace vague quantifiers with the actual number, name, or comparison.

| Vague | Better |
|---|---|
| "many studies" | "twelve studies" or "the studies surveyed in Section 2.3" |
| "significantly improved" | "improved by 12.3 percentage points (p < .001)" |
| "much faster" | "3.4x faster (median wall-clock)" |
| "various researchers" | name them, or cite the systematic review |
| "in some cases" | "in 47 of 200 trials" |
| "very accurate" | cite the metric |

## Worked Example

**Bad (informal, hedgy, vague, voice-shifty):**
> You can pretty clearly see that our approach was much better than the baseline. Several recent papers have kind of suggested similar things. The data was analyzed using standard techniques, and we are getting really good results which we think show that the method works.

**Good (formal register, calibrated, specific, consistent voice):**
> Our approach outperforms the baseline by 8.4 F1 points on the held-out test set (Table 3). Wei et al. (2022) and Park et al. (2023) report comparable gains in related domains. We analyzed the data with the procedure described in §3.4. The results indicate that the method generalizes within the studied domain; broader claims require the additional experiments described in Chapter 6.

The improved version preserves every claim of the original while removing second-person address, vague quantifiers, reflexive hedging, and tense drift.

## Paragraph Discipline

A well-formed academic paragraph:

1. Opens with a topic sentence stating its claim.
2. Supports the claim with evidence — numbers, citations, or analytic reasoning.
3. Closes by linking to the next paragraph or chapter.

If you can shuffle a chapter's paragraphs without the reader noticing, the paragraphs lack connective tissue. Add bridge sentences ("This pattern motivates the analysis in §4.2…").

Target paragraph length: 100–200 words. Single-sentence paragraphs are rare in academic prose; > 300-word paragraphs usually contain two paragraphs in disguise.

## Common Failure Modes

| Pattern | Why it fails |
|---|---|
| Mixing past and present in one paragraph | Reads as careless; reviewers flag it |
| Reflexive hedging ("It could be argued…") | Adds words, removes confidence, no information gain |
| Synonym cycling (researchers / scholars / authors / investigators in one paragraph) | Reads as thesaurus abuse; betrays AI assistance |
| Second-person address ("you can see that…") | Wrong register; trivially fixable |
| Passive Methods, passive Results, passive Discussion | Erases the author; weakens claims |
| "It is important to note that…" before a routine fact | Filler; signals padding |
| Contractions ("don't", "can't") | Informal register; never appropriate |
| Adjectives without referents ("substantial", "robust", "significant" with no number) | Rhetorical, not scientific |

## Pre-Submission Audit

- [ ] Tense is consistent within paragraphs and matches the rubric
- [ ] Active voice dominates Methods and Results
- [ ] No second-person address anywhere
- [ ] No contractions
- [ ] Every degree adjective has a number, citation, or comparison
- [ ] No reflexive hedging — every hedge survives the deletion test
- [ ] One term per concept; no synonym cycling
- [ ] Paragraphs have topic sentences and connective tissue
- [ ] Run `skill-avoid-ai-writing` after this skill — they catch different defects

## Integration

- `domains/thesis/skill-avoid-ai-writing` — runs after this skill; catches AI-style vocabulary this skill doesn't list
- `domains/thesis/skill-thesis-structure` — decides what content goes where; this skill polishes the prose
- `domains/thesis/skill-results-writing` — Results-specific tense and reporting rules supersede generic ones here
- `domains/thesis/skill-discussion-writing` — calibrated hedging is allowed there; reflexive hedging still isn't
- `domains/thesis/skill-abstract-writing` — abstract has tightest register requirements
- `domains/thesis/skill-consistency-checker` — final terminology pass
- `domains/thesis/skill-argument-validator` — checks the logic this skill polishes the prose of
- `domains/thesis/skill-citation-management` — citation format is separate from prose register

## Resources

- [Academic Phrasebank (University of Manchester)](https://www.phrasebank.manchester.ac.uk/) — canonical register-appropriate phrasings, sortable by section
- [Williams & Bizup, *Style: Lessons in Clarity and Grace*](https://www.pearson.com/en-us/subject-catalog/p/style-lessons-in-clarity-and-grace/P200000003858) — the standard reference for sentence-level academic prose
- [Helen Sword, *Stylish Academic Writing*](https://www.hup.harvard.edu/catalog.php?isbn=9780674064485) — addresses the register-vs-deadness tradeoff
- [APA Style — Verb Tense Guide](https://apastyle.apa.org/style-grammar-guidelines/grammar/verb-tense)
