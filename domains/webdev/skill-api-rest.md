---
name: skill-api-rest
description: REST API design discipline — resource modeling, status codes, idempotency, pagination, versioning, and the seams where the API hands off to validation, auth, errors, and the database. Use when designing a new endpoint, reviewing an API PR, debating REST vs GraphQL, or auditing an existing API for consistency. For request validation see skill-validation; for error response shape see skill-error-handling; for endpoint authorization see skill-auth; for GraphQL alternatives see skill-api-graphql.
---

# REST API Design

A REST API's quality is measured not by how clever its routes are but by how predictable they are. The agent's job is to make the second endpoint look like the first.

## When to Activate

Use when:
- Designing a new endpoint or set of endpoints
- Reviewing a PR that adds or changes API surface
- Choosing between REST and GraphQL for a new service
- Adding pagination, filtering, sorting, or rate limiting
- Versioning a breaking change
- Standardizing error responses across a fleet of services
- A teammate asks "should this be PUT or PATCH?" / "what status code?"

**Trigger phrases:** "design the API", "add an endpoint", "REST vs GraphQL", "PUT vs PATCH", "status code", "idempotent", "pagination", "API versioning", "rate limit", "OpenAPI", "Swagger"

## When NOT to Use

| Situation | Use instead |
|---|---|
| GraphQL schema, resolvers, federation | `skill-api-graphql` |
| Request body schema validation | `skill-validation` |
| Error response shape, retries, circuit breakers | `skill-error-handling` |
| Endpoint authentication / authorization | `skill-auth` |
| Real-time push (WebSocket / SSE) | `skill-api-realtime` |
| The DB query the endpoint runs | `skill-database` |

## Iron Laws

1. **Resources are nouns; HTTP verbs are the verbs.** No `/getUser`, no `/createOrder` — they're just `GET /users/{id}` and `POST /orders`.
2. **Idempotent methods stay idempotent under retries.** GET, PUT, DELETE retried N times must equal once. POST is the exception — give it an `Idempotency-Key` header if it can be retried.
3. **Status codes are part of the contract.** 200 for OK, 201 for created, 204 for no body, 4xx for client error, 5xx for server error — never 200 with `{ "error": ... }` in the body.
4. **Every change is either backward-compatible or a new version.** Removing a field, renaming a path, or tightening validation in place is a breaking change.
5. **Validation and authorization are mandatory at the edge** — see `skill-validation` and `skill-auth`.

## Resource Modeling Rubric

| Question | Use |
|---|---|
| Is this a thing the user can list / read / update / delete? | Make it a resource: `/things`, `/things/{id}` |
| Is this an action that doesn't fit CRUD on a resource? | RPC-style sub-resource: `POST /orders/{id}/refund` (not `/refundOrder`) |
| Is the relationship a containment? | Nest: `/users/{id}/orders` |
| Is the relationship many-to-many or independent? | Top-level: `/orders?userId=...` |
| Does this require querying many resources at once? | Filtering on the collection: `/orders?status=open&userId=...` |
| Is this a tiny piece of related data fetched separately? | Sub-resource: `/users/{id}/avatar` |

Rule of thumb: if you have to think hard about whether to nest, don't. Top-level resources with filter params age better than deep nesting.

## HTTP Method & Status Code Rubric

| Method | Use for | Idempotent | Common status codes |
|---|---|---|---|
| `GET /things` | List | ✅ | 200 with array; 200 `{data: [], next: null}`; never 204 for empty |
| `GET /things/{id}` | Read | ✅ | 200, 404, 304 (with ETag) |
| `POST /things` | Create | ❌ (use `Idempotency-Key`) | 201 + `Location: /things/{id}`; 400 / 409 / 422 |
| `PUT /things/{id}` | Replace | ✅ | 200 (or 204), 404, 409 (version conflict) |
| `PATCH /things/{id}` | Partial update | ❌ in general; some teams design idempotent PATCH | 200 / 204, 404, 409 |
| `DELETE /things/{id}` | Delete | ✅ | 204 (no body), 404 if you treat missing as error, otherwise 204 again |

Status code crib:
- **200 OK** — success with body
- **201 Created** — POST succeeded; include `Location` header
- **202 Accepted** — async work queued
- **204 No Content** — success without body (common for DELETE / PUT)
- **301 / 308** — permanent redirect (308 preserves method)
- **400 Bad Request** — malformed request (parse failure, missing required header)
- **401 Unauthorized** — no/invalid credentials
- **403 Forbidden** — authenticated but not allowed
- **404 Not Found** — resource doesn't exist or you're not allowed to know
- **409 Conflict** — state conflict (version mismatch, duplicate)
- **410 Gone** — permanent removal
- **412 Precondition Failed** — `If-Match` / `If-None-Match` failed
- **422 Unprocessable Entity** — well-formed but semantic validation failed
- **429 Too Many Requests** — rate limit hit; include `Retry-After`
- **500 Internal Server Error** — uncaught exception; never user-facing detail
- **502 / 503 / 504** — upstream failure / unavailable / timeout

