---
name: skill-auth
description: Authentication and authorization implementation patterns for web apps — sessions, JWTs, OAuth/OIDC, MFA, password handling, and session lifecycle. Use when adding sign-in/sign-up, building an auth flow, integrating an identity provider, or reviewing an auth PR. For broader threat-modeling, OWASP defenses, and secrets discipline across the SDLC see shared/skill-security.
---

# Authentication & Authorization — Implementation

Authentication answers "who are you"; authorization answers "what can you do." Both must be wrong-by-default: every endpoint denies until proven safe, every credential is hashed, every session is revocable.

## When to Activate

Use when:
- Adding a sign-in, sign-up, or password reset flow
- Choosing between sessions and JWTs for a new app
- Integrating Google / GitHub / Apple / corporate SSO via OAuth or OIDC
- Adding MFA (TOTP, WebAuthn / passkeys, SMS as fallback only)
- Implementing role- or attribute-based authorization on routes / API
- Auditing an existing auth flow for token handling, session revocation, password storage
- A teammate asks "JWT or session cookie?"

**Trigger phrases:** "login", "sign in", "sign up", "password reset", "MFA", "2FA", "OAuth", "OIDC", "passkey", "WebAuthn", "JWT vs session", "RBAC", "role check", "auth middleware", "logout invalidation"

## When NOT to Use

| Situation | Use instead |
|---|---|
| Threat modeling, OWASP top 10 review, secrets in CI | `shared/skill-security` |
| Validating the *shape* of auth payloads | `skill-validation` |
| Storing passwords or tokens in a DB schema | `skill-database` (constraints) + this skill (hashing) |
| Securing the deploy pipeline / IAM | `skill-devops` + `shared/skill-security` |
| Vercel-managed auth (Clerk, Auth0, Descope marketplace) | `vercel:auth` |

## Iron Laws

1. **Passwords are hashed with a memory-hard algorithm** — Argon2id (preferred) or bcrypt cost ≥12. Never SHA-256, MD5, or "encrypted."
2. **Session tokens are revocable.** A logged-out session must stop working immediately, on every server, including replicas.
3. **MFA defaults to phishing-resistant.** WebAuthn/passkeys > TOTP > SMS. SMS is a fallback, never the primary factor for high-value accounts.
4. **Authorize on the server, every request.** Hiding a button in the UI is not authorization.
5. **Never roll your own crypto, OAuth flow, or OIDC validation.** Use a library; understand which library you chose and why.

## Sessions vs JWTs — pick by deployment shape

| Question | Use sessions (server-side, cookie-id) | Use JWTs |
|---|---|---|
| Need instant logout / password-change kill | ✅ revoke by deleting record | ❌ tokens valid until expiry unless you maintain a denylist |
| Single backend / shared session store (Redis) | ✅ simple, fast | Overkill |
| Many independent services, one user | Possible with shared store | ✅ stateless, validated by signature |
| Mobile / SPA / 3rd-party API | Cookies cross-origin is painful | ✅ access + refresh token pattern |
| Concerned about token theft | ✅ short server-side lifetime | Refresh tokens with rotation needed |

Default for a normal web app: **server-side sessions with HttpOnly + Secure + SameSite=Lax cookies.** Switch to JWTs only when you have multiple backends or cross-domain needs that sessions can't serve cleanly.

If you choose JWTs anyway: keep access tokens short (≤15min), use refresh tokens with rotation, and maintain a denylist for compromised tokens. Otherwise "logout" is a lie.

## Password Handling

```ts
// Argon2id — Node.js example with `argon2`
import argon2 from 'argon2';

// At sign-up / password change
export async function hashPassword(plain: string): Promise<string> {
  return argon2.hash(plain, {
    type: argon2.argon2id,
    memoryCost: 64 * 1024,  // 64 MB — RFC 9106 minimum, raise for high-value
    timeCost: 3,
    parallelism: 1,
  });
}

// At sign-in
export async function verifyPassword(hash: string, plain: string): Promise<boolean> {
  try {
    return await argon2.verify(hash, plain);
  } catch {
    return false;
  }
}
```

What this enforces: parameters are pinned (memory, time, parallelism); verification can re-hash with new params if you ever increase them; failures return false instead of leaking error type.

```python
# Argon2id — Python equivalent with `argon2-cffi`
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher(memory_cost=64 * 1024, time_cost=3, parallelism=1)

def hash_password(plain: str) -> str:
    return ph.hash(plain)

def verify_password(stored_hash: str, plain: str) -> bool:
    try:
        ph.verify(stored_hash, plain)
        return True
    except VerifyMismatchError:
        return False
```

