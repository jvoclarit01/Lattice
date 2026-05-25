---
name: skill-contribution-checker
description: Verifying that the contributions claimed in the Introduction and Conclusion are genuinely novel, supported by the work, and correctly typed (technical vs empirical vs theoretical vs artifact). Use when drafting the Contributions list, before submitting a paper or thesis, or when an advisor questions whether a claim is "new enough." For checking the logical chain that supports a contribution claim see `skill-argument-validator`.
---

# Contribution Checker

The Introduction promises contributions; the rest of the thesis must deliver them. This skill audits that promise — both for novelty and for fit. A "contribution" that is actually re-discovery or that the experiments don't support is a defense liability.

## When to Activate

Use when:
- Drafting the contributions bullet list in the Introduction
- Drafting the contribution restatement in the Conclusion
- A reviewer asks "what is actually novel here?"
- An advisor says the contributions feel "thin" or "overstated"
- Submitting to a venue that explicitly evaluates novelty (top-tier ML, mathematics, theoretical CS)
- Comparing your work against a recently published paper that looks similar

**Trigger phrases:** "what's novel", "verify contributions", "is this new", "contribution audit", "compare to prior work", "is this enough for a thesis"

## When NOT to Use

| Situation | Use instead |
|---|---|
| Checking whether evidence supports a claim | `skill-argument-validator` |
| Polishing the prose of a contribution statement | `skill-academic-writing` |
| Writing the Introduction itself | `skill-introduction-writing` |
| Writing the Conclusion's contribution synthesis | `skill-conclusion-writing` |
| Surveying prior work to identify the gap | `skill-literature-review` |
| Evaluating method rigor | `skill-research-methodology` |

## Iron Laws

1. **A contribution is a delta from prior art.** State the prior art and the delta; "we propose X" without context is not a contribution claim.
2. **Each claimed contribution must trace to a specific Results subsection.** If a contribution has no experiment, table, or proof in the body, it cannot live in the Introduction.
3. **Type the contribution honestly.** Engineering artifacts ("we built a system") are valid contributions, but should not be sold as theoretical or empirical contributions.
4. **Three solid contributions beat seven thin ones.** Reviewers count the strongest, not the most.

## The 4-Question Contribution Test

Run every claimed contribution through these four questions. If any answer is "no" or "unsure," the contribution needs revision.

| # | Question | What "no" means |
|---|---|---|
| 1 | **Novel?** Is there prior work doing the same thing in the same setting? | If yes, the contribution is incremental — scope it as such or drop it |
| 2 | **Supported?** Is there a Results subsection, theorem, or artifact in the thesis that demonstrates it? | If no, either add the experiment or remove the claim |
| 3 | **Significant?** Would a reasonable peer in the subfield care? Why? | If no, fold into a larger contribution or drop |
| 4 | **Correctly typed?** Is "novel method" actually a novel method, or a known method applied to a new dataset? | Mistyping is the most common defense rejection reason |

The four-question test is the minimum bar. Any contribution that survives all four can be defended. Any that fails one is a liability.

## Contribution Types — Choose the Right Label

Mistyping a contribution is the most common reviewer flag. The four canonical types in CS / empirical theses:

| Type | What it is | Example | Failure when mistyped |
|---|---|---|---|
| **Technical / methodological** | A new algorithm, model, or technique | "We propose a sparse-attention layer that reduces FLOPs by 40%" | Mistyped as theoretical → reviewer wants proofs |
| **Empirical** | A new finding about how something behaves | "We show that domain pretraining gives diminishing returns past 10M tokens" | Mistyped as theoretical → reviewer wants formal analysis |
| **Theoretical** | A proof, theorem, or new theoretical framework | "We prove convergence of method M under condition C" | Mistyped as technical → reviewer wants empirical validation |
| **Artifact / system** | A reproducible system, dataset, benchmark, or tool | "We release CleanBench, a 200K-sample benchmark for…" | Mistyped as method → reviewer asks "what is the algorithmic novelty?" |

A single thesis usually combines two or three types. Be explicit about which is which.

## Novelty Verification Procedure

Before claiming novelty, run this procedure:

1. **Search the obvious venues.** The top three conferences/journals in the subfield, last 3 years.
2. **Search by problem, not by solution.** Authors who solved the same problem differently still count as prior art.
3. **Read the abstracts of the top 5 most-cited papers in the area from the last 24 months.** New work hides in the recency window.
4. **Search Google Scholar with two query rewrites:** your title's keywords; a paraphrase of the contribution.
5. **Check workshop and arXiv preprints.** Concurrent work matters for novelty framing even if not yet refereed.
6. **Cite the closest prior art and write one sentence on the delta.** "Smith (2024) studied X in setting A; we extend to setting B by C."

If you cannot find any closely related work, that is itself a flag — either you are looking in the wrong place or the problem is too narrow to be a contribution.

## Calibrated Contribution Language

Match the language to the actual delta. Reviewers calibrate against this.

| Delta | Language |
|---|---|
| New problem and a method to solve it | "We introduce X and propose…" |
| Existing problem, new method | "We propose a method that…" |
| Existing method, new domain | "We adapt M to setting S, showing…" |
| Existing method, new analysis | "We provide the first empirical study of M on S, finding…" |
| Existing method, more thorough evaluation | "We benchmark M across N settings, identifying…" |
| Replication of prior result | "We replicate and extend (Smith, 2022) to…" |
| Negative result | "We show that the expected gain from M does not transfer to…" |

Negative and replication results are real contributions. Frame them honestly; do not dress them up as new methods.

