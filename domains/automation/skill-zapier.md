---
name: skill-zapier
description: Zapier workflow (Zaps) and CLI Developer Platform discipline. Details Storage by Zapier limitations, Zapier Tables, credential management, custom CLI integration structure, unit testing, and SDK error wrappers. Use when designing Zaps, writing Code steps, or building custom CLI integrations.
---

# Zapier — Workflow (Zaps) & CLI Developer Platform

Zapier provides instant SaaS connectivity, but Zaps easily become brittle due to hardcoded secrets, lack of version control, and storage capacity faults. This skill enforces secure credential isolation and robust CLI integration patterns.

## When to Activate

Use when:
- Building or refactoring Zaps in the Zapier visual editor
- Writing custom JavaScript/Python Code steps inside a Zap
- Designing integrations using the **Zapier CLI Developer Platform** (Node.js SDK)
- Storing temporary state using *Storage by Zapier*
- Configuring custom OAuth or API authentication headers in the Developer Portal

**Trigger phrases:** "Zapier", "Zapier CLI", "Storage by Zapier", "Zapier Tables", "z.request", "z.errors.Error", "Zapier Code step"

## Iron Laws

1. **Never store sensitive data in Storage by Zapier.** It is a public key-value store with a strict **25 KB limit per key**. Use Zapier Tables or secure external vaults (Google Drive, Box) for sensitive file processing.
2. **Never hardcode secrets in Code steps.** Use the `inputData` parameters to pass connection credentials securely, or define a custom integration where the user authenticates via the standard UI.
3. **Use the Zapier CLI for complex apps.** Avoid the UI-based developer editor for integrations requiring custom OAuth, multiple files, or automated tests. Version control your CLI project using Git.
4. **Surfaces clear errors using the SDK.** In CLI integrations, wrap failures in `z.errors.Error` to present readable error messages in the user's dashboard, rather than raw stack traces.

---

## State & File Storage Options

Choose the right storage medium depending on data longevity and security:

| Storage Type | Best for | Limits & Constraints |
|---|---|---|
| **Storage by Zapier** | Lightweight state flags, counters, simple cross-zap state | 25 KB per key; data may be cleared after periods of inactivity. |
| **Zapier Tables** | Persistent structured records, manual UAT data lists | 50,000 records per table maximum; shared within team account. |
| **Secure Vault (Drive/Box)** | Sensitive documents, client files, raw exports | Must trigger a post-processing step to delete files from temp storage immediately after transfer. |

---

## CLI Integration Architecture (Node.js SDK)

When building a custom integration using the **Zapier CLI**:

### 1. Modular Directory Structure
Maintain a standard structure for your Node.js integration:
```
my-integration/
├── index.js          # Main exports (triggers, searches, creates)
├── package.json      # Dependencies and runtimes (requires Node 18+)
├── authentication.js # OAuth2 or API key configuration
├── triggers/         # Directory containing individual trigger modules
├── searches/         # Directory containing search endpoints
└── test/             # Directory containing local Jest/Mocha unit tests
```

### 2. Standard Request Handler
Always use the built-in `z` library methods for making external requests to ensure auto-retry and logging function properly:
```javascript
const perform = async (z, bundle) => {
  const response = await z.request({
    url: 'https://api.example.com/v1/users',
    method: 'GET',
    params: {
      active: true
    }
  });

  if (response.status === 401) {
    throw new z.errors.RefreshAuthError('AccessToken expired. Triggering refresh...');
  }

  if (response.status !== 200) {
    throw new z.errors.Error(
      `Failed to fetch users: ${response.content}`, 
      'APIError', 
      response.status
    );
  }

  return response.data; // Must return an array of objects
};
```

---

## Review Checklist

- [ ] **No Hardcoded Keys:** Are API keys, Client Secrets, and tokens excluded from files committed to Git?
- [ ] **z.request Used:** Are all outbound requests routed through the SDK's `z.request` rather than raw `axios` or `fetch`?
- [ ] **Unit Tests:** Does the CLI app contain unit tests verifying the authentication handshake and perform outputs?
- [ ] **Storage Bounds:** Are *Storage by Zapier* payload keys verified to be under 25 KB?
- [ ] **Idempotent Zaps:** Are Zaps designed to handle retry events safely without creating duplicate SaaS records?
