---
name: skill-results-writing
description: Writing the Results section of a thesis or paper — what numbers to report, how to format them, what tense and voice to use, and the strict line between reporting (here) and interpretation (in skill-discussion-writing). Use when drafting or revising a Results chapter, deciding what to include in tables vs prose, or reporting statistical tests.
---

# Results Writing

The Results section reports what happened. Interpretation, comparison to prior work, and "what it means" belong in the Discussion. This boundary is the most-violated rule in scientific writing — keep it sharp.

## When to Activate

Use when:
- Drafting a Results chapter or section
- Deciding what to include in prose vs. table vs. figure
- Reporting any statistical test (t-test, ANOVA, regression, ML metrics)
- A reviewer asks for more detail in Results
- Differentiating "what we found" from "what it means"

**Trigger phrases:** "results section", "report findings", "p-value", "effect size", "statistical reporting", "what to put in results"

## When NOT to Use

| Situation | Use instead |
|---|---|
| Interpreting what results *mean* | `skill-discussion-writing` |
| Designing the figures/tables themselves | `skill-figures-and-tables` |
| Writing the Conclusion (synthesis, not reporting) | `skill-conclusion-writing` |
| ML evaluation methodology (which metrics to use) | `ml/skill-ml-evaluation` |
| Tense/voice questions across the whole paper | `skill-academic-writing` |

## Iron Laws

1. **Report, don't interpret.** "Accuracy was 84.2%" is Results. "This suggests the model generalizes well" is Discussion. Cross the line and a reviewer will (correctly) flag it.
2. **Past tense, third person, active where possible.** "We trained the model on 5,000 examples" not "The model is trained on 5,000 examples" or "It will be shown that…"
3. **Every claim cites a number, table, or figure.** "Performance improved" without "(from 78.3% to 84.2%, see Table 3)" is not Results — it's a wish.

## What Goes Where

| Content | Goes in |
|---|---|
| Descriptive statistics, raw counts, distributions | Results |
| Test statistics, p-values, effect sizes, CIs | Results |
| Tables and figures (with neutral captions) | Results |
| "X was significantly higher than Y" | Results |
| "X was higher because…" | Discussion |
| "This contradicts Smith (2021)…" | Discussion |
| "Implications for practice…" | Discussion |
| "Future work…" | Discussion or Conclusion |
| Limitations | Discussion |

If a sentence answers "why" or "so what," it doesn't belong in Results.

## Statistical Reporting Templates

Use exact, consistent formats. Don't paraphrase the numbers.

### Descriptive statistics (continuous)
> Participants' age ranged from 18 to 64 years (*M* = 32.4, *SD* = 8.1, *N* = 247).

### t-test (independent samples)
> The treatment group (*M* = 4.21, *SD* = 0.83) scored higher than the control group (*M* = 3.74, *SD* = 0.91), *t*(245) = 4.18, *p* < .001, *d* = 0.54, 95% CI [0.28, 0.80].

### One-way ANOVA
> Condition had a significant effect on response time, *F*(2, 144) = 7.83, *p* < .001, η² = 0.10.

### Linear regression
> The model explained 38% of the variance in outcome scores (*R*² = .38, adjusted *R*² = .36, *F*(3, 243) = 49.7, *p* < .001). Years of experience was the strongest predictor (β = 0.42, *p* < .001).

### Logistic regression
> Treatment condition predicted recovery (OR = 2.34, 95% CI [1.62, 3.39], *p* < .001).

### Correlation
> Age and reaction time were positively correlated, *r*(245) = .31, *p* < .001.

### Chi-squared
> The distribution of preferences differed across groups, χ²(2, *N* = 247) = 14.3, *p* < .001, Cramer's *V* = 0.24.

### ML classification
> The model achieved 84.2% accuracy (95% CI [82.1, 86.1]), with macro-F1 = 0.81 and AUROC = 0.89 on the held-out test set (*N* = 1,200). See Table 3 for per-class metrics and Figure 4 for the ROC curves.

### ML regression
> RMSE on the test set was 12.4 (95% CI [11.8, 13.1]), with *R*² = 0.71. Errors did not differ significantly across the four data sources (*F*(3, 1196) = 1.42, *p* = .24).

## Required Reporting Elements

For every analysis, include:

