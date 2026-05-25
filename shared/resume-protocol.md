# The Resume Protocol

At the start of every session:

1. **Check for `.lattice-plan.md`** in current directory
2. **If found**:
   - Read the entire file
   - Identify the active mode
   - Check the status of each domain
   - Review open questions
   - Review Global Constants
   - Resume from the last completed step
3. **If not found**:
   - Start fresh with mode detection

## What to Resume

When resuming, pick up exactly where we left off:

- **Active mode** → Continue in the same mode
- **Domain statuses** → Only work on Pending or In Progress domains
- **Open questions** → Address unresolved questions first
- **Global Constants** → Use existing constants, don't re-ask
- **Stack/approach** → Continue with confirmed approach

## What NOT to Resume

- **Done domains** → Marked as complete, don't revisit unless user requests
- **Answered questions** → Already resolved, don't re-ask
- **Confirmed decisions** → Already made, don't challenge unless new information

## The Principle

The Resume Protocol is about **context preservation**. The user should never have to repeat themselves or re-answer questions already answered. The `.lattice-plan.md` is the project's memory — use it.

## Example Resume

> "Found `.lattice-plan.md`. Resuming project-lattice mode.
>
> **Status:**
> - Active mode: project-lattice
> - Phase: executing
> - Done domains: skill-frontend, skill-backend
> - In Progress: skill-database
> - Pending: skill-auth, skill-devops
>
> **Next step:** Continue with skill-database domain. You're building a PostgreSQL database for the user authentication system. Let me read the current schema and continue from there."
