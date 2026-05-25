---
name: skill-qa
description: Testing strategy and quality assurance discipline — test type selection, testing pyramid economics, component and API testing patterns, visual regression, contract testing, CI quality gates, and flaky test management. Use when choosing a testing strategy for a new project, adding tests to an existing codebase, setting up CI quality gates, debugging flaky tests, or reviewing test coverage in a PR. For TDD methodology see shared/skill-tdd; for accessibility testing see skill-a11y; for database testing see skill-database.
---

# QA — Testing Strategy & Quality Discipline

Tests exist to catch regressions before users do. The strategy is about *what* to test and *how much* — not about hitting a coverage number. 90% coverage with the wrong tests is worse than 60% coverage with the right ones.

## When to Activate

Use when:
- Choosing a testing strategy for a new project or feature
- Adding tests to an untested codebase (where to start?)
- Setting up CI quality gates (coverage, lint, type-check, visual regression)
- Debugging flaky tests or slow test suites
- Reviewing a PR for test quality (not just quantity)
- Deciding between unit, integration, E2E, or contract tests for a use case

**Trigger phrases:** "testing strategy", "unit test", "integration test", "E2E test", "test coverage", "flaky test", "CI pipeline", "quality gate", "Playwright", "Vitest", "Jest", "testing library", "visual regression", "contract test", "snapshot test"

## When NOT to Use

| Situation | Use instead |
|---|---|
| TDD methodology (RED-GREEN-REFACTOR cycle) | `shared/skill-tdd` |
| Accessibility testing (axe, screen reader) | `skill-a11y` |
| Database testing (migrations, fixtures) | `skill-database` |
| CI/CD pipeline design (deploy gates) | `skill-deployment` |
| Performance testing (load, stress) | `skill-performance` |

## Iron Laws

1. **Test behavior, not implementation.** If refactoring the internals breaks your test, the test is coupled to implementation. Test inputs → outputs.
2. **Every bug gets a regression test.** Found a bug? Write a test that fails with the bug present, then fix it. Never fix a bug without a test.
3. **Flaky tests are bugs.** A test that sometimes passes is never trustworthy. Fix it, quarantine it, or delete it — never ignore it.
4. **CI must be green to merge.** No "it's flaky, just re-run." No "I'll fix the test later." Green CI is a non-negotiable gate.

## Test Type Selection

| What you're testing | Test type | Tool | Speed | Confidence |
|---|---|---|---|---|
| Pure function, utility, parser | Unit | Vitest, Jest, pytest | ⚡ Fast | Low-medium (isolated) |
| Component renders correctly with props | Component | Testing Library + Vitest | ⚡ Fast | Medium |
| API endpoint returns correct response | Integration | Supertest, httpx | 🔵 Medium | Medium-high |
| Service + database together | Integration | Testcontainers, fixtures | 🔵 Medium | High |
| Full user flow through real browser | E2E | Playwright, Cypress | 🔴 Slow | High |
| API contract between services | Contract | Pact, API snapshot | ⚡ Fast | Medium |
| UI looks correct (no visual drift) | Visual regression | Playwright screenshots, Chromatic | 🔴 Slow | Medium |

**Don't test everything with E2E.** E2E tests are expensive, slow, and flaky. Use them for critical user flows (signup, checkout, payment). Use faster test types for everything else.

## Testing Pyramid (revised)

```
         ╱╲        E2E: 5-10 critical user flows
        ╱  ╲       (signup, checkout, payment)
       ╱────╲
      ╱      ╲     Integration: API endpoints, service+DB
     ╱        ╲    (each endpoint, each service method)
    ╱──────────╲
   ╱            ╲   Component + Unit: functions, components
  ╱              ╲  (every utility, every component variation)
 ╱────────────────╲
```

Invest most in the bottom two layers. The top layer catches what the others can't (cross-page flows, real browser behavior).

## Component Testing (React + Testing Library)

