---
name: skill-deployment
description: Release strategies, deployment pipelines, and rollback discipline for web applications. Use when shipping a release, choosing between blue-green/canary/rolling/feature-flag rollouts, designing CI/CD pipelines, or recovering from a bad deploy. NOT for infrastructure provisioning, Docker, or Kubernetes — that's skill-devops.
---

# Deployment — Release Strategy & Pipelines

This skill owns *how a change reaches users*. The infrastructure that runs the change belongs to `skill-devops`.

## When to Activate

Use when:
- Designing or modifying a CI/CD pipeline
- Choosing a release strategy for a new feature
- Setting up environments (dev/staging/prod) for a release flow
- Coordinating a database migration with an app deploy
- Building a rollback plan, post-mortem, or incident playbook
- Implementing feature flags for gradual rollout
- Setting up health checks and smoke tests for a release

## When NOT to Use

| Situation | Use instead |
|---|---|
| Writing Dockerfiles or Compose configs | `skill-devops` |
| Provisioning K8s clusters or cloud infra | `skill-devops` |
| Setting up application metrics/tracing | `skill-observability` |
| Designing a database schema migration's *correctness* | `skill-database` |
| Securing the deploy pipeline secrets | `skill-auth` + `shared/skill-security` |

## Iron Laws

1. **Every deploy must be revertible in under 10 minutes** — if not, it isn't a deploy, it's a rewrite.
2. **No untested change reaches production.** "Tested in staging" requires staging traffic patterns close to prod.
3. **Forward-compatible migrations only.** Old code must work with the new schema before old code is killed.

## Release Strategy Selection

| Strategy | Use when | Cost | Rollback | Risk profile |
|---|---|---|---|---|
| **Blue-Green** | Stateless apps, you can afford 2× capacity | High (double infra) | Instant (flip traffic) | Best for binary cutover |
| **Canary** | Need real-traffic validation, observability is mature | Medium | Fast (shift weights down) | Best for risky changes |
| **Rolling** | Constrained capacity, change is low-risk | Low | Slow (re-deploy old) | Default for routine changes |
| **Feature Flag** | UI/behavior changes, A/B tests | Low | Instant (flip flag) | Decouple deploy from release |
| **Recreate** | Stateful single-node services | Low | Slow + downtime | Avoid in prod unless forced |

Pick by answering: how bad is a 5-minute outage? how confident are you in pre-prod testing? do you need to compare A vs B?

## CI/CD Pipeline Skeleton

A pipeline must enforce the Iron Laws above. Minimum gates:

```yaml
name: Deploy

on:
  push:
    branches: [main]
  pull_request:

concurrency:
  group: deploy-${{ github.ref }}
  cancel-in-progress: false   # never cancel a deploy mid-flight

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }
      - run: npm ci
      - run: npm run lint
      - run: npm test -- --coverage
      - run: npm run build

  deploy-staging:
    needs: test
    if: github.ref == 'refs/heads/main'
    environment: staging
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./scripts/deploy.sh staging
      - run: ./scripts/smoke-test.sh https://staging.example.com

  deploy-prod:
    needs: deploy-staging
    environment:
      name: production
      url: https://example.com
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./scripts/deploy.sh production --canary 10
      - run: ./scripts/smoke-test.sh https://example.com
      - run: ./scripts/promote-canary.sh
```

Required gates: lint → test → build → staging deploy → smoke test → prod canary → smoke test → promote. Skipping any of these is a regression of discipline.

## Environments

| Env | Purpose | Data | Traffic | Cost target |
|---|---|---|---|---|
| Local | Author's machine | Mocked / fixture | None | Free |
| Dev | Integration sandbox | Mocked / synthetic | None | Low |
| Staging | Pre-prod verification | Sanitized prod copy | Replayed prod traffic | Prod-like |
| Production | Real users | Real | Real | Real |

Staging-prod parity matters more than infra cost. A staging that doesn't see realistic traffic doesn't catch realistic bugs.

## Database Migrations + App Deploys

The two most common production outages: deploying app code that needs a column the migration hasn't run, or running a migration that locks the table while the old app is still serving traffic.

Rule: every migration must work for both old code and new code simultaneously. The deploy sequence is:

1. Deploy migration (additive only — add columns, indexes, tables)
2. Deploy new app code (writes to both old and new shape)
3. Backfill old rows
4. Deploy code that reads only the new shape
5. Deploy migration that drops the old shape

Skipping the dual-write phase is the #1 cause of avoidable migration outages.

## Rollback Plan

Before every deploy, write down (in the PR description, not your head):
- **Trigger**: what error rate / SLO breach / manual signal triggers rollback?
- **Action**: what's the exact command/click? Who has permission?
- **Time budget**: how long do you debug forward before reverting?
- **Data**: are there migrations or queue messages that complicate revert?

If you can't answer these in <2 minutes, the deploy isn't ready.

## Feature Flags

Decouples deploy from release. Code ships dark; flags turn it on per user/cohort/percentage.

- **Use** for UI changes, algorithm swaps, A/B tests, kill switches for risky paths.
- **Don't use** as a permanent config knob — flags older than 60 days become tech debt.
- **Always** include a kill-switch path even if the flag is "on for everyone." This is your fastest rollback.

## Common Failure Modes

- **"Works on staging" but breaks in prod** → staging-prod parity is broken (data shape, traffic pattern, secrets, network policy).
- **Deploy succeeds, app fails 3 minutes later** → no smoke test in pipeline, or smoke test only hits trivial endpoints.
- **Rollback fails** → forward-only migration, or the rollback path itself was never tested.
- **Canary looks fine, full rollout breaks** → canary cohort wasn't representative (e.g., internal users only).
- **Deploy gets stuck because pipeline auto-cancelled** → `concurrency: cancel-in-progress: true` mid-deploy. Never cancel deploy jobs.

## Integration

- `skill-devops` — provides the runtime (containers, K8s, cloud) this skill ships changes to
- `skill-observability` — provides the metrics/logs that drive canary go/no-go decisions
- `skill-database` — coordinates schema migrations with the deploy sequence
- `skill-finishing-branch` — handoff point: branch is done, now we deploy
- `superpowers:verification-before-completion` — before claiming a deploy is done

## Resources

- [Vercel deployment expert guide](../../shared/) and the `vercel:deployments-cicd` skill
- [Database Migration Best Practices (PostgreSQL)](https://www.postgresql.org/docs/current/ddl-alter.html)
- [Feature Flag Best Practices (Martin Fowler)](https://martinfowler.com/articles/feature-toggles.html)
