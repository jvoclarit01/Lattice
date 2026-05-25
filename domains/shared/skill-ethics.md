---
name: skill-ethics
description: Ethics framework for any project that affects people — impact analysis, transparency, privacy, accountability, and human oversight. Use BEFORE building, when handling personal data, automating consequential decisions, or facing "should we build this?" questions. For ML-specific bias detection see ml/skill-bias-and-fairness; for ML explanations see ml/skill-explainability.
---

# Ethics & Responsibility

This skill is the *framework* — what to assess, when to escalate, who to involve. ML-specific implementation (fairness metrics, model explanations, privacy techniques like differential privacy) lives in the ml domain.

## When to Activate

Use BEFORE building, and at every release thereafter, when:
- The system makes or aids a decision about a person (hiring, lending, medical, criminal justice, education, housing, insurance)
- Personal data or PII is collected, stored, or processed
- The system can be misused to harm someone (deepfakes, surveillance, manipulation)
- The system affects access to opportunity (recommendations, ranking, allocation)
- A regulator, ethics board, or affected community has standing to ask "is this OK?"

**Trigger phrases:** "is this ethical?", "should we build this?", "GDPR / HIPAA / FERPA", "fairness concerns", "privacy implications", "responsible AI", "consent", "harm"

## When NOT to Use

- Implementing fairness metrics → `ml/skill-bias-and-fairness`
- Producing model explanations → `ml/skill-explainability`
- Threat modeling for security → `shared/skill-security`
- Compliance documentation specifics → consult legal/compliance, not this skill

## The Five Pillars

1. **Fairness** — Identify who is affected and ensure outcomes don't disproportionately harm any group
2. **Transparency** — Document how the system works at a level matching the stakes
3. **Accountability** — Someone owns the outcome; someone can be appealed to
4. **Privacy** — Collect minimum necessary; protect what's collected; honor consent
5. **Safety** — Test failure modes, ensure human oversight where stakes are high

These are not optional steps. Skipping one is a defect.

## The Pre-Build Question

Before you write the first line, answer these:

1. **Who could be harmed?** Name specific groups, including non-users (people the system makes decisions about without their participation).
2. **What's the worst plausible failure?** Not the worst imaginable — the worst plausible. If it's "someone is wrongly denied a loan," that's different from "someone dies."
3. **Is automation the right answer here?** Some decisions deserve human judgment, even if AI could approximate them.
4. **What recourse do affected parties have?** If your answer is "they can email support," that's not recourse.
5. **Who at this org owns the decision to deploy?** If no one's name is on it, the system isn't ready.

If any of these is unanswered, the project isn't ready to start.

## Phase 1 — Impact Analysis

Document, in this order:
- **Intended use cases** (what the system is FOR)
- **Foreseeable misuse** (what bad actors do with it; what well-intentioned users misapply it to)
- **Affected populations** (users, subjects, third parties)
- **Severity tiers** for failure modes (financial loss, dignitary harm, physical safety, irreversible decisions)
- **Risk tolerance** for each tier (zero tolerance for some — stop and reconsider)

This document is the basis for every subsequent decision.

## Phase 2 — Bias & Fairness Audit

What to assess (each of these is a defect if present):
- **Representation gaps** in training/eval data — are protected groups underrepresented?
- **Historical encoding** — does the data reflect past discrimination the system would now perpetuate?
- **Measurement parity** — are features measured consistently across groups?
- **Performance parity** — does the system work as well for each group?
- **Outcome parity** — are decisions distributed in proportion to ground-truth need?

For implementation (fairlearn metrics, mitigation strategies), see `ml/skill-bias-and-fairness`. This skill governs *whether* to do the audit and *what counts as failing* it.

The 80% rule (4:1 disparate impact ratio) is a legal floor in some jurisdictions, not a goal — aim for parity, not just legal cover.

## Phase 3 — Transparency

Two audiences, two levels of detail:

**Affected users / public:**
- Plain-language description of what the system does and what data it uses
- The decision space: what kinds of outcomes are possible
- A path to human review for adverse decisions
- A clear statement of what the system *does not decide*

**Internal / regulatory:**
- Full model documentation (`ml/skill-model-description`'s model card)
- Training data provenance (`ml/skill-data-collection` for ethics; `thesis/skill-dataset-documentation` for cards)
- Known limitations and failure modes
- Audit trail of decisions and version history

If you can't explain the system at the user level in two sentences, you have a transparency problem.

## Phase 4 — Privacy

Defaults that protect:
- **Collect the minimum** that achieves the stated purpose. "We might use it later" is not a justification.
- **Pseudonymize at intake** when you can — store an opaque ID, keep the linkage table separate and access-controlled.
- **Encrypt at rest and in transit.** Default for everything personal, not opt-in.
- **Retention has an end date.** "Forever" is a policy failure.
- **Access is logged.** If you can't say who looked at a record and when, you don't actually control access.

Consent is necessary but not sufficient — design a system that protects users even if consent was poorly informed.

For technical implementation (differential privacy, federated learning, secure aggregation), see specialized resources or domain-specific skills.

## Phase 5 — Safety & Oversight

Where stakes are high, automation must be paired with:
- **Confidence thresholds** — below threshold, route to human
- **Human-in-the-loop** for irreversible or high-impact decisions
- **Override mechanisms** — humans can countermand the system without bureaucratic overhead
- **Monitoring for drift** — fairness and accuracy degrade over time (`ml/skill-monitoring`)
- **Incident response** — when the system harms someone, what's the playbook?

"AI has final say" is rarely the right design for consequential decisions. Even when it's the *fastest* design.

## Stop-the-Line Conditions

If any of these are true, do not deploy:
- Disparate impact ratio worse than 4:1 with no defensible justification
- A user-affecting failure mode has no detection mechanism
- A user-affecting failure mode has no recourse path
- The training data was collected without consent and the use case is novel
- The deploy team can't name the person accountable for harm

These are not "address before launch" — they are "do not launch."

## Integration

- `ml/skill-bias-and-fairness` — implements Phase 2 with concrete metrics & mitigation
- `ml/skill-explainability` — implements Phase 3 transparency for ML systems
- `ml/skill-monitoring` — implements Phase 5 drift detection
- `ml/skill-data-collection` — ethical data collection upstream of any of this
- `shared/skill-security` — privacy is a subset of security; threat-model accordingly
- `shared/skill-self-review` — request an ethics-focused review before launch
- `thesis/skill-research-methodology` — IRB / ethics statement for thesis work

## Resources

- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [OECD AI Principles](https://www.oecd.org/ai/)
- [Algorithmic Impact Assessment (Government of Canada)](https://www.canada.ca/en/government/system/digital-government/digital-government-innovations/responsible-use-ai/algorithmic-impact-assessment.html)
- [Datasheets for Datasets](https://arxiv.org/abs/1803.09010)
- [Model Cards for Model Reporting](https://arxiv.org/abs/1810.03993)
