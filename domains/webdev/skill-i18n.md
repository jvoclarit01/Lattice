---
name: skill-i18n
description: Internationalization and localization — translation key architecture, pluralization, ICU message format, locale negotiation, RTL support, date/number formatting, extraction tooling, and CI checks for missing keys. Use when adding multi-language support, extracting hardcoded strings, setting up i18n for a new project, fixing broken plurals, or reviewing a PR for i18n compliance. For form labels and ARIA see skill-a11y; for validation error messages see skill-validation.
---

# Internationalization (i18n) — Translation Architecture

Every hardcoded string is a translation debt. i18n done right means every user-visible string goes through `t()`, pluralization uses ICU rules (not `count === 1`), and your CI catches missing keys before users do.

## When to Activate

Use when:
- Adding multi-language support to a new or existing app
- Extracting hardcoded strings into translation keys
- Setting up i18n tooling (i18next, vue-i18n, next-intl)
- Fixing broken plurals, date formats, or RTL layout
- Adding a new locale to an existing i18n setup
- Reviewing a PR for i18n compliance (no hardcoded strings)

**Trigger phrases:** "translate", "i18n", "localization", "multi-language", "RTL", "right-to-left", "pluralization", "translation key", "locale", "hardcoded string", "date format", "number format"

## When NOT to Use

| Situation | Use instead |
|---|---|
| Form labels, ARIA attributes, screen reader text | `skill-a11y` (but strings should still be translated) |
| Validation error messages format | `skill-validation` (use `t()` for the message text) |
| Date/time handling at the DB level | `skill-database` (store UTC always) |

## Iron Laws

1. **No hardcoded user-visible strings — ever.** Every string goes through `t()`. No exceptions for "just this one button" or "it's English-only for now."
2. **Pluralization uses ICU rules, not ternaries.** `count === 1 ? 'item' : 'items'` breaks in Russian (3 plural forms), Arabic (6), and many others. Use ICU MessageFormat or your library's plural system.
3. **Store dates as UTC; format at render time.** The database stores `2024-01-15T10:30:00Z`. The UI shows `Jan 15, 2024` or `15 janv. 2024` depending on locale.
4. **Missing keys break the build.** If a key exists in `en` but not in `fr`, the CI fails. Users should never see a raw key like `signup.email_placeholder`.

## i18n Setup — React (i18next)

```ts
// i18n/config.ts
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import ICU from 'i18next-icu';
import HttpBackend from 'i18next-http-backend';
import LanguageDetector from 'i18next-browser-languagedetector';

i18n
  .use(ICU)                      // ICU MessageFormat for plurals
  .use(HttpBackend)              // Load translations from /locales/{lng}.json
  .use(LanguageDetector)         // Detect user's preferred language
  .use(initReactI18next)
  .init({
    fallbackLng: 'en',
    supportedLngs: ['en', 'es', 'fr', 'ar', 'ja'],
    ns: ['common', 'auth', 'orders'],      // Namespace per feature
    defaultNS: 'common',
    interpolation: { escapeValue: false },  // React already escapes
    detection: {
      order: ['cookie', 'navigator', 'htmlTag'],
    },
  });

export default i18n;
```

### Translation files

```json
// locales/en/common.json
{
  "greeting": "Hello, {name}!",
  "items_count": "{count, plural, one {# item} other {# items}}",
  "last_login": "Last login: {date, date, medium}"
}

// locales/es/common.json
{
  "greeting": "¡Hola, {name}!",
  "items_count": "{count, plural, one {# artículo} other {# artículos}}",
  "last_login": "Último inicio de sesión: {date, date, medium}"
}

// locales/ar/common.json — Arabic has 6 plural forms
{
  "items_count": "{count, plural, zero {لا عناصر} one {عنصر واحد} two {عنصران} few {# عناصر} many {# عنصرًا} other {# عنصر}}"
}
```

### Usage in components

```tsx
import { useTranslation } from 'react-i18next';

function OrderSummary({ items, lastLogin }: Props) {
  const { t } = useTranslation('orders');

  return (
    <div>
      <p>{t('items_count', { count: items.length })}</p>
      <p>{t('last_login', { date: lastLogin })}</p>
    </div>
  );
}
```

## Namespace Strategy

| Namespace | Contains | Loaded |
|---|---|---|
| `common` | Nav, footer, buttons, generic labels | Always |
| `auth` | Login, signup, password reset | Auth pages only |
| `orders` | Order flow, cart, checkout | Order pages only |
| `errors` | Error messages, validation feedback | On demand |
| `admin` | Admin panel strings | Admin routes only |

Lazy-load namespaces per route to avoid loading all translations upfront.

## Date, Number, and Currency Formatting