Common mistakes:
- Using bcrypt with the default cost (10) on modern hardware — raise to 12+
- Truncating passwords to 72 bytes silently (bcrypt limit) — pre-hash with SHA-256 if you must support long passphrases
- Storing the hash in the same column as the salt — Argon2/bcrypt store the salt inside the hash string; treat it as opaque

## Session Cookies

```ts
// Express + express-session + Redis store
import session from 'express-session';
import RedisStore from 'connect-redis';
import { createClient } from 'redis';

const redis = createClient({ url: process.env.REDIS_URL });
await redis.connect();

app.use(session({
  store: new RedisStore({ client: redis }),
  name: '__Host-sid',                 // __Host- prefix forces Secure + path=/ + no Domain
  secret: process.env.SESSION_SECRET!, // 32+ random bytes
  resave: false,
  saveUninitialized: false,
  cookie: {
    httpOnly: true,                   // not readable by JS — defends against XSS
    secure: true,                     // HTTPS only
    sameSite: 'lax',                  // CSRF mitigation; 'strict' for high-value flows
    maxAge: 1000 * 60 * 60 * 24 * 7,  // 7 days
  },
}));
```

Logout must delete the server-side record, not just clear the cookie:

```ts
app.post('/logout', (req, res) => {
  req.session.destroy((err) => {
    if (err) return res.status(500).end();
    res.clearCookie('__Host-sid');
    res.status(204).end();
  });
});
```

For password change, also invalidate *all other* sessions for that user. A common implementation: store a `tokenVersion` column on the user; embed it in each session or JWT; bump it on password change; reject any session whose version doesn't match.

## OAuth 2.0 / OpenID Connect

Don't implement either from scratch. Use a vetted library: `passport` (Node), `authlib` (Python), `next-auth` / Auth.js (Next.js), or a managed provider (Clerk, Auth0, Cognito).

Discipline regardless of library:
- **Authorization Code flow with PKCE** for public clients (SPAs, mobile, desktop)
- **Validate ID token signature** against the provider's JWKS — never decode-and-trust
- **Verify `iss`, `aud`, `exp`, `nbf`, and `nonce`** on every ID token
- **State parameter** must match what you sent — defends against CSRF on the redirect
- **Store refresh tokens server-side**, never in localStorage or client JS

```ts
// Auth.js (Next.js) — Google sign-in with safe defaults
import NextAuth from 'next-auth';
import Google from 'next-auth/providers/google';

export const { handlers, auth } = NextAuth({
  providers: [
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
  ],
  session: { strategy: 'database' },   // sessions table, revocable
  callbacks: {
    async signIn({ account, profile }) {
      return profile?.email_verified === true;  // refuse unverified emails
    },
  },
});
```

What this enforces: signature/issuer validation handled by Auth.js; `email_verified` checked before account creation; sessions are server-side and revocable.

## Multi-Factor Authentication

| Factor | Strength | When to use |
|---|---|---|
| WebAuthn / passkeys | Phishing-resistant, device-bound | First choice for any new app |
| TOTP (Authenticator app) | Strong, no SIM-swap risk | Default secondary factor |
| Backup codes | Recovery only | Always pair with TOTP/passkey |
| Email link / code | Weak (email is often the recovery itself) | Acceptable as user-attested second factor for low-risk apps |
| SMS | Weakest, SIM-swappable | Last resort; never sole MFA |

```ts
// TOTP enrollment with `otpauth` and a QR code
import { authenticator } from 'otplib';

export function generateTotpSecret(userEmail: string, issuer: string) {
  const secret = authenticator.generateSecret();
  const otpauth = authenticator.keyuri(userEmail, issuer, secret);
  return { secret, otpauth };  // store secret encrypted at rest
}

export function verifyTotp(secret: string, token: string): boolean {
  return authenticator.verify({ token, secret });
}
```

Discipline: store the TOTP secret encrypted (envelope encryption with a KMS key); allow a window of one step (±30s); rate-limit verification attempts; require an active MFA before allowing MFA changes.

