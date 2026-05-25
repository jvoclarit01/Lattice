<!-- ADAPTED from D:/skills/community/development/using-git-worktrees/SKILL.md
     Adaptations: Lattice frontmatter, added When to Activate + Trigger phrases,
     softened "native worktree tools" emphasis (Lattice has no built-in harness
     worktree tool, so git fallback is primary), added Integration section.
     Detection logic, .gitignore safety verification, and sandbox fallback
     preserved verbatim. -->
---
name: skill-git-worktrees
description: Set up an isolated git worktree so feature work doesn't pollute the current workspace. Use when starting a new feature branch, executing an implementation plan, doing parallel work on multiple branches, or any time you need a clean checkout that won't disturb the current branch. Detects existing isolation first, prefers native worktree tools when available, falls back to manual git worktree with .gitignore safety verification. Trigger when the user mentions feature branches, parallel work, isolated workspaces, or asks to start fresh on a new branch.
---

# Git Worktrees

## When to Activate

**Always activate for:**
- Starting a new feature branch from a known-clean base
- Executing a multi-step implementation plan that should not contaminate the current branch
- Working on a hotfix while keeping the in-progress feature untouched
- Reviewing a PR locally without losing your current changes
- Any "I want to try X without breaking what I'm doing" situation

**Trigger phrases:**
- "new branch", "feature branch", "start a branch"
- "isolated workspace", "clean checkout", "scratch workspace"
- "work on this in parallel", "side branch"
- "without affecting my current branch", "without losing my changes"
- "git worktree", "worktree"

## Overview

Ensure work happens in an isolated workspace. Detect existing isolation first. Prefer your platform's native worktree tools. Fall back to manual `git worktree` only when no native tool is available.

**Core principle:** Detect existing isolation first. Then use native tools. Then fall back to git. Never fight the harness.

**Announce at start:** "I'm using the skill-git-worktrees skill to set up an isolated workspace."

## Step 0: Detect Existing Isolation

**Before creating anything, check if you are already in an isolated workspace.**

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
```

**Submodule guard:** `GIT_DIR != GIT_COMMON` is also true inside git submodules. Before concluding "already in a worktree," verify you are not in a submodule:

```bash
# If this returns a path, you're in a submodule, not a worktree — treat as normal repo
git rev-parse --show-superproject-working-tree 2>/dev/null
```

**If `GIT_DIR != GIT_COMMON` (and not a submodule):** You are already in a linked worktree. Skip to Step 3 (Project Setup). Do NOT create another worktree.

Report with branch state:
- On a branch: "Already in isolated workspace at `<path>` on branch `<name>`."
- Detached HEAD: "Already in isolated workspace at `<path>` (detached HEAD, externally managed). Branch creation needed at finish time."

**If `GIT_DIR == GIT_COMMON` (or in a submodule):** You are in a normal repo checkout.

Has the user already indicated their worktree preference (in `.lattice-plan.md` or in their instructions)? If not, ask for consent before creating one:

> "Set up an isolated worktree for this work? It protects your current branch from changes."

Honor any existing declared preference without re-asking. If the user declines, work in place and skip to Step 3.

## Step 1: Create Isolated Workspace

**You have two mechanisms. Try them in this order.**

### 1a. Native Worktree Tools (preferred when available)

<!-- ADAPTED: original assumed superpowers harness with EnterWorktree-style tools;
     Lattice typically runs in plain Claude Code without those, so this branch is
     a "if you happen to have one, use it" rather than the primary path. -->

The user has consented to an isolated workspace (Step 0). If you have a tool with a name like `EnterWorktree`, `WorktreeCreate`, a `/worktree` command, or a `--worktree` flag, use it and skip to Step 3.

Native tools handle directory placement, branch creation, and cleanup automatically. Using `git worktree add` when you have a native tool creates phantom state your harness can't see or manage.

In a default Lattice environment running on Claude Code without extensions, no such native tool exists — proceed to Step 1b.

### 1b. Git Worktree Fallback

**This is the default path in Lattice.** Create a worktree manually using git.

#### Directory Selection

Follow this priority order. Explicit user preference always beats observed filesystem state.

1. **Check `.lattice-plan.md` and your instructions for a declared worktree directory preference.** If the user has already specified one, use it without asking.

2. **Check for an existing project-local worktree directory:**
   ```bash
   ls -d .worktrees 2>/dev/null     # Preferred (hidden)
   ls -d worktrees 2>/dev/null      # Alternative
   ```
   If found, use it. If both exist, `.worktrees` wins.

3. **If there is no other guidance available**, default to `.worktrees/` at the project root.

#### Safety Verification (project-local directories only)

**MUST verify directory is ignored before creating worktree:**

```bash
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

