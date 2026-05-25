---
name: skill-a11y
description: Web accessibility discipline — semantic HTML, ARIA patterns for complex widgets, keyboard navigation, focus management in SPAs, color contrast, screen reader testing, and WCAG compliance. Use when building forms, modals, dropdowns, tabs, or any interactive component; reviewing a PR for accessibility; fixing screen reader or keyboard issues; or auditing a page against WCAG 2.2. For i18n/RTL see skill-i18n; for form validation logic see skill-validation; for visual design see skill-frontend.
---

# Accessibility (a11y) — Semantic HTML & ARIA Discipline

Accessibility isn't a feature — it's a constraint that applies to every component, every interaction, every deploy. The rule is simple: if you can't use it without a mouse, you haven't finished building it.

## When to Activate

Use when:
- Building any interactive component (form, modal, dropdown, tabs, combobox)
- Reviewing a PR for accessibility compliance
- Fixing a keyboard navigation or screen reader bug
- Running a WCAG audit against a page or component
- Adding error messages, live regions, or status updates
- Choosing between a `<div>` and a semantic element

**Trigger phrases:** "accessibility", "a11y", "screen reader", "keyboard navigation", "ARIA", "WCAG", "focus trap", "focus management", "color contrast", "alt text", "aria-label", "tab order", "skip link"

## When NOT to Use

| Situation | Use instead |
|---|---|
| Translation of accessible labels | `skill-i18n` (strings should still use `t()`) |
| Form validation logic (Zod/Pydantic) | `skill-validation` (but error display uses ARIA from here) |
| Component architecture / framework selection | `skill-frontend` |
| Visual design, colors, typography | `skill-frontend` (but contrast ratios are here) |

## Iron Laws

1. **Semantic HTML first, ARIA second.** A `<button>` is always better than `<div role="button" tabindex="0">`. ARIA is a repair tool for when HTML doesn't have the right element.
2. **Every interactive element is keyboard-accessible.** If it responds to click, it responds to Enter/Space. If it opens a menu, Escape closes it. No exceptions.
3. **Focus must be visible and managed.** When a modal opens, focus moves inside. When it closes, focus returns to the trigger. Focus indicators are never hidden with `outline: none`.
4. **Dynamic content is announced.** When content changes without a page load (toast, error, status), a live region tells screen readers what happened.

## WCAG Quick Reference

| Level | Key Requirements | Target |
|---|---|---|
| **A** (minimum) | Alt text, keyboard access, no seizure triggers, page titles | Mandatory |
| **AA** (standard) | 4.5:1 contrast, resize to 200%, focus visible, error identification | Target for most apps |
| **AAA** (enhanced) | 7:1 contrast, sign language for video, no timing | Aspirational |

**Target AA** for all production applications.

## Semantic HTML Cheat Sheet

| Instead of... | Use... | Why |
|---|---|---|
| `<div onclick>` | `<button>` | Keyboard, focus, role built-in |
| `<div class="nav">` | `<nav>` | Landmark for screen reader navigation |
| `<div class="header">` | `<header>` | Landmark |
| `<div class="main">` | `<main>` | Landmark; skip link target |
| `<span class="link">` | `<a href>` | Keyboard, focus, right-click, announced as link |
| `<div class="h2">` | `<h2>` | Heading hierarchy for screen reader outline |
| `<div class="list">` | `<ul>/<ol>` | Screen reader announces "list, 5 items" |

## Component Patterns

### Accessible Modal

```tsx
function Modal({ isOpen, onClose, title, children }: ModalProps) {
  const closeRef = useRef<HTMLButtonElement>(null);
  const previousFocus = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (isOpen) {
      previousFocus.current = document.activeElement as HTMLElement;
      closeRef.current?.focus();  // Move focus into modal
    } else {
      previousFocus.current?.focus();  // Return focus on close
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      onKeyDown={(e) => e.key === 'Escape' && onClose()}
    >
      <div className="modal-overlay" onClick={onClose} aria-hidden="true" />
      <div className="modal-content">
        <h2 id="modal-title">{title}</h2>
        {children}
        <button ref={closeRef} onClick={onClose} aria-label="Close dialog">
          ×
        </button>
      </div>
    </div>
  );
}
```

