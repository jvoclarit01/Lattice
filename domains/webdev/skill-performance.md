---
name: skill-performance
description: Web application performance — Core Web Vitals, bundle optimization, image/font loading, caching strategy, API latency, database queries, and rendering performance. Use when investigating slow page loads, optimizing Lighthouse scores, debugging API latency, or planning a performance budget. For general performance methodology see shared/skill-performance.
---

# Web Performance

This skill covers the *web-specific* performance levers. The methodology (measure first, profile, optimize critical path, verify) is in `shared/skill-performance`.

## When to Activate

Use when:
- Investigating why a page or interaction feels slow
- Optimizing Core Web Vitals (LCP, INP, CLS)
- Debugging high TTFB, slow API endpoints, or N+1 queries
- Reducing bundle size or improving load times on slow networks
- Setting up a performance budget for a team or product
- Reviewing a Lighthouse / PageSpeed Insights report

**Trigger phrases:** "slow page", "high LCP", "improve Lighthouse", "bundle size", "INP", "long tasks", "API is slow", "N+1", "tree shaking", "code splitting"

## When NOT to Use

| Situation | Use instead |
|---|---|
| You don't yet have a measurement — start with methodology | `shared/skill-performance` |
| Database query design / schema | `skill-database` |
| Production monitoring setup | `skill-observability` |
| ML inference latency | `ml/skill-model-serving` |

## Iron Laws

1. **Lab data ≠ field data.** Lighthouse on your laptop doesn't predict real-user metrics. Both matter; field data is ground truth.
2. **Optimize for the median network and device, not yours.** Real users are on 4G phones, not gigabit fiber on an M3 Pro.
3. **Performance budgets must be enforced in CI**, not aspirational. Unenforced budgets always slip.

## Targets That Matter

| Metric | Target (good) | What it measures |
|---|---|---|
| LCP (Largest Contentful Paint) | < 2.5s | Time to main content visible |
| INP (Interaction to Next Paint) | < 200ms | Responsiveness across all interactions |
| CLS (Cumulative Layout Shift) | < 0.1 | Visual stability |
| TTFB (Time to First Byte) | < 600ms | Server response speed |
| FCP (First Contentful Paint) | < 1.8s | First pixel painted |
| Total bundle (JS, gzip) | < 200KB initial | Download cost |
| API P95 latency | depends; set a target | Server-side responsiveness |

INP replaced FID in 2024 — if you're still tracking FID, update.

## Frontend — Where Time Goes

In rough priority for most apps:

### 1. Critical-path rendering

- **Render-blocking resources** — every `<script>` and CSS file in `<head>` blocks paint
- **Use `defer` for non-critical JS, `async` for independent scripts, inline critical CSS** for above-the-fold styles
- **Preload** the LCP image: `<link rel="preload" as="image" href="/hero.webp">`
- **Preconnect** to required third-party origins: `<link rel="preconnect" href="https://api.example.com">`

### 2. Bundle size & code splitting

```js
// Route-based split — only load Dashboard when its route is visited
const Dashboard = lazy(() => import('./Dashboard'));

// Component-level split for heavy interactive components
const Chart = lazy(() => import('./Chart'));
```

What to enforce in CI:
- Bundle-size limit per route (e.g., `size-limit`, `bundlesize`)
- Tree-shaking is actually working (run `webpack-bundle-analyzer` or `vite-bundle-visualizer` once a sprint)
- No accidental `lodash` whole-library imports — use `lodash-es` + per-method imports, or replace

### 3. Images

- **Modern formats** — WebP for general, AVIF where supported, fall back to JPEG
- **Responsive images** — `srcset` and `sizes` so phones don't download desktop images
- **Lazy load** below the fold: `<img loading="lazy">`
- **Width and height attributes always set** — prevents CLS

```html
<img
  src="/hero-768.webp"
  srcset="/hero-480.webp 480w, /hero-768.webp 768w, /hero-1280.webp 1280w"
  sizes="(max-width: 600px) 480px, (max-width: 900px) 768px, 1280px"
  width="1280" height="720"
  alt="…"
  fetchpriority="high"
>
```

### 4. Fonts

- **Subset to characters you use** — full Latin Extended is overkill for most products
- **`font-display: swap`** so text renders before the font loads
- **Self-host where possible** — Google Fonts adds an extra DNS / TLS round-trip

### 5. Long tasks & main-thread work

INP regressions are almost always long tasks (>50ms blocks).

- **Break up heavy work** — `requestIdleCallback` or `scheduler.yield()` for non-urgent work
- **Web Workers** for CPU-heavy computation (parsing, image processing, crypto)
- **Avoid layout thrashing** — batch reads/writes to layout properties
- **Virtualize long lists** (`react-window`, `tanstack-virtual`)

