---
name: skill-data-collection
description: Sourcing and ingesting data for ML — public datasets, APIs, web scraping (static, SPA, paginated), authenticated endpoints, and the legal/ethical envelope around all of it. Use when a project needs data that doesn't exist yet in the warehouse, when designing an ingestion job, or when a scrape has stopped working. For cleaning/transforming what you collected see `skill-data-preprocessing`; for tracking the resulting dataset version see `skill-data-versioning`; for the ethics posture itself see `shared/skill-ethics`.
---

# Data Collection

Collection is the first place a model can become unsalvageable. A scraper that silently truncates pagination, an API that returns shadow-banned accounts, a dataset whose license forbids commercial use — none of these are visible at training time, but all of them poison every downstream stage.

## When to Activate

Use when:
- Bootstrapping a dataset from an external source (API, scrape, public corpus)
- Replacing or augmenting a dataset that has gone stale
- A scraper that worked yesterday is now returning empty results
- Choosing between buying a dataset, scraping, or labeling from scratch
- A reviewer asks "where did this data come from and are we allowed to use it?"
- Designing an ingestion job that needs to run on a schedule

**Trigger phrases:** "scrape this site", "pull data from X API", "find a dataset for", "Selenium / Playwright", "rate limited", "robots.txt", "is this dataset usable for commercial work", "the SPA doesn't return HTML".

## When NOT to Use

| Situation | Use instead |
|---|---|
| Cleaning data you already have | `skill-data-preprocessing` |
| Versioning the resulting dataset | `skill-data-versioning` |
| Building features from raw data | `skill-feature-engineering` |
| Audit-style fairness check on a dataset | `skill-bias-and-fairness` |
| Licensing/consent/IRB review of a sourcing plan | `shared/skill-ethics` |
| General web automation that isn't producing a dataset | `webdev/skill-testing` |

## Iron Laws

1. **Provenance or it didn't happen.** Every row needs a recorded `source`, `collected_at`, and `collection_config_hash`. Without these you cannot reproduce, re-scrape, or defend the dataset in review.
2. **Read the license before you write the parser.** "Public on the web" is not "free to use". Check ToS, robots.txt, dataset license, and downstream commercial restrictions *before* you spend a week building the pipeline.
3. **A scraper that doesn't fail loudly is a scraper that lies.** If pagination ends early, an auth token expires, or a selector breaks, the job must error — not return a smaller, silently corrupted dataset.

## Source Decision Matrix

| Need | Pick | Trade-off |
|---|---|---|
| Standard benchmark task | Hugging Face Datasets / OpenML / UCI | Often already used by competitors; no edge |
| Real-world tabular | Kaggle, gov open-data portals, BigQuery public datasets | Quality varies; check license per-dataset |
| Time-series / market data | Vendor API (Polygon, AlphaVantage, Bloomberg) | Cost; but reliable, dated, licensed |
| User-generated content | Reddit / Twitter / Stack Exchange APIs (where ToS allows) | Rate limits; ToS changes frequently |
| Internal product data | Warehouse / event stream | Almost always the right answer if available |
| Niche domain, no API | Targeted scrape | Brittle; legal risk; revisit after every site update |
| Synthetic | LLM-generated / simulators | Bias from generator; useful as augmentation, not sole source |

Default order to consider: **internal warehouse → public dataset → licensed API → scrape → synthetic**. Each step down adds risk and engineering cost.

## Static HTML Scrape

```python
import hashlib
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential

USER_AGENT = "research-bot/1.0 (contact: data-team@example.com)"

@retry(stop=stop_after_attempt(5), wait=wait_exponential(min=1, max=30))
def fetch(url: str, client: httpx.Client) -> httpx.Response:
    r = client.get(url, headers={"User-Agent": USER_AGENT}, timeout=30)
    if r.status_code == 429:
        # Honor rate limits; tenacity will retry after backoff
        raise httpx.HTTPStatusError("rate limited", request=r.request, response=r)
    r.raise_for_status()
    return r

def scrape_listing(base_url: str, out_dir: Path) -> list[dict]:
    out_dir.mkdir(parents=True, exist_ok=True)
    results: list[dict] = []
    with httpx.Client(follow_redirects=True) as client:
        for page in range(1, 1_000):           # explicit upper bound, never `while True`
            url = f"{base_url}?page={page}"
            html = fetch(url, client).text
            soup = BeautifulSoup(html, "html.parser")
            items = soup.select("article.post")
            if not items:                       # explicit pagination terminator
                break
            for el in items:
                results.append({
                    "title": el.select_one("h2").get_text(strip=True),
                    "url": el.select_one("a")["href"],
                    "source": base_url,
                    "collected_at": datetime.now(timezone.utc).isoformat(),
                })
            time.sleep(1.0)                     # polite default; respect site
    return results
```

Three things this enforces: a contact in the User-Agent, exponential backoff on 429s, and an explicit page cap. The `while True` pagination loop is the most common silent-truncation bug.

## SPA / JavaScript-Rendered Pages

```python
from playwright.sync_api import sync_playwright

def scrape_spa(url: str) -> list[dict]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(user_agent=USER_AGENT)
        page = ctx.new_page()
        page.goto(url, wait_until="networkidle")

        # Many SPAs paginate by infinite scroll; scroll until row count stops growing
        prev = -1
        for _ in range(50):  # explicit cap
            count = page.locator("li.row").count()
            if count == prev:
                break
            prev = count
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(500)

        rows = page.locator("li.row").all()
        out = [{"text": r.inner_text()} for r in rows]
        browser.close()
        return out
```