What this enforces: `role="dialog"` + `aria-modal`, focus moves in on open, returns on close, Escape closes, overlay click closes, title linked via `aria-labelledby`.

### Accessible Tabs

```tsx
function Tabs({ tabs }: { tabs: Array<{ id: string; label: string; content: ReactNode }> }) {
  const [active, setActive] = useState(tabs[0].id);

  const handleKeyDown = (e: KeyboardEvent, index: number) => {
    let next = index;
    if (e.key === 'ArrowRight') next = (index + 1) % tabs.length;
    if (e.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
    if (next !== index) {
      setActive(tabs[next].id);
      // Focus the newly active tab
      document.getElementById(`tab-${tabs[next].id}`)?.focus();
    }
  };

  return (
    <div>
      <div role="tablist" aria-label="Content tabs">
        {tabs.map((tab, i) => (
          <button
            key={tab.id}
            id={`tab-${tab.id}`}
            role="tab"
            aria-selected={active === tab.id}
            aria-controls={`panel-${tab.id}`}
            tabIndex={active === tab.id ? 0 : -1}
            onClick={() => setActive(tab.id)}
            onKeyDown={(e) => handleKeyDown(e, i)}
          >
            {tab.label}
          </button>
        ))}
      </div>
      {tabs.map((tab) => (
        <div
          key={tab.id}
          id={`panel-${tab.id}`}
          role="tabpanel"
          aria-labelledby={`tab-${tab.id}`}
          hidden={active !== tab.id}
        >
          {tab.content}
        </div>
      ))}
    </div>
  );
}
```

What this enforces: `role="tablist/tab/tabpanel"`, arrow key navigation, `aria-selected`, `tabIndex` roving, `aria-controls` linking.

### Form Error Announcement

```tsx
<label htmlFor="email">Email</label>
<input
  id="email"
  type="email"
  aria-invalid={!!errors.email}
  aria-describedby={errors.email ? 'email-error' : 'email-hint'}
/>
<p id="email-hint">We'll never share your email.</p>
{errors.email && (
  <p id="email-error" role="alert">
    {errors.email.message}
  </p>
)}
```

`role="alert"` triggers a screen reader announcement when the error appears. `aria-describedby` links the input to its hint or error message.

## Focus Management in SPAs

```tsx
// Route change — announce new page and move focus
function RouteAnnouncer() {
  const location = useLocation();
  const ref = useRef<HTMLHeadingElement>(null);

  useEffect(() => {
    // Focus the main heading after route change
    ref.current?.focus();
    // Update document title
    document.title = getPageTitle(location.pathname);
  }, [location]);

  return <h1 ref={ref} tabIndex={-1}>{/* page title */}</h1>;
}
```

Without this, a route change in an SPA is silent to screen readers — the page "changes" but nothing announces it.

## Live Regions

```html
<!-- Status updates — polite, waits for user to finish -->
<div aria-live="polite" aria-atomic="true">
  {statusMessage}
</div>

<!-- Urgent alerts — assertive, interrupts immediately -->
<div aria-live="assertive" role="alert">
  {errorMessage}
</div>
```

| Level | Use for |
|---|---|
| `polite` | Success messages, status updates, search result counts |
| `assertive` | Error messages, time-sensitive alerts |
| `off` | Regions that update frequently (live scores — use sparingly) |

## Skip Link

```tsx
<a href="#main-content" className="skip-link">
  Skip to main content
</a>
{/* ... nav ... */}
<main id="main-content" tabIndex={-1}>
  {/* content */}
</main>
```

```css
.skip-link {
  position: absolute;
  top: -100%;
  left: 0;
  background: #000;
  color: #fff;
  padding: 8px 16px;
  z-index: 1000;
}
.skip-link:focus {
  top: 0;
}
```

## Color Contrast

