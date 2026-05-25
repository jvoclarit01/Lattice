---
name: skill-performance
description: General performance methodology — measure first, find the actual bottleneck, optimize the critical path, verify the win, monitor for regression. Domain-agnostic discipline that applies to web apps, ML pipelines, backend services, data analysis. For domain-specific performance work see webdev/skill-performance, ml/skill-training, ml/skill-model-serving.
---

# Performance — General Methodology

This skill is *how to think about performance*, not which lever to pull in which framework. The discipline is universal; the specifics live in domain skills.

## When to Activate

Use when:
- Something is "slow" and you don't yet know why
- You're tempted to "just optimize it" without measuring
- A performance target is set and you need a plan to hit it
- A regression appeared in production
- Reviewing a teammate's optimization PR

**Trigger phrases:** "this is slow", "optimize this", "performance bottleneck", "scale this", "why is X slow", "regression in latency"

## When NOT to Use

| Situation | Use instead |
|---|---|
| Web Core Web Vitals, bundle size, frontend perf | `webdev/skill-performance` |
| ML training throughput, GPU utilization | `ml/skill-training` |
| Model inference latency, batching, serving | `ml/skill-model-serving` |
| Database query optimization specifics | `webdev/skill-database` |
| Production monitoring & alerting | `webdev/skill-observability` / `ml/skill-monitoring` |

## Iron Laws

1. **Measure before you optimize. Measure after you optimize.** No exceptions. "Should be faster now" is not a measurement.
2. **The fastest code is the code that doesn't run.** Optimize by removing work, not by speeding up unnecessary work.
3. **Optimize the critical path, not the easy path.** Saving 10ms on the 1% case while ignoring the 99% case is malpractice.

## The Loop

```
┌─────────────────────────────────────────────────┐
│  1. Define the target (what "fast enough" means)│
│  2. Measure the current state                    │
│  3. Profile to find the actual bottleneck        │
│  4. Hypothesize a fix                            │
│  5. Implement ONE change                         │
│  6. Measure again                                │
│  7. Decide: keep, revert, or iterate             │
└─────────────────────────────────────────────────┘
```

Step 5 is "ONE change" because if you ship five at once, you don't know which one mattered. You'll inherit two improvements and three regressions and never separate them.

## Step 1 — Define the Target

A target without a number is a wish.

| Bad target | Good target |
|---|---|
| "Make it fast" | "P95 latency under 200ms at 1000 RPS" |
| "Reduce memory" | "Stay under 512MB resident with 10k concurrent users" |
| "Improve load time" | "LCP under 2.5s on 3G simulation" |

Targets must be:
- **Quantified** — a number with a unit
- **At a percentile** — averages hide the long tail; P95/P99 reveal it
- **Under a load** — performance under no load is meaningless

## Step 2 — Measure Honestly

The first measurement is the baseline. Save it.

Common measurement mistakes:
- Measuring on a warm cache when production sees cold caches
- Measuring localhost when production has network round-trips
- Running once instead of N times — first-run noise dominates
- Mixing build-time and run-time measurements
- Forgetting to include the work that surrounds the work (auth, parsing, serialization)

Run the measurement at least 10 times. Report median or P95, not mean (means are sensitive to outliers).

## Step 3 — Profile, Don't Guess

Profilers tell you where the time actually goes. Almost always, it's not where you thought.

| Stack | Tool |
|---|---|
| Python | `cProfile`, `py-spy`, `scalene` (cpu+mem+gpu) |
| Node.js | `node --prof`, Chrome DevTools, `clinic.js` |
| Go | `go tool pprof` |
| Java/JVM | async-profiler, JFR |
| Browser | Chrome DevTools Performance tab |
| Database | `EXPLAIN ANALYZE` (Postgres), `EXPLAIN` (MySQL/MongoDB) |

```python
import cProfile, pstats
profiler = cProfile.Profile()
profiler.enable()
expensive_function()
profiler.disable()
pstats.Stats(profiler).sort_stats("cumulative").print_stats(20)
```

