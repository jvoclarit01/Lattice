---
name: skill-prompt-engineering
description: Designing prompts for production LLM applications — system prompts, XML structure, prefill, tool use, structured output, prompt caching, and evaluation. Use when shipping an LLM-backed feature, when output quality is unstable, or when token costs are high enough that caching matters. For Anthropic SDK setup, model selection, and feature configuration see the `claude-api` skill; for retrieval-augmented prompts see `skill-rag`.
---

# Prompt Engineering

A prompt is a program. It has inputs, structure, control flow, and a contract with the model. "Prompting 101" tips like "be specific" are correct but rarely the missing ingredient — the missing ingredient is usually structure, prefill, caching, or evaluation.

## When to Activate

Use when:
- Designing the system + user prompt for a production LLM feature
- Output quality is inconsistent across similar inputs
- Token costs are large enough that prompt caching would matter
- The model needs to call tools, return structured JSON, or follow a multi-step procedure
- You're evaluating two prompt variants and need a real comparison
- Migrating prompts between models (Claude versions, vendor changes)

**Trigger phrases:** "the model keeps adding extra text", "make this output JSON", "prompt caching", "tool use", "structured output", "the prompt works half the time", "system vs user prompt", "few-shot examples", "prefill".

## When NOT to Use

| Situation | Use instead |
|---|---|
| SDK setup, retries, streaming, model selection | `claude-api` (or vendor docs) |
| Adding retrieval to ground prompts in documents | `skill-rag` |
| Fine-tuning a base model on custom data | `skill-finetuning` |
| Evaluating a deployed LLM system end-to-end | `skill-ml-evaluation` |
| Detecting bias/toxicity in LLM outputs | `skill-bias-and-fairness` |
| Building agentic loops with planning | `skill-rag` (for RAG agents) or vendor agent SDK |

## Iron Laws

1. **Structure beats verbosity.** XML tags, sectioned system prompts, and explicit output schemas produce more reliable outputs than longer free-form instructions. Bullet lists of rules beat paragraphs.
2. **An untestable prompt is a liability.** Every shipped prompt has a fixture set with at least 20 inputs and an automated evaluation that runs on every change. "I tried it once and it worked" is not engineering.
3. **Cache everything stable.** If a prompt has a 5,000-token preamble that doesn't change between requests, caching it cuts cost ~10x and latency ~2x. Not caching is leaving money on the table.

## Prompt Anatomy (Claude convention)

```
┌─ system ─────────────────────────────────────────────┐
│ Role + identity                                      │
│ <constraints>...</constraints>                        │
│ <output_format>...</output_format>                    │
│ <examples>... few-shot ...</examples>                 │
└──────────────────────────────────────────────────────┘
┌─ user ───────────────────────────────────────────────┐
│ <task>specific request with variables</task>          │
│ <input>...the actual input...</input>                 │
└──────────────────────────────────────────────────────┘
┌─ assistant (prefill, optional) ──────────────────────┐
│ {                                                     │
└──────────────────────────────────────────────────────┘
```

Stable content (role, format, examples) goes in the system prompt and gets cached. Per-request content goes in the user prompt.

## XML Tags as Structure

Claude is trained to respect XML-like tags. Use them to delimit sections, examples, and outputs.

```python
SYSTEM = """You are a contract-clause classifier. You categorize each clause into
exactly one of: payment, termination, liability, ip, confidentiality, other.

<rules>
- Output a single JSON object, no prose.
- If uncertain, choose "other".
- Never invent categories.
</rules>

<examples>
<example>
<input>Either party may terminate with 30 days written notice.</input>
<output>{"category": "termination", "confidence": 0.95}</output>
</example>
<example>
<input>All payments due within 30 days of invoice.</input>
<output>{"category": "payment", "confidence": 0.98}</output>
</example>
</examples>"""

USER = """<input>{clause}</input>"""
```