| Text size | Minimum ratio (AA) | Enhanced ratio (AAA) |
|---|---|---|
| Normal text (< 18px / 14px bold) | 4.5:1 | 7:1 |
| Large text (≥ 18px / 14px bold) | 3:1 | 4.5:1 |
| UI components and graphics | 3:1 | N/A |

Test with browser DevTools (Accessibility tab shows contrast ratio) or [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/).

## Testing

### Automated (catches ~30% of issues)

```ts
// jest-axe — run axe-core in component tests
import { axe, toHaveNoViolations } from 'jest-axe';
expect.extend(toHaveNoViolations);

test('form has no a11y violations', async () => {
  const { container } = render(<SignupForm />);
  expect(await axe(container)).toHaveNoViolations();
});
```

```yaml
# CI — Lighthouse accessibility audit
- name: Lighthouse A11y
  run: npx lighthouse https://staging.example.com --only-categories=accessibility --output=json
```

### Manual (catches the other 70%)

- [ ] Tab through every interactive element — is the order logical?
- [ ] Can you complete every flow with keyboard only?
- [ ] Are focus indicators visible on every focusable element?
- [ ] Test with a screen reader (VoiceOver, NVDA, or JAWS)
- [ ] Zoom to 200% — does content reflow without horizontal scroll?
- [ ] Disable CSS — does the content still make sense?

## Common Failure Modes

| Pattern | Why it fails / consequence |
|---|---|
| `<div onclick>` instead of `<button>` | No keyboard access, no focus, no screen reader announcement |
| `outline: none` without replacement | Focus indicator invisible — keyboard users are lost |
| Modal opens but focus stays behind it | Screen reader reads behind the modal; keyboard can't reach close button |
| Route change in SPA with no announcement | Screen reader user doesn't know the page changed |
| `aria-label` on a `<div>` that isn't interactive | Ignored by most screen readers; label without a role |
| Color alone conveys information (red = error) | Color-blind users can't distinguish — add icon or text |
| Images without alt text | Screen reader announces filename: "IMG_20240115_103024.jpg" |
| `placeholder` used instead of `<label>` | Disappears on focus; not announced reliably by screen readers |
| Form errors without `role="alert"` | Screen reader doesn't announce the error when it appears |
| Autoplaying video/audio with no controls | Violates WCAG; users can't stop it |

## Accessibility Review Checklist

- [ ] Semantic HTML used (no `<div>` buttons or links)
- [ ] All images have descriptive `alt` (or `alt=""` for decorative)
- [ ] Focus indicators visible on all interactive elements
- [ ] Keyboard navigation works for all interactions
- [ ] Modals trap focus, return focus on close, close on Escape
- [ ] Forms have `<label>`, `aria-invalid`, `aria-describedby` for errors
- [ ] Error messages use `role="alert"` for screen reader announcement
- [ ] Color contrast meets AA (4.5:1 normal, 3:1 large)
- [ ] SPA route changes announce new page to screen readers
- [ ] Skip link present, links to `<main>`
- [ ] `axe-core` or equivalent runs in CI with zero violations
- [ ] Manual screen reader test completed for critical flows

## Integration

- `domains/webdev/skill-frontend` — component architecture that these patterns apply to
- `domains/webdev/skill-validation` — validation errors displayed with ARIA patterns from here
- `domains/webdev/skill-i18n` — ARIA labels and screen reader text need translation via `t()`
- `domains/webdev/skill-error-handling` — React error boundaries should render accessible fallback UI
- `domains/webdev/skill-performance` — lazy loading must not break focus or tab order

## Resources

- [WAI-ARIA Authoring Practices Guide (APG)](https://www.w3.org/WAI/ARIA/apg/) — canonical component patterns
- [WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/)
- [axe-core](https://github.com/dequelabs/axe-core) — automated accessibility testing engine
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Inclusive Components (Heydon Pickering)](https://inclusive-components.design/) — practical component patterns
- [Testing Library](https://testing-library.com/) — queries by role encourage accessible markup