```tsx
// Test BEHAVIOR, not implementation
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { SignupForm } from './SignupForm';

test('shows validation error for short password', async () => {
  const user = userEvent.setup();
  render(<SignupForm onSubmit={vi.fn()} />);

  await user.type(screen.getByLabelText(/password/i), 'short');
  await user.click(screen.getByRole('button', { name: /sign up/i }));

  expect(screen.getByRole('alert')).toHaveTextContent(/at least 12 characters/i);
});

test('calls onSubmit with form data when valid', async () => {
  const onSubmit = vi.fn();
  const user = userEvent.setup();
  render(<SignupForm onSubmit={onSubmit} />);

  await user.type(screen.getByLabelText(/email/i), 'test@example.com');
  await user.type(screen.getByLabelText(/password/i), 'securePassword123');
  await user.click(screen.getByRole('button', { name: /sign up/i }));

  expect(onSubmit).toHaveBeenCalledWith({
    email: 'test@example.com',
    password: 'securePassword123',
  });
});
```

What this gets right: queries by role/label (not CSS selectors), tests user behavior (type + click), asserts on outcomes (error shown, callback called), doesn't test internal state.

## API Integration Testing

```ts
// Supertest + Vitest — tests the actual Express/Fastify app
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import request from 'supertest';
import { createApp } from '../src/app';
import { setupTestDb, teardownTestDb } from './helpers/db';

describe('POST /api/users', () => {
  let app: Express;

  beforeAll(async () => {
    await setupTestDb();
    app = createApp();
  });

  afterAll(async () => {
    await teardownTestDb();
  });

  it('creates a user and returns 201', async () => {
    const res = await request(app)
      .post('/api/users')
      .send({ name: 'Jane', email: 'jane@example.com', password: 'securePassword123' })
      .expect(201);

    expect(res.body).toMatchObject({
      id: expect.any(String),
      name: 'Jane',
      email: 'jane@example.com',
    });
    expect(res.headers.location).toMatch(/^\/api\/users\//);
  });

  it('returns 422 for invalid email', async () => {
    const res = await request(app)
      .post('/api/users')
      .send({ name: 'Jane', email: 'not-an-email', password: 'securePassword123' })
      .expect(422);

    expect(res.body.error.code).toBe('VALIDATION_ERROR');
    expect(res.body.error.details).toContainEqual(
      expect.objectContaining({ field: 'email' }),
    );
  });

  it('returns 409 for duplicate email', async () => {
    await request(app)
      .post('/api/users')
      .send({ name: 'Jane', email: 'dup@example.com', password: 'securePassword123' });

    await request(app)
      .post('/api/users')
      .send({ name: 'Jane2', email: 'dup@example.com', password: 'securePassword123' })
      .expect(409);
  });
});
```

## E2E Testing (Playwright)

```ts
// Only for critical user flows
import { test, expect } from '@playwright/test';

test('complete signup flow', async ({ page }) => {
  await page.goto('/signup');

  await page.getByLabel(/email/i).fill('e2e@example.com');
  await page.getByLabel(/password/i).fill('securePassword123');
  await page.getByRole('button', { name: /sign up/i }).click();

  // Should redirect to dashboard
  await expect(page).toHaveURL('/dashboard');
  await expect(page.getByRole('heading', { level: 1 })).toContainText(/welcome/i);
});

test('shows error for duplicate email', async ({ page }) => {
  await page.goto('/signup');

  await page.getByLabel(/email/i).fill('existing@example.com');
  await page.getByLabel(/password/i).fill('securePassword123');
  await page.getByRole('button', { name: /sign up/i }).click();

  await expect(page.getByRole('alert')).toContainText(/already exists/i);
});
```

## CI Quality Gates

