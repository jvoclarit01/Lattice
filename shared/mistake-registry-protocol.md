---
name: mistake-registry-protocol
description: Lattice mistake registry protocol. Details the SQLite schema, signature hashing, pre-execution hooks, and remediation rules for agent mistakes.
---

# Mistake Registry Protocol

The Mistake Registry is a SQLite-backed persistence layer that records, categorizes, and mitigates errors made by agents to prevent repeat failures.

## 1. Database Schema

The registry database is stored under `.lattice/mistakes.db` with the following schema:

```sql
CREATE TABLE IF NOT EXISTS mistake_registry (
    id TEXT PRIMARY KEY,
    signature_hash TEXT UNIQUE NOT NULL, -- SHA-256 of error_type | file_pattern | tool_sequence | param_shape
    first_seen TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    occurrence_count INTEGER NOT NULL DEFAULT 1,
    context_snapshot TEXT NOT NULL,      -- JSON containing system state and relevant logs
    fix_applied TEXT NOT NULL,           -- JSON containing code change diffs or command fixes
    pattern_extracted TEXT NOT NULL,     -- Description of the mistake pattern and how to avoid it
    severity TEXT NOT NULL CHECK(severity IN ('warn', 'block', 'escalate'))
);
```

---

## 2. Signature Hashing

To match a new error against registered mistakes, Lattice computes a SHA-256 hash using the following pipe-delimited values:
1. `error_type`: E.g., `compiler_error_ts2322`, `command_exit_1`, `lint_failure`.
2. `file_pattern`: Glob pattern of the affected file(s).
3. `tool_sequence`: Sequence of the last 3 tools called before the error.
4. `param_shape`: Keys/arguments structure of the tool that triggered the error.

---

## 3. Severity & Mitigation Rules

When a signature match is detected, Lattice executes based on the `severity` level:

### `warn`
- **Behavior**: Appends a warning message to the active agent prompt.
- **Action**: Alert the agent to use caution in the specific file or tool call.

### `block`
- **Behavior**: Intercepts the tool execution *before* it runs on the host.
- **Action**: Returns a structured fix directly to the agent without invoking the tool. The agent is forced to rewrite the tool call or modify the target file first.

### `escalate`
- **Behavior**: Immediately pauses autonomous execution.
- **Action**: Raises a prompt dialog to the operator explaining the mistake pattern and asks for manual guidance.

---

## 4. Lifecycle

- **Append-Only**: The mistake registry is append-only.
- **No Decay**: Mistake records do not decay or expire over time.
- **Evolution**: If an error is solved in a new way, the `fix_applied` and `pattern_extracted` columns are updated to capture the optimal remedy.
