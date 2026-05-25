---
name: skill-testing
description: Testing strategy — choosing what to test, which test type pays off, how to structure a test suite that catches regressions without becoming a maintenance tax. Use when designing a test plan, reviewing test coverage, choosing between unit/integration/e2e/contract/property/load tests, or fixing a flaky/slow suite. For the discipline of writing tests before code see `shared/skill-tdd`; for end-to-end QA strategy see `webdev/skill-qa`.
---

# Testing — Strategy and Test-Type Selection

A test exists to catch a regression, document behavior, or unblock a refactor. If a test does none of these, delete it. This skill is about choosing the right test for the job; the discipline of test-first lives in `shared/skill-tdd`.

## When to Activate

Use when:
- Designing the test plan for a new service, package, or feature area
- Reviewing a PR's test coverage ("are these the right tests?", not "do they pass?")
- Deciding between an integration test and a slower e2e test
- A suite is flaky, slow, or has stopped catching real bugs
- Adding the first tests to a legacy module
- Setting up a new repo's CI test stages

**Trigger phrases:** "what should I test", "test plan", "test pyramid", "is this enough coverage", "how do I test X", "the suite is flaky", "tests are slow", "contract test", "property test", "load test"

## When NOT to Use

| Situation | Use instead |
|---|---|
| Writing a single failing test before implementing a feature | `shared/skill-tdd` (the discipline) |
| End-to-end QA strategy, exploratory testing, release sign-off | `webdev/skill-qa` |
| Debugging a specific failing test | `shared/skill-debugging` |
| ML model evaluation (metrics, train/test contamination) | `ml/skill-ml-evaluation` |
| Performance regression target setting | `shared/skill-performance` |
| Security-focused tests (authz, injection, fuzzing) | `shared/skill-security` |

This skill governs *strategy*. `skill-tdd` governs *cadence*. Use both.

## Iron Laws

1. **Test behavior, not implementation.** If renaming a private method breaks a test, the test was wrong.
2. **One assertion of intent per test.** Multiple `assert` lines are fine; multiple things being verified are not — the failure must point at one cause.
3. **Tests must be deterministic.** A flaky test is a broken test. Fix or delete; never `retry` your way out of nondeterminism.
4. **Coverage is a smoke alarm, not a goal.** 100% line coverage of trivial getters is worse than 70% coverage with property tests on the core domain.
5. **The suite must run fast enough that engineers run it.** Unit tests under 30s total; full suite under what your team will tolerate locally. Slower than that, it doesn't get run, which means it doesn't catch anything.

## The Pyramid (and Why It's Still Right)

```
          /\
         /  \   E2E         5–10%   minutes      flaky, brittle, expensive
        /----\
       / Integ \  Integration  20–30%  seconds   real DB/HTTP, fixtures
      /--------\
     /  Unit    \  Unit          60–70%  ms        pure functions, isolated
    /------------\
```

The shape isn't a target — it's a consequence. E2E tests cost more (slower, flakier, bigger setup) than integration tests, which cost more than unit tests. You should have many of the cheap kind and few of the expensive kind, because the expensive ones don't pay back per test what the cheap ones do.

Inverted pyramids ("ice cream cone") happen when teams skip unit tests because "we have e2e coverage." That suite eventually slows from minutes to hours, becomes flaky, gets disabled in CI, and stops catching anything.

## Test Type Decision Matrix

| Type | Use when | Avoid when | Cost | Confidence per test |
|---|---|---|---|---|
| **Unit** | Logic in a pure function or small class; algorithm; data transform | The code is mostly orchestration / I/O glue | Cheap | Low–medium |
| **Integration** | Component crosses a real boundary: DB, HTTP, queue, file system | The boundary is already covered by a contract test elsewhere | Medium | Medium–high |
| **Contract** | Two services agree on a schema (API consumer/provider, message queue) | Single deployable, no network boundary | Medium | High at the boundary |
| **End-to-End** | Critical user journey (sign-up, checkout, core workflow) | Anything not on the critical path; first line of defense | Expensive | High but localized |
| **Property** | Pure function with invariants (round-trip, idempotence, ordering, math identities) | Behavior depends on external state | Cheap (CPU) but design cost | High — finds edge cases humans miss |
| **Mutation** | Assessing whether your existing tests actually catch bugs | Tests aren't stable yet; mutation runs on a moving target | Expensive (long runs) | Diagnostic — used periodically, not in CI per-PR |
| **Load / Performance** | Validating P95 latency, throughput, capacity targets | Functional correctness — load tests don't replace correctness tests | Expensive (infra) | Specific to perf target |
| **Snapshot** | Stable serialized output that is hard to assert structurally (rendered UI, generated config) | Frequently-changing output — snapshots get rubber-stamped | Cheap to write, expensive to maintain | Low if rubber-stamped |
| **Smoke** | "Does the service start at all?" pre-deploy check | A substitute for real coverage | Cheap | Very low — confirms presence, not correctness |