422 vs 400: use 400 when the request couldn't be parsed at all (bad JSON, missing required header), 422 when it parsed but didn't validate (e.g., `email` isn't an email).

## Idempotency for POST

Network retries are inevitable. Without idempotency keys, retried `POST /orders` creates duplicate orders.

```ts
// Express middleware — accept Idempotency-Key on POST
import crypto from 'node:crypto';
import { redis } from './redis';

export async function idempotency(req, res, next) {
  if (req.method !== 'POST') return next();
  const key = req.header('Idempotency-Key');
  if (!key) return next();   // optional; or return 400 if you require it

  const cacheKey = `idem:${req.user.id}:${key}`;
  const stored = await redis.get(cacheKey);
  if (stored) {
    const { status, body } = JSON.parse(stored);
    return res.status(status).json(body);
  }

  // Capture the response so retries return the same answer
  const send = res.json.bind(res);
  res.json = (body) => {
    redis.setex(cacheKey, 24 * 3600, JSON.stringify({ status: res.statusCode, body }));
    return send(body);
  };
  next();
}
```

What this enforces: a retried `POST` with the same key returns the original response, not a second creation. Use a 24-hour cache window — long enough to outlast retry storms, short enough to not bloat Redis.

## Concrete Endpoint Example

```ts
// Express + Zod + your auth middleware. The pattern, not the framework, is what matters.
import { Router } from 'express';
import { z } from 'zod';
import { requirePermission } from './auth';

const router = Router();

const CreateOrder = z.object({
  items: z.array(z.object({
    productId: z.string().uuid(),
    quantity: z.number().int().positive(),
  })).min(1),
  shippingAddressId: z.string().uuid(),
});

// POST /orders — create
router.post(
  '/orders',
  requirePermission('order.create'),
  async (req, res, next) => {
    const parsed = CreateOrder.safeParse(req.body);
    if (!parsed.success) {
      return res.status(422).json({
        error: { code: 'VALIDATION_ERROR', issues: parsed.error.issues },
      });
    }
    try {
      const order = await orderService.create(req.user.id, parsed.data);
      res.status(201)
         .location(`/orders/${order.id}`)
         .json(order);
    } catch (e) {
      next(e);   // global error handler — see skill-error-handling
    }
  },
);

// GET /orders/:id — read
router.get(
  '/orders/:id',
  requirePermission('order.read'),
  async (req, res, next) => {
    const order = await orderService.find(req.user.id, req.params.id);
    if (!order) return res.status(404).json({ error: { code: 'NOT_FOUND' } });
    res.set('ETag', `"${order.version}"`);
    if (req.header('If-None-Match') === `"${order.version}"`) {
      return res.status(304).end();
    }
    res.json(order);
  },
);

export default router;
```

What this gets right: validation at the edge (422 with structured issues), authorization via middleware, `Location` on creation, ETag for cache validation, errors flow to a global handler.

## Pagination

Cursor-based for anything that grows; offset-based only for small, stable collections.

```ts
// Cursor pagination — opaque, stable across inserts
GET /orders?limit=50&cursor=eyJpZCI6MTAwfQ
{
  "data": [...],
  "next_cursor": "eyJpZCI6MTUwfQ",
  "has_more": true
}
```

Why cursor: offset pagination skips rows that may have been inserted/deleted between requests; on a busy system this duplicates or skips items. Cursor is also faster — `WHERE id > :cursor LIMIT N` is index-friendly, while `OFFSET 100000` reads and discards 100,000 rows.

Always:
- Cap `limit` server-side (e.g., 100 max)
- Make cursor opaque (base64-encoded JSON or HMAC-signed) — clients shouldn't construct one
- Include `has_more` so clients don't need to compare lengths

## Filtering, Sorting, Field Selection

```http
GET /orders?status=open&user_id=123&sort=-created_at&fields=id,total
```

- Filtering uses query params; document the supported fields, don't accept arbitrary column names from input (SQL injection risk via ORM passthrough)
- Sort: prefix `-` for descending, support whitelisted fields only
- Field selection (sparse fieldsets) reduces payload — handy on mobile

Don't accept arbitrary `?filter=col1=val OR col2=val` strings. That's an attempt to put SQL in a query string.

## Versioning

The two real options:
1. **URL versioning** — `/v1/orders`, `/v2/orders`. Easiest to route, easy to reason about, ugly for hypermedia purists.
2. **Header versioning** — `Accept: application/vnd.example.v2+json`. Cleaner URLs, harder to test in a browser.

Default: URL versioning. Forwards-compatible changes (adding a field, adding an endpoint) are not version bumps. Bump the version only for breaking changes; keep the previous version available for at least one full release cycle.

## Rate Limiting

```ts
// Token bucket per user + per IP
import rateLimit from 'express-rate-limit';

app.use(rateLimit({
  windowMs: 60_000,
  limit: 100,
  standardHeaders: 'draft-7',  // RateLimit-Limit, RateLimit-Remaining, RateLimit-Reset
  keyGenerator: (req) => req.user?.id ?? req.ip,
}));
```

When rate-limited, return 429 with a `Retry-After` header. Different limits for unauthenticated vs authenticated traffic; tighter limits on `/login` and `/reset` (see `skill-auth`).

## Documentation: OpenAPI

Don't hand-write the docs. Generate them from code or write OpenAPI first and generate handlers/clients.

- Code-first: `zod-to-openapi`, `tsoa`, `fastify-swagger`, FastAPI (auto-generates), Spring Doc
- Schema-first: write `openapi.yaml`, generate types/clients with `openapi-typescript`, `oapi-codegen`

A REST API without published OpenAPI is a research project, not a product.

## Common Failure Modes

| Pattern | Why it fails / consequence |
|---|---|
| `200 OK` with `{ "error": ... }` body | Breaks every HTTP-aware client and proxy; cache poisoning |
| `POST /createUser` and `POST /deleteUser` | Verb in URL; you've reinvented RPC, badly |
| Unbounded `?limit=` | Memory blowup, accidental DoS |
| Offset pagination on a write-heavy table | Duplicates and skips under concurrent inserts |
| Adding a required field to v1 in place | Existing clients break overnight |
| Returning 200 for not-found because "the request succeeded" | Clients now have to look at the body to tell — no caching, no smart retries |
| Authorization in the controller, ORM call elsewhere | Side-channel skips the gate |
| Filtering by passing `?where=raw_sql` | SQL injection waiting to happen |
| 500 leaks stack trace to the client | Information disclosure; debug clue for attackers |
| No `Idempotency-Key` on a payment endpoint | Double-charge under network retry |
| `PATCH` accepts arbitrary keys | Mass-assignment vulnerability (privilege escalation through `?role=admin`) |

## API Review Checklist

- [ ] URLs are noun-based, plural, hierarchical
- [ ] Methods match semantics (no GET that mutates)
- [ ] Status codes match outcome (no 200-with-error)
- [ ] Validation runs at the boundary; errors are 422 with structured issues
- [ ] Auth middleware required, not opt-in
- [ ] Pagination is cursor-based with capped limit
- [ ] Mutating endpoints with retry potential support `Idempotency-Key`
- [ ] Errors follow the project's error envelope (see `skill-error-handling`)
- [ ] OpenAPI is generated and published
- [ ] Rate limits exist on auth-sensitive paths
- [ ] No PII / stack trace in error responses
- [ ] Versioning policy is documented and breaking changes go to a new version

## Integration

- `domains/webdev/skill-validation` — Zod / Yup / Pydantic schemas validate the request body shown above
- `domains/webdev/skill-error-handling` — uniform error envelope, retries, circuit breakers
- `domains/webdev/skill-auth` — `requirePermission` middleware shown here is implemented there
- `domains/webdev/skill-database` — DB-side details (transactions, optimistic concurrency for PATCH)
- `domains/webdev/skill-api-graphql` — when REST starts to feel wrong, this is the alternative
- `domains/webdev/skill-api-realtime` — WebSocket / SSE for push patterns REST can't serve
- `domains/webdev/skill-observability` — request logs, RED metrics, distributed tracing
- `domains/webdev/skill-deployment` — versioning policy connects to release strategy
- `superpowers:requesting-code-review` — API changes deserve a structured review

## Resources

- [REST API Design Rulebook (O'Reilly)](https://www.oreilly.com/library/view/rest-api-design/9781449317904/) — Mark Massé
- [JSON:API specification](https://jsonapi.org/) — opinionated but consistent
- [Stripe API design](https://stripe.com/docs/api) — gold standard for REST API ergonomics
- [Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines/blob/vNext/Guidelines.md)
- [HTTP Idempotency-Key Header (IETF draft)](https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/)
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