```yaml
# .github/workflows/ci.yml
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }
      - run: npm ci

      # Gate 1: Type safety
      - run: npx tsc --noEmit

      # Gate 2: Lint
      - run: npm run lint

      # Gate 3: Unit + Component tests with coverage
      - run: npm test -- --coverage
        env:
          CI: true

      # Gate 4: Integration tests
      - run: npm run test:integration

      # Gate 5: Build succeeds
      - run: npm run build

      # Gate 6: Bundle size check
      - run: npx size-limit

  e2e:
    needs: quality
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npm run test:e2e
```

| Gate | What it catches | Speed |
|---|---|---|
| Type check | Type errors, missing imports | ⚡ |
| Lint | Style issues, unused vars, import order | ⚡ |
| Unit + Component | Logic bugs, rendering issues | ⚡ |
| Integration | API contract violations, DB issues | 🔵 |
| Build | Import errors, env issues | 🔵 |
| Bundle size | Accidental dependency bloat | ⚡ |
| E2E | Cross-page flow regressions | 🔴 |

## Flaky Test Management

| Symptom | Likely cause | Fix |
|---|---|---|
| Fails only in CI | Timing-dependent; hardcoded ports; missing env var | Use `waitFor`, randomize ports, validate env |
| Fails intermittently | Race condition; shared state between tests | Isolate test state; use `beforeEach` cleanup |
| Different results on re-run | Random data without seed; time-dependent logic | Seed random; mock `Date.now()` |
| Fails after unrelated change | Tests coupled to implementation | Test behavior, not internals |

**Policy:** Flaky tests get a 48-hour fix window. After that, quarantine (move to `*.flaky.test.ts`) or delete. Never leave flaky tests in the main suite.

## Common Failure Modes

| Pattern | Why it fails / consequence |
|---|---|
| Testing `useState` internals instead of rendered output | Refactoring breaks tests; tests don't prove user behavior |
| Querying by CSS class or test ID instead of role/label | Tests pass but component is inaccessible |
| E2E for every feature | Suite takes 45 min; nobody runs it; tests go stale |
| No test database isolation | Tests pass alone, fail together (shared state) |
| `expect(result).toMatchSnapshot()` everywhere | Snapshots are noisy; nobody reviews the diff; auto-update bypasses review |
| Coverage threshold without test quality review | 90% coverage with `expect(true).toBe(true)` |
| Tests that mock everything | Proves nothing — the mock is the test |
| No CI enforcement | "Tests pass locally" but PR merges with failures |

## QA Review Checklist

- [ ] Tests cover the happy path AND error paths (at least one each)
- [ ] Component tests query by role/label, not CSS selectors
- [ ] Integration tests test real endpoints against a test database
- [ ] E2E tests only for critical user flows (≤10)
- [ ] No snapshot tests without explicit review policy
- [ ] CI runs all gates: type-check → lint → test → build → E2E
- [ ] Coverage threshold enforced (but quality > quantity)
- [ ] Flaky tests quarantined or fixed within 48 hours
- [ ] Test data uses factories, not hardcoded values
- [ ] Each test is independent — no shared mutable state

## Integration

- `shared/skill-tdd` — TDD methodology (RED-GREEN-REFACTOR) governs how tests are written
- `domains/webdev/skill-a11y` — accessibility tests (axe, screen reader) complement functional tests
- `domains/webdev/skill-frontend` — component testing patterns for React/Vue/Svelte
- `domains/webdev/skill-api-rest` — API integration test patterns match endpoint design
- `domains/webdev/skill-database` — test database setup, fixtures, migrations
- `domains/webdev/skill-deployment` — CI gates are the testing step in the deploy pipeline
- `domains/webdev/skill-validation` — validation logic is prime unit-test territory

## Resources

- [Vitest](https://vitest.dev/) — fast, Vite-native test runner
- [Testing Library](https://testing-library.com/) — query by role, test behavior
- [Playwright](https://playwright.dev/) — reliable E2E testing
- [Testcontainers](https://testcontainers.com/) — disposable databases for integration tests
- [size-limit](https://github.com/ai/size-limit) — bundle-size budgets in CI
- [Kent C. Dodds — Testing Trophy](https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications)