- [ ] Sample size (N or n per group)
- [ ] Test statistic and degrees of freedom
- [ ] Exact p-value (not "p < .05" — "p = .003" or "p < .001" if very small)
- [ ] Effect size (Cohen's *d*, η², OR, *r*², etc.)
- [ ] 95% confidence interval where applicable

Missing any of these is a defect. Reviewers will ask. APA, AMA, and most ML conferences now require effect sizes and CIs.

## Tense and Voice

| Doing what | Tense | Example |
|---|---|---|
| Reporting your own actions and findings | Past | "We collected data from 247 participants" |
| Describing what a figure or table shows | Present | "Figure 3 shows the distribution of scores" |
| Stating a generally established fact | Present | "Cohen's *d* of 0.5 represents a medium effect" |

Active voice where possible: "We trained the model" beats "The model was trained." Passive is acceptable when the agent is unimportant: "Data were collected via online survey."

## Figures vs Tables vs Prose

A reasonable split for most thesis Results sections:

| Use | When |
|---|---|
| **Prose** | Headline numbers (1–4 per analysis); the story-carrying claims |
| **Table** | Multiple groups, multiple metrics, exact values matter, comparisons |
| **Figure** | Trends, distributions, relationships, model curves (ROC, learning curves) |

Rule: every prose claim should be **anchored** to a table or figure. Every table or figure should be **referenced** in prose. Orphan tables (never mentioned) and orphan claims (no source) are both defects.

For figure/table design see `skill-figures-and-tables`.

## Skeleton for a Results Section

A common structure that scales from a paper to a thesis chapter:

1. **Sample / dataset characteristics** — who/what was studied, descriptive stats
2. **Manipulation or model checks** — did the intervention or training do what it should?
3. **Primary analyses** — addresses your main RQs/hypotheses, in the order they were stated
4. **Secondary / exploratory analyses** — clearly labeled as exploratory
5. **Robustness checks** — sensitivity analyses, ablations, alternative specifications

For each subsection: state the question, the test, the result, and point to the table/figure. No interpretation.

## Worked Example — From Stub to Discipline

**Bad (interprets, hedges, no numbers):**
> The model performed well overall, doing especially well on the training data, which suggests it learned the patterns effectively. Accuracy was reasonable on the test set too.

**Good (reports, anchored, no interpretation):**
> The model achieved 96.4% accuracy on the training set and 84.2% (95% CI [82.1, 86.1]) on the held-out test set (N = 1,200; Table 3). Macro-F1 was 0.81 and AUROC was 0.89. Per-class metrics ranged from F1 = 0.74 (Class C, n = 180) to F1 = 0.88 (Class A, n = 540).

The improved version is two sentences and conveys five times as much. The original does the work of zero sentences.

## Common Failure Modes

| Pattern | Why it's a defect |
|---|---|
| "The results show that…" with no numbers in the sentence | Empty calorie — adds words, no information |
| Mixing past and present tense within a paragraph | Distracting; review for consistency |
| `p < .05` without effect size | Significance ≠ magnitude |
| Reporting only the significant tests | Cherry-picking; report what was preregistered or planned |
| Re-stating values from a table verbatim | The table is the source; prose should highlight, not duplicate |
| "Surprisingly," "Interestingly," "As expected" | All interpretation — move to Discussion |
| Walls of statistics with no narrative | Reader can't find the story; group by RQ, lead with headline |

## Pre-Submission Checklist

- [ ] Every claim has a number, table, or figure backing it
- [ ] No interpretation crept in (search for: "suggests", "implies", "because", "due to", "consistent with")
- [ ] All statistics include sample size, test, df, p-value, effect size, CI
- [ ] Tense is past for actions/findings; present for figure/table descriptions
- [ ] Every figure and table is referenced in prose, in order
- [ ] Significant *and* non-significant planned analyses are reported
- [ ] Reporting style matches journal/department guidelines (APA 7, AMA, IEEE, etc.)
- [ ] Run `skill-avoid-ai-writing` over the section before submission

## Integration

- `skill-discussion-writing` — where everything you wanted to say but couldn't goes
- `skill-figures-and-tables` — design of the artifacts this section anchors to
- `skill-thesis-structure` — places this section within the larger document
- `skill-academic-writing` — tense, voice, person rules across the whole paper
- `skill-avoid-ai-writing` — Results sections are AI-tell-prone; run this before submission
- `skill-citation-management` — citing prior reported numbers correctly
- `ml/skill-ml-evaluation` — choosing which metrics to compute (input to this skill)
- `ml/skill-explainability` — error analysis content suitable for Results

## Resources

- [APA 7 Statistical Guidelines](https://apastyle.apa.org/style-grammar-guidelines/tables-figures/statistical-tables)
- [Reporting Statistics in APA Style](https://my.ilstu.edu/~jhkahn/apastats.html)
- [TRIPOD reporting guidelines (for clinical prediction models)](https://www.tripod-statement.org/)