If you can't say which row applies, you don't yet know what the test is for.

## AAA — The Only Structural Pattern You Need

```python
def test_discount_applies_before_tax():
    # Arrange
    cart = Cart(items=[Item(price=100, qty=2)])
    coupon = Coupon(rate=0.10)

    # Act
    total = cart.total(coupon=coupon, tax_rate=0.05)

    # Assert
    assert total == 189.0  # (200 - 20) * 1.05
```

The blank lines are the structure. If you can't draw clean Arrange / Act / Assert lines, the test is doing too much. Split it.

## What to Test First in a New Module

1. **The happy path** — one test that exercises the common case end-to-end through the module.
2. **The boundary conditions** — empty input, max input, zero, negative, the wrong type if your language allows it.
3. **The error contract** — every documented exception/error code must have a test that triggers it.
4. **The invariants** — properties that should hold across all inputs (use property-based tests).

This ordering is also the order of leverage: each later category catches bugs the earlier ones miss.

## Test Data Management

| Approach | When | Trade-off |
|---|---|---|
| Inline literals | Tiny, self-contained tests | Duplicates if reused; fine — duplication in tests is preferable to coupling |
| Fixtures (pytest, JUnit `@BeforeEach`) | Reusable setup across tests in one file | Hidden state; readers must hunt for what's set up |
| Factories (Factory Boy, FactoryBot, Mother objects) | Creating objects with mostly-default fields, varying one | Best balance for non-trivial domains |
| Faker | Names, emails, addresses where shape matters but value doesn't | Don't use for determinism-sensitive tests; seed it if you must |
| Recorded fixtures (VCR, nock) | Replaying real HTTP responses | Recordings rot; refresh on schema changes |
| Anonymized prod snapshots | Reproducing prod-only bugs | PII risk; redact rigorously |

Rule: if reading the test forces you to read the fixture, the fixture is wrong. The test should make its inputs visible at the call site.

## Coverage Philosophy

Line coverage answers "did this line execute?" — not "is this line correct?" A test that runs every line and asserts nothing has 100% coverage and zero value.

What to actually look at:
- **Branch coverage** > line coverage. Did both branches of every `if` get hit?
- **Mutation score** > branch coverage. If I mutate the code, do tests actually fail? Mutation testing is the honest measure.
- **Critical-path coverage targets:** 100%. The rest: as much as is useful, no more.

Don't chase coverage numbers; investigate uncovered code. Sometimes the right answer is "this is genuinely untestable glue, document it."

## Patterns by Stack — Pointers, Not Tutorials

Each language has idiomatic libraries. Use them; don't rebuild the wheel.

| Stack | Unit / Integration | E2E | Property | Load |
|---|---|---|---|---|
| Python | pytest, fixtures, `parametrize` | Playwright, Selenium | Hypothesis | Locust, k6 |
| TypeScript / Node | Vitest / Jest, supertest | Playwright, Cypress | fast-check | k6, Artillery |
| Go | `testing` stdlib, testify, `httptest` | rod, chromedp | rapid, gopter | k6, vegeta |
| Java / JVM | JUnit 5, Mockito, Testcontainers | Playwright, Selenide | jqwik | Gatling, JMeter |
| Rust | `cargo test`, `proptest` | (uncommon) | proptest, quickcheck | drill, k6 |

The tutorials for any of these are one search away. What this skill cares about is *which row* you should be looking at — see the decision matrix above.

### Pytest fixture pattern (illustrative)

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()

def test_user_persists(db):
    db.add(User(name="ada", email="ada@example.com"))
    db.commit()
    assert db.query(User).count() == 1
```

The pattern that matters: `yield` + `try/finally` so cleanup runs on test failure. Forgetting that leaves your CI runner with leaked DB connections.

### Property test pattern (illustrative)

```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_sort_is_idempotent(xs):
    assert sorted(sorted(xs)) == sorted(xs)

@given(st.lists(st.integers()))
def test_sort_preserves_multiset(xs):
    from collections import Counter
    assert Counter(sorted(xs)) == Counter(xs)
```

The pattern that matters: state the *property*, not an example. The property is what stays true across all inputs Hypothesis can throw at you. The two-line property catches bugs an example-based test never would.

### Load test pattern (illustrative)

```python
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task(3)  # weight: 3x more frequent than other tasks
    def view_post(self):
        self.client.get(f"/post/{self.environment.runner.user_count % 100}")

    @task
    def login(self):
        self.client.post("/login", json={"username": "test", "password": "test"})
```

The pattern that matters: weights model real traffic mix, not synthetic 1:1. Load test against the workload you actually have.

## Test Independence and Determinism

Tests must run in any order, and any subset, and pass identically.

```python
# DEFECT — order-dependent
class TestUser:
    user_id = None  # mutable class state

    def test_create(self):
        TestUser.user_id = create_user("ada")
        assert TestUser.user_id

    def test_update(self):
        update_user(TestUser.user_id, "Ada Lovelace")  # depends on test_create

