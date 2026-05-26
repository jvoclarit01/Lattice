---
name: skill-make
description: Make (Integromat) scenario development and design discipline. Details visual error handler directives (Rollback, Resume, Break, Ignore), transactional ACID boundaries, JSON blueprint serialization, and webhook design. Use when building, testing, or documenting Make scenarios.
---

# Make — Scenario Development & Design

Make (Integromat) provides a powerful visual layout for automation, but scenarios easily drift from code repositories and fail due to unhandled API errors on individual data bundles. This skill enforces modular, transactional scenario architectures.

## When to Activate

Use when:
- Designing or editing workflows in the Make.com visual dashboard
- Exporting or importing Make JSON blueprints for version control
- Building custom error routes using Make error modules
- Configuring webhooks and data stores inside Make
- Mapping data arrays using Make's built-in formulas

**Trigger phrases:** "Make.com", "Integromat", "Make scenario", "Make blueprint", "Make error handler", "Break directive", "Rollback directive"

## Iron Laws

1. **Never commit changes without backing up the JSON blueprint.** Make does not have built-in git-based automatic versioning. Save exported blueprints under a `blueprints/` directory in your project's Git repository.
2. **Handle errors at the module boundary.** Use visual error handlers on any API module that is prone to network failure, rate limiting, or schema mismatches.
3. **Prefer Webhooks over Polling.** Polling modules (e.g., checking for updates every 15 minutes) deplete operations quotas and introduce latency. Use instant webhooks wherever supported.
4. **Enforce transaction rollback on critical databases.** If a scenario writes to multiple SQL tables or transactional APIs, use the `Rollback` directive to prevent partial state corruption.

---

## Error Handling Directives

Make executes data in "bundles." If an error occurs on a module, you must attach one of the following directives to control flow:

| Directive | Module Behavior | Use Case |
|---|---|---|
| **`Rollback`** | Reverts all operations performed by transaction-supporting modules and stops execution. | Highly critical financial or database writes where partial data is forbidden. |
| **`Resume`** | Supplies a mock or fallback object and allows the scenario to continue processing. | Non-critical calls where default data is acceptable (e.g., fallback images, empty strings). |
| **`Break`** | Pauses execution and places the bundle in a manual queue for human verification. | Complex business rules where data must be corrected manually rather than dropped. |
| **`Ignore`** | Ignores the error on this bundle and continues processing subsequent bundles. | Batch data scraping or syncing where one bad row shouldn't stop the rest. |

---

## Scenario Architecture & IaC (Infrastructure as Code)

### 1. Modular Blueprint Isolation
Avoid massive "spaghetti scenarios" containing dozens of modules. Instead, apply the **hub-and-spoke pattern**:
- Break operations into isolated scenarios (e.g., Ingestion Scenario $\rightarrow$ Processing Scenario $\rightarrow$ Alert Scenario).
- Connect scenarios via **Webhooks** or **Mailboxes** to decouple state.

### 2. JSON Blueprint Version Control
Create a directory in your Git repository: `.lattice/make-scenarios/`
For every scenario modification:
1. Export the `.json` blueprint from Make.
2. Save to `.lattice/make-scenarios/<scenario-name>.json`.
3. Commit with a message detailing module edits (e.g., `feat(make-auth): add Slack notifier module`).

---

## Review Checklist

- [ ] **Error Handlers:** Do critical API modules have explicit error routes (`Rollback` or `Break`)?
- [ ] **JSON Blueprint:** Is the visual layout backed up to version control?
- [ ] **Idempotent Webhooks:** Does the webhook endpoint check the transaction ID before executing actions?
- [ ] **Data Stores:** Are internal Make Data Stores used only for transient state, not as primary sources of truth?
- [ ] **ISO 8601:** Are all date/time fields formatted to UTC ISO 8601 inside the payload mapping?
