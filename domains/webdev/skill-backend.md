---
name: skill-backend
description: Backend architecture discipline — project structure, middleware pipelines, dependency injection, background jobs, queue patterns, and the seams where architecture hands off to API design, database, auth, and error handling. Use when scaffolding a new backend service, choosing a framework, designing a middleware pipeline, adding background processing, or reviewing a backend PR for structural choices. For API endpoint design see skill-api-rest / skill-api-graphql; for database queries see skill-database; for auth see skill-auth; for error responses see skill-error-handling.
---

# Backend Architecture

The hardest backend bugs don't come from bad queries — they come from the wrong project structure, a middleware pipeline nobody can reason about, or business logic scattered across controllers and utilities.

## When to Activate

Use when:
- Scaffolding a new backend service or project structure
- Choosing between Express, Fastify, Hono, NestJS, FastAPI, Django, or Gin
- Designing a middleware pipeline (auth → validation → rate limit → handler → error)
- Adding background jobs, queues, or scheduled tasks
- Reviewing a backend PR for architectural concerns (not endpoint logic)
- Refactoring a controller that has grown into a god-object
- A teammate asks "where does this logic go?"

**Trigger phrases:** "new backend", "project structure", "middleware order", "background job", "queue pattern", "dependency injection", "service layer", "controller vs service", "Express vs Fastify", "monolith vs microservice"

## When NOT to Use

| Situation | Use instead |
|---|---|
| Designing REST endpoints / status codes / pagination | `skill-api-rest` |
| Designing a GraphQL schema or resolver | `skill-api-graphql` |
| Writing database queries, migrations, indexing | `skill-database` |
| Auth flows, password hashing, sessions, JWTs | `skill-auth` |
| Error response shape, retries, circuit breakers | `skill-error-handling` |
| Input validation schemas (Zod / Pydantic) | `skill-validation` |
| Real-time push (WebSocket / SSE) | `skill-api-realtime` |
| Docker, K8s, IaC, cloud provisioning | `skill-devops` |
| CI/CD pipelines, release strategy | `skill-deployment` |

## Iron Laws

1. **Controllers are thin.** A controller parses the request, calls a service, formats the response. If it has business logic, it's wrong.
2. **Business logic lives in the service layer.** Services don't know about HTTP, headers, or response codes — they take data in, return data out, throw domain errors.
3. **Middleware order matters and must be documented.** Auth before validation, validation before handler, error handler outermost. Swapping two middleware can create a security hole.
4. **Side effects go through queues.** Sending email, generating PDFs, calling external APIs — these don't belong in the request path. Queue them; fail gracefully if the queue is down.

## Framework Selection

| Question | Choose this | Why |
|---|---|---|
| Minimal, flexible, huge ecosystem | Express | Most middleware, most tutorials, most hireable |
| Performance-sensitive API, schema-driven | Fastify | 2-3× Express throughput, built-in validation |
| Edge/serverless, minimal footprint | Hono | Tiny runtime, works on Cloudflare/Deno/Bun/Node |
| Enterprise, large team, DI-heavy | NestJS | Opinionated structure, decorators, modules |
| Python, async-first, auto-docs | FastAPI | Pydantic validation, OpenAPI generated |
| Python, batteries-included, ORM, admin | Django | Mature, admin panel, ORM, auth built in |
| Go, high performance, compiled | Gin / Echo | Low latency, strong typing, small binary |

Default: **Fastify** for new Node.js services (perf + validation). **Express** if team is already fluent. **FastAPI** for Python.

## Project Structure

```
src/
├── server.ts              # Bootstrap: create app, load config, start listening
├── config/
│   └── index.ts           # Environment config, validated with Zod at startup
├── middleware/
│   ├── auth.ts            # Authentication (session / JWT verification)
│   ├── validate.ts        # Request body validation (Zod / Joi)
│   ├── rate-limit.ts      # Rate limiting
│   └── error-handler.ts   # Global error handler (outermost)
├── routes/
│   ├── users.ts           # Route definitions — thin, call services
│   └── orders.ts
├── services/
│   ├── user.service.ts    # Business logic — no HTTP awareness
│   └── order.service.ts
├── repositories/
│   ├── user.repo.ts       # Database access — query builders / ORM calls
│   └── order.repo.ts
├── jobs/
│   ├── worker.ts          # Queue consumer bootstrap
│   ├── send-email.job.ts  # Job handler
│   └── generate-pdf.job.ts
├── errors/
│   └── app-error.ts       # Domain error classes (see skill-error-handling)
└── types/
    └── index.ts           # Shared types / interfaces
```

What this enforces: route → service → repository layering. Each layer has one reason to change. The `jobs/` directory makes background work visible and testable.

## Middleware Pipeline

Order matters. The pipeline runs top-to-bottom on request, bottom-to-top on response.

```ts
// server.ts — Fastify example; same order applies to Express
import Fastify from 'fastify';

const app = Fastify({ logger: true });

// 1. Request ID + correlation (outermost after logger)
app.addHook('onRequest', correlationId);

// 2. Rate limiting — reject before doing work
await app.register(rateLimit, { max: 100, timeWindow: '1 minute' });

// 3. Auth — verify identity
app.addHook('onRequest', authenticate);

// 4. Routes — each route validates its own body via schema
app.register(userRoutes, { prefix: '/api/users' });
app.register(orderRoutes, { prefix: '/api/orders' });

// 5. Error handler — outermost catch
app.setErrorHandler(globalErrorHandler);
```