Tag names should be descriptive (`<rules>`, `<examples>`, `<input>`) — the model uses them as scaffolding. Don't reuse one generic `<text>` for everything.

## Prefill (Anthropic-specific, very high leverage)

You can pre-write the start of the assistant's response. The model continues from there, which lets you constrain output format without elaborate instructions.

```python
import anthropic

client = anthropic.Anthropic()
resp = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    system=SYSTEM,
    messages=[
        {"role": "user", "content": USER.format(clause=clause)},
        {"role": "assistant", "content": "{"},   # prefill the opening brace
    ],
)
output = "{" + resp.content[0].text   # prepend the prefill back
```

This eliminates "Sure, here's the JSON:" preambles entirely. Best uses: forcing JSON, forcing a specific section format, forcing a refusal-or-answer binary.

## Structured Output

When the SDK supports tool use as a structured-output mechanism (Anthropic, OpenAI), prefer it over JSON-via-prompt:

```python
TOOLS = [{
    "name": "classify_clause",
    "description": "Classify a contract clause.",
    "input_schema": {
        "type": "object",
        "properties": {
            "category": {
                "type": "string",
                "enum": ["payment", "termination", "liability", "ip",
                         "confidentiality", "other"],
            },
            "confidence": {"type": "number", "minimum": 0, "maximum": 1},
            "rationale": {"type": "string"},
        },
        "required": ["category", "confidence"],
    },
}]

resp = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    tools=TOOLS,
    tool_choice={"type": "tool", "name": "classify_clause"},
    messages=[{"role": "user", "content": USER.format(clause=clause)}],
)
result = next(b.input for b in resp.content if b.type == "tool_use")
```

The schema is enforced by the API. This is more reliable than "respond in JSON" and gives you typed Pydantic-ready outputs.

## Prompt Caching

For Claude, mark stable prefixes with `cache_control`. Subsequent calls with the same prefix hit the cache for ~1/10 the input cost:

```python
SYSTEM_BLOCKS = [
    {
        "type": "text",
        "text": LONG_TAXONOMY_DOCUMENT,  # 5K tokens of category definitions
        "cache_control": {"type": "ephemeral"},
    },
    {"type": "text", "text": "Now classify the user's clause."},
]

resp = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=512,
    system=SYSTEM_BLOCKS,
    messages=[{"role": "user", "content": clause}],
)
```

What to cache: large static instructions, taxonomies, code-style guides, retrieved-document context that's reused across queries within a session. Don't cache content that changes per request — cache misses cost more than no-cache.

For deeper coverage of cache lifecycle, hit-rate measurement, and migration between models, see the `claude-api` skill.

## Few-Shot Examples (when and how)

| Task | Examples needed |
|---|---|
| Classification with novel labels | 3–8 per class |
| Rewriting / style transfer | 5–10 demonstrating range |
| Structured extraction | 3–5 covering edge cases |
| Code generation | 1–2; quality > quantity |
| Open-ended reasoning | 0; let CoT do the work |

Place examples *after* rules in the system prompt, inside `<examples>`. If your example set is large, consider retrieving the most-similar k examples per query (dynamic few-shot) instead of pinning all of them.

## Chain-of-Thought / Extended Thinking

For Claude, you can request explicit thinking:

```python
resp = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=4096,
    thinking={"type": "enabled", "budget_tokens": 8192},
    messages=[{"role": "user", "content": problem}],
)
```

Thinking blocks are billed separately and don't appear to end-users — useful for complex reasoning where the answer is short but the path matters. For simpler tasks, asking the model to "think step by step" inline is sufficient and cheaper.

## Tool Use Loop