## Backend — Where API Latency Goes

In rough priority:

### 1. Database queries

- **N+1 is the #1 cause of slow APIs.** Fix with eager-loading, joins, or batch loading (DataLoader pattern).
- **Add the missing index.** `EXPLAIN ANALYZE` shows the plan; sequential scans on big tables = missing index.
- **`SELECT *` is a tax** — fetch only the columns you actually use.
- **Pagination is mandatory** for any list that can grow.

```sql
EXPLAIN ANALYZE
SELECT id, email FROM users WHERE org_id = $1 ORDER BY created_at DESC LIMIT 20;
```

For depth, see `skill-database`.

### 2. Caching

| Layer | Use for | TTL guidance |
|---|---|---|
| Browser cache (Cache-Control) | Static assets | Long (months) with content hashes in filename |
| CDN | Static + cacheable HTML | Long; purge on deploy |
| Reverse proxy (Varnish, Nginx) | Cacheable API responses | Seconds-to-minutes |
| In-memory (Redis, Memcached) | Hot reads, sessions, rate limits | Seconds-to-hours |
| Application memory (LRU) | Per-process hot data | Minutes |

```js
// Cache-aside pattern
async function getUser(id) {
  const cached = await redis.get(`user:${id}`);
  if (cached) return JSON.parse(cached);
  const user = await db.users.findById(id);
  await redis.setex(`user:${id}`, 300, JSON.stringify(user));   // 5 min TTL
  return user;
}
```

Aim for >80% cache hit rate on hot keys. If you can't measure hit rate, you can't claim caching is working.

### 3. Connection pooling

```js
// Postgres example — pool, don't open per-request
import { Pool } from 'pg';
const pool = new Pool({
  max: 20,                    // tune to DB capacity, not arbitrary
  idleTimeoutMillis: 30_000,
  connectionTimeoutMillis: 2_000,
});
```

### 4. Reduce payload

- gzip / brotli compression on responses
- Field selection (GraphQL or `?fields=id,name`)
- Pagination
- HTTP/2 or HTTP/3 to amortize connection overhead

## Network

- **HTTP/2 / HTTP/3** — multiplexing, header compression, no head-of-line blocking
- **CDN for static assets and increasingly for HTML** (edge SSR)
- **`Cache-Control` and `ETag`** — let the browser do the work for unchanged resources

## Measurement

| Tool | Best for |
|---|---|
| Chrome DevTools Performance tab | Local profiling, finding long tasks |
| Lighthouse | Lab audit; in CI |
| WebPageTest | Realistic conditions, multiple locations |
| Real User Monitoring (RUM) — `web-vitals` library, Vercel Analytics, Sentry | Field data |
| `EXPLAIN ANALYZE` | Database query plans |

Always pair lab and field. Lab tells you what *can* go wrong; field tells you what *is* going wrong.

```js
// Capture Core Web Vitals from real users
import { onLCP, onINP, onCLS } from 'web-vitals';
onLCP(metric => sendToAnalytics(metric));
onINP(metric => sendToAnalytics(metric));
onCLS(metric => sendToAnalytics(metric));
```

## Common Failure Modes

| Symptom | Likely cause |
|---|---|
| LCP good locally, bad in field | Real users on slow networks; missing image preload; LCP image is below-the-fold lazy-loaded |
| INP regression after a release | New synchronous handler, large component re-render, or heavy library on a frequent path |
| CLS regression | Image without `width`/`height`, ad/embed inserted asynchronously, web font swap |
| TTFB good but first paint slow | Render-blocking JS/CSS in head |
| API P95 fine, P99 terrible | Cold-cache cases or one specific tenant with N+1 |
| Lighthouse score regresses sometimes | Test environment is noisy; need stable CI runner or median-of-N |

## Integration

- `shared/skill-performance` — methodology that governs every fix here
- `skill-database` — query optimization specifics
- `skill-observability` — RUM and APM that surface field-data regressions
- `skill-frontend` — when redesigning, build with these constraints in mind
- `skill-deployment` — performance budget gates in CI before promotion

## Resources

- [Web.dev Core Web Vitals](https://web.dev/articles/vitals)
- [`web-vitals` library](https://github.com/GoogleChrome/web-vitals)
- [WebPageTest](https://www.webpagetest.org/) · [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci)
- [Browser performance APIs (PerformanceObserver)](https://developer.mozilla.org/en-US/docs/Web/API/PerformanceObserver)
- [size-limit](https://github.com/ai/size-limit) — bundle-size budgets in CI
