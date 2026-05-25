---
name: skill-validation
description: Input validation architecture — where to validate, schema libraries (Zod, Pydantic, Joi), shared schemas between frontend and backend, form integration, custom validators, and sanitization. Use when adding validation to a new endpoint, choosing a validation library, sharing schemas across client and server, or reviewing validation coverage in a PR. For error response shape see skill-error-handling; for form UX (labels, ARIA) see skill-a11y; for auth-specific validation see skill-auth.
---

# Validation — Input Discipline

Every input is hostile until proven safe. Validation is the wall between user input and your business logic — it runs at the boundary, uses schemas (not ad-hoc if-statements), and is shared between frontend and backend so they can't disagree.

## When to Activate

Use when:
- Adding validation to a new API endpoint or form
- Choosing between Zod, Yup, Joi, Pydantic, or class-validator
- Sharing a validation schema between frontend and backend
- Integrating validation with a form library (React Hook Form, Formik, VeeValidate)
- Sanitizing input or output (XSS, SQL injection prevention)
- Reviewing a PR for validation coverage

**Trigger phrases:** "validate input", "Zod schema", "Pydantic model", "form validation", "sanitize", "XSS", "schema validation", "shared schema", "validation error", "required field"

## When NOT to Use

| Situation | Use instead |
|---|---|
| HTTP status codes for validation errors (422 vs 400) | `skill-api-rest` |
| Error response envelope for validation failures | `skill-error-handling` |
| Typed errors in GraphQL mutations | `skill-api-graphql` |
| Form accessibility (labels, aria-invalid, error announcements) | `skill-a11y` |
| Auth-specific input (password strength, token format) | `skill-auth` |
| Database-level constraints (UNIQUE, CHECK, FK) | `skill-database` |

## Iron Laws

1. **Validate at the boundary, always.** The API endpoint validates before calling the service. The frontend validates before submitting. The queue consumer validates before processing. Never trust upstream.
2. **Use schemas, not if-statements.** `if (!email || !email.includes('@'))` is a bug factory. `z.string().email()` is a contract.
3. **Share schemas between frontend and backend.** If the frontend accepts an input that the backend rejects, the UX is broken. One schema, two runtimes.
4. **Sanitize output, not just input.** Escaping HTML on output (not stripping on input) prevents XSS while preserving data fidelity.

## Where to Validate

| Layer | What to validate | Library |
|---|---|---|
| **Frontend form** | UX feedback before submit (field format, required, length) | React Hook Form + Zod, VeeValidate + Zod, Svelte native |
| **API boundary** | Full request body, params, query — authoritative | Zod (TS), Pydantic (Python), Joi (JS) |
| **Service layer** | Business rules (e.g., "can't order > 50 items") | Domain logic, not schema libraries |
| **Database** | Constraints (UNIQUE, NOT NULL, CHECK, FK) | DDL — last line of defense |

The API boundary is the **source of truth**. Frontend validation is a UX optimization — it must never be the only validation.

## Schema Libraries — Decision Table

| Library | Language | Strengths | When to choose |
|---|---|---|---|
| **Zod** | TypeScript | Type inference, composable, tree-shakeable | Default for TypeScript projects |
| **Pydantic** | Python | FastAPI integration, auto-docs, perf (Rust core in v2) | Default for Python |
| **Joi** | JavaScript | Mature, expressive, widely used | Legacy JS projects |
| **Yup** | TypeScript | Formik integration | Projects already using Formik |
| **Valibot** | TypeScript | Smaller bundle than Zod | Bundle-size-critical apps |
| **ArkType** | TypeScript | Runtime + type safety, fast | Performance-critical validation |

Default: **Zod** for TypeScript, **Pydantic** for Python. These are the ecosystems' winners.

## Shared Schema Pattern

```ts
// shared/schemas/user.ts — ONE schema, used by both frontend and backend
import { z } from 'zod';

export const CreateUserSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters').max(100),
  email: z.string().email('Invalid email address'),
  password: z.string().min(12, 'Password must be at least 12 characters'),
});

export type CreateUser = z.infer<typeof CreateUserSchema>;

// In the API handler (backend):
const parsed = CreateUserSchema.safeParse(req.body);
if (!parsed.success) {
  throw new ValidationError(parsed.error.issues.map(i => ({
    field: i.path.join('.'),
    message: i.message,
  })));
}

// In the form (frontend):
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

const form = useForm<CreateUser>({
  resolver: zodResolver(CreateUserSchema),
});
```

What this enforces: one schema definition, shared via a monorepo package or shared module. Frontend and backend can never disagree on what's valid.

## Form Integration (React Hook Form + Zod)

```tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { CreateUserSchema, type CreateUser } from '@shared/schemas/user';
import { useTranslation } from 'react-i18next';

export function SignupForm() {
  const { t } = useTranslation();
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<CreateUser>({ resolver: zodResolver(CreateUserSchema) });

  return (
    <form onSubmit={handleSubmit(onSubmit)} noValidate>
      <label htmlFor="email">{t('signup.email')}</label>
      <input
        id="email"
        type="email"
        autoComplete="email"
        {...register('email')}
        aria-invalid={!!errors.email}
        aria-describedby={errors.email ? 'email-err' : undefined}
      />
      {errors.email && (
        <p id="email-err" role="alert">{errors.email.message}</p>
      )}

      <label htmlFor="password">{t('signup.password')}</label>
      <input
        id="password"
        type="password"
        autoComplete="new-password"
        {...register('password')}
        aria-invalid={!!errors.password}
        aria-describedby={errors.password ? 'pw-err' : undefined}
      />
      {errors.password && (
        <p id="pw-err" role="alert">{errors.password.message}</p>
      )}

      <button type="submit" disabled={isSubmitting}>
        {t('signup.submit')}
      </button>
    </form>
  );
}
```

