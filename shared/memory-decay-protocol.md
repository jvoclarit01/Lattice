---
name: memory-decay-protocol
description: Lattice memory decay protocol. Outlines the math-based rules governing memory retention tiers, decay curves, reinforcement, and consolidation.
---

# Memory Decay Protocol

Lattice operates on an Ebbinghaus-style forgetting curve model to manage agent memory, ensuring relevant experiences stay active while obsolete details fade.

## 1. Memory Tiers

Agent memory is partitioned into four distinct tiers, each with unique retention profiles:

| Tier | Lifecycle / Half-Life | Purpose |
|---|---|---|
| **Episodic** | 7 days half-life | Short-term context, recent execution logs, and run-specific details. |
| **Procedural** | 90 days half-life | Workflows, workflow habits, styling preferences, and structural choices. |
| **Mistakes** | Infinite (Never decays) | Registry of errors, bugs, and incorrect tool calls. Always checked. |
| **Vault** | Infinite (Immutable) | User instructions, locked configurations, and critical security profiles. |

---

## 2. Retention Mechanics

### The Decay Formula
The strength of a memory $S$ at time $t$ (in days) is calculated as:

$$S(t) = S_0 \cdot e^{-t \cdot \frac{\ln(2)}{h}} \cdot M_i$$

Where:
- $S_0$: Initial memory strength (default: `1.0`).
- $h$: Half-life in days (e.g., `7.0` for Episodic, `90.0` for Procedural).
- $M_i$: Importance multiplier (default: `1.0`, configured via tags or pinning).

### Access Boost
Every time a memory is read, accessed, or verified during a step:
- Strength is incremented: $S_{new} = \min(S_{current} + 0.20, 1.0)$.
- The timestamp of last access is updated, resetting the decay clock.

---

## 3. Thresholds & Forgetting

- **Forget Threshold (`0.15`)**: If $S(t) < 0.15$, the memory is hidden from active context.
- **Tombstone State**: Forgotten memories are placed in a tombstone index for 7 days. If referenced or manually retrieved within this window, they are revived with $S = 0.50$. After 7 days in the tombstone state, they are permanently pruned.

---

## 4. Consolidation

Episodic memories that are reinforced repeatedly are promoted to the Procedural tier:
- **Rule**: If an episodic pattern or behavior is successfully applied $\ge 5$ times within a rolling 30-day window, it consolidates into a permanent procedural rule ($h = 90$).

---

## 5. Memory Pinning

Operators can manually pin memory objects to prevent decay:
- **Command**: `lattice memory pin <id> --importance 3.0`
- **Effect**: Sets $M_i = 3.0$, scaling the retention curve and preventing it from falling below the forget threshold for an extended duration.