Prefer Playwright over Selenium for new code — async support, more reliable network-idle detection, smaller flakes. Set `wait_until="networkidle"` (not `load`) when content fetches happen after first paint.

## Paginated / Authenticated APIs

```python
import os
from typing import Iterator

def paged_api(endpoint: str, token: str) -> Iterator[dict]:
    """Cursor pagination with token refresh awareness."""
    cursor: str | None = None
    with httpx.Client(headers={"Authorization": f"Bearer {token}"}) as client:
        while True:
            params = {"limit": 200}
            if cursor:
                params["cursor"] = cursor
            r = client.get(endpoint, params=params, timeout=30)
            if r.status_code == 401:
                raise RuntimeError("Auth expired mid-pagination — refresh token and resume from cursor")
            r.raise_for_status()
            payload = r.json()
            yield from payload["data"]
            cursor = payload.get("next_cursor")
            if not cursor:
                return
```

**Resume-from-cursor is non-negotiable** for any job that may be interrupted. Persist `cursor` to disk every N pages so a 6-hour pull doesn't restart from page 1 after a network blip.

## OAuth / Token Lifecycle

For OAuth-protected APIs, store refresh tokens in a secrets manager (not `.env`), and design the fetch loop to refresh on 401 and retry the request once. Never hard-code expiry timers — clocks drift and providers rotate keys.

```python
def with_token(req_fn, token_provider):
    """Call req_fn(token); on 401 refresh once and retry."""
    try:
        return req_fn(token_provider.current())
    except httpx.HTTPStatusError as e:
        if e.response.status_code != 401:
            raise
        return req_fn(token_provider.refresh())
```

## Dataset Documentation (the part everyone skips)

Every collected dataset gets a sibling `DATASET_CARD.md`:

```markdown
# Dataset: customer_reviews_2026q1
- Source: example.com/api/v3/reviews
- Collection date range: 2026-03-01 .. 2026-03-31
- Collection config hash: a3f2...
- License: CC-BY-4.0 (attribution required, see ATTRIBUTION.md)
- Row count: 142,318
- Known biases: English-only filter applied; geographic skew toward US/UK
- Excluded: items where author = "deleted" (n=4,201)
- Refresh cadence: monthly
- PII: emails redacted at collection time; usernames retained as IDs
- Contact: data-team@example.com
```

Without this card, the next person on the project re-derives all of it from grep — badly. See also `thesis/skill-dataset-documentation` for the academic-publication version.

## Ethics & Legal Quick-Gate

Before any non-trivial collection, answer in writing:

| Question | If "no" or unclear |
|---|---|
| Does the source's ToS / license permit this use? | Stop, escalate to legal |
| If scraping, does robots.txt allow these paths? | Stop |
| Will collected data contain PII? | Plan redaction *at collection time*, not later |
| Is consent required (GDPR/CCPA/HIPAA)? | Don't collect until consent flow exists |
| Are there protected categories that need handling? | Coordinate with `skill-bias-and-fairness` early |
| Is rate / volume reasonable for the host? | Throttle harder; add an off-hours window |

For deep treatment of consent, IRB, dual-use, and licensing chains, see `shared/skill-ethics`.

## Common Failure Modes

| Pattern | Consequence |
|---|---|
| `while True` pagination loop | Infinite loops on bug; or silent early termination on a sentinel mismatch |
| No `User-Agent` with contact | Site bans your IP; harder to recover than throttling |
| Rate-limit handling = blanket `time.sleep(60)` | Wastes hours; doesn't honor `Retry-After` header |
| Storing scraped HTML in git | Repo bloats to GB; use object storage + DVC |
| No `collected_at` per row | Can't tell stale rows from fresh ones; can't audit |
| ToS check happens after model ships | Model may be unusable; potential takedown |
| Selectors hardcoded in 30 places | One redesign breaks the whole pipeline; keep parsing in one module |
| Auth token in code / commit history | Credential leak; revoke and rotate immediately |
| Single-pass scrape, no idempotency | Re-running creates duplicates; design for `(source, source_id)` uniqueness |

## Integration

- `skill-data-preprocessing` — receives the raw artifacts produced here
- `skill-data-versioning` — pins the dataset snapshot and config that produced it
- `skill-bias-and-fairness` — review collection design for representation gaps before you scale ingestion
- `skill-mlops` — schedule the ingestion DAG; data-validation step belongs there
- `shared/skill-ethics` — license, consent, IRB, dual-use considerations
- `shared/skill-security` — secrets handling for API keys and OAuth tokens
- `thesis/skill-dataset-documentation` — formal datasheet/data-card layout for publications

## Resources

- [Datasheets for Datasets — Gebru et al.](https://arxiv.org/abs/1803.09010) — the canonical dataset-documentation framework
- [Hugging Face Datasets](https://huggingface.co/docs/datasets) — start here for NLP/CV benchmarks
- [Common Crawl access patterns](https://commoncrawl.org/get-started)
- [Playwright for Python](https://playwright.dev/python/docs/intro) — preferred over Selenium for new scrapers
- [robots.txt specification (RFC 9309)](https://www.rfc-editor.org/rfc/rfc9309.html)
- [GDPR Art. 6 lawful bases](https://gdpr-info.eu/art-6-gdpr/) — when in doubt, this is the article you cite
