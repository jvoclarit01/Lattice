---
name: skill-error-handling
description: Error handling architecture — error envelope standard, typed error classes, global handlers, React error boundaries, retry/circuit-breaker discipline, and the seams where errors hand off to observability and API responses. Use when designing an error strategy for a new service, adding a global error handler, debugging inconsistent error responses, or reviewing error handling in a PR. For input validation see skill-validation; for auth error flows see skill-auth; for production monitoring see skill-observability.
---

# Error Handling — Architecture & Discipline

Errors happen. The question is whether your users see a blank screen or a helpful message, and whether your on-call sees a structured log or a stack trace in Sentry with no context.

## When to Activate

Use when:
- Designing the error strategy for a new service or app
- Adding a global error handler (Express, Fastify, Next.js, FastAPI)
- Defining a project-wide error envelope for API responses
- Adding React error boundaries or frontend error recovery
- Implementing retry logic or circuit breakers for external calls
- Debugging inconsistent error responses across endpoints
- A teammate asks "what status code?" or "how do we handle this error?"

**Trigger phrases:** "error handling", "error boundary", "global error handler", "error envelope", "retry logic", "circuit breaker", "500 error", "unhandled exception", "error response format", "graceful degradation"

## When NOT to Use

| Situation | Use instead |
|---|---|
| Choosing HTTP status codes for REST endpoints | `skill-api-rest` |
| Typed errors in GraphQL (result unions) | `skill-api-graphql` |
| Validating input before it becomes an error | `skill-validation` |
| Auth-specific error flows (401/403, token expiry) | `skill-auth` |
| Logging, metrics, alerting on errors | `skill-observability` |
| Retry logic for third-party API integrations | `skill-integrations` (uses patterns from here) |

## Iron Laws

1. **Every error has a type, a code, and a message.** No naked `throw new Error('something broke')` — use typed error classes with machine-readable codes.
2. **Internal details never reach the client.** Stack traces, SQL queries, file paths — these are for logs, not for HTTP responses.
3. **Every async boundary has an error handler.** Unhandled promise rejections, uncaught exceptions, error boundaries — silence is a bug.
4. **Retries are idempotent or they don't happen.** Retrying a non-idempotent operation can double-charge, send duplicate emails, or corrupt data.

## Error Envelope Standard

Every API error response in the project uses this shape:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email address",
    "details": [
      { "field": "email", "message": "Must be a valid email" }
    ],
    "requestId": "req_abc123"
  }
}
```

| Field | Required | Purpose |
|---|---|---|
| `code` | ✅ | Machine-readable, stable across versions. Clients switch on this. |
| `message` | ✅ | Human-readable, localized if possible. UI can display this. |
| `details` | Optional | Structured data: validation issues, conflict info, rate-limit reset time |
| `requestId` | ✅ | Correlation ID for log lookup (see `skill-observability`) |

Never return `{ "error": "something went wrong" }` — that's a string, not a structured envelope.

## Typed Error Classes

```ts
// errors/app-error.ts
export class AppError extends Error {
  constructor(
    public readonly code: string,
    message: string,
    public readonly statusCode: number = 500,
    public readonly details?: unknown,
  ) {
    super(message);
    this.name = 'AppError';
  }
}

// Domain-specific errors — extend AppError
export class NotFoundError extends AppError {
  constructor(resource: string, id: string) {
    super('NOT_FOUND', `${resource} ${id} not found`, 404);
  }
}

export class ValidationError extends AppError {
  constructor(issues: Array<{ field: string; message: string }>) {
    super('VALIDATION_ERROR', 'Request validation failed', 422, issues);
  }
}

export class ConflictError extends AppError {
  constructor(message: string) {
    super('CONFLICT', message, 409);
  }
}

export class RateLimitError extends AppError {
  constructor(retryAfter: number) {
    super('RATE_LIMITED', 'Too many requests', 429, { retryAfter });
  }
}
```

What this enforces: every error thrown in the service layer carries a machine-readable code and an appropriate status code. The global handler maps `AppError` to the envelope; unknown errors become 500.

## Global Error Handler

```ts
// middleware/error-handler.ts — Express / Fastify
import { AppError } from '../errors/app-error';

export function globalErrorHandler(err: Error, req: Request, res: Response, _next: NextFunction) {
  const requestId = req.headers['x-request-id'] || crypto.randomUUID();

  if (err instanceof AppError) {
    // Known domain error — structured response, appropriate level
    req.log.warn({ err, requestId }, err.message);
    return res.status(err.statusCode).json({
      error: {
        code: err.code,
        message: err.message,
        details: err.details,
        requestId,
      },
    });
  }

  // Unknown error — log full stack, return generic message
  req.log.error({ err, requestId }, 'Unhandled error');
  return res.status(500).json({
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred',
      requestId,
    },
  });
}
```

What this enforces: known errors get their code and status; unknown errors never leak internals. Every response includes `requestId` for log correlation.

```python
# FastAPI equivalent
from fastapi import Request
from fastapi.responses import JSONResponse

class AppError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 500, details=None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(status_code=exc.status_code, content={
        "error": {
            "code": exc.code,
            "message": exc.message,
            "details": exc.details,
            "requestId": request.state.request_id,
        },
    })

@app.exception_handler(Exception)
async def unhandled_error_handler(request: Request, exc: Exception):
    logger.error("Unhandled error", exc_info=exc, request_id=request.state.request_id)
    return JSONResponse(status_code=500, content={
        "error": {
            "code": "INTERNAL_ERROR",
            "message": "An unexpected error occurred",
            "requestId": request.state.request_id,
        },
    })
