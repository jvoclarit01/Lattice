---
name: skill-reproducibility
description: General (non-ML) reproducibility — version control discipline, environment pinning, config management, and "same input → same output" guarantees. Use when standing up a new repo, debugging "works on my machine," documenting how to rerun analysis, or preparing a project for handoff. For ML-specific reproducibility (seeds, GPU determinism, experiment tracking) see ml/skill-reproducibility.
---

# Reproducibility — General

This is the cross-domain reproducibility skill. It covers what every project (web, thesis, ML, data analysis) needs.

For ML-specific concerns (random seeds, GPU determinism, experiment tracking, data versioning) see `domains/ml/skill-reproducibility`.

## When to Activate

Use when:
- Starting a new repo (set discipline up front, not later)
- Debugging "works on my machine" / "doesn't reproduce"
- Preparing a project for handoff or open source
- A reviewer or collaborator needs to rerun your analysis
- Writing a thesis methodology section that requires reproducibility

**Trigger phrases:** "can't reproduce", "works on my machine", "environment issue", "set up the repo", "lock the deps"

## When NOT to Use

- Random seeds, GPU determinism, model checkpoints → `ml/skill-reproducibility`
- CI/CD pipeline reproducibility → `webdev/skill-deployment`
- Container image reproducibility → `webdev/skill-devops`

## Iron Laws

1. **The artifact you ship must be buildable from the source you ship.** No "I patched something locally before publishing."
2. **Pin exact versions for shipping; allow ranges only for development tools.** A `^` or `~` on a runtime dep is a future "can't reproduce."
3. **Document the human steps too.** "Run X, then Y" is not reproducible; a script is.

## Three Layers of Reproducibility

| Layer | What's pinned | Tool examples |
|---|---|---|
| Source | Code at a specific commit | Git tags, semver releases |
| Environment | Language version + every dep, transitively | `poetry.lock`, `package-lock.json`, `requirements.txt` (pinned), `Dockerfile` |
| Configuration | Inputs, parameters, secrets layout | `config.yaml`, `.env.example`, schema validation |

A reproducible project locks all three. Missing any layer → reproduction is best-effort.

## Source — Git Discipline

```bash
git init
git commit -m "Initial commit"
git tag -a v1.0.0 -m "First reproducible release"
```

Discipline:
- One change per commit, with a message that explains *why* (not just what)
- Tag releases — `v1.0.0`, `v1.1.0` — so reviewers can `git checkout v1.0.0` and reproduce that version
- Keep `main` always green; do experimental work on branches
- Don't rewrite published history (no `push --force` to shared branches)

## Environment — Lock the World

### Python

```toml
# pyproject.toml — Poetry
[tool.poetry.dependencies]
python = "==3.11.7"          # exact, not "^3.11"
numpy = "==1.26.4"
pandas = "==2.1.4"
```

```bash
poetry lock                    # produces poetry.lock with full transitive graph
poetry install                 # honors the lock; same install everywhere
```

For pip:

```
# requirements.txt — pinned exactly
numpy==1.26.4
pandas==2.1.4
```

```bash
pip-compile requirements.in   # if using pip-tools to generate lock
pip install -r requirements.txt
```

### Node.js

```bash
npm ci                         # NOT npm install — install exactly from package-lock.json
```

`package-lock.json` must be committed. Without it, `npm install` will pull whatever version satisfies the semver range — which can change.

### Containers

When pinning at the language level isn't enough (system libs, binaries, GPU drivers), containerize. See `webdev/skill-devops` for Dockerfile patterns. Two reproducibility-relevant rules:

- Pin the base image with a version + digest: `FROM python:3.11.7-slim-bookworm@sha256:...`
- Don't `apt-get update && apt-get install` without pinning package versions if exact reproducibility matters

## Configuration — Make Inputs Explicit

Every parameter that affects output should live in a config file, not in the code.

```yaml
# config.yaml
project: my-analysis
seed: 42
data:
  source: data/raw/dataset.csv
  filter_date: "2024-01-01"
output_dir: results/
```

```python
import yaml
with open("config.yaml") as f:
    config = yaml.safe_load(f)
```

Validate the schema (Pydantic, `dataclasses`, `voluptuous`) so a typo fails fast instead of silently using a default.

Secrets go in a separate, gitignored file (`.env`) with a checked-in `.env.example` showing the required keys.

## Reproducibility Checklist

Before declaring a project reproducible:

- [ ] Single command (or short script) recreates the environment from a clean machine
- [ ] Every input is in version control or has a recorded location + version
- [ ] Every parameter is in a config file, not hard-coded
- [ ] A README documents the run command and expected output
- [ ] At least one other person has reproduced the result, end-to-end
- [ ] CI runs the reproduction at least on every release tag

The last two are the ones people skip — and the ones that catch real reproducibility bugs.

## Common Failure Modes

| Symptom | Likely cause |
|---|---|
| `pip install` works for you, fails for collaborator | `requirements.txt` uses ranges; transitive deps drifted |
| Code worked last month, breaks today | Unpinned base image or system package |
| Results differ between machines | Hidden config (env vars, locale, timezone, file system case sensitivity) |
| Can't rerun analysis from a year ago | No tag for that version; main has moved on |
| README says "run `make`" but `make` errors | Repro path was never tested on a clean machine |

## Integration

- `ml/skill-reproducibility` — adds seeding, GPU determinism, experiment tracking
- `webdev/skill-devops` — containerization patterns for environment lockdown
- `shared/skill-tdd` — tests are how you verify reproducibility didn't drift
- `shared/skill-debugging` — when reproduction fails, scientific method to find why
- `thesis/skill-research-methodology` — reproducibility statement in a thesis

## Resources

- [Reproducible Research in Python](https://www.reproducible-python.org/)
- [The Turing Way — Reproducible Research](https://the-turing-way.netlify.app/reproducible-research/reproducible-research.html)
- [Twelve-Factor App: Config](https://12factor.net/config)
