# Lattice Micro-Heuristics Cheatsheet
This is a compiled high-density index of the 66+ Lattice domain disciplines. Use this for global system prompt awareness and dynamic JIT skill loading.

## Domain: SHARED

### `skill-debugging`
* **Description:** 
* **Heuristics:** Enforce standard discipline for this domain.

### `skill-docs`
* **Description:** Documentation discipline — choosing the right artifact (README vs ADR vs API doc vs runbook vs tutorial vs reference) and keeping it honest, current, and example-driven. Use when starting a new repo, exposing a public API, recording an architectural decision, before a handoff, or when a reviewer asks "where are the docs?". For thesis prose see `thesis/skill-academic-writing`; for review of someone else's docs see `shared/skill-self-review`.
* **Iron Laws / Key Heuristics:**
  1. **Docs live with the code.** Out-of-tree docs rot first; nobody updates them with the PR. Markdown in the repo or auto-generated from source — nothing else.
  2. **Every example must run as written.** Untested examples are anti-documentation; readers waste hours on snippets that haven't worked since Python 3.6.
  3. **Document the "why," not the "what."** The diff already shows what changed. Docs explain why this approach was chosen, what alternatives were rejected, what assumptions break.
  4. **No documentation without a target reader.** "For internal use" is a tell. Name the role: new contributor, on-call engineer, API consumer, future-you.

### `skill-ethics`
* **Description:** Ethics framework for any project that affects people — impact analysis, transparency, privacy, accountability, and human oversight. Use BEFORE building, when handling personal data, automating consequential decisions, or facing "should we build this?" questions. For ML-specific bias detection see ml/skill-bias-and-fairness; for ML explanations see ml/skill-explainability.
* **Heuristics:** Enforce standard discipline for this domain.

### `skill-performance`
* **Description:** General performance methodology — measure first, find the actual bottleneck, optimize the critical path, verify the win, monitor for regression. Domain-agnostic discipline that applies to web apps, ML pipelines, backend services, data analysis. For domain-specific performance work see webdev/skill-performance, ml/skill-training, ml/skill-model-serving.
* **Iron Laws / Key Heuristics:**
  1. **Measure before you optimize. Measure after you optimize.** No exceptions. "Should be faster now" is not a measurement.
  2. **The fastest code is the code that doesn't run.** Optimize by removing work, not by speeding up unnecessary work.
  3. **Optimize the critical path, not the easy path.** Saving 10ms on the 1% case while ignoring the 99% case is malpractice.

### `skill-receiving-feedback`
* **Description:** 
* **Heuristics:** Enforce standard discipline for this domain.

### `skill-reproducibility`
* **Description:** General (non-ML) reproducibility — version control discipline, environment pinning, config management, and "same input → same output" guarantees. Use when standing up a new repo, debugging "works on my machine," documenting how to rerun analysis, or preparing a project for handoff. For ML-specific reproducibility (seeds, GPU determinism, experiment tracking) see ml/skill-reproducibility.
* **Iron Laws / Key Heuristics:**
  1. **The artifact you ship must be buildable from the source you ship.** No "I patched something locally before publishing."
  2. **Pin exact versions for shipping; allow ranges only for development tools.** A `^` or `~` on a runtime dep is a future "can't reproduce."
  3. **Document the human steps too.** "Run X, then Y" is not reproducible; a script is.