**If NOT ignored:** Add to `.gitignore`, commit the change, then proceed.

**Why critical:** Prevents accidentally committing worktree contents to repository.

#### Create the Worktree

```bash
project=$(basename "$(git rev-parse --show-toplevel)")

# For project-local: path="$LOCATION/$BRANCH_NAME"
# Example:
path=".worktrees/$BRANCH_NAME"

git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

**Sandbox fallback:** If `git worktree add` fails with a permission error (sandbox denial), tell the user the sandbox blocked worktree creation and you're working in the current directory instead. Then run setup and baseline tests in place.

## Step 3: Project Setup

Auto-detect and run appropriate setup:

```bash
# Node.js
if [ -f package.json ]; then npm install; fi

# Rust
if [ -f Cargo.toml ]; then cargo build; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install || pip install -e .; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

## Step 4: Verify Clean Baseline

Run tests to ensure workspace starts clean:

```bash
# Use project-appropriate command
npm test / cargo test / pytest / go test ./...
```

**If tests fail:** Report failures, ask whether to proceed or investigate.

**If tests pass:** Report ready.

### Report

```
Worktree ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```

## Quick Reference

| Situation | Action |
|-----------|--------|
| Already in linked worktree | Skip creation (Step 0) |
| In a submodule | Treat as normal repo (Step 0 guard) |
| Native worktree tool available | Use it (Step 1a) |
| No native tool (default in Lattice) | Git worktree fallback (Step 1b) |
| `.worktrees/` exists | Use it (verify ignored) |
| `worktrees/` exists | Use it (verify ignored) |
| Both exist | Use `.worktrees/` |
| Neither exists | Check `.lattice-plan.md`, then default `.worktrees/` |
| Directory not ignored | Add to `.gitignore` + commit |
| Permission error on create | Sandbox fallback, work in place |
| Tests fail during baseline | Report failures + ask |
| No package.json/Cargo.toml | Skip dependency install |

## Common Mistakes

### Fighting the harness

- **Problem:** Using `git worktree add` when the platform already provides isolation
- **Fix:** Step 0 detects existing isolation. Step 1a defers to native tools.

### Skipping detection

- **Problem:** Creating a nested worktree inside an existing one
- **Fix:** Always run Step 0 before creating anything

### Skipping ignore verification

- **Problem:** Worktree contents get tracked, polluting `git status`
- **Fix:** Always use `git check-ignore` before creating a project-local worktree

### Assuming directory location

- **Problem:** Creates inconsistency, violates project conventions
- **Fix:** Follow priority: existing > `.lattice-plan.md` declaration > default

### Proceeding with failing tests

- **Problem:** Can't distinguish new bugs from pre-existing issues
- **Fix:** Report failures, get explicit permission to proceed

## Red Flags

**Never:**
- Create a worktree when Step 0 detects existing isolation
- Use `git worktree add` when you have a native worktree tool — if you have it, use it
- Skip Step 1a by jumping straight to Step 1b's git commands when a native tool exists
- Create a worktree without verifying it's ignored (project-local)
- Skip baseline test verification
- Proceed with failing tests without asking

**Always:**
- Run Step 0 detection first
- Prefer native tools over git fallback when both exist
- Follow directory priority: existing > `.lattice-plan.md` > default
- Verify directory is ignored for project-local
- Auto-detect and run project setup
- Verify clean test baseline

## Integration with Other Skills

- **domains/webdev/skill-finishing-branch.md** — pairs directly with this skill; cleans up the worktree after merge or discard
- **domains/webdev/skill-tdd.md** _(via domains/shared/skill-tdd.md)_ — clean baseline tests in Step 4 are the starting point for the first RED test
- **domains/webdev/skill-deployment.md** — feature branches in worktrees keep deployment-relevant changes isolated
- **shared/resume-protocol.md** — when resuming work, check whether a worktree from a prior session still exists before creating a new one