```python
def chat_with_tools(user_message: str, tools: list, executors: dict) -> str:
    messages = [{"role": "user", "content": user_message}]
    while True:
        resp = client.messages.create(
            model="claude-opus-4-7", max_tokens=2048,
            tools=tools, messages=messages,
        )
        messages.append({"role": "assistant", "content": resp.content})
        if resp.stop_reason != "tool_use":
            return "".join(b.text for b in resp.content if b.type == "text")
        # Execute every tool the model called this turn
        tool_results = []
        for block in resp.content:
            if block.type == "tool_use":
                result = executors[block.name](**block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result),
                })
        messages.append({"role": "user", "content": tool_results})
```

Two production hardenings: (1) cap loop iterations (e.g., 10) to prevent runaway agents, (2) validate `block.input` against the schema before calling the executor — the model can produce malformed args.

## Prompt Evaluation

A prompt without an eval set is unmaintainable. Minimal viable eval:

```python
import json

# fixtures.jsonl: each line is {"input": ..., "expected": ...}
def eval_prompt(prompt_fn, fixtures_path: str) -> dict:
    correct = 0
    total = 0
    failures = []
    with open(fixtures_path) as f:
        for line in f:
            row = json.loads(line)
            output = prompt_fn(row["input"])
            ok = output == row["expected"]   # or grading_fn(output, row["expected"])
            correct += int(ok)
            total += 1
            if not ok:
                failures.append({"input": row["input"], "got": output,
                                 "want": row["expected"]})
    return {"acc": correct / total, "n": total, "failures": failures[:10]}
```

For graded outputs (summaries, rewrites), use a stronger model as judge with a rubric, or use task-specific metrics (ROUGE, BLEU, exact match on extracted entities). Track eval metric on every prompt change in CI; reject regressions the same way you reject test failures.

## Migrating Prompts Across Models

| Symptom | Likely cause |
|---|---|
| Verbose preamble appears on new model | Old model trained to suppress it; new one isn't — add explicit instruction or prefill |
| Tool calls now ignored | Newer model expects updated tool-use format; check SDK version |
| Output schema differs subtly | Some models are stricter about required fields; tighten schema or add validator |
| Latency 3x higher | Reasoning model invoked by default; check `thinking` setting |

Re-run the eval set on every model migration. Don't ship "should be fine, same family."

## Common Failure Modes

| Pattern | Consequence |
|---|---|
| 8-paragraph free-form system prompt | Inconsistent adherence; model "forgets" middle instructions |
| Asking for JSON without schema/tool | Markdown fences, prose preambles, key-name drift |
| One mega-prompt for many tasks | Hard to evaluate; one task's improvement regresses another |
| Few-shot examples that contradict the rules | Model follows the examples; rules look unenforced |
| No prompt versioning | Can't reproduce what produced a specific output 3 weeks ago |
| Ignoring prompt caching with 10K-token preamble | 10x higher bill than necessary |
| Eval = "I read 5 outputs and they looked good" | Quality regresses silently |
| Putting per-request content in the cached prefix | Cache miss every call; worse than no caching |
| `temperature=0` everywhere | Stuck in failure modes; no diversity for reranking/voting |

## Integration

- `claude-api` — Anthropic SDK setup, model selection, retries, streaming, full caching API
- `skill-rag` — when prompts include retrieved context
- `skill-finetuning` — when prompting hits a ceiling and you need a tuned model
- `skill-ml-evaluation` — eval methodology (statistical comparison, CIs) for prompt versions
- `skill-bias-and-fairness` — auditing LLM outputs for disparate behavior across groups
- `shared/skill-security` — prompt injection defense, jailbreak hardening, output sanitization
- `shared/skill-tdd` — fixture-driven prompt development is just TDD with strings

## Resources

- [Anthropic prompt engineering guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — the canonical reference for Claude
- [Anthropic prompt caching docs](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [Anthropic tool use docs](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- [Promptfoo](https://www.promptfoo.dev/) — open-source prompt evaluation harness
- [OpenAI structured outputs](https://platform.openai.com/docs/guides/structured-outputs) — for cross-vendor work
- [Lilian Weng — Prompt Engineering](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/) — survey of techniques