# CORRECT — each test self-contained
def test_create_user(db):
    uid = create_user(db, "ada")
    assert db.query(User).get(uid)

def test_update_user(db):
    uid = create_user(db, "ada")
    update_user(db, uid, "Ada Lovelace")
    assert db.query(User).get(uid).name == "Ada Lovelace"
```

Sources of nondeterminism to hunt down: clock (`now()`), randomness (unseeded), thread scheduling, network, filesystem ordering, hash iteration order (some languages).

## Mocking — Use Sparingly, Mock at Boundaries

Mock external systems you don't own (3rd-party APIs, payment gateways). Don't mock your own code unless you must. Heavy mocking is a design smell — code that needs five mocks to test is too coupled.

```python
# Acceptable — mocking an external HTTP boundary you don't own
@patch("billing.stripe_client.charge")
def test_checkout_charges_card(stripe):
    stripe.return_value = {"id": "ch_123", "status": "succeeded"}
    result = checkout(cart, payment_method="pm_456")
    assert result.status == "paid"
    stripe.assert_called_once_with(amount=cart.total_cents, payment_method="pm_456")
```

If you find yourself asserting on calls into your own modules, you're testing the wiring instead of the behavior. Refactor toward a real call.

## Common Failure Modes

| Pattern | Why it fails |
|---|---|
| Tests of private methods or attributes (`obj._internal`) | Couples tests to implementation; refactors break tests instead of code |
| One giant `test_user_lifecycle` covering create/update/delete | First failure hides the rest; can't tell which step broke |
| Mock everything, then assert on the mocks | Tests pass when code is broken; you proved the mock works, not the code |
| Snapshot tests rubber-stamped on every diff | Snapshot becomes write-only; provides zero signal |
| Adding a `time.sleep(1)` to fix flakiness | Hides nondeterminism; sleep eventually fails again under load |
| Unit tests that hit a real database | Cripples test speed; flakes on DB state; not a unit test |
| 100% line coverage with no branch / mutation testing | False sense of safety; many lines covered, few behaviors verified |
| Tests retried until they pass (`@flaky(max_runs=5)`) | Encodes flakiness as policy; the bug you're hiding eventually ships |
| Tests written *after* the code, all passing immediately | Proves nothing — see `shared/skill-tdd` |
| Inverted pyramid (mostly e2e) | Suite slows from seconds to hours; bugs ship while CI runs |

## Test Plan Review Checklist

When reviewing a test plan or a PR's tests:

- [ ] Each test name describes the behavior being verified
- [ ] Test type matches the row in the decision matrix
- [ ] Happy path, boundary, and error contract all present for new behavior
- [ ] No test depends on another test's side effects
- [ ] No `sleep` / time-based race conditions
- [ ] External services mocked at the boundary; internal code called for real
- [ ] Critical-path coverage is full; non-critical coverage is reasonable
- [ ] Suite still completes within the team's tolerance (CI budget)

## Integration

- `shared/skill-tdd` — the discipline of test-first; this skill picks *which* tests, that one says *when* to write them
- `shared/skill-debugging` — every bug fix gets a regression test (Phase 4 in skill-debugging)
- `shared/skill-self-review` — reviewer checks "did this PR include the right kinds of tests?"
- `shared/skill-performance` — performance tests are tests too; targets defined there, written here
- `shared/skill-security` — security tests (authz negatives, injection probes) are tests; this skill tells you to write them
- `webdev/skill-qa` — release-time QA strategy, exploratory testing, sign-off (different scope)
- `webdev/skill-database` — integration tests against real DBs; transactional rollback patterns
- `webdev/skill-api-rest` — contract tests at HTTP boundaries
- `ml/skill-ml-evaluation` — ML-specific test concerns (data leakage, metric correctness)
- `superpowers:test-driven-development` — Anthropic's bundled TDD skill; same discipline

## Resources

- [Diátaxis-style test taxonomy: Martin Fowler — TestPyramid](https://martinfowler.com/bliki/TestPyramid.html)
- [Hypothesis (Python property-based testing)](https://hypothesis.works/)
- [fast-check (TS property-based testing)](https://fast-check.dev/)
- [Testcontainers (real-DB integration tests across stacks)](https://testcontainers.com/)
- [Pact (consumer-driven contract testing)](https://pact.io/)
- [k6 (load testing)](https://k6.io/) · [Locust](https://locust.io/)
- [Mutmut (Python mutation testing)](https://mutmut.readthedocs.io/) · [Stryker (JS/TS mutation testing)](https://stryker-mutator.io/)
- [Google Testing Blog](https://testing.googleblog.com/) — long-running source of test-strategy posts