### `skill-security`
* **Description:** Security discipline across the SDLC — threat modeling, secure-by-default design, OWASP-grade defenses against the top vulnerabilities, secrets management, and security review gates. Use when designing or reviewing any feature that touches authentication, user data, secrets, payments, network boundaries, or LLM/AI input. NOT a substitute for a real security audit on high-stakes systems.
* **Iron Laws / Key Heuristics:**
  1. **Trust no input.** Anything that crosses a trust boundary — user, network, file, env var, LLM output — is hostile until validated.
  2. **Never invent crypto.** Use vetted libraries (libsodium, AWS KMS, the platform's standard crypto module). If you're writing AES yourself, stop.
  3. **Secrets never live in code.** Not in source, not in container images, not in client-side bundles. Inject at runtime from a secrets manager.
  4. **Default deny.** Permissions, network access, CORS, file access — start at zero and grant the minimum needed.

### `skill-self-review`
* **Description:** 
* **Heuristics:** Enforce standard discipline for this domain.

### `skill-tdd`
* **Description:** 
* **Heuristics:** Enforce standard discipline for this domain.

### `skill-testing`
* **Description:** Testing strategy — choosing what to test, which test type pays off, how to structure a test suite that catches regressions without becoming a maintenance tax. Use when designing a test plan, reviewing test coverage, choosing between unit/integration/e2e/contract/property/load tests, or fixing a flaky/slow suite. For the discipline of writing tests before code see `shared/skill-tdd`; for end-to-end QA strategy see `webdev/skill-qa`.
* **Iron Laws / Key Heuristics:**
  1. **Test behavior, not implementation.** If renaming a private method breaks a test, the test was wrong.
  2. **One assertion of intent per test.** Multiple `assert` lines are fine; multiple things being verified are not — the failure must point at one cause.
  3. **Tests must be deterministic.** A flaky test is a broken test. Fix or delete; never `retry` your way out of nondeterminism.
  4. **Coverage is a smoke alarm, not a goal.** 100% line coverage of trivial getters is worse than 70% coverage with property tests on the core domain.
  5. **The suite must run fast enough that engineers run it.** Unit tests under 30s total; full suite under what your team will tolerate locally. Slower than that, it doesn't get run, which means it doesn't catch anything.

## Domain: WEBDEV

### `skill-a11y`
* **Description:** Web accessibility discipline — semantic HTML, ARIA patterns for complex widgets, keyboard navigation, focus management in SPAs, color contrast, screen reader testing, and WCAG compliance. Use when building forms, modals, dropdowns, tabs, or any interactive component; reviewing a PR for accessibility; fixing screen reader or keyboard issues; or auditing a page against WCAG 2.2. For i18n/RTL see skill-i18n; for form validation logic see skill-validation; for visual design see skill-frontend.
* **Iron Laws / Key Heuristics:**
  1. **Semantic HTML first, ARIA second.** A `<button>` is always better than `<div role="button" tabindex="0">`. ARIA is a repair tool for when HTML doesn't have the right element.
  2. **Every interactive element is keyboard-accessible.** If it responds to click, it responds to Enter/Space. If it opens a menu, Escape closes it. No exceptions.
  3. **Focus must be visible and managed.** When a modal opens, focus moves inside. When it closes, focus returns to the trigger. Focus indicators are never hidden with `outline: none`.
  4. **Dynamic content is announced.** When content changes without a page load (toast, error, status), a live region tells screen readers what happened.

### `skill-api-graphql`
* **Description:** GraphQL schema design and operational discipline — SDL, resolvers and the N+1 trap, typed errors, subscriptions, federation vs monolith, and security limits (depth, complexity, persisted queries). Use when designing a new GraphQL schema, debugging a slow GraphQL endpoint, debating REST vs GraphQL, or auditing a GraphQL API for security. For REST design see skill-api-rest; for WebSocket/SSE push patterns see skill-api-realtime; for input validation libraries see skill-validation.
* **Iron Laws / Key Heuristics:**
  1. **Resolvers never hit the database in a loop.** Every list field crosses through DataLoader (or the equivalent batching primitive). N+1 is a defect, not a perf tweak.
  2. **Errors are typed in the schema.** Use union or interface result types for expected failures; reserve top-level `errors` for unexpected ones.
  3. **Public endpoints have a query budget.** Depth limit + complexity limit + (in production) persisted queries — pick at least two.
  4. **Auth is on the resolver, not the gateway.** Field-level authorization is a feature of GraphQL; using only gateway-level auth surrenders that feature.
  5. **Schema changes are versioned by deprecation, not by URL.** `@deprecated(reason: "...")` then remove after one consumer migration cycle.

### `skill-api-realtime`
* **Description:** Real-time communication patterns — WebSocket, Server-Sent Events (SSE), and long polling for web applications. Use when adding live updates, chat, notifications, collaborative editing, presence indicators, or any feature where the server pushes data to the client. For GraphQL subscriptions see skill-api-graphql; for REST endpoint design see skill-api-rest; for auth on WebSocket connections see skill-auth.
* **Iron Laws / Key Heuristics:**
  1. **Authenticate on connect AND on each message.** A user's permissions can change mid-session — don't trust the initial handshake forever.
  2. **Always implement reconnection with backoff.** Networks drop. Tabs sleep. Clients must reconnect automatically without flooding the server.
  3. **Filter server-side, not client-side.** Don't broadcast every event to every client and let the browser discard. That's a privacy leak and a bandwidth waste.
  4. **Heartbeat or die.** Without a ping/pong, you can't distinguish "connection is idle" from "connection is dead." Dead connections leak memory.

### `skill-api-rest`
* **Description:** REST API design discipline — resource modeling, status codes, idempotency, pagination, versioning, and the seams where the API hands off to validation, auth, errors, and the database. Use when designing a new endpoint, reviewing an API PR, debating REST vs GraphQL, or auditing an existing API for consistency. For request validation see skill-validation; for error response shape see skill-error-handling; for endpoint authorization see skill-auth; for GraphQL alternatives see skill-api-graphql.
* **Iron Laws / Key Heuristics:**
  1. **Resources are nouns; HTTP verbs are the verbs.** No `/getUser`, no `/createOrder` — they're just `GET /users/{id}` and `POST /orders`.
  2. **Idempotent methods stay idempotent under retries.** GET, PUT, DELETE retried N times must equal once. POST is the exception — give it an `Idempotency-Key` header if it can be retried.
  3. **Status codes are part of the contract.** 200 for OK, 201 for created, 204 for no body, 4xx for client error, 5xx for server error — never 200 with `{ "error": ... }` in the body.
  4. **Every change is either backward-compatible or a new version.** Removing a field, renaming a path, or tightening validation in place is a breaking change.
  5. **Validation and authorization are mandatory at the edge** — see `skill-validation` and `skill-auth`.

### `skill-auth`
* **Description:** Authentication and authorization implementation patterns for web apps — sessions, JWTs, OAuth/OIDC, MFA, password handling, and session lifecycle. Use when adding sign-in/sign-up, building an auth flow, integrating an identity provider, or reviewing an auth PR. For broader threat-modeling, OWASP defenses, and secrets discipline across the SDLC see shared/skill-security.
* **Iron Laws / Key Heuristics:**
  1. **Passwords are hashed with a memory-hard algorithm** — Argon2id (preferred) or bcrypt cost ≥12. Never SHA-256, MD5, or "encrypted."
  2. **Session tokens are revocable.** A logged-out session must stop working immediately, on every server, including replicas.
  3. **MFA defaults to phishing-resistant.** WebAuthn/passkeys > TOTP > SMS. SMS is a fallback, never the primary factor for high-value accounts.
  4. **Authorize on the server, every request.** Hiding a button in the UI is not authorization.
  5. **Never roll your own crypto, OAuth flow, or OIDC validation.** Use a library; understand which library you chose and why.

### `skill-backend`
* **Description:** Backend architecture discipline — project structure, middleware pipelines, dependency injection, background jobs, queue patterns, and the seams where architecture hands off to API design, database, auth, and error handling. Use when scaffolding a new backend service, choosing a framework, designing a middleware pipeline, adding background processing, or reviewing a backend PR for structural choices. For API endpoint design see skill-api-rest / skill-api-graphql; for database queries see skill-database; for auth see skill-auth; for error responses see skill-error-handling.
* **Iron Laws / Key Heuristics:**
  1. **Controllers are thin.** A controller parses the request, calls a service, formats the response. If it has business logic, it's wrong.
  2. **Business logic lives in the service layer.** Services don't know about HTTP, headers, or response codes — they take data in, return data out, throw domain errors.
  3. **Middleware order matters and must be documented.** Auth before validation, validation before handler, error handler outermost. Swapping two middleware can create a security hole.
  4. **Side effects go through queues.** Sending email, generating PDFs, calling external APIs — these don't belong in the request path. Queue them; fail gracefully if the queue is down.

### `skill-database`
* **Description:** Database design discipline — type selection (SQL vs NoSQL vs key-value vs graph), schema design, normalization, indexing strategy, query optimization, migrations, transactions, and data integrity. Use when designing a schema, writing or optimizing queries, planning a migration, choosing a database type, or debugging slow queries. For ORM setup in backend code see skill-backend; for API-level pagination see skill-api-rest; for connection pooling metrics see skill-observability.
* **Iron Laws / Key Heuristics:**
  1. **Choose the database for the workload, not the resume.** A key-value store doesn't replace a relational DB for transactional data; a graph DB is overkill for a user table.
  2. **Index for query patterns, not for tables.** Every index you add speeds one read and slows every write. Profile first, index second.
  3. **Migrations are code — version-controlled, reviewed, reversible.** No console-click schema changes in production.
  4. **Transactions protect invariants.** If two operations must succeed or fail together, they belong in a transaction. "We'll fix it later" means data corruption now.

### `skill-deployment`
* **Description:** Release strategies, deployment pipelines, and rollback discipline for web applications. Use when shipping a release, choosing between blue-green/canary/rolling/feature-flag rollouts, designing CI/CD pipelines, or recovering from a bad deploy. NOT for infrastructure provisioning, Docker, or Kubernetes — that's skill-devops.
* **Iron Laws / Key Heuristics:**
  1. **Every deploy must be revertible in under 10 minutes** — if not, it isn't a deploy, it's a rewrite.
  2. **No untested change reaches production.** "Tested in staging" requires staging traffic patterns close to prod.
  3. **Forward-compatible migrations only.** Old code must work with the new schema before old code is killed.

### `skill-devops`
* **Description:** Infrastructure-as-code, containerization, orchestration, and platform engineering for web applications. Use when writing Dockerfiles, designing Kubernetes manifests, provisioning cloud infrastructure with Terraform/Pulumi, managing secrets, or building developer platforms. NOT for release strategies or deployment pipelines — that's skill-deployment.
* **Iron Laws / Key Heuristics:**
  1. **Infrastructure changes go through code review** — no console clicks in production.
  2. **Containers are immutable** — config goes in env vars or mounted volumes, never baked-in secrets.
  3. **The Dockerfile must be reproducible** — same input, same image. Pin every base, every dep, every binary.

### `skill-error-handling`
* **Description:** Error handling architecture — error envelope standard, typed error classes, global handlers, React error boundaries, retry/circuit-breaker discipline, and the seams where errors hand off to observability and API responses. Use when designing an error strategy for a new service, adding a global error handler, debugging inconsistent error responses, or reviewing error handling in a PR. For input validation see skill-validation; for auth error flows see skill-auth; for production monitoring see skill-observability.
* **Iron Laws / Key Heuristics:**
  1. **Every error has a type, a code, and a message.** No naked `throw new Error('something broke')` — use typed error classes with machine-readable codes.
  2. **Internal details never reach the client.** Stack traces, SQL queries, file paths — these are for logs, not for HTTP responses.
  3. **Every async boundary has an error handler.** Unhandled promise rejections, uncaught exceptions, error boundaries — silence is a bug.
  4. **Retries are idempotent or they don't happen.** Retrying a non-idempotent operation can double-charge, send duplicate emails, or corrupt data.

### `skill-finishing-branch`
* **Description:** 
* **Heuristics:** Enforce standard discipline for this domain.

### `skill-frontend`
* **Description:** Frontend architecture choices and discipline for web UIs — framework selection, styling strategy, state management, component boundaries, and the seams where UI hands off to data, accessibility, and i18n. Use when starting a new frontend, picking a framework or styling approach, refactoring component structure, or reviewing a frontend PR's structural choices. For accessibility specifics see skill-a11y; for translation/locale see skill-i18n; for input validation see skill-validation; for the WHY of slow UIs see skill-performance.
* **Iron Laws / Key Heuristics:**
  1. **Pick the framework for the workload, not the resume.** A static marketing site doesn't need Next.js + Redux; a real-time dashboard does.
  2. **One source of truth per piece of state.** Server data and UI state are different — don't duplicate server data into Redux.
  3. **Components have one reason to change.** A `<UserProfile>` that fetches, formats, and renders breaks when any of those three change.
  4. **Hardcoded strings are a bug.** Every user-visible string is a translation key (see `skill-i18n`).

### `skill-git-worktrees`
* **Description:** 
* **Heuristics:** Enforce standard discipline for this domain.

### `skill-i18n`
* **Description:** Internationalization and localization — translation key architecture, pluralization, ICU message format, locale negotiation, RTL support, date/number formatting, extraction tooling, and CI checks for missing keys. Use when adding multi-language support, extracting hardcoded strings, setting up i18n for a new project, fixing broken plurals, or reviewing a PR for i18n compliance. For form labels and ARIA see skill-a11y; for validation error messages see skill-validation.
* **Iron Laws / Key Heuristics:**
  1. **No hardcoded user-visible strings — ever.** Every string goes through `t()`. No exceptions for "just this one button" or "it's English-only for now."
  2. **Pluralization uses ICU rules, not ternaries.** `count === 1 ? 'item' : 'items'` breaks in Russian (3 plural forms), Arabic (6), and many others. Use ICU MessageFormat or your library's plural system.
  3. **Store dates as UTC; format at render time.** The database stores `2024-01-15T10:30:00Z`. The UI shows `Jan 15, 2024` or `15 janv. 2024` depending on locale.
  4. **Missing keys break the build.** If a key exists in `en` but not in `fr`, the CI fails. Users should never see a raw key like `signup.email_placeholder`.

### `skill-integrations`
* **Description:** Third-party integration discipline — API client wrappers, webhook processing, idempotency, retry + circuit breaker patterns, rate-limit respect, SDK vs raw HTTP decisions, and testing external dependencies. Use when integrating with payment processors (Stripe), email services (SendGrid, Resend), cloud storage (S3), analytics, or any external API. For retry/circuit-breaker theory see skill-error-handling; for auth flows (OAuth, OIDC) see skill-auth; for designing your own API see skill-api-rest.
* **Iron Laws / Key Heuristics:**
  1. **Wrap every external call.** Never call `stripe.paymentIntents.create()` directly from a controller. Wrap it in a service so you can retry, circuit-break, log, and mock it.
  2. **Webhook handlers must be idempotent.** The same webhook WILL be delivered more than once. Processing it twice must not create duplicate records or duplicate side effects.
  3. **Verify every webhook signature.** An unverified webhook endpoint is an unauthenticated write API. Attackers will find it.
  4. **Respect rate limits proactively.** Don't wait for 429s — track your usage, implement client-side throttling, and back off gracefully.

### `skill-observability`
* **Description:** Observability architecture — structured logging, RED/USE metrics, distributed tracing, SLOs/SLIs, correlation IDs, alerting discipline, and dashboard design for web applications. Use when setting up logging for a new service, adding metrics or tracing, defining SLOs, investigating production issues, or reviewing observability coverage in a PR. For web performance (Core Web Vitals, bundle size) see skill-performance; for error handling patterns see skill-error-handling.
* **Iron Laws / Key Heuristics:**
  1. **Structured logs only.** No `console.log('user created')` — every log line is a JSON object with level, message, timestamp, and context fields.
  2. **Every request has a correlation ID.** Generated at the edge, propagated through every service call, included in every log line and error response.
  3. **Alert on symptoms, not causes.** Alert when the error rate SLO is breached, not when CPU hits 80%. CPU at 80% might be fine; error rate at 5% never is.
  4. **If you can't measure it, you can't ship it.** Every feature ships with its metrics. A feature without telemetry is invisible in production.

### `skill-performance`
* **Description:** Web application performance — Core Web Vitals, bundle optimization, image/font loading, caching strategy, API latency, database queries, and rendering performance. Use when investigating slow page loads, optimizing Lighthouse scores, debugging API latency, or planning a performance budget. For general performance methodology see shared/skill-performance.
* **Iron Laws / Key Heuristics:**
  1. **Lab data ≠ field data.** Lighthouse on your laptop doesn't predict real-user metrics. Both matter; field data is ground truth.
  2. **Optimize for the median network and device, not yours.** Real users are on 4G phones, not gigabit fiber on an M3 Pro.
  3. **Performance budgets must be enforced in CI**, not aspirational. Unenforced budgets always slip.

### `skill-qa`
* **Description:** Testing strategy and quality assurance discipline — test type selection, testing pyramid economics, component and API testing patterns, visual regression, contract testing, CI quality gates, and flaky test management. Use when choosing a testing strategy for a new project, adding tests to an existing codebase, setting up CI quality gates, debugging flaky tests, or reviewing test coverage in a PR. For TDD methodology see shared/skill-tdd; for accessibility testing see skill-a11y; for database testing see skill-database.
* **Iron Laws / Key Heuristics:**
  1. **Test behavior, not implementation.** If refactoring the internals breaks your test, the test is coupled to implementation. Test inputs → outputs.
  2. **Every bug gets a regression test.** Found a bug? Write a test that fails with the bug present, then fix it. Never fix a bug without a test.
  3. **Flaky tests are bugs.** A test that sometimes passes is never trustworthy. Fix it, quarantine it, or delete it — never ignore it.
  4. **CI must be green to merge.** No "it's flaky, just re-run." No "I'll fix the test later." Green CI is a non-negotiable gate.

### `skill-validation`
* **Description:** Input validation architecture — where to validate, schema libraries (Zod, Pydantic, Joi), shared schemas between frontend and backend, form integration, custom validators, and sanitization. Use when adding validation to a new endpoint, choosing a validation library, sharing schemas across client and server, or reviewing validation coverage in a PR. For error response shape see skill-error-handling; for form UX (labels, ARIA) see skill-a11y; for auth-specific validation see skill-auth.
* **Iron Laws / Key Heuristics:**
  1. **Validate at the boundary, always.** The API endpoint validates before calling the service. The frontend validates before submitting. The queue consumer validates before processing. Never trust upstream.
  2. **Use schemas, not if-statements.** `if (!email || !email.includes('@'))` is a bug factory. `z.string().email()` is a contract.
  3. **Share schemas between frontend and backend.** If the frontend accepts an input that the backend rejects, the UX is broken. One schema, two runtimes.
  4. **Sanitize output, not just input.** Escaping HTML on output (not stripping on input) prevents XSS while preserving data fidelity.

## Domain: ML

### `skill-bias-and-fairness`
* **Description:** Bias and fairness best practices for ML systems. Use when detecting bias, ensuring fairness, or mitigating unfair outcomes. Covers bias detection, fairness metrics, and mitigation strategies.
* **Heuristics:** Enforce standard discipline for this domain.

### `skill-compute-infra`
* **Description:** ML compute infrastructure — picking GPU/TPU instance types, sizing distributed training jobs, running on SLURM/Ray/Kubernetes, and applying DDP/FSDP/ZeRO parallelism. Use when training won't fit on one GPU, when you need to choose between A100/H100/MI300, when setting up multi-node jobs, or when sizing a cluster budget. For inference-time serving infra (vLLM, Triton, autoscaling), see `skill-model-serving`; for the lifecycle around training (pipelines, registries), see `skill-mlops`.
* **Iron Laws / Key Heuristics:**
  1. **Profile before you scale.** A poorly-utilized 8x A100 node costs more than a well-utilized 1x A100. Run `nvidia-smi dmon`, `torch.profiler`, or `nsys` first. Multi-GPU does not fix a data-loading bottleneck.
  2. **Match parallelism to the bottleneck.** OOM on weights → FSDP/ZeRO. OOM on activations → activation checkpointing or tensor parallel. Compute-bound → DDP. Picking the wrong axis just adds communication overhead.
  3. **Spot/preemptible without checkpointing is a coin-flip with your budget.** If a 24-hour job has no resume-from-checkpoint, never use spot. With checkpointing every 30 minutes, spot saves 60–80%.

### `skill-data-collection`
* **Description:** Sourcing and ingesting data for ML — public datasets, APIs, web scraping (static, SPA, paginated), authenticated endpoints, and the legal/ethical envelope around all of it. Use when a project needs data that doesn't exist yet in the warehouse, when designing an ingestion job, or when a scrape has stopped working. For cleaning/transforming what you collected see `skill-data-preprocessing`; for tracking the resulting dataset version see `skill-data-versioning`; for the ethics posture itself see `shared/skill-ethics`.
* **Iron Laws / Key Heuristics:**
  1. **Provenance or it didn't happen.** Every row needs a recorded `source`, `collected_at`, and `collection_config_hash`. Without these you cannot reproduce, re-scrape, or defend the dataset in review.
  2. **Read the license before you write the parser.** "Public on the web" is not "free to use". Check ToS, robots.txt, dataset license, and downstream commercial restrictions *before* you spend a week building the pipeline.
  3. **A scraper that doesn't fail loudly is a scraper that lies.** If pagination ends early, an auth token expires, or a selector breaks, the job must error — not return a smaller, silently corrupted dataset.

### `skill-data-preprocessing`
* **Description:** Cleaning and transforming raw tabular data for ML — handling missing values, outliers, duplicates, scaling, encoding, and avoiding train/test leakage. Use when preparing a dataset for modeling, when fixing a notebook that's mutating dataframes inconsistently, or when a model trained great offline but tanked in production. For creating new features from cleaned data see `skill-feature-engineering`; for collecting raw data in the first place see `skill-data-collection`.
* **Iron Laws / Key Heuristics:**
  1. **Fit on train, transform on everything.** Every fitted statistic — mean, median, scale, vocabulary, IQR cutoffs — comes from the training set. Computing it on `train + test` or on the full dataframe before splitting is leakage. Always.
  2. **Pandas operations are not in-place by default.** `df.dropna()` returns a new dataframe and discards it. Either reassign (`df = df.dropna()`) or use `inplace=True`. Reading a notebook that does neither is reading a bug.
  3. **Save the fitted preprocessor with the model.** Inference-time preprocessing must apply the same fitted transformer (same scaler, same encoder, same imputer) the model was trained with. Recomputing at inference = silent skew.

### `skill-data-versioning`
* **Description:** Versioning datasets and data artifacts for ML — DVC, Git LFS, lakeFS, MLflow dataset logging, and the discipline of pinning data state to model state. Use when the same code produces different metrics on different days, when a colleague can't reproduce your result, when setting up a new ML repo, or when adopting a feature/data store. For training-config and seed reproducibility see `skill-reproducibility`; for the cleaning steps applied to raw data see `skill-data-preprocessing`.
* **Iron Laws / Key Heuristics:**
  1. **Data version is part of the model version.** Every model artifact records the exact dataset hash that produced it. Without this, "reproducible training" is fiction.
  2. **Data does not live in git; pointers do.** A `.dvc` pointer or LFS placeholder goes in git. The actual bytes go to object storage. Mixing them tanks repo clone times for everyone forever.
  3. **Schema drift is a versioning event.** A new column, a renamed field, a changed type — these are version bumps, not "small fixes". Otherwise downstream code breaks invisibly.

### `skill-experiment-tracking`
* **Description:** Tracking ML experiments — picking between MLflow, Weights & Biases, Neptune, Comet, and TensorBoard, structuring runs/projects/artifacts, deciding self-host vs SaaS, and avoiding the "200 untitled runs" anti-pattern. Use when starting a new ML project, when comparing tools, when migrating between trackers, or when a tracker has become a graveyard. For the registry/promotion workflow built on top of tracking see `skill-mlops`; for reproducibility seeds and env pinning see `skill-reproducibility`.
* **Iron Laws / Key Heuristics:**
  1. **Every training run is a logged run, or it didn't happen.** Notebook runs without tracking go in a sandbox folder. The moment a result is shared, it has a tracked run with config + git SHA + data version.
  2. **Pick one tool per org, then commit.** Mixing MLflow and W&B "because both have nice features" creates two graveyards instead of one knowledge base. Choose, document, enforce.
  3. **An experiment without a meaningful name is a graveyard plot.** `Run-2026-04-12-19-32-untitled-29` is not a name. The run name encodes the hypothesis being tested: `lr-sweep-baseline-augmentation-on`.

### `skill-explainability`
* **Description:** Model explainability and ML results interpretation. Use when explaining model decisions, computing feature attributions (SHAP, LIME), running error analysis, or communicating ML outputs to stakeholders. Covers technical explanation methods AND interpreting/communicating the results those methods produce.
* **Iron Laws / Key Heuristics:**
  1. **Correlation in an explanation is not causation in the world.** SHAP tells you what the model relied on, not what actually causes the outcome. Never present feature importance as a causal claim.
  2. **Local ≠ global.** A feature with low global importance can dominate a single prediction; a globally important feature can be irrelevant for a given case. Pick the right scope for the question being asked.
  3. **Validate every explanation against held-out behavior.** A SHAP value that contradicts test-set patterns is a bug, not an insight.

### `skill-feature-engineering`
* **Description:** Building, transforming, and selecting features without leaking information from the future or the test set. Covers numerical/categorical/temporal/text features, target/frequency encoding done leak-free, interaction terms, and feature stores. Use when designing features, when accuracy on training is dramatically better than on validation, or when reviewing a notebook for hidden leakage. For raw cleaning before features see `skill-data-preprocessing`; for feature stores at production scale see `skill-mlops`.
* **Iron Laws / Key Heuristics:**
  1. **Fit on train, transform on test.** Every fitted statistic — mean, scale, target mean, vocabulary, PCA components — comes from training data only. Anything else is leakage.
  2. **Time-aware features must respect time.** Lag, rolling, and target-aggregate features computed across the full series leak the future into training rows. Use `expanding`, `rolling` with proper offsets, or `groupby(...).shift()`.
  3. **A feature that requires the target to compute belongs in a cross-fold pipeline.** Naive target encoding = leakage. There is no "I'll be careful" exception; encode it correctly or pick a different encoding.

### `skill-finetuning`
* **Description:** Adapting a pretrained model to a downstream task — full fine-tuning, parameter-efficient methods (LoRA, QLoRA, adapters, prefix-tuning), instruction tuning, and the discipline that prevents catastrophic forgetting and overfitting on small datasets. Use when adapting a foundation model to your data, choosing between full FT and PEFT, debugging a fine-tune that lost the base model's capabilities, or preparing a deployable adapter. For training from scratch see `skill-training`; for prompting an unmodified model see `skill-prompt-engineering`.
* **Iron Laws / Key Heuristics:**
  1. **Try prompts and RAG first.** Fine-tuning is the heaviest, most expensive, hardest-to-revert lever. If a well-engineered prompt or retrieval augmentation hits your bar, ship that.
  2. **PEFT before full fine-tuning.** A LoRA adapter trained at 1-5% of the parameters reaches near-full-FT quality on most adaptation tasks at a fraction of the cost and with no catastrophic forgetting. Reach for full FT only when PEFT demonstrably underperforms.
  3. **Hold out a "general capability" eval.** Fine-tuning silently degrades unrelated abilities. Always measure on the original benchmarks (or a small slice of them) AS WELL as your task metric — see "Catastrophic Forgetting" below.
  4. **Lower the LR by 10-100× from training-from-scratch.** The base model is in a delicate basin; large updates ruin what's already there.

### `skill-ml-evaluation`
* **Description:** Rigorous offline ML evaluation — picking metrics that match the business cost, computing bootstrap confidence intervals, comparing models with statistical tests, and assessing calibration (Brier, ECE, reliability diagrams). Use when measuring model quality, comparing two candidate models, or producing numbers a stakeholder will defend in review. For production-time monitoring of these metrics see `skill-monitoring`; for fairness-stratified evaluation see `skill-bias-and-fairness`.
* **Iron Laws / Key Heuristics:**
  1. **No point estimate without an interval.** Every reported metric gets a 95% CI. A model that's 0.82 ± 0.03 AUC and one that's 0.84 ± 0.04 AUC are not distinguishable; pretending otherwise is dishonest.
  2. **Choose the metric before you see the test set.** Picking the metric that makes your model look best is `p-hacking`. The metric is part of the problem definition, not the result.
  3. **Calibration matters whenever probabilities are used.** If downstream code uses `p > 0.5` or expects "70% means 70 out of 100", a model can be high-AUC and dangerously miscalibrated. Always check.

### `skill-mlops`
* **Description:** MLOps — the systems engineering around ML models in production. Pipelines, model registries, CI/CD for ML, scheduled retraining, environment promotion. Use when designing or debugging the lifecycle that takes a notebook to production: training pipeline, registry, deployment, retraining trigger. For training algorithm choices see `skill-training`; for runtime serving infra see `skill-model-serving`; for data versioning see `skill-data-versioning`.
* **Iron Laws / Key Heuristics:**
  1. **Every model in production has a known git commit, data version, and training config.** If you can't answer "what produced this model?" in under a minute, you don't have MLOps — you have hope.
  2. **Promotion is a gate, not an event.** "Move to prod" must run an evaluation suite (offline + canary) and block on regression. A merge-button promotion is a bug factory.
  3. **No retraining without a rollback.** Automated retraining without the ability to revert to the previous model in <5 minutes is a foot-gun. Retain N previous versions, hot-swappable.

### `skill-model-architecture`
* **Description:** Designing neural network architectures — picking and composing layers for tabular, vision, sequence, and text/audio inputs. Covers the architecture decision rubric, residual/normalization/regularization patterns, and the common bug patterns that make models fail to learn at all. Use when designing a new model from scratch or replacing a component (e.g., swapping an LSTM for a Transformer block). For picking among existing model families (XGBoost vs MLP vs ConvNet) at the high level, see `skill-model-selection`. For adapting pretrained models, see `skill-finetuning`.
* **Iron Laws / Key Heuristics:**
  1. **The architecture's inductive bias must match the data structure.** Convolutions encode translation invariance. Recurrences encode temporal order. Self-attention encodes pairwise relations. Picking the wrong primitive can't be fixed by "more layers."
  2. **Every block has normalization, residual, and a nonlinearity — in that order, debated.** Skipping any of the three is a bug ~95% of the time. Modern transformers use Pre-LN (`norm → attn/mlp → +residual`); CNNs since ResNet use Post-LN-ish variants. Pick one and stay consistent.
  3. **Sanity-check shapes and overfit a tiny batch before any real training.** If the model can't drive loss to ~0 on 16 examples, it's broken. No amount of compute will fix a bug; debug now.

### `skill-model-selection`
* **Description:** Picking a model family for a problem and tuning its hyperparameters — baselines first, decision trees by data type and size, principled hyperparameter search (grid / random / Bayesian / ASHA), and apples-to-apples comparison with proper CV and statistical tests. Use when starting a new ML problem, choosing between candidate algorithms, or deciding between hyperparameter values. For deep-learning architecture decisions specifically, see `skill-model-architecture`. For the metrics used during comparison, see `skill-ml-evaluation`.
* **Iron Laws / Key Heuristics:**
  1. **Always ship a baseline before tuning.** A `DummyClassifier` or majority-class baseline anchors what "0.85 accuracy" means. Tuning before baselines is theater.
  2. **Compare on identical splits.** Different `random_state`, different scaler fit, different fold = invalid comparison. Use a fixed pipeline and a fixed CV object.
  3. **Tune the metric you ship on.** If you ship recall@95% precision, don't tune for accuracy and check recall later — that's overfitting to the wrong objective.

### `skill-model-serving`
* **Description:** Serving trained models behind an API — framework choice (FastAPI, Triton, vLLM, TGI, TorchServe, BentoML), dynamic batching, streaming, autoscaling, latency vs throughput tradeoffs. Use when building or scaling an inference endpoint, when latency is too high, when GPU utilization is stuck low under load, or when picking between hosted and self-hosted serving. For training-side compute see `skill-compute-infra`; for the orchestration around serving see `skill-mlops`; for production monitoring of the served model see `skill-monitoring`.
* **Iron Laws / Key Heuristics:**
  1. **Latency and throughput trade off; pick one as the target.** A serving stack tuned for p99 latency will leave throughput on the table, and vice versa. "Both are important" is how you ship neither.
  2. **Batching without timeout is a lie.** Dynamic batching needs a max-wait-ms cap or tail latency goes to infinity. The cap is a hard SLA input, not a knob to forget.
  3. **Health checks must exercise the model.** A liveness probe that returns 200 because the process is alive doesn't catch a CUDA OOM, a corrupt weight file, or a tokenizer mismatch. Probe the actual `/predict` path with a fixture.

### `skill-monitoring`
* **Description:** Production ML monitoring — detecting feature/label/prediction drift, alerting on quality regressions, and instrumenting model services with metrics that catch silent failures. Use when a model is in production, when designing the observability layer for an ML service, or when a model "stopped working" and you can't tell why. For the orchestrated retraining loop that drift triggers see `skill-mlops`; for offline evaluation methodology see `skill-ml-evaluation`.
* **Iron Laws / Key Heuristics:**
  1. **Three layers or it's incomplete.** System (latency/errors), data (input distributions), and prediction (output + ground-truth lag). Missing one of these means a class of failures is invisible.
  2. **An alert without a runbook is noise.** Every alert must point to (a) what likely broke, (b) what to check first, (c) who owns it. Otherwise it gets snoozed and ignored.
  3. **Ground truth lags reality; design for it.** Labels arrive hours/days/weeks after predictions. Monitoring must use proxies (drift, prediction distribution, business metrics) that are observable in real time.

### `skill-prompt-engineering`
* **Description:** Designing prompts for production LLM applications — system prompts, XML structure, prefill, tool use, structured output, prompt caching, and evaluation. Use when shipping an LLM-backed feature, when output quality is unstable, or when token costs are high enough that caching matters. For Anthropic SDK setup, model selection, and feature configuration see the `claude-api` skill; for retrieval-augmented prompts see `skill-rag`.
* **Iron Laws / Key Heuristics:**
  1. **Structure beats verbosity.** XML tags, sectioned system prompts, and explicit output schemas produce more reliable outputs than longer free-form instructions. Bullet lists of rules beat paragraphs.
  2. **An untestable prompt is a liability.** Every shipped prompt has a fixture set with at least 20 inputs and an automated evaluation that runs on every change. "I tried it once and it worked" is not engineering.
  3. **Cache everything stable.** If a prompt has a 5,000-token preamble that doesn't change between requests, caching it cuts cost ~10x and latency ~2x. Not caching is leaving money on the table.

### `skill-rag`
* **Description:** RAG (Retrieval-Augmented Generation) systems best practices. Use when building RAG applications, document QA systems, or knowledge retrieval systems. Covers vector databases, chunking strategies, retrieval methods, and generation optimization.
* **Heuristics:** Enforce standard discipline for this domain.

### `skill-reproducibility`
* **Description:** ML reproducibility — controlling randomness, versioning data and models, pinning environments, and tracking experiments so a result can be reproduced bit-for-bit (or as close as the platform allows). Use when training models, publishing research, debugging a "different results each run" problem, or setting up a new ML repo.
* **Iron Laws / Key Heuristics:**
  1. **Seed everything, log the seed, log the framework versions.** Without all three, "reproducible" is a wish.
  2. **GPU + nondeterministic ops = best-effort only.** Document which kernels remain nondeterministic; don't claim bit-exactness you can't deliver.
  3. **Data version is part of the result.** A model trained on `data v1.2` is not the model trained on `data v1.3` — even if every other setting matches.

### `skill-training`
* **Description:** Training ML models from scratch (or near-scratch) — designing the training loop, picking optimizers and schedules, scaling across GPUs, monitoring loss curves, and preventing the failure modes that quietly waste compute. Use when authoring or auditing a training pipeline, debugging a loss that won't decrease, scaling a single-GPU loop to multi-GPU, or reviewing a teammate's training script. For fine-tuning a pretrained model see `skill-finetuning`; for parameter-efficient methods (LoRA, QLoRA) also see `skill-finetuning`.
* **Iron Laws / Key Heuristics:**
  1. **The training loop is for one job: take a batch, compute loss, step, log.** Anything else (data preprocessing, eval, checkpointing) is a separate function. A 200-line training loop is a bug surface.
  2. **Validate every 1-5% of training, not "at the end."** A loss-curve viewed in a notebook hours later is a wasted experiment. Log per-step train loss and per-N-steps val loss to your tracker.
  3. **Save a checkpoint before you need one.** Save every N steps AND on best-val-metric. A crashed run with no checkpoint is GPU-hours of pure cost.
  4. **Seed it, log the seed, log the framework versions.** Without these you can't reproduce a result and can't debug a regression — see `skill-reproducibility`.

## Domain: THESIS

### `skill-abstract-writing`
* **Description:** Abstract writing best practices for academic papers. Use when writing abstracts, summarizing research, or creating executive summaries. Covers abstract structure, content, and style.
* **Heuristics:** Enforce standard discipline for this domain.

### `skill-academic-writing`
* **Description:** Sentence- and paragraph-level discipline for academic prose — tense, voice, person, hedging calibration, and the formal register. Use when polishing the prose layer of any thesis chapter, deciding whether to use "we" vs passive, choosing a tense for a sentence, or auditing a paragraph for ambiguity and unsupported claims. For section-specific structure (Results, Discussion, etc.) see the dedicated section skills; for AI-style writing patterns see `skill-avoid-ai-writing`.
* **Iron Laws / Key Heuristics:**
  1. **Past tense for what you did and found; present for what is and what figures show; future only for proposed work.** Mixing tenses within a paragraph is the most common register defect.
  2. **Active voice unless the actor is genuinely irrelevant.** "We trained the model" beats "The model was trained." Passive is a tool, not a default.
  3. **Every adjective of degree must be earned with a number, citation, or comparison.** "Substantial improvement" without "(from 78% to 84%)" is hand-waving.
  4. **No contractions, no second person, no rhetorical questions.** Academic register excludes them. Period.
  5. **One concept, one term.** Once you've named a thing "the embedding layer," it stays "the embedding layer" for the rest of the thesis. No synonym cycling.

### `skill-argument-validator`
* **Description:** Auditing the logical structure of thesis claims — checking that conclusions follow from evidence, that warrants connecting data to claims are explicit, and that the most common ML/empirical argument flaws (overgeneralization from one dataset, post-hoc reasoning, p-hacking framing) are not present. Use when defending a contribution, anticipating reviewer objections, or auditing the argument chain in Discussion or Conclusion. For sentence-level prose polish see `skill-academic-writing`; for terminology consistency see `skill-consistency-checker`.
* **Iron Laws / Key Heuristics:**
  1. **Every claim has data, a warrant, and an explicit scope.** A claim with no data is rhetoric; a claim with no warrant is a leap; a claim with no scope is overgeneralization.
  2. **Generalization beyond the evaluated domain requires explicit justification.** If you tested only on English news articles, you cannot conclude the model "generalizes to NLP."
  3. **Statistical significance is not effect size, and effect size is not practical importance.** Each requires a separate argument.
  4. **Limitations and counterarguments are surfaced, not buried.** If a reviewer can think of a confound in 30 seconds and it isn't acknowledged, the argument fails on credibility before substance.

### `skill-avoid-ai-writing`
* **Description:** 
* **Heuristics:** Enforce standard discipline for this domain.

### `skill-citation-management`
* **Description:** Citation and reference management — choosing a tool (Zotero / Mendeley / EndNote / BibTeX / CSL), curating a personal library, generating accurate in-text citations and reference lists in the chosen style, DOI / identifier hygiene, and building the citation graph that feeds the literature review. Use when setting up a reference manager, importing or fixing BibTeX, managing identifiers and metadata, or auditing the reference list before submission. For the *style* decision (APA vs IEEE vs Chicago) and document layout, route to `skill-formatting`; for the prose work of synthesizing prior work, route to `skill-literature-review`.
* **Iron Laws / Key Heuristics:**
  1. **One library, one tool, one source of truth.** Mixing two reference managers, or maintaining a "manual" `.bib` alongside a managed one, guarantees drift and broken citations.
  2. **Every entry has a stable identifier.** DOI for journal articles; ArXiv ID for preprints; ISBN for books; URL with retrieval date as last resort. Entries without identifiers cannot be verified.
  3. **The reference list is generated, not typed.** Hand-typed references introduce errors that survive proofreading. Use the manager's export.
  4. **Every in-text citation has a reference; every reference is cited in text.** Orphan citations and orphan references are both defects.
  5. **Cite the work you actually read.** "As cited in" is acceptable for unobtainable primary sources; routine "as cited in" use signals the author has not read the cited work.

### `skill-conclusion-writing`
* **Description:** Writing the Conclusion chapter — restating the problem, synthesizing the contributions, sketching long-horizon research directions unbounded by this thesis's specific limitations, and closing with a one-paragraph reflection on broader significance. Use when drafting or revising the Conclusion, deciding what is "future work" vs Discussion's narrower next-experiments, or finalizing the contribution restatement that mirrors the Introduction. For limitations-driven next experiments and prior-work comparison, route to `skill-discussion-writing`.
* **Iron Laws / Key Heuristics:**
  1. **No new results, no new interpretations, no new comparisons to prior work.** All three were the Discussion's job. The Conclusion only synthesizes.
  2. **The contribution restatement must match the Introduction's preview verbatim or be a clear superset.** Drift between Introduction and Conclusion contributions is a defense liability.
  3. **Future Work in the Conclusion is broad and unbounded by this thesis's limitations.** Specific next experiments tied to this study's limits live in the Discussion. Mixing the two creates redundancy.
  4. **One closing paragraph, not three.** A long, ornate reflection inflates routine work. Earn the closing through specificity, not flourish.
  5. **No "the future looks bright."** Generic closings ("only time will tell," "as we move forward," "exciting times ahead") are AI-style filler. Cut on sight.

### `skill-consistency-checker`
* **Description:** Surface-level consistency audit across a complete thesis — terminology, notation, capitalization, hyphenation, abbreviation expansion, cross-reference resolution, citation-key uniqueness, and figure/table numbering. Use as the final pass before submission, after writing has stabilized and the document is structurally complete. For deeper logical / argument auditing, route to `skill-argument-validator`; for AI-style writing patterns and reflexive hedging, route to `skill-avoid-ai-writing`; for layout / fonts / page setup, route to `skill-formatting`.
* **Iron Laws / Key Heuristics:**
  1. **One concept, one term — across the entire document.** If you named a thing "the embedding layer" in Chapter 3, it stays "the embedding layer" in every later chapter. Synonyms are noise.
  2. **One symbol, one meaning — across the entire document.** Reusing `λ` for a regularization weight in Chapter 4 and a learning-rate decay in Chapter 5 is a defect. Disambiguate or rename.
  3. **Abbreviations expanded once, on first use, in the front matter and the body.** Re-expanding an abbreviation in every chapter is noise; failing to expand it on first use is a defect.
  4. **Every cross-reference resolves.** No `Section ??`, no `[?]`, no "see Section X" where Section X was renumbered.
  5. **Run this pass last, after structural and prose passes have stabilized.** Re-running consistency after major revisions is fine; running it *before* prose stabilization wastes effort because edits will reintroduce drift.

### `skill-contribution-checker`
* **Description:** Verifying that the contributions claimed in the Introduction and Conclusion are genuinely novel, supported by the work, and correctly typed (technical vs empirical vs theoretical vs artifact). Use when drafting the Contributions list, before submitting a paper or thesis, or when an advisor questions whether a claim is "new enough." For checking the logical chain that supports a contribution claim see `skill-argument-validator`.
* **Iron Laws / Key Heuristics:**
  1. **A contribution is a delta from prior art.** State the prior art and the delta; "we propose X" without context is not a contribution claim.
  2. **Each claimed contribution must trace to a specific Results subsection.** If a contribution has no experiment, table, or proof in the body, it cannot live in the Introduction.
  3. **Type the contribution honestly.** Engineering artifacts ("we built a system") are valid contributions, but should not be sold as theoretical or empirical contributions.
  4. **Three solid contributions beat seven thin ones.** Reviewers count the strongest, not the most.

### `skill-dataset-documentation`
* **Description:** Dataset documentation best practices for academic research. Use when documenting datasets, describing data sources, or ensuring data reproducibility. Covers data documentation, metadata, and data sharing.
* **Heuristics:** Enforce standard discipline for this domain.

### `skill-discussion-writing`
* **Description:** Writing the Discussion chapter — interpreting results, comparing to prior work, surfacing limitations, and proposing the narrow next experiments those limitations imply. Use when drafting or revising Discussion, deciding what counts as interpretation vs reporting, or framing limitations honestly without deflating the contribution. For broad long-horizon research directions and the closing synthesis, route to `skill-conclusion-writing`; for the logical audit of the claims this chapter makes, route to `skill-argument-validator`.
* **Iron Laws / Key Heuristics:**
  1. **No new results.** A number, table, or figure introduced for the first time in the Discussion is a Results-section defect. If a result is load-bearing for the interpretation, it must already exist in Results.
  2. **Every interpretive claim points at a Results subsection or table.** "These findings suggest X" without "(see §4.3, Table 5)" is rhetoric.
  3. **Limitations are surfaced, not buried.** A reviewer who can identify a confound in 30 seconds will reject any limitations section that fails to mention it.
  4. **Future Work in Discussion is limitations-driven and narrow.** Each entry maps 1:1 to a specific limitation in this chapter and proposes the next experiment to address it. Long-horizon directions live in the Conclusion.
  5. **Calibrate language to the evidence tier.** Single dataset → "in this setting…"; multiple datasets and seeds → "our method outperforms…"; theoretical guarantee + empirics → strongest claims permitted.

### `skill-figures-and-tables`
* **Description:** Figures and tables best practices for academic papers. Use when creating figures, designing tables, or visualizing data. Covers figure design, table formatting, and visualization best practices.
* **Heuristics:** Enforce standard discipline for this domain.

### `skill-formatting`
* **Description:** Document layout for theses and academic papers — page setup, margins, fonts, heading hierarchy, lists, code blocks, equation typesetting, figure/table placement, and the choice between LaTeX and Word. Use when configuring a thesis template, enforcing department style, choosing a citation *style* (not generating citations), or auditing layout consistency before submission. For citation generation, BibTeX management, and reference-list mechanics, route to `skill-citation-management`; for figure/table content design, route to `skill-figures-and-tables`.
* **Iron Laws / Key Heuristics:**
  1. **The department template supersedes all general guidance.** If your department mandates a font, margin, or style, use it — even when this skill or a general style guide says otherwise. Read the template before the first draft.
  2. **One toolchain for the whole document.** Mixing LaTeX and Word for different chapters creates inconsistency that no amount of polish recovers. Pick once, commit.
  3. **Consistency over preference.** Whatever font, spacing, heading style, and citation *style* you pick, apply it identically across all chapters. Inconsistent layout reads as carelessness.
  4. **Figures and tables are referenced before they appear, captioned below figures and above tables.** This is the dominant convention; some department templates invert it — follow the template.
  5. **No formatting decisions in the final week.** Layout drift in the last days before submission breaks cross-references and pagination. Lock formatting once the document is structurally complete.

### `skill-introduction-writing`
* **Description:** Writing the Introduction chapter — hook, problem statement, research questions, contribution preview, thesis outline, and the funnel structure that takes the reader from broad motivation to specific contribution. Use when drafting Chapter 1, restructuring an introduction that has bloated to 40 pages, or aligning the introduction's contributions list with what the thesis actually delivers. For surveying prior work in depth, route to `skill-literature-review`; for the formal contribution audit, route to `skill-contribution-checker`.
* **Iron Laws / Key Heuristics:**
  1. **The introduction is a funnel, not an inverted pyramid.** Open broad enough to motivate; narrow paragraph by paragraph until the contribution sits at the bottom. Reverse funnels (specific opening, broad close) hide the contribution.
  2. **No comprehensive literature review.** Cite the 5-10 most central prior works to motivate the gap; the full treatment is Chapter 2's job. If the Introduction is past 15% of the thesis, prior work has leaked in.
  3. **Research questions are numbered, falsifiable, and answered chapter-by-chapter.** "How can we improve X?" is not a research question; "Does method M outperform baseline B on tasks T1-T3?" is.
  4. **The contribution preview must match the Conclusion's restatement.** Drift between Introduction and Conclusion is a defense liability. Write the Introduction last (or revise it last), once the contributions are stable.
  5. **End with a forward pointer, not a summary.** The Introduction does not summarize what you have not yet done. It points at the chapters that will do it.

### `skill-literature-review`
* **Description:** Literature review best practices for academic papers. Use when conducting literature reviews, synthesizing research, or identifying research gaps. Covers literature search, synthesis, and gap identification.
* **Heuristics:** Enforce standard discipline for this domain.

### `skill-ml-experiment-design`
* **Description:** ML experiment design best practices for academic research. Use when designing ML experiments, planning empirical studies, or conducting ML research. Covers experimental design, evaluation metrics, and reproducibility.
* **Heuristics:** Enforce standard discipline for this domain.

### `skill-model-description`
* **Description:** Model description best practices for academic research. Use when describing ML models, documenting architectures, or reporting model details. Covers model documentation, architecture description, and hyperparameter reporting.
* **Heuristics:** Enforce standard discipline for this domain.

### `skill-research-methodology`
* **Description:** Designing and writing the Methodology chapter of a thesis — choosing among experimental, observational, ML training/evaluation, and qualitative designs; reporting at the level of detail required for replication; documenting data, materials, procedures, analysis plan, and ethics. Use when planning a study, writing the Methods chapter, or auditing methodological rigor before defense. For ML-specific evaluation procedure see `domains/ml/skill-ml-evaluation`; for dataset documentation specifically see `skill-dataset-documentation`.
* **Iron Laws / Key Heuristics:**
  1. **Replicability is the standard.** A peer with your Methods chapter, the artifacts cited, and standard tooling should be able to reproduce your study without contacting you.
  2. **Justify every design choice in one sentence.** "We used X because Y" beats "We used X." Implicit choices invite reviewer challenge.
  3. **State what you did, not what you should have done.** Methodology is descriptive of the actual study, not aspirational. Limitations belong in Discussion.
  4. **Pre-register or label exploratory.** Analyses planned before data inspection are confirmatory; analyses developed after are exploratory. Mixing these without labels is HARKing.

### `skill-results-writing`
* **Description:** Writing the Results section of a thesis or paper — what numbers to report, how to format them, what tense and voice to use, and the strict line between reporting (here) and interpretation (in skill-discussion-writing). Use when drafting or revising a Results chapter, deciding what to include in tables vs prose, or reporting statistical tests.
* **Iron Laws / Key Heuristics:**
  1. **Report, don't interpret.** "Accuracy was 84.2%" is Results. "This suggests the model generalizes well" is Discussion. Cross the line and a reviewer will (correctly) flag it.
  2. **Past tense, third person, active where possible.** "We trained the model on 5,000 examples" not "The model is trained on 5,000 examples" or "It will be shown that…"
  3. **Every claim cites a number, table, or figure.** "Performance improved" without "(from 78.3% to 84.2%, see Table 3)" is not Results — it's a wish.

### `skill-thesis-structure`
* **Description:** Architecting a thesis or dissertation — chapter ordering, length budgets per chapter, what each chapter must accomplish, and explicit handoff to the section-specific writing skills. Use when planning a thesis outline, deciding chapter boundaries, allocating word counts, or routing a writing task to the right specialist skill.
* **Iron Laws / Key Heuristics:**
  1. **One claim, one place.** If your hypothesis appears in Introduction, Methodology, and Discussion, only the Introduction should *state* it; Methodology *operationalizes* it; Discussion *evaluates* it. No re-statements of the same claim across chapters.
  2. **Results contains no interpretation; Discussion contains no new results.** This is the most-violated rule. Police it.
  3. **Every chapter has a job.** If you can't say in one sentence what a chapter accomplishes that no other chapter does, the chapter is misallocated.

## Domain: AUTOMATION

### `skill-make`
* **Description:** Make (Integromat) scenario development and design discipline. Details visual error handler directives (Rollback, Resume, Break, Ignore), transactional ACID boundaries, JSON blueprint serialization, and webhook design. Use when building, testing, or documenting Make scenarios.
* **Iron Laws / Key Heuristics:**
  1. **Never commit changes without backing up the JSON blueprint.** Make does not have built-in git-based automatic versioning. Save exported blueprints under a `blueprints/` directory in your project's Git repository.
  2. **Handle errors at the module boundary.** Use visual error handlers on any API module that is prone to network failure, rate limiting, or schema mismatches.
  3. **Prefer Webhooks over Polling.** Polling modules (e.g., checking for updates every 15 minutes) deplete operations quotas and introduce latency. Use instant webhooks wherever supported.
  4. **Enforce transaction rollback on critical databases.** If a scenario writes to multiple SQL tables or transactional APIs, use the `Rollback` directive to prevent partial state corruption.

### `skill-n8n`
* **Description:** n8n workflow development and operations discipline. Details execution database pruning, encryption key persistence, least-privilege security, credential handling, and global error workflows. Use when creating, configuring, hosting, or debugging n8n workflows, webhook integrations, or community nodes.
* **Iron Laws / Key Heuristics:**
  1. **Never run without a persistent encryption key.** Set `N8N_ENCRYPTION_KEY` to a static, secure key on startup. If left empty, n8n generates a random key on boot; if the container restarts, all credentials will be permanently corrupted.
  2. **Prune executions aggressively.** Never leave default retention on high-volume production servers. SQLite and Postgres databases will bloat and stall the system.
  3. **Isolate credentials in the UI.** Never paste API keys, passwords, or tokens directly inside HTTP or Code nodes. Use n8n's native credential helper forms.
  4. **All workflows must route to a global Error Trigger.** A webhook failure or external API timeout must not stall the pipeline silently.

### `skill-scripting`
* **Description:** Custom automation scripting discipline for Python and JavaScript/Node.js. Details hard loop iteration count safety boundaries, sorted keys schema drift checkers, JIT credentials ingestion, rate limit backoffs, and X-Workflow-Depth headers. Use when writing, refactoring, or reviewing scheduled scripts, API integrations, data sync loops, or command-line cron jobs.
* **Iron Laws / Key Heuristics:**
  1. **Every loop must have a hard boundary.** Never write `while True:` or unbounded loops. Every loop must be bound by a maximum iteration count or an explicit timeout context.
  2. **Validate schemas with sorted keys fingerprints.** Use a zero-dependency path-sorting function at the ingestion gate to detect third-party API schema drift instantly.
  3. **Respect rate-limiting backpressure.** Parse `Retry-After` headers and inject random-jitter backoffs; do not spam upstream APIs.
  4. **Propagate execution-depth headers.** Webhooks and API calls triggered by scripts must pass `X-Workflow-Depth` to prevent runaway cross-platform recursion.

### `skill-temporal`
* **Description:** Temporal.io durable execution workflow development discipline. Details workflow determinism constraints, Activity isolation for side effects, Worker Versioning, activity timeouts (Start-To-Close, Heartbeat), and idempotency keys. Use when designing, implementation, or reviewing Temporal workflows, activities, or worker services.
* **Iron Laws / Key Heuristics:**
  1. **Workflows must be strictly deterministic.** Never call external APIs, write to databases, query system clocks (e.g., `time.Now()` or `new Date()`), generate random numbers, or create UUIDs directly inside a workflow. All side effects must reside inside **Activities**.
  2. **Never deploy changes to active workflow code without versioning.** Use **Worker Versioning** (recommended) or the SDK's `GetVersion` / `Patch` API to branch code paths for in-flight executions. Modifying a running workflow definition directly breaks replay history.
  3. **Always set `StartToCloseTimeout` on Activities.** Never rely solely on `ScheduleToClose`. If a worker dies mid-activity, Temporal needs `StartToCloseTimeout` to detect the crash and reassign the task.
  4. **All Activities must be idempotent.** Activities are designed to be retried automatically upon network or server failures. They must handle duplicate executions safely without writing duplicate database rows.

### `skill-zapier`
* **Description:** Zapier workflow (Zaps) and CLI Developer Platform discipline. Details Storage by Zapier limitations, Zapier Tables, credential management, custom CLI integration structure, unit testing, and SDK error wrappers. Use when designing Zaps, writing Code steps, or building custom CLI integrations.
* **Iron Laws / Key Heuristics:**
  1. **Never store sensitive data in Storage by Zapier.** It is a public key-value store with a strict **25 KB limit per key**. Use Zapier Tables or secure external vaults (Google Drive, Box) for sensitive file processing.
  2. **Never hardcode secrets in Code steps.** Use the `inputData` parameters to pass connection credentials securely, or define a custom integration where the user authenticates via the standard UI.
  3. **Use the Zapier CLI for complex apps.** Avoid the UI-based developer editor for integrations requiring custom OAuth, multiple files, or automated tests. Version control your CLI project using Git.
  4. **Surfaces clear errors using the SDK.** In CLI integrations, wrap failures in `z.errors.Error` to present readable error messages in the user's dashboard, rather than raw stack traces.