For passkeys, use [SimpleWebAuthn](https://simplewebauthn.dev/) (Node) or `webauthn` (Python) — implementing the dance manually is a mistake.

## Authorization — RBAC and ABAC

Authorization happens on the server, on every request. The UI hides things for usability, not security.

```ts
// RBAC — Express middleware that gates by role
type Role = 'admin' | 'editor' | 'viewer';

const PERMISSIONS: Record<Role, Set<string>> = {
  admin: new Set(['post.read', 'post.write', 'post.delete', 'user.manage']),
  editor: new Set(['post.read', 'post.write']),
  viewer: new Set(['post.read']),
};

export function requirePermission(perm: string) {
  return (req: Request, res: Response, next: NextFunction) => {
    const user = req.session.user;
    if (!user) return res.status(401).json({ error: 'unauthenticated' });
    const allowed = (user.roles as Role[]).some((r) => PERMISSIONS[r]?.has(perm));
    if (!allowed) return res.status(403).json({ error: 'forbidden' });
    next();
  };
}

app.delete('/posts/:id', requirePermission('post.delete'), deletePost);
```

ABAC adds attributes (resource owner, time of day, IP range):

```ts
// ABAC example — only the post's author or an admin can delete
async function canDeletePost(user: User, postId: string) {
  if (user.roles.includes('admin')) return true;
  const post = await db.posts.findById(postId);
  return post?.authorId === user.id;
}

app.delete('/posts/:id', async (req, res) => {
  const ok = await canDeletePost(req.session.user, req.params.id);
  if (!ok) return res.status(403).end();
  await db.posts.delete(req.params.id);
  res.status(204).end();
});
```

For complex policies (multi-tenant, hierarchical resources), use a policy engine — [OPA](https://www.openpolicyagent.org/), [Cerbos](https://www.cerbos.dev/), or [Oso](https://www.osohq.com/). Avoid hand-rolling once your `if`/`else` exceeds three nested checks.

## Account Recovery

Password reset is the most-attacked auth surface. Treat it as if every reset is an attack until proven otherwise.

- **Single-use, time-limited tokens** (15–60 minutes) bound to a user
- **Tokens stored hashed** in the DB — never plaintext
- **Always respond identically** for "email exists" vs "email doesn't exist" — no user enumeration
- **Invalidate all sessions** on successful password change
- **Send notification email** to the registered address on password change ("If this wasn't you, contact support")
- **Rate-limit** reset requests per email and per IP

## Common Failure Modes

| Pattern | Why it fails / consequence |
|---|---|
| `password === db.password` (plain compare) | Logs and DB dumps reveal everything |
| Logout only clears the cookie | Stolen cookie still valid; "log out everywhere" doesn't work |
| JWT-only auth with no denylist | Logout is a UI illusion; compromised tokens valid until expiry |
| Storing access token in `localStorage` | Any XSS = account takeover |
| Verifying JWT with `algorithm: 'none'` accepted | Attacker forges tokens with no signature |
| Trusting email-passed-in-token without provider signature check | Account takeover via forged ID token |
| MFA enrollment doesn't require current factor | Attacker who steals session disables MFA |
| Password reset reveals which emails are registered | User enumeration → targeted phishing |
| Authorization on the client only ("hide the admin button") | API still serves the data; trivially bypassed |
| Same JWT secret across environments | Staging compromise → prod compromise |
| Roles checked in the controller, not on the model | Direct ORM call from another path skips the gate |

## Auth Review Checklist

- [ ] Passwords hashed with Argon2id or bcrypt (cost ≥12), never plain or fast-hashed
- [ ] Session/JWT supports server-side revocation (logout works immediately)
- [ ] Cookies are HttpOnly + Secure + SameSite, with `__Host-` prefix where applicable
- [ ] CSRF protection on state-changing requests when using cookies (token or `SameSite=Strict`)
- [ ] OAuth/OIDC uses Authorization Code + PKCE; ID tokens validated via JWKS
- [ ] MFA available; phishing-resistant option (passkey/TOTP) is the primary path
- [ ] Account recovery tokens are single-use, hashed, and time-limited
- [ ] No user enumeration in sign-up, sign-in, or password reset responses
- [ ] Authorization enforced server-side on every endpoint
- [ ] Rate limits on `/login`, `/signup`, `/reset` keyed by IP and account
- [ ] Audit log records sign-in, sign-out, password change, MFA enrollment, role change
- [ ] Secrets (JWT signing key, OAuth client secret) come from env / vault, never repo

## Integration

- `shared/skill-security` — broader OWASP, threat modeling, secrets management, supply chain
- `domains/webdev/skill-validation` — schema-validate auth payloads (login, signup, MFA enrollment)
- `domains/webdev/skill-api-rest` — protecting endpoints with the middleware shown here
- `domains/webdev/skill-database` — schema for users, sessions, MFA factors, audit log
- `domains/webdev/skill-error-handling` — uniform error responses that don't leak enumeration
- `domains/webdev/skill-observability` — auth events are high-value telemetry
- `vercel:auth` — Clerk / Auth0 / Descope marketplace flows on Vercel
- `superpowers:requesting-code-review` — auth changes deserve mandatory review

## Resources

- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [Argon2 RFC 9106](https://www.rfc-editor.org/rfc/rfc9106.html) — parameter guidance
- [OAuth 2.0 Security Best Current Practice (RFC 9700)](https://www.rfc-editor.org/rfc/rfc9700.html)
- [SimpleWebAuthn](https://simplewebauthn.dev/) — passkey implementation
- [Auth.js / NextAuth](https://authjs.dev/) — drop-in auth for Next.js
