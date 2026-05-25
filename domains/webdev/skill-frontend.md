---
name: skill-frontend
description: Frontend architecture choices and discipline for web UIs — framework selection, styling strategy, state management, component boundaries, and the seams where UI hands off to data, accessibility, and i18n. Use when starting a new frontend, picking a framework or styling approach, refactoring component structure, or reviewing a frontend PR's structural choices. For accessibility specifics see skill-a11y; for translation/locale see skill-i18n; for input validation see skill-validation; for the WHY of slow UIs see skill-performance.
---

# Frontend — Architecture & Choice Discipline

## Before You Start: Required Skill Invocations

Lattice frontend work delegates to two installed skills. Invoke them first:

1. **Design system** (project init or major reset only):
   invoke `ui-ux-pro-max:ui-ux-pro-max` with product_type, industry, and stack.
   Output lands in `.lattice/design-system/`.

2. **Craft rules** (every UI write):
   `design-taste-frontend` auto-activates per its own SKILL.md triggers — enforces
   anti-AI-slop bans (no Inter, no purple, no h-screen, no 3-col card rows,
   dial-aware variance). Honor verdicts; do not override without operator approval.

This file covers framework / state / component architecture. Visual craft and
design tokens live in the two skills above — do not duplicate them here.

## When to Activate

Use when:
- Starting a new web app and choosing framework / build tool / styling
- Adding a major feature that needs a new state management or data-fetching pattern
- Reviewing a frontend PR for structure, not just visuals
- Refactoring a component that has grown into a god-object
- Setting up a design system or component library boundary
- Deciding between SSR, SSG, ISR, CSR, or RSC for a page
- A teammate asks "should this be one component or three?"

**Trigger phrases:** "new frontend", "which framework", "React vs Vue", "Tailwind vs CSS Modules", "component boundary", "split this component", "state management", "client component vs server component", "SSR or SPA"

## When NOT to Use

| Situation | Use instead |
|---|---|
| Concrete WCAG / keyboard / screen reader work | `skill-a11y` |
| Translation strings, locale negotiation, RTL | `skill-i18n` |
| Validating form input with Zod / Yup / Pydantic | `skill-validation` |
| Slow LCP / INP / bundle size investigation | `skill-performance` |
| Designing the API the frontend consumes | `skill-api-rest` / `skill-api-graphql` |
| Picking colors, typography, layout polish | `frontend-design:frontend-design` |
| Visual diff or pixel-perfect Figma mapping | `figma:figma-implement-design` |

## Iron Laws

1. **Pick the framework for the workload, not the resume.** A static marketing site doesn't need Next.js + Redux; a real-time dashboard does.
2. **One source of truth per piece of state.** Server data and UI state are different — don't duplicate server data into Redux.
3. **Components have one reason to change.** A `<UserProfile>` that fetches, formats, and renders breaks when any of those three change.
4. **Hardcoded strings are a bug.** Every user-visible string is a translation key (see `skill-i18n`).

## Framework Selection

| Question | Choose this | Why |
|---|---|---|
| Static or content-heavy site, low interactivity | Astro, Eleventy, Hugo | Ship HTML, hydrate islands only where needed |
| Marketing / SEO-first with some interactivity | Next.js (App Router), Nuxt, SvelteKit | RSC + SSR + ISR; hydrate sparingly |
| App-shaped UI, lots of client interaction, SEO not critical | Vite + React/Vue/Svelte (SPA) | Fast dev loop, no SSR overhead |
| Realtime / dashboard / collab tool | React or Svelte + Vite, with WebSockets/SSE | Tight render loop, fine-grained reactivity |
| Team is React-fluent, ecosystem matters | React (+ Next or Vite) | Largest ecosystem, most hireable |
| Team values progressive enhancement, smaller bundle | Svelte / SvelteKit, Vue | Smaller runtimes, simpler mental model |
| Internal tool, prototyping speed | Next.js + shadcn/ui | Batteries included, components ready |

What "fluent team" means: at least one engineer can debug the framework's reconciler / compiler / scheduler without StackOverflow. If nobody can, you're picking a framework that nobody owns.

### React vs Vue vs Svelte — short version

- **React** — biggest ecosystem, server components, most hiring market. Pay tax in mental overhead (memo, deps arrays, hooks-rules).
- **Vue** — gentler learning curve, single-file components, Composition API is now the default. Smaller community than React but mature.
- **Svelte** — compile-time framework, less runtime, idiomatic stores. Smaller ecosystem; rune-based reactivity (Svelte 5) is new.

For a green-field web app today: React with Next.js is the safe default; Svelte if your team already loves it; Vue if you're in the Laravel/Inertia world.

## Styling Strategy

