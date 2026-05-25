<!-- ADAPTED from D:/GSD/get-shit-done/references/universal-anti-patterns.md.
     Adaptations: removed all GSD-specific rules (gsd-tools.cjs, gsd-sdk query,
     subagent_type "gsd-*", PLAN naming pattern, iOS rules, schema-detect),
     replaced .planning/ with .lattice-plan.md / .lattice/ paths, kept the universal
     rules that apply to Lattice: context budget, file reading, behavioral, error
     recovery. Added Lattice-specific rules around modes and protocols. -->

# Universal Anti-Patterns Reference

Rules that apply to ALL Lattice skills and protocols. Individual skills may have additional specific anti-patterns; this is the floor.

Lattice skills and protocols `@-reference` this doc. The orchestrator and active mode load it at the start of any non-trivial work.

## Context Budget Rules

1. **Never** read every domain skill in `domains/*/` proactively. Load only the skills relevant to the current mode and active step. The orchestrator routes; it does not pre-load.

2. **Never** inline large reference files into in-flight work. If a skill needs a reference, name the path and let the reader load it when needed. Inlining wastes context for content that may not be used.

3. **Never** read every phase folder under `.lattice/phases/`. Read only the active phase's CONTEXT.md / PLAN.md / SUMMARY.md, plus the immediately-prior phase's SUMMARY.md if cross-phase context is needed.

4. **Delegate** heavy work where possible. The orchestrator routes; it does not build, analyze, research, investigate, or verify. For long phases, consider spawning a fresh-context agent per parallel task group.

5. **Proactive pause warning.** If the session has consumed significant context (multiple large file reads, many tool calls, several rounds of revision), surface to the user: "Context budget is getting heavy. Consider checkpointing progress to `.lattice-plan.md` and resuming in a fresh session."

## File Reading Rules

6. **Do not** re-read full file contents when a smaller scope is sufficient. If you need only the status field, read the status section. If you need only the most recent decisions, read those.

7. **Do not** read every phase's full PLAN.md across the whole project. Only the active phase. Earlier phases get summarized via SUMMARY.md frontmatter or the index in `.lattice-plan.md`.

8. **Do not** treat `.lattice-plan.md` as a write-only log. Read it at the start of any session to understand state.

9. **For phase artifacts:** read in this order at session start — `.lattice-plan.md` → active phase folder index → CONTEXT.md → PLAN.md if EXECUTE is active. Do not read SUMMARY.md or VERIFICATION.md unless they are directly relevant to the current step.

## Subagent / Delegation Rules

10. **When spawning subagents,** give them only the artifacts they need. An executor for one parallel task group needs that group's PLAN.md slice, the phase CONTEXT.md, and not much else. It does NOT need every domain skill or the full project history.

11. **Do not re-litigate decisions** that are already locked in CONTEXT.md or earlier phases' SUMMARY.md. Locked decisions are honored unconditionally unless the user explicitly revisits them.

## Questioning Anti-Patterns

Reference: `questioning-protocol.md` for the full anti-pattern list. Headlines:

12. **Do not** walk through checklists. Checklist walking (asking items one by one from a list) is the #1 anti-pattern. Use progressive depth: start broad, dig where interesting.

13. **Do not** use corporate speak. Avoid jargon like "stakeholder alignment", "synergize", "deliverables", "value prop". Use plain language.

14. **Do not** apply premature constraints. Don't narrow the solution space before understanding the problem. Ask about the problem first, then constrain.

15. **Do not** ask about the user's technical experience or skill level. Lattice does the building; the user's role is direction-setting.

## State Management Anti-Patterns

16. **Always update `.lattice-plan.md` after a phase transitions or a domain status changes.** Stale state in `.lattice-plan.md` defeats the resume protocol.

17. **Update SUMMARY.md as you go**, not all at once at the end. If EXECUTE is interrupted, partial SUMMARY.md is more useful than no SUMMARY.md.

18. **Do not** overwrite a CONTEXT.md decision silently during EXECUTE. If a locked decision needs to change, route through DISCUSS and document the revision.

## Behavioral Rules

19. **Do not** create new files (skills, protocols, phase folders, plans) the user did not approve. Always confirm before writing new artifacts.

20. **Do not** modify files outside the current step's stated scope. Each phase's PLAN.md names the files it touches; stay inside that list.

21. **Do not** suggest multiple next actions without clear priority. One primary suggestion, alternatives listed secondary.

22. **Do not** use `git add .` or `git add -A`. Stage specific files only. Sensitive files (`.env`, credentials, large binaries) get accidentally swept into commits otherwise.

23. **Do not** include sensitive information (API keys, passwords, tokens, secrets) in any Lattice artifact. Use environment variables and document the names, not the values.

24. **Do not** declare a step "done" without writing its artifact. DISCUSS done means CONTEXT.md exists. PLAN done means PLAN.md exists and plan-checker passed. EXECUTE done means SUMMARY.md exists. VERIFY done means VERIFICATION.md exists with a clear recommendation.

## Error Recovery Rules

25. **Git lock detection.** Before any git operation, if it fails with "Unable to create lock file", check for stale `.git/index.lock` and advise the user to remove it. Do not remove automatically.

26. **Tests failing at session start.** If pre-existing tests fail during a baseline check (e.g., skill-git-worktrees Step 4), report the failures and ask whether to proceed or investigate. Do not assume failures are pre-existing without confirming.

27. **Partial state recovery.** If `.lattice-plan.md` references a phase folder that doesn't exist, or vice versa, do not proceed silently. Warn the user and suggest diagnosing the mismatch before continuing.

## Lattice-Specific Rules

28. **Mode conflicts must be flagged immediately.** If `.lattice-plan.md` says active mode is `model-lattice` but the user is asking for webdev work, do not silently switch modes. Surface the conflict and apply the Unsure Protocol.

29. **Per-mode resume.** When resuming a project, check the active mode in `.lattice-plan.md` first. The mode determines which `modes/*-Lattice.md` orchestrator handles the session and which `domains/` are eligible.

30. **Locked decisions in CONTEXT.md are unconditional.** A user can revisit them by saying "let me revisit decision D2" — but anything else (a new task, a deviation during EXECUTE, a cleaner refactor opportunity) does not justify silently changing them.

31. **Decision coverage is not optional.** Every decision in CONTEXT.md must map to at least one PLAN.md task and must be verified in VERIFICATION.md. Skipping coverage tracking is the #1 source of phase outcomes that don't match user intent.

32. **The Unsure Protocol applies wherever the user is uncertain.** Don't accept "I don't know" or a blank field. Present 2 options with pros/cons, recommend, and let the user confirm.

## The Principle

Anti-patterns are the things that look efficient in the moment but cost more later. The list isn't exhaustive — it's the floor. When in doubt, prefer explicitness, prefer artifacts, prefer asking, prefer narrow scope.