```ts
// Use Intl API — built into browsers, no library needed
const date = new Date('2024-01-15T10:30:00Z');

// Date
new Intl.DateTimeFormat('en-US', { dateStyle: 'medium' }).format(date);
// → "Jan 15, 2024"
new Intl.DateTimeFormat('fr-FR', { dateStyle: 'medium' }).format(date);
// → "15 janv. 2024"

// Number
new Intl.NumberFormat('en-US').format(1234567.89);    // → "1,234,567.89"
new Intl.NumberFormat('de-DE').format(1234567.89);    // → "1.234.567,89"

// Currency
new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(29.99);
// → "$29.99"
new Intl.NumberFormat('ja-JP', { style: 'currency', currency: 'JPY' }).format(2999);
// → "¥2,999"

// Relative time
new Intl.RelativeTimeFormat('en', { numeric: 'auto' }).format(-1, 'day');
// → "yesterday"
```

Don't use `date-fns` or `moment` for locale formatting when `Intl` does it natively.

## RTL Support

```css
/* Use CSS logical properties — works for both LTR and RTL */
.sidebar {
  margin-inline-start: 16px;    /* Not margin-left */
  padding-inline-end: 8px;      /* Not padding-right */
  border-inline-start: 2px solid;/* Not border-left */
  float: inline-start;          /* Not float: left */
  text-align: start;            /* Not text-align: left */
}
```

```tsx
// Set dir attribute based on locale
const rtlLocales = new Set(['ar', 'he', 'fa', 'ur']);

function App() {
  const { i18n } = useTranslation();
  const dir = rtlLocales.has(i18n.language) ? 'rtl' : 'ltr';

  return <html lang={i18n.language} dir={dir}>...</html>;
}
```

## Key Extraction & CI

### Extraction (automated)

```bash
# i18next-parser — scans code for t() calls, extracts keys to JSON
npx i18next-parser --config i18next-parser.config.js
```

```js
// i18next-parser.config.js
module.exports = {
  locales: ['en', 'es', 'fr', 'ar'],
  output: 'locales/$LOCALE/$NAMESPACE.json',
  input: ['src/**/*.{ts,tsx}'],
  defaultNamespace: 'common',
  keySeparator: '.',
  namespaceSeparator: ':',
};
```

### CI check for missing keys

```yaml
# .github/workflows/i18n-check.yml
- name: Check for missing translations
  run: |
    npx i18next-parser --fail-on-update
    # Exits non-zero if new keys found or keys missing in any locale
```

## Common Failure Modes

| Pattern | Why it fails / consequence |
|---|---|
| `count === 1 ? 'item' : 'items'` | Breaks in Russian, Arabic, and 100+ other languages |
| Hardcoded strings "just for now" | They never get translated; tech debt compounds |
| Concatenating translated strings | "Hello " + name + "!" breaks in SOV languages (Japanese) |
| Using `date-fns` locale instead of `Intl` | Extra bundle weight; `Intl` is native and handles all locales |
| `margin-left` in CSS | Breaks RTL layout; use `margin-inline-start` |
| No namespace strategy | All translations in one file; loads everything on every page |
| CI doesn't check missing keys | Missing translations discovered by users in production |
| Translation keys are sentences | `"Click here to submit your order"` → fragile, hard to find |
| Storing localized dates in the database | Can't reformat; locale tied to data, not presentation |

## i18n Review Checklist

- [ ] All user-visible strings use `t()` — no hardcoded text
- [ ] Pluralization uses ICU MessageFormat (not ternary operators)
- [ ] Interpolation used for dynamic values — no string concatenation
- [ ] Dates stored as UTC, formatted with `Intl.DateTimeFormat` at render
- [ ] Numbers and currencies formatted with `Intl.NumberFormat`
- [ ] CSS uses logical properties (`inline-start`, `inline-end`) not physical (`left`, `right`)
- [ ] `dir` attribute set on `<html>` based on locale
- [ ] Namespaces per feature, lazy-loaded per route
- [ ] CI check fails on missing translation keys
- [ ] Translation keys are short, descriptive identifiers (not sentences)

## Integration

- `domains/webdev/skill-frontend` — component architecture references `t()` for all strings
- `domains/webdev/skill-validation` — validation error messages should use `t()` for user-facing text
- `domains/webdev/skill-a11y` — ARIA labels and screen-reader text need translation too
- `domains/webdev/skill-error-handling` — error messages in the envelope can be localized
- `domains/webdev/skill-performance` — lazy-loaded namespaces reduce initial bundle size

## Resources

- [i18next docs](https://www.i18next.com/) — ecosystem leader for JS i18n
- [ICU MessageFormat](https://unicode-org.github.io/icu/userguide/format_parse/messages/) — the standard for plurals and formatting
- [MDN Intl API](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl) — native browser formatting
- [CSS Logical Properties](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_logical_properties_and_values) — RTL-ready CSS
- [next-intl](https://next-intl-docs.vercel.app/) — i18n for Next.js App Router
