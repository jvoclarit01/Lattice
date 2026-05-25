---
name: skill-integrations
description: Third-party integration discipline — API client wrappers, webhook processing, idempotency, retry + circuit breaker patterns, rate-limit respect, SDK vs raw HTTP decisions, and testing external dependencies. Use when integrating with payment processors (Stripe), email services (SendGrid, Resend), cloud storage (S3), analytics, or any external API. For retry/circuit-breaker theory see skill-error-handling; for auth flows (OAuth, OIDC) see skill-auth; for designing your own API see skill-api-rest.
---

# Third-Party Integrations

Every external dependency is a liability. It can go down, change its API, throttle you, or leak your secrets. The job of an integration layer is to contain that blast radius — wrap it, retry it, circuit-break it, and mock it for tests.

## When to Activate

Use when:
- Integrating with a payment processor (Stripe, PayPal, Square)
- Adding email/SMS delivery (SendGrid, Resend, Twilio)
- Connecting to cloud storage (S3, GCS, Cloudflare R2)
- Processing incoming webhooks from third parties
- Wrapping an SDK or raw HTTP client for an external API
- Deciding between using an SDK and calling an API directly

**Trigger phrases:** "Stripe integration", "SendGrid", "webhook", "third-party API", "external service", "API client", "SDK wrapper", "S3 upload", "payment integration", "webhook signature"

## When NOT to Use

| Situation | Use instead |
|---|---|
| Designing your own REST API | `skill-api-rest` |
| OAuth / OIDC flows for user auth | `skill-auth` |
| Retry/circuit-breaker theory | `skill-error-handling` (patterns are reused here) |
| Storing secrets securely | `skill-devops` (secrets management) |
| Queue-based async processing | `skill-backend` (background jobs) |

## Iron Laws

1. **Wrap every external call.** Never call `stripe.paymentIntents.create()` directly from a controller. Wrap it in a service so you can retry, circuit-break, log, and mock it.
2. **Webhook handlers must be idempotent.** The same webhook WILL be delivered more than once. Processing it twice must not create duplicate records or duplicate side effects.
3. **Verify every webhook signature.** An unverified webhook endpoint is an unauthenticated write API. Attackers will find it.
4. **Respect rate limits proactively.** Don't wait for 429s — track your usage, implement client-side throttling, and back off gracefully.

## SDK vs Raw HTTP

| Choose SDK when | Choose raw HTTP when |
|---|---|
| Official SDK exists and is maintained | SDK is unmaintained or bloated |
| SDK handles auth, pagination, retries | You need fine-grained control |
| SDK types match your language | SDK wraps a simple REST API |
| Team will use multiple SDK features | You only need 1-2 endpoints |

Default: **Use the official SDK if it exists.** Only go raw HTTP if the SDK is unmaintained or you need exactly one endpoint.

## Integration Wrapper Pattern

```ts
// services/payment.service.ts — wraps Stripe, isolates the dependency
import Stripe from 'stripe';
import { CircuitBreaker } from '../lib/circuit-breaker';
import { withRetry } from '../lib/retry';
import { AppError } from '../errors/app-error';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);
const breaker = new CircuitBreaker(5, 30_000);

export class PaymentService {
  async createPaymentIntent(amount: number, currency: string, userId: string) {
    return breaker.call(() =>
      withRetry(() =>
        stripe.paymentIntents.create({
          amount,
          currency,
          metadata: { userId },
          idempotency_key: `pi_${userId}_${Date.now()}`,  // prevents duplicate charges on retry
        }),
      ),
    );
  }

  async refund(paymentIntentId: string, reason: string) {
    try {
      return await stripe.refunds.create({
        payment_intent: paymentIntentId,
        reason: 'requested_by_customer',
        metadata: { reason },
      });
    } catch (err) {
      if (err instanceof Stripe.errors.StripeError) {
        throw new AppError('PAYMENT_ERROR', err.message, 502);
      }
      throw err;
    }
  }
}
```

What this enforces: Stripe is never imported outside this file. Retry + circuit breaker wrap every call. Stripe-specific errors are translated to domain errors. Idempotency keys prevent duplicate charges.

## Webhook Processing

```ts
// routes/webhooks/stripe.ts
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

app.post('/webhooks/stripe', express.raw({ type: 'application/json' }), async (req, res) => {
  // Step 1: Verify signature (Iron Law #3)
  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(
      req.body,
      req.headers['stripe-signature']!,
      process.env.STRIPE_WEBHOOK_SECRET!,
    );
  } catch {
    return res.status(400).json({ error: 'Invalid signature' });
  }

  // Step 2: Idempotency check (Iron Law #2)
  const processed = await db.webhookEvents.findUnique({ where: { eventId: event.id } });
  if (processed) {
    return res.json({ received: true });  // Already handled — return 200
  }

  // Step 3: Process event
  try {
    switch (event.type) {
      case 'payment_intent.succeeded':
        await handlePaymentSucceeded(event.data.object as Stripe.PaymentIntent);
        break;
      case 'payment_intent.payment_failed':
        await handlePaymentFailed(event.data.object as Stripe.PaymentIntent);
        break;
      default:
        logger.info({ type: event.type }, 'Unhandled webhook event type');
    }

    // Step 4: Record successful processing
    await db.webhookEvents.create({
      data: { eventId: event.id, type: event.type, processedAt: new Date() },
    });

    res.json({ received: true });
  } catch (err) {
    logger.error({ err, eventId: event.id }, 'Webhook processing failed');
    res.status(500).json({ error: 'Processing failed' });
    // Stripe will retry — that's fine because we're idempotent
  }
});
```