What this gets right: Zod schema shared with backend, `aria-invalid` + `aria-describedby` for accessibility (see `skill-a11y`), i18n via `t()` (see `skill-i18n`), `noValidate` to let Zod handle validation not the browser.

## Advanced Patterns

### Composing schemas

```ts
const AddressSchema = z.object({
  street: z.string().min(1),
  city: z.string().min(1),
  zip: z.string().regex(/^\d{5}(-\d{4})?$/),
});

const CreateOrderSchema = z.object({
  items: z.array(z.object({
    productId: z.string().uuid(),
    quantity: z.number().int().positive().max(100),
  })).min(1).max(50),
  shippingAddress: AddressSchema,
  billingAddress: AddressSchema.optional(),  // reuse
});
```

### Transforming and refining

```ts
const SearchParamsSchema = z.object({
  page: z.coerce.number().int().positive().default(1),  // coerce string→number from query params
  limit: z.coerce.number().int().min(1).max(100).default(20),
  sort: z.enum(['created', 'name', 'price']).default('created'),
  order: z.enum(['asc', 'desc']).default('desc'),
});

const DateRangeSchema = z.object({
  startDate: z.coerce.date(),
  endDate: z.coerce.date(),
}).refine(
  (d) => d.endDate > d.startDate,
  { message: 'End date must be after start date', path: ['endDate'] },
);
```

### Pydantic (Python)

```python
from pydantic import BaseModel, EmailStr, Field, field_validator

class CreateUser(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=12)

    @field_validator('password')
    @classmethod
    def password_strength(cls, v: str) -> str:
        if v.lower() == v:
            raise ValueError('Password must contain uppercase')
        return v
```

## Sanitization

Validate input; sanitize output.

```ts
// Output sanitization — prevent XSS when rendering user-generated content
import DOMPurify from 'dompurify';

// In React — dangerouslySetInnerHTML is the only place you'd need this
const safeHtml = DOMPurify.sanitize(userContent);

// Better: don't use dangerouslySetInnerHTML at all — React escapes by default
<p>{userContent}</p>  // Safe — React escapes HTML entities
```

**SQL injection** is prevented by parameterized queries, not validation — see `skill-database`.

## Common Failure Modes

| Pattern | Why it fails / consequence |
|---|---|
| Validation only on frontend | API accepts anything; curl bypasses all checks |
| `if (!email.includes('@'))` instead of a schema | Misses edge cases; not composable; error messages inconsistent |
| Frontend and backend schemas out of sync | Frontend accepts, backend rejects → confusing UX |
| Validating on input, not output (for XSS) | Stripped data on write; can't restore. Sanitize on render instead |
| No `.safeParse()` — using `.parse()` with no try/catch | Throws an uncaught ZodError; 500 instead of 422 |
| Accepting arbitrary query params for filtering | SQL injection via ORM passthrough or mass-assignment |
| Not validating file uploads (type, size) | Arbitrary file upload → RCE, storage abuse |
| Custom validator logic not tested | Business rule silently wrong; schema "passes" but data is invalid |
| Coercing types silently (`+"123"`) | `+"abc"` is `NaN`, not an error — use `z.coerce.number()` which validates |

## Validation Review Checklist

- [ ] Every API endpoint validates request body/params/query with a schema library
- [ ] Frontend and backend share the same validation schema (or a compatible one)
- [ ] Form fields have `aria-invalid` and error messages via `aria-describedby`
- [ ] `.safeParse()` (not `.parse()`) used at API boundary — errors caught, not thrown
- [ ] Validation errors return 422 with structured `details` (see `skill-error-handling`)
- [ ] File uploads validated for type (allowlist), size, and name
- [ ] Query params whitelisted — no arbitrary column filtering
- [ ] Output sanitized (not input stripped) for XSS prevention
- [ ] Custom validators have unit tests
- [ ] Schema reused via composition, not copy-pasted

## Integration

- `domains/webdev/skill-error-handling` — `ValidationError` class and 422 responses
- `domains/webdev/skill-api-rest` — Zod schemas used in endpoint examples
- `domains/webdev/skill-api-graphql` — input types feed into mutation resolver validation
- `domains/webdev/skill-frontend` — React Hook Form + Zod form pattern
- `domains/webdev/skill-auth` — password/email validation is a specialization
- `domains/webdev/skill-a11y` — `aria-invalid`, error announcements for form fields
- `domains/webdev/skill-i18n` — validation error messages may need translation
- `domains/webdev/skill-database` — database constraints are the last line of defense

## Resources

- [Zod docs](https://zod.dev/) — TypeScript-first schema validation
- [Pydantic docs](https://docs.pydantic.dev/) — Python data validation
- [React Hook Form](https://react-hook-form.com/) — performant form library
- [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
- [DOMPurify](https://github.com/cure53/DOMPurify) — XSS sanitization