What to look for:
- The top 1-3 functions by cumulative time — that's the critical path
- Functions called millions of times — algorithmic complexity issue
- Lock contention, GC pauses, syscalls — qualitative bottlenecks profilers reveal

## Step 4 — Hypothesize

Before you change anything, write down:
- What you think is slow
- Why you think so (cite the profile)
- What change you're going to try
- What you expect the impact to be (quantify)

If reality doesn't match the prediction, your mental model is wrong — investigate that, don't paper over it with another change.

## Step 5 — Change ONE Thing

Common high-impact changes (in rough order of leverage):
- **Algorithmic improvement** — O(n²) → O(n log n) beats any constant-factor optimization
- **Avoid the work** — cache, memoize, lazy-load, batch
- **Reduce I/O** — fewer DB queries, smaller payloads, fewer network round-trips
- **Parallelize** — concurrency for I/O-bound, parallelism for CPU-bound
- **Use the right data structure** — hash for lookups, heap for top-k, etc.
- **Constant-factor tuning** — only after the above; usually <2× wins

## Step 6 — Measure Again

Same methodology as Step 2. Compare to baseline.

If the change didn't help (or made things worse): revert it. Don't rationalize keeping a "should be better" change.

If it helped less than predicted: your model is incomplete. Profile again before continuing.

## Common Anti-Patterns

| Pattern | Why it fails |
|---|---|
| "Cache everything" | Cache invalidation is hard; stale data is a bug; cache hit ratio matters more than cache size |
| "Add more workers" | Scales until it doesn't (DB contention, lock thrashing, network saturation) |
| Premature micro-optimization | Inlining a function while the DB query takes 90% of time |
| Optimizing benchmarks instead of users | Faster microbenchmark, identical or worse end-to-end UX |
| Optimizing one request type while ignoring the mix | Fixing the 1% expensive endpoint while the 99% endpoint regresses 10% |
| Removing instrumentation "for performance" | You will need it back the next time something breaks |

## Common Real Bottlenecks

These show up in nearly every system, in roughly this order of frequency:

1. **N+1 queries** — fix with eager-load / batch / join
2. **Missing or wrong index** — fix with `EXPLAIN ANALYZE` and a focused index
3. **Synchronous I/O on the hot path** — make it async, parallel, or batch
4. **Re-rendering / re-computing instead of caching** — memoize, cache, dedupe
5. **Serialization overhead** — JSON for hot internal RPCs is often a tax
6. **Excessive payload size** — compress, paginate, project only needed fields
7. **Lock contention** — narrow critical sections, sharding, lock-free structures
8. **Memory pressure** — leaks, oversized caches, oversized batch sizes triggering GC

For domain-specific implementations of the fixes, see the domain performance skills.

## Step 7 — Lock In, Then Watch

After a fix lands:
- Add a regression test or benchmark that catches the bug returning
- Add monitoring that alerts before users notice (`webdev/skill-observability`, `ml/skill-monitoring`)
- Document why you made the change — the next person needs to know what NOT to undo

## Integration

- `webdev/skill-performance` — Core Web Vitals, bundles, image/font optimization, frontend specifics
- `webdev/skill-database` — query optimization, indexing, connection pooling
- `webdev/skill-observability` — production performance monitoring & alerting
- `ml/skill-training` — training-time performance (GPU util, batch size, mixed precision)
- `ml/skill-model-serving` — inference performance (batching, vLLM, Triton)
- `shared/skill-debugging` — profiling fits the same scientific method as debugging
- `shared/skill-tdd` — performance regression tests are tests

## Resources

- [Brendan Gregg's Performance pages](https://www.brendangregg.com/) — definitive on systems performance
- [Web.dev Performance](https://web.dev/performance/)
- [py-spy](https://github.com/benfred/py-spy) · [scalene](https://github.com/plasma-umass/scalene) · [pprof](https://github.com/google/pprof)