What this enforces: signature verified before any processing, idempotency via `webhookEvents` table, explicit event routing, errors logged with event ID, 200 returned for already-processed events (prevents infinite retry loops).

## Rate-Limit Respect

```ts
// lib/rate-limiter-client.ts — client-side throttle for outbound API calls
class OutboundRateLimiter {
  private queue: Array<() => void> = [];
  private running = 0;

  constructor(
    private maxConcurrent: number = 5,
    private minDelay: number = 100,  // ms between requests
  ) {}

  async schedule<T>(fn: () => Promise<T>): Promise<T> {
    while (this.running >= this.maxConcurrent) {
      await new Promise<void>((resolve) => this.queue.push(resolve));
    }
    this.running++;
    try {
      const result = await fn();
      await new Promise((r) => setTimeout(r, this.minDelay));
      return result;
    } finally {
      this.running--;
      this.queue.shift()?.();
    }
  }
}

// Usage
const emailLimiter = new OutboundRateLimiter(3, 200);  // 3 concurrent, 200ms gap

async function sendBulkEmails(recipients: string[]) {
  await Promise.all(
    recipients.map((to) =>
      emailLimiter.schedule(() => emailService.send({ to, template: 'welcome' })),
    ),
  );
}
```

When you receive a `429 Too Many Requests`, read the `Retry-After` header and back off. Don't just retry immediately.

## Testing Integrations

```ts
// Mock the SERVICE, not the SDK directly
// tests/payment.service.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { PaymentService } from '../services/payment.service';

// Mock at the module level
vi.mock('stripe', () => ({
  default: vi.fn().mockImplementation(() => ({
    paymentIntents: {
      create: vi.fn().mockResolvedValue({
        id: 'pi_test_123',
        status: 'requires_payment_method',
        amount: 2000,
      }),
    },
    refunds: {
      create: vi.fn().mockResolvedValue({ id: 're_test_123', status: 'succeeded' }),
    },
  })),
}));

describe('PaymentService', () => {
  const service = new PaymentService();

  it('creates a payment intent', async () => {
    const result = await service.createPaymentIntent(2000, 'usd', 'user_123');
    expect(result.id).toBe('pi_test_123');
    expect(result.amount).toBe(2000);
  });

  it('wraps Stripe errors as AppError', async () => {
    // Simulate Stripe failure
    vi.mocked(stripe.refunds.create).mockRejectedValueOnce(
      new Stripe.errors.StripeError({ message: 'Card declined' }),
    );

    await expect(service.refund('pi_123', 'test')).rejects.toThrow(AppError);
  });
});
```

For webhook testing, use the provider's CLI:

```bash
# Stripe webhook testing
stripe listen --forward-to localhost:3000/webhooks/stripe
stripe trigger payment_intent.succeeded
```

## Common Failure Modes

| Pattern | Why it fails / consequence |
|---|---|
| Calling SDK directly from controller | Can't retry, circuit-break, or mock; blast radius is unbounded |
| No webhook signature verification | Attackers Lattice events; create fake payments/refunds |
| Webhook handler not idempotent | Duplicate delivery → duplicate order, double email |
| Ignoring `Retry-After` header on 429 | Gets rate-limited harder; eventually blocked |
| API key in source code | Compromised on push; rotated too late |
| No circuit breaker on external calls | Downstream outage cascades to your service (thread pool exhaustion) |
| Testing against real API in CI | Flaky, slow, costs money, hits rate limits |
| Not recording webhook event IDs | Can't detect duplicates; can't audit what was processed |
| Using `express.json()` for webhook routes | Stripe needs raw body for signature verification; `express.json()` parses it |

## Integration Review Checklist

- [ ] External API wrapped in a service class — not called directly from routes
- [ ] Retry + circuit breaker applied to all external HTTP calls
- [ ] Webhook signatures verified before processing
- [ ] Webhook handlers are idempotent (event ID tracked in DB)
- [ ] API keys/secrets come from environment, never source code
- [ ] Rate limits respected with client-side throttling
- [ ] External errors translated to domain errors (`AppError`)
- [ ] Integration tests mock the service, not the SDK internals
- [ ] Webhook routes use raw body parser (not `express.json()`) for signature verification
- [ ] Logs include external request/response IDs for debugging

## Integration

- `domains/webdev/skill-error-handling` — retry and circuit breaker patterns reused from here
- `domains/webdev/skill-backend` — integration services live in the service layer; async work goes through queues
- `domains/webdev/skill-auth` — OAuth flows for third-party auth providers
- `domains/webdev/skill-observability` — external call metrics (latency, error rate, circuit breaker state)
- `domains/webdev/skill-devops` — secrets management for API keys
- `domains/webdev/skill-qa` — testing strategy for external dependencies (mock at service boundary)
- `domains/webdev/skill-validation` — validate webhook payloads before processing

## Resources

- [Stripe API docs](https://stripe.com/docs/api) — gold standard for API integration
- [Stripe Webhook Best Practices](https://stripe.com/docs/webhooks/best-practices)
- [Resend](https://resend.com/docs) — modern email API
- [AWS SDK v3](https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/) — modular AWS client
- [Circuit Breaker Pattern (Martin Fowler)](https://martinfowler.com/bliki/CircuitBreaker.html)