| Choice | Use when | Trade-off |
|---|---|---|
| **Tailwind CSS** | Speed, design-system already exists, team is comfortable with utility classes | Long class strings; needs a component layer to stay sane |
| **CSS Modules** | You want scoped CSS without runtime, no design-system constraint | More files; less reuse without a token system |
| **CSS-in-JS (Emotion, styled-components)** | Heavy theming, runtime style switching | Runtime cost; SSR setup is non-trivial; falling out of fashion |
| **Vanilla Extract / Panda CSS** | Want type-safe styles compiled to CSS | Newer; smaller community |
| **Plain CSS + design tokens** | Small project, no framework, want minimal deps | You'll reinvent scoping |

Default for a new app: **Tailwind + a small components layer (e.g., shadcn/ui)**. It composes with React Server Components, has zero runtime, and lets you ship a v1 quickly. Use CSS Modules instead if your team has strong CSS-architect taste and wants stricter scoping.

## State Management

The most common frontend mistake: putting server data into Redux/Zustand/Pinia. Server data needs caching, refetching, and invalidation — that's TanStack Query, SWR, RTK Query, or Apollo. UI state (modals, hover, multi-step form draft) is what client stores are for.

| Data shape | Use this |
|---|---|
| Server data (lists, detail, mutations) | TanStack Query / SWR / RTK Query / Apollo |
| Local component state | `useState` / `useReducer` / Vue `ref` / Svelte `$state` |
| Cross-component UI state | React Context, Zustand, Vue's provide/inject, Svelte stores |
| App-wide complex state with time travel needs | Redux Toolkit (rare; usually overkill) |
| Form state | React Hook Form + Zod, Vee-Validate + Yup, or Svelte's native bindings |
| URL-driven state (filters, tabs) | The URL itself (`searchParams`) — don't duplicate into a store |

```tsx
// Server state — TanStack Query owns caching, refetching, invalidation
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

export function useUser(id: string) {
  return useQuery({
    queryKey: ['user', id],
    queryFn: () => fetch(`/api/users/${id}`).then(r => r.json()),
    staleTime: 30_000,
  });
}

export function useUpdateUser() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (u: User) =>
      fetch(`/api/users/${u.id}`, {
        method: 'PUT',
        body: JSON.stringify(u),
      }).then(r => r.json()),
    onSuccess: (data) => {
      qc.setQueryData(['user', data.id], data);
    },
  });
}
```

What this enforces: one place owns server data; mutations invalidate the right keys; the component never hand-rolls a fetch + setState dance.

```tsx
// UI state — Zustand owns local cross-component state, not server data
import { create } from 'zustand';

type UIState = {
  sidebarOpen: boolean;
  toggleSidebar: () => void;
};

export const useUI = create<UIState>((set) => ({
  sidebarOpen: false,
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
}));
```

Don't put `users` into this store — it'll go stale, drift from the server, and you'll write reconciliation code forever.

## Component Boundaries

A component should answer one of these:
- **Data** — owns a query / mutation, passes data down
- **Layout** — arranges children, no logic
- **Presentation** — renders props, is pure
- **Interaction** — owns local UI state and event handlers

```tsx
// BAD — one component does fetching, state, formatting, rendering, mutation
function UserPage({ id }) {
  const [user, setUser] = useState(null);
  const [editing, setEditing] = useState(false);
  useEffect(() => {
    fetch(`/api/users/${id}`).then(r => r.json()).then(setUser);
  }, [id]);
  // ... 200 more lines
}

// GOOD — split the responsibilities
function UserPage({ id }: { id: string }) {
  const { data: user, isLoading } = useUser(id);          // data
  if (isLoading) return <Skeleton />;
  if (!user) return <NotFound />;
  return <UserPageLayout user={user} />;                  // layout
}

function UserPageLayout({ user }: { user: User }) {
  const [editing, setEditing] = useState(false);          // interaction
  return editing
    ? <UserEditForm user={user} onDone={() => setEditing(false)} />
    : <UserDetails user={user} onEdit={() => setEditing(true)} />;
}

function UserDetails({ user, onEdit }: { user: User; onEdit: () => void }) {
  return (                                                // presentation
    <article>
      <h1>{user.name}</h1>
      <button onClick={onEdit}>Edit</button>
    </article>
  );
}
```

Split when: a component has more than ~200 lines, more than two responsibilities, or you're prop-drilling something three levels deep.

## Rendering Strategy (Next.js / Nuxt / SvelteKit)

| Page type | Strategy | Why |
|---|---|---|
| Marketing, blog, docs | SSG / ISR | Cacheable, fast, SEO |
| Personalized dashboard | SSR | Per-request user-specific data |
| Heavy interactive widget | CSR (client component) | RSC can't hydrate stateful islands |
| Mostly static page with one widget | RSC + Client Component island | Best of both |
| Real-time data | CSR + WebSocket/SSE | Server can't usefully render a realtime feed |

