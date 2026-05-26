---
name: skill-scripting
description: Custom automation scripting discipline for Python and JavaScript/Node.js. Details hard loop iteration count safety boundaries, sorted keys schema drift checkers, JIT credentials ingestion, rate limit backoffs, and X-Workflow-Depth headers. Use when writing, refactoring, or reviewing scheduled scripts, API integrations, data sync loops, or command-line cron jobs.
---

# Scripting — Custom Automation Discipline

Custom scripts (Python/JS) offer maximum flexibility, but easily trigger infinite runtime loops, suffer from unhandled schema drift, or fail silently under rate-limit throttling. This skill enforces strict execution boundaries and defensive scripting.

## When to Activate

Use when:
- Writing scheduled cron jobs in Python or Node.js
- Scripting ETL pipelines or data synchronization triggers
- Writing custom webhook endpoints using lightweight libraries (Flask, FastAPI, Express)
- Implementing custom API clients and loops
- Debugging memory leaks or rate-limit blocks in running scripts

**Trigger phrases:** "Python script", "Node script", "cron job script", "data sync script", "X-Workflow-Depth", "loop safety limit", "infinite recursion"

## Iron Laws

1. **Every loop must have a hard boundary.** Never write `while True:` or unbounded loops. Every loop must be bound by a maximum iteration count or an explicit timeout context.
2. **Validate schemas with sorted keys fingerprints.** Use a zero-dependency path-sorting function at the ingestion gate to detect third-party API schema drift instantly.
3. **Respect rate-limiting backpressure.** Parse `Retry-After` headers and inject random-jitter backoffs; do not spam upstream APIs.
4. **Propagate execution-depth headers.** Webhooks and API calls triggered by scripts must pass `X-Workflow-Depth` to prevent runaway cross-platform recursion.

---

## Unbounded Loop Safety-Valves

Unbounded loops lead to resource exhaustion and runaway API billing. Implement safety bounds at compile/write time:

### 1. Hard Iteration Safety-Valve
```python
# GOOD: Explicit loop index ceiling
MAX_ITERATIONS = 1000
for i in range(MAX_ITERATIONS):
    process_batch()
    if no_more_data():
        break
else:
    # Executes if loop completes without breaking
    raise Exception("Loop safety threshold exceeded! Forcefully terminating execution.")
```

### 2. Time-Bound Execution (Context Managers)
In Python, wrap high-volume loops in a signal-based timeout or a simple execution check:
```python
import time

start_time = time.time()
TIMEOUT_SECONDS = 300  # 5 minutes

while data_available():
    if time.time() - start_time > TIMEOUT_SECONDS:
        raise TimeoutError("Script execution timeout reached. Saving partial progress and exiting.")
    process_data()
```

---

## Schema Drift Guard (Zero-Dependency Python Implementation)

Compare sorted, flattened JSON path keys against a hardcoded signature to detect structural drift:

```python
def flatten_keys(obj, prefix=""):
    keys = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            pre = f"{prefix}." if prefix else ""
            keys.update(flatten_keys(v, f"{pre}{k}"))
    elif isinstance(obj, list):
        # Flatten array elements under a generic list index
        for idx, item in enumerate(obj[:1]): # Check first item template only
            pre = f"{prefix}[]"
            keys.update(flatten_keys(item, pre))
    else:
        # Append data type name
        keys[prefix] = type(obj).__name__
    return keys

def verify_schema(payload, expected_signature):
    flattened = flatten_keys(payload)
    # Sort and join to form signature
    sorted_keys = sorted(f"{k}:{v}" for k, v in flattened.items())
    actual_signature = ",".join(sorted_keys)
    return actual_signature == expected_signature

# Example verification:
expected_sig = "user.active:bool,user.age:int,user.name:str"
if not verify_schema(incoming_payload, expected_sig):
    raise ValueError("Upstream API schema drift detected! Terminating ingest.")
```

---

## Ingest Loop Prevention (Depth Forwarding)

Webhooks calling scripts that trigger other webhooks can enter circular loops. Block recursion:

```javascript
// Express Webhook Receiver Ingestion Gate (Node.js)
app.post('/webhook', (req, res) => {
  const depth = parseInt(req.headers['x-workflow-depth'] || '1', 10);
  const MAX_DEPTH = 5;

  if (depth > MAX_DEPTH) {
    console.error("Workflow loop aborted! Depth limit exceeded.");
    return res.status(429).send("Too many workflow hops.");
  }

  // Forward incremented depth to downstream API
  const downstreamHeaders = {
    'X-Workflow-Depth': (depth + 1).toString(),
    'X-Workflow-Execution-ID': req.headers['x-workflow-execution-id'] || generateUuid()
  };

  triggerDownstreamAPI(downstreamHeaders);
  res.status(200).send("Accepted");
});
```

---

## Review Checklist

- [ ] **Loop Safety-Valve:** Does every loop have a defined maximum count (`MAX_ITERATIONS`) or a time-out check?
- [ ] **Secrets Isolated:** Are credentials loaded JIT from environment parameters, rather than committed as hardcoded strings?
- [ ] **Idempotency Keys:** Does the script check a database constraint or local lock state before performing mutations?
- [ ] **Schema Drift Gate:** Is the sorted keys comparison function active at the ingestion entry point?
- [ ] **Depth Header:** Does the script forward `X-Workflow-Depth` in all outbound API requests?
- [ ] **Retry with Jitter:** Do API request catch blocks implement exponential backoff with random jitter?
