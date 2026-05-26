# Design Graveyard (TOMBSTONE.md)

This file registry tracks aborted tasks, design dead-ends, library incompatibilities, and failed experiments. Its purpose is to prevent future agent runs or development sessions from repeating identical failing execution paths.

## Checklist before adding a Tombstone
- [ ] Has the task been explicitly aborted or the path abandoned?
- [ ] Is there a clear, verifiable reason why it failed (e.g. error message, library version clash)?
- [ ] Is there an alternative path we took instead?

---

## Tombstone Registry

| Timestamp | Task / File Path | Attempted Approach | Why it Failed (Post-Mortem) | Alternative Path taken |
|---|---|---|---|---|
| YYYY-MM-DD | e.g. `auth-jwt-refresh` | e.g. Using library `jsonwebtoken-native` for refresh tokens | e.g. Library lacks native Windows support, throws compilation error during install | e.g. Switched to `jose` library |

---

## Retrospective Learnings & Incompatibilities

### [System/Environment Incompatible Library]
- **Tried:** `libname`
- **Result:** detailed compiler or API error.
- **Remediation:** list alternative library or version pin to use.