## Worked Examples

**Bad (vague, untyped, unsupported):**
> Our main contributions are: (1) a novel approach to NLP, (2) state-of-the-art results, (3) new insights into transformer behavior.

Audit:
- "Novel approach to NLP" — too vague to be auditable; what problem in NLP?
- "SOTA results" — on which benchmark, beating which baseline?
- "New insights into transformer behavior" — typed as empirical but no analysis chapter referenced.

**Good (typed, scoped, supported):**
> This thesis makes three contributions:
> (1) **Method.** We propose Hierarchical Sparse Attention (HSA), an attention variant that reduces FLOPs by 38% on long-context inputs (Chapter 4, §4.3).
> (2) **Empirical.** We show that HSA matches dense-attention performance on five long-context benchmarks (Table 5.1) while degrading gracefully on inputs beyond training length (§5.4) — a behavior not observed in prior sparse-attention work.
> (3) **Artifact.** We release HSA-Bench, a benchmark of 12K naturally-long-context examples drawn from legal and scientific corpora (Appendix B).

Each contribution is typed, scoped to evidence, and points at a specific section.

## Contribution Statement Templates

Use the structure that matches your dominant contribution type. Fill in the slots; do not paraphrase.

### Method-dominant
> This thesis proposes [METHOD], which [WHAT IT DOES]. Unlike prior work that [LIMITATION OF PRIOR ART], [METHOD] [KEY DELTA]. We evaluate [METHOD] on [DATASETS], showing [QUANTITATIVE RESULTS]. The contributions are: (1) [METHODOLOGICAL CONTRIBUTION]; (2) [EMPIRICAL CONTRIBUTION]; (3) [ARTIFACT, IF ANY].

### Empirical-dominant
> Despite [PRIOR ASSUMPTION], the behavior of [SYSTEM] under [CONDITION] has not been systematically studied. This thesis provides [SCOPE OF EMPIRICAL STUDY]. We find that [PRIMARY FINDING] and [SECONDARY FINDING], contradicting [PRIOR EXPECTATION] / extending [PRIOR FINDING]. The contributions are: (1) [STUDY DESIGN AND DATASET]; (2) [PRIMARY EMPIRICAL FINDING]; (3) [SECONDARY FINDING OR IMPLICATION].

### Theoretical-dominant
> We study [PROBLEM]. Existing analyses [LIMITATION]. This thesis develops [FRAMEWORK / PROOF TECHNIQUE] and proves [THEOREM]. The contributions are: (1) [THEORETICAL CONTRIBUTION]; (2) [COROLLARY OR IMPLICATION]; (3) [EMPIRICAL VALIDATION OF THE THEORY].

## Common Failure Modes

| Pattern | Consequence |
|---|---|
| "Novel framework" without naming the prior frameworks it differs from | Reviewer cannot evaluate novelty |
| Five contributions where two would do | Each contribution defended too thinly |
| Contribution claimed in Introduction does not match any Results subsection | Reviewer questions integrity |
| Empirical contribution mistyped as theoretical | Mismatch with reviewer expectations; rejection |
| "We are the first to…" without an exhaustive prior-art search | Concurrent or prior work surfaces; credibility damage |
| System contribution sold as method contribution | Reviewer asks "what is the algorithmic insight?" — none exists |
| Contributions list = Methods table of contents | Conflates work done with delta from prior work |
| Negative result framed as positive | Loses honesty credit; reviewers detect the inversion |

## Pre-Submission Contribution Checklist

- [ ] Each contribution has a type label (method / empirical / theoretical / artifact)
- [ ] Each contribution traces to at least one Results / Theorem / Artifact section
- [ ] Each contribution is bounded ("on benchmarks A and B" not "in NLP")
- [ ] Closest prior art is cited and the delta is stated
- [ ] No more than 3–5 contributions; thin ones are merged or cut
- [ ] Language matches the size of the delta (calibration table above)
- [ ] Concurrent work in the last 12 months has been searched
- [ ] Negative results, if any, are framed as such
- [ ] The Conclusion's contribution restatement matches the Introduction's verbatim or is a clear superset

## Integration

- `domains/thesis/skill-introduction-writing` — Introduction is where contributions are first stated
- `domains/thesis/skill-conclusion-writing` — Conclusion restates contributions; this skill ensures alignment
- `domains/thesis/skill-argument-validator` — checks that the evidence supports the claim once novelty is verified
- `domains/thesis/skill-literature-review` — provides the prior-art map this skill compares against
- `domains/thesis/skill-discussion-writing` — Discussion frames the significance dimension of contributions
- `domains/thesis/skill-thesis-structure` — routes contribution claims to the right chapters
- `domains/thesis/skill-academic-writing` — calibrated language for contribution claims

## Resources

- [Lipton & Steinhardt, *Troubling Trends in Machine Learning Scholarship*](https://arxiv.org/abs/1807.03341) — surveys mistyped and overstated contributions
- [NeurIPS Reviewer Guidelines (Soundness/Significance/Novelty)](https://nips.cc/Conferences/2024/ReviewerGuidelines) — operationalization of how reviewers grade novelty
- [The 3-Sigma Rule in CS Papers (Patrick Cousot, ICSE)](https://www.di.ens.fr/~cousot/publications.www/CousotCousot-ICSE-79.pdf) — example of clear contribution typing
- [How to Read a Paper (S. Keshav)](https://web.stanford.edu/class/ee384m/Handouts/HowtoReadPaper.pdf) — useful framing for the inverse: how reviewers extract your contributions