```

## Frontend Error Boundaries (React)

```tsx
// components/ErrorBoundary.tsx
import { Component, type ReactNode } from 'react';

type Props = { children: ReactNode; fallback?: ReactNode };
type State = { error: Error | null };

export class ErrorBoundary extends Component<Props, State> {
  state: State = { error: null };

  static getDerivedStateFromError(error: Error) {
    return { error };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    // Send to error tracking (Sentry, etc.)
    reportError({ error, componentStack: info.componentStack });
  }

  render() {
    if (this.state.error) {
      return this.props.fallback ?? (
        <div role="alert">
          <h2>Something went wrong</h2>
          <button onClick={() => this.setState({ error: null })}>Try again</button>
        </div>
      );
    }
    return this.props.children;
  }
}

// Usage — wrap at route level, not at the app root only
<ErrorBoundary fallback={<OrderErrorFallback />}>
  <OrderPage />
</ErrorBoundary>
```

Place error boundaries at feature boundaries, not just at the app root. A crash in the order page shouldn't blank out the sidebar.

## Retry & Circuit Breaker

### Retry with exponential backoff

```ts
async function withRetry<T>(
  fn: () => Promise<T>,
  { maxRetries = 3, baseDelay = 1000 } = {},
): Promise<T> {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (err) {
      if (attempt === maxRetries) throw err;
      // Don't retry client errors (4xx) — they won't succeed on retry
      if (err instanceof AppError && err.statusCode < 500) throw err;
      const delay = baseDelay * Math.pow(2, attempt) + Math.random() * 500;
      await new Promise((r) => setTimeout(r, delay));
    }
  }
  throw new Error('unreachable');
}
```

### Circuit breaker

```ts
class CircuitBreaker {
  private failures = 0;
  private lastFailure = 0;
  private state: 'closed' | 'open' | 'half-open' = 'closed';

  constructor(
    private threshold: number = 5,
    private cooldown: number = 30_000,
  ) {}

  async call<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === 'open') {
      if (Date.now() - this.lastFailure > this.cooldown) {
        this.state = 'half-open';
      } else {
        throw new AppError('SERVICE_UNAVAILABLE', 'Circuit breaker open', 503);
      }
    }
    try {
      const result = await fn();
      this.failures = 0;
      this.state = 'closed';
      return result;
    } catch (err) {
      this.failures++;
      this.lastFailure = Date.now();
      if (this.failures >= this.threshold) this.state = 'open';
      throw err;
    }
  }
}
```

When to use which:
- **Retry** — transient network failures, 502/503/504 from upstream
- **Circuit breaker** — upstream is down or degraded; stop hammering it
- **Both** — retry inside the circuit breaker's `fn`

## Common Failure Modes

| Pattern | Why it fails / consequence |
|---|---|
| `throw new Error('failed')` without a code | Client can't distinguish error types; no i18n, no conditional handling |
| Stack trace in HTTP response | Information disclosure; attackers learn your file paths and dependencies |
| No global error handler | Unhandled exceptions crash the process or return raw framework errors |
| Error boundary only at app root | One component crash blanks the entire page |
| Retrying a non-idempotent POST | Duplicate order, double charge, duplicate email |
| No circuit breaker on flaky upstream | Thread pool exhaustion; your service goes down because theirs did |
| `catch (e) { /* ignore */ }` | Silent failures; data corruption nobody notices for days |
| 200 OK with `{ "error": "..." }` in body | Breaks every HTTP-aware client, proxy, and cache |
| Logging `err.message` but not `err.stack` | No stack trace in logs; can't find the source |
| Different error shape per endpoint | Frontend has to special-case every API call |

## Error Handling Review Checklist

- [ ] All errors use typed error classes with `code`, `message`, and `statusCode`
- [ ] Global error handler catches both `AppError` and unknown `Error`
- [ ] No stack traces or internal paths in HTTP responses
- [ ] Every response includes `requestId` for log correlation
- [ ] Error envelope follows the project standard (code + message + details + requestId)
- [ ] React error boundaries at feature boundaries, not just app root
- [ ] Retry logic only on idempotent operations
- [ ] Circuit breaker on all external service calls
- [ ] `async/await` errors are caught (no unhandled rejections)
- [ ] Error logging includes full error + request context (see `skill-observability`)

## Integration

- `domains/webdev/skill-api-rest` — status code selection, error envelope shown in endpoint examples
- `domains/webdev/skill-api-graphql` — typed errors via result unions (GraphQL's equivalent)
- `domains/webdev/skill-backend` — `AppError` class and global handler live in the project structure
- `domains/webdev/skill-validation` — validation errors feed into `ValidationError` class
- `domains/webdev/skill-auth` — auth errors (401/403) are a special case of `AppError`
- `domains/webdev/skill-observability` — structured error logging, request ID correlation, alerting
- `domains/webdev/skill-integrations` — retry + circuit breaker for third-party calls
- `domains/webdev/skill-frontend` — error boundaries, error/loading/empty state branches

## Resources

- [Express Error Handling](https://expressjs.com/en/guide/error-handling.html)
- [Fastify Error Handling](https://fastify.dev/docs/latest/Reference/Errors/)
- [React Error Boundaries](https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary)
- [Circuit Breaker Pattern (Martin Fowler)](https://martinfowler.com/bliki/CircuitBreaker.html)
- [RFC 7807 — Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc7807) — standard error format