In Next.js App Router: default is server component (`async` allowed, no hooks). Add `'use client'` only at the leaves that actually need interactivity. Most teams over-mark client components and lose the RSC benefit.

## Forms

Form code is where validation, accessibility, i18n, and error handling all converge. Don't reinvent — use a form library.

```tsx
// React Hook Form + Zod — validation library shared with backend
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useTranslation } from 'react-i18next';

const Signup = z.object({
  email: z.string().email(),
  password: z.string().min(12),
});
type Signup = z.infer<typeof Signup>;

export function SignupForm() {
  const { t } = useTranslation();
  const { register, handleSubmit, formState: { errors } } =
    useForm<Signup>({ resolver: zodResolver(Signup) });

  return (
    <form onSubmit={handleSubmit((data) => signup(data))} noValidate>
      <label htmlFor="email">{t('signup.email')}</label>
      <input id="email" type="email" autoComplete="email" {...register('email')}
             aria-invalid={!!errors.email} aria-describedby="email-err" />
      {errors.email && <p id="email-err" role="alert">{errors.email.message}</p>}
      {/* … */}
      <button type="submit">{t('signup.submit')}</button>
    </form>
  );
}
```

What this gets right: Zod schema can be shared with the backend; `aria-invalid` + `aria-describedby` for screen readers (see `skill-a11y`); strings via `t()` (see `skill-i18n`); no manual `onChange` plumbing.

## Error and Loading States

Every async UI has three branches: loading, error, success. Forgetting any one is a defect.

```tsx
function UserList() {
  const { data, isLoading, error } = useQuery({ queryKey: ['users'], queryFn: fetchUsers });
  if (isLoading) return <Skeleton rows={10} />;
  if (error) return <ErrorState error={error} retry={() => /* refetch */} />;
  if (!data?.length) return <EmptyState />;
  return <ul>{data.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}
```

A "loading" spinner with no skeleton is a UX defect; a missing error branch is a correctness defect. Empty-state design matters as much as the happy path.

## Common Failure Modes

| Pattern | Why it fails / consequence |
|---|---|
| Server data lives in Zustand/Redux | Cache invalidation written by hand; eventual divergence from server |
| Every component is `'use client'` in Next App Router | Lost RSC benefits; bundles balloon; no streaming |
| God-component with fetching + state + formatting + rendering | One change touches everything; tests are integration-shaped only |
| Hardcoded English strings | Translating is a project, not a flag-flip; every fix needs `i18n` PR |
| `useEffect` for fetching | No caching, no dedup, no retries; refactor to TanStack Query / SWR |
| CSS-in-JS without SSR setup | FOUC, hydration mismatch, slow LCP |
| Form built with raw `useState` for each field | No validation surface, accessibility errors, lots of bugs |
| Tailwind classes copy-pasted across components | Need a `<Button variant>` instead of 14 places to update |
| Prop drilling 4+ levels | Missing context or compound component pattern |

## Frontend Review Checklist

- [ ] Server data goes through a query library (no `useEffect` + `fetch`)
- [ ] Client components are leaves, not entire pages (Next App Router)
- [ ] Loading, error, empty, success branches all exist
- [ ] Form has `aria-invalid`, error messages tied via `aria-describedby`
- [ ] Strings come from i18n (`t(...)`), not hardcoded
- [ ] Images have `width`, `height`, `alt`, and `loading="lazy"` below the fold
- [ ] No new `any` in TypeScript; component props are typed
- [ ] Bundle hasn't grown unexpectedly (check `size-limit` if configured)
- [ ] Component does one thing; new file if it grew a second responsibility

## Integration

- `domains/webdev/skill-a11y` — concrete WCAG, keyboard, ARIA patterns the form examples here gesture at
- `domains/webdev/skill-i18n` — translation keys, locale negotiation, RTL
- `domains/webdev/skill-validation` — Zod / Yup / Pydantic for input schemas
- `domains/webdev/skill-performance` — bundle size, Core Web Vitals, code splitting specifics
- `domains/webdev/skill-api-rest` / `skill-api-graphql` — designing the API the frontend consumes
- `frontend-design:frontend-design` — visual polish, distinctive interfaces
- `figma:figma-implement-design` — translating Figma designs to code
- `vercel:nextjs` / `vercel:shadcn` / `vercel:turbopack` — Next.js, shadcn, Turbopack expert guidance
- `superpowers:test-driven-development` — discipline for writing component tests RED-first

## Resources

- [React Server Components, Plainly](https://nextjs.org/docs/app/getting-started/server-and-client-components)
- [TanStack Query docs](https://tanstack.com/query/latest)
- [Patterns.dev](https://www.patterns.dev/) — rendering and design patterns explained
- [Refactoring UI](https://www.refactoringui.com/) — component-level visual design
- [Web.dev "Learn HTML/CSS/Forms"](https://web.dev/learn/) — semantics-first foundations
