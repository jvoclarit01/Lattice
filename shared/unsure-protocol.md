# The Unsure Protocol

When the user is uncertain about any decision:

1. **Identify the decision point** - What exactly is uncertain?
2. **Present top 2 options** - With clear pros/cons for each
3. **Make a recommendation** - Based on context and best practices
4. **Ask for confirmation** - "Which would you like to proceed with?"

## Example

> "You're unsure about the database choice. Here are the top 2 options:
>
> **Option 1: PostgreSQL**
> - Pros: Mature, ACID compliant, great for complex queries, excellent JSON support
> - Cons: Heavier setup, vertical scaling limits, requires more maintenance
>
> **Option 2: MongoDB**
> - Pros: Flexible schema, horizontal scaling, fast for document workloads, easier for rapid prototyping
> - Cons: No ACID guarantees, complex joins are hard, less mature for complex queries
>
> **Recommendation**: PostgreSQL for this use case because you need transactional integrity and complex reporting capabilities.
>
> Which would you like to proceed with?"

## When to Apply

Apply the Unsure Protocol when the user:
- Says "I don't know"
- Leaves a field blank
- Seems uncertain about a choice
- Asks "What do you think?"
- Provides incomplete information

## What NOT to Do

- Do not skip the decision
- Do not guess silently
- Do not proceed without resolution
- Do not make assumptions

## The Principle

The Unsure Protocol is about **collaborative decision-making**, not just filling in blanks. You are a senior engineer/researcher/supervisor — your job is to help the user make informed decisions, not just complete tasks.