Why this order: rate-limit rejects floods before wasting auth work. Auth runs before any route logic. Error handler wraps everything.

## Service Layer Pattern

```ts
// services/order.service.ts — no HTTP, no req/res, just data in → data out
import { OrderRepo } from '../repositories/order.repo';
import { AppError } from '../errors/app-error';

export class OrderService {
  constructor(private orders: OrderRepo, private queue: JobQueue) {}

  async create(userId: string, items: OrderItem[]): Promise<Order> {
    // Business rule: can't order more than 50 items
    if (items.length > 50) {
      throw new AppError('ORDER_TOO_LARGE', 'Maximum 50 items per order', 422);
    }

    const order = await this.orders.insert({ userId, items, status: 'pending' });

    // Side effect → queue, not inline
    await this.queue.add('send-confirmation-email', {
      orderId: order.id,
      userId,
    });

    return order;
  }
}
```

What this enforces: service doesn't import `Request` or `Response`. It throws domain errors (not HTTP errors). Side effects go through the queue. The controller converts domain errors to HTTP responses.

## Background Jobs & Queues

```ts
// jobs/send-email.job.ts — BullMQ example
import { Worker } from 'bullmq';

const worker = new Worker('email', async (job) => {
  const { orderId, userId } = job.data;
  const order = await orderRepo.findById(orderId);
  const user = await userRepo.findById(userId);
  await emailService.send({
    to: user.email,
    template: 'order-confirmation',
    data: { order },
  });
}, {
  connection: redis,
  concurrency: 5,
  limiter: { max: 10, duration: 1000 },   // 10 emails/sec
});

worker.on('failed', (job, err) => {
  logger.error({ jobId: job?.id, err }, 'Email job failed');
});
```

| Tool | Best for |
|---|---|
| BullMQ (Node + Redis) | Job queues with retries, rate limits, priorities |
| Celery (Python + Redis/RabbitMQ) | Distributed task queues with scheduling |
| Temporal / Inngest | Long-running workflows, durable execution |
| pg-boss (Node + Postgres) | Queue without Redis (uses Postgres) |
| SQS / Cloud Tasks | Managed, serverless queue |

Queue discipline:
- **Idempotent handlers** — jobs can be retried; the second run must not duplicate side effects
- **Dead letter queue** — failed jobs go somewhere visible, not into the void
- **Concurrency limits** — don't overwhelm downstream services
- **Visibility into queue depth** — alert when backlog grows (see `skill-observability`)

## Common Failure Modes

| Pattern | Why it fails / consequence |
|---|---|
| Business logic in the controller | Can't unit-test without HTTP, can't reuse in a queue job |
| Service imports `req` / `res` | Layer boundary broken; service can't be used from a CLI or job |
| No service layer — controller calls ORM directly | Business rules scattered, duplicated across routes |
| Middleware order not documented | New dev adds auth after the route — unauthenticated access |
| Side effects inline in request path | User waits for email to send; email failure = 500 on the order |
| No dead letter queue | Failed jobs silently vanish; nobody knows email wasn't sent |
| Job handler not idempotent | Retry sends duplicate email, charges card twice |
| Environment config read from `process.env` everywhere | Typos, missing vars discovered at runtime, not startup |
| God-service with 2000 lines | Split by domain: `OrderService`, `InventoryService`, `PaymentService` |

## Backend Review Checklist

- [ ] Controllers are thin — parse request, call service, format response
- [ ] Business logic lives in services, not controllers or middleware
- [ ] Services don't import HTTP types (`Request`, `Response`, `Context`)
- [ ] Middleware order is documented and correct (rate-limit → auth → validate → route → error)
- [ ] Side effects go through a queue, not inline in the request path
- [ ] Queue jobs are idempotent
- [ ] Dead letter queue configured for failed jobs
- [ ] Environment config validated at startup (Zod / Pydantic), not at first use
- [ ] Error classes are domain-specific (see `skill-error-handling`)
- [ ] No `any` types in TypeScript services

## Integration

- `domains/webdev/skill-api-rest` — endpoint design, status codes, pagination the routes expose
- `domains/webdev/skill-api-graphql` — resolvers are the "controller" equivalent in GraphQL
- `domains/webdev/skill-database` — repositories call the DB; schema and query optimization live there
- `domains/webdev/skill-auth` — `authenticate` middleware shown here is implemented there
- `domains/webdev/skill-error-handling` — `AppError` class and global error handler details
- `domains/webdev/skill-validation` — Zod / Pydantic schemas for request validation
- `domains/webdev/skill-observability` — structured logging, queue depth metrics, request tracing
- `domains/webdev/skill-devops` — containerization and infra for the service
- `domains/webdev/skill-deployment` — CI/CD pipeline that ships the service

## Resources

- [Fastify docs](https://fastify.dev/docs/latest/) — schema validation, hooks, encapsulation
- [BullMQ](https://docs.bullmq.io/) — Redis-backed job queue for Node.js
- [The Twelve-Factor App](https://12factor.net/) — config, backing services, concurrency
- [NestJS Architecture](https://docs.nestjs.com/fundamentals/custom-providers) — DI and module patterns
- [Celery docs](https://docs.celeryq.dev/) — Python distributed task queue
