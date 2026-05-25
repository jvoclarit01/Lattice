---
name: skill-api-graphql
description: GraphQL schema design and operational discipline — SDL, resolvers and the N+1 trap, typed errors, subscriptions, federation vs monolith, and security limits (depth, complexity, persisted queries). Use when designing a new GraphQL schema, debugging a slow GraphQL endpoint, debating REST vs GraphQL, or auditing a GraphQL API for security. For REST design see skill-api-rest; for WebSocket/SSE push patterns see skill-api-realtime; for input validation libraries see skill-validation.
---

# GraphQL API Design

A REST API's surface is the URL space; a GraphQL API's surface is the schema. The schema is a *contract* — every type, field, and argument is a public commitment, and the operational pitfalls (N+1, runaway queries, federation drift) all trace back to schema decisions made early.

## When to Activate

Use when:
- Designing a new GraphQL schema (types, queries, mutations, subscriptions)
- A teammate proposes "let's switch to GraphQL" — you need the trade-offs sharp
- Debugging a slow GraphQL endpoint (almost always N+1)
- Adding subscriptions or splitting a monolith into federated subgraphs
- Reviewing a GraphQL PR for resolver discipline, auth, or query-cost controls
- Auditing a public GraphQL endpoint for depth/complexity/PQ defenses

**Trigger phrases:** "GraphQL schema", "resolver", "DataLoader", "N+1", "federation vs monolith", "Apollo Federation", "subgraph", "subscription", "persisted query", "query depth limit", "query complexity"

## When NOT to Use

| Situation | Use instead |
|---|---|
| REST endpoint / status code / pagination decisions | `skill-api-rest` |
| Real-time push that doesn't fit GraphQL subscriptions | `skill-api-realtime` |
| Input shape validation libraries (Zod/Yup/Pydantic) | `skill-validation` |
| Endpoint authentication / authorization patterns | `skill-auth` |
| DB query optimization underneath a resolver | `skill-database` |
| Error response shape, retries, circuit breakers | `skill-error-handling` |
| Tracing & metrics for GraphQL operations | `skill-observability` |

## Iron Laws

1. **Resolvers never hit the database in a loop.** Every list field crosses through DataLoader (or the equivalent batching primitive). N+1 is a defect, not a perf tweak.
2. **Errors are typed in the schema.** Use union or interface result types for expected failures; reserve top-level `errors` for unexpected ones.
3. **Public endpoints have a query budget.** Depth limit + complexity limit + (in production) persisted queries — pick at least two.
4. **Auth is on the resolver, not the gateway.** Field-level authorization is a feature of GraphQL; using only gateway-level auth surrenders that feature.
5. **Schema changes are versioned by deprecation, not by URL.** `@deprecated(reason: "...")` then remove after one consumer migration cycle.

## REST vs GraphQL — pick the workload, not the trend

| Question | Lean REST | Lean GraphQL |
|---|---|---|
| One stable client shape per resource | ✅ | Overhead |
| Many clients, each wants different fields | Over-fetching painful | ✅ native projection |
| File upload / streaming / binary payloads | ✅ HTTP-native | Awkward (multipart spec) |
| Cacheable at the HTTP layer (CDN, Varnish) | ✅ URL-keyed | Hard (POST + body) |
| Aggregating across 5+ services from a UI | Lots of round-trips | ✅ one query |
| Public API consumed by unknown clients | ✅ predictable cost | ⚠ persisted queries required |
| Team has zero GraphQL experience | ✅ | High learning curve |
| You need subscriptions baked in | Push to SSE/WS sibling | ✅ if already on GraphQL |

GraphQL is best where *the same data backs many UIs with different shapes*. It is worst where the workload is "a CDN-cacheable JSON document under one URL." Don't pick by fashion.

## Schema Design (SDL)

Schema is the contract. Three rules: name fields by domain meaning, mark non-null only when truly always present, and prefer specific types over scalars.

```graphql
# schema.graphql

scalar DateTime
scalar URL

"""A user account."""
type User {
  id: ID!
  email: String!
  displayName: String!
  avatarUrl: URL
  createdAt: DateTime!

  # Connection — paginated, with cursor & metadata.
  posts(first: Int = 20, after: String): PostConnection!
}

type Post {
  id: ID!
  title: String!
  body: String!
  author: User!           # always present — hard FK in DB
  publishedAt: DateTime   # nullable — drafts have no publishedAt
}

# Relay-style cursor pagination
type PostConnection {
  edges: [PostEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}
type PostEdge { node: Post!  cursor: String! }
type PageInfo { hasNextPage: Boolean!  endCursor: String }

input CreatePostInput {
  title: String!
  body: String!
}

# Typed error union — see "Errors" section below.
union CreatePostResult = CreatePostSuccess | ValidationError | NotAuthorized

type CreatePostSuccess { post: Post! }
type ValidationError    { field: String!  message: String! }
type NotAuthorized      { reason: String! }

type Query {
  me: User
  user(id: ID!): User
  post(id: ID!): Post
}

type Mutation {
  createPost(input: CreatePostInput!): CreatePostResult!
}
```

What this enforces: nullability is meaningful (drafts have no `publishedAt`, but every `Post` has an `author`); pagination is cursor-based; errors are part of the type system; mutations return a result union, not just a `Post`.

Common mistakes:
- Marking everything non-null because "it's always there in our DB right now" — schema is forever, your DB shape is not
- Mutations that return only the mutated entity — there's no place for typed errors
- Stuffing every field into `Query.everything: JSON!` — you've reinvented REST badly

## Resolvers and the N+1 Problem

The default resolver shape is naive: for each parent, look up children. With 100 posts in a list, you do 100 author lookups. DataLoader batches a single tick's worth of keys into one query.

```ts
// Apollo Server 4 + DataLoader — Node.js
import DataLoader from 'dataloader';
import { db } from './db';

// Build per-request loaders. Never share across requests (caches user data).
export function buildLoaders() {
  return {
    userById: new DataLoader(async (ids: readonly string[]) => {
      const rows = await db.users.findMany({ where: { id: { in: [...ids] } } });
      const byId = new Map(rows.map((u) => [u.id, u]));
      return ids.map((id) => byId.get(id) ?? null);   // order MUST match ids
    }),
  };
}

// In context factory
export const context = async ({ req }) => ({
  user: await authFromReq(req),
  loaders: buildLoaders(),
});

// Resolver — hits the loader, never the DB directly for parent->child traversal
export const resolvers = {
  Post: {
    author: (post, _args, ctx) => ctx.loaders.userById.load(post.authorId),
  },
};
```

What this enforces: per-request loader, ordered output keyed to input, parent-to-child resolution batches. Two non-obvious rules:
- **Build loaders per request, not per process.** A long-lived loader leaks one user's data into another's request.
- **Order matters.** DataLoader's contract is `keys[i] -> values[i]`. Returning a different order silently corrupts results.

For multi-table or aggregate fetches, use a join-aware ORM (Prisma's `include`, SQLAlchemy `joinedload`, Drizzle's relations). DataLoader + ORM include is the standard combination.

## Typed Errors

Top-level `errors` in a GraphQL response is for *exceptional* failures (resolver threw). Expected failures (validation, not-authorized, not-found) belong in the schema.

```graphql
union UpdateUserResult =
    UpdateUserSuccess
  | ValidationError
  | NotFound
  | NotAuthorized
```

```ts
// Resolver
Mutation: {
  async updateUser(_p, { id, input }, ctx) {
    if (!ctx.user) return { __typename: 'NotAuthorized', reason: 'unauthenticated' };
    const target = await ctx.loaders.userById.load(id);
    if (!target) return { __typename: 'NotFound', resource: 'User', id };
    if (target.id !== ctx.user.id && !ctx.user.isAdmin) {
      return { __typename: 'NotAuthorized', reason: 'forbidden' };
    }
    const parsed = UpdateUserInput.safeParse(input);   // see skill-validation
    if (!parsed.success) {
      return {
        __typename: 'ValidationError',
        issues: parsed.error.issues.map((i) => ({ field: i.path.join('.'), message: i.message })),
      };
    }
    const updated = await db.users.update({ where: { id }, data: parsed.data });
    return { __typename: 'UpdateUserSuccess', user: updated };
  },
}
```

Why this matters: clients that get `data: null, errors: [...]` can't rely on partial data; clients that get `data: { updateUser: { __typename: 'ValidationError', ... } }` can render specific UI per failure. Reserve thrown exceptions for "the resolver itself is broken."

## Subscriptions

WebSocket-based push for query-shaped updates. Don't subscribe to "everything that changed" — subscribe to a specific shape and key.

```ts
// graphql-ws + Redis pub/sub
import { createPubSub } from '@graphql-yoga/subscription';
import { createClient } from 'redis';
import { createRedisEventTarget } from '@graphql-yoga/redis-event-target';

const publishClient = createClient({ url: process.env.REDIS_URL });
const subscribeClient = publishClient.duplicate();
await Promise.all([publishClient.connect(), subscribeClient.connect()]);

export const pubsub = createPubSub({
  eventTarget: createRedisEventTarget({ publishClient, subscribeClient }),
});

// Schema
// type Subscription { postPublished(authorId: ID): Post! }

export const resolvers = {
  Subscription: {
    postPublished: {
      subscribe: (_p, args) =>
        pubsub.subscribe(args.authorId ? `post.published.${args.authorId}` : 'post.published'),
      resolve: (payload) => payload,
    },
  },
  Mutation: {
    async publishPost(_p, { id }, ctx) {
      const post = await ctx.posts.publish(id);
      pubsub.publish('post.published', post);
      pubsub.publish(`post.published.${post.authorId}`, post);
      return post;
    },
  },
};
```

Subscription discipline:
- Authorize on subscribe AND on each emitted event — group membership can change
- Filter server-side (`postPublished(authorId: ...)`), don't ship every event to every client
- Use Redis (or NATS, Kafka) pub/sub when you have more than one server replica — in-memory `EventEmitter` won't fan out across pods
- For non-query-shaped real-time (presence, cursors, OT/CRDT), use raw WebSocket/SSE — see `skill-api-realtime`

## Federation vs Monolithic Schema

Federation (Apollo Federation v2 is the de-facto standard) splits one schema across multiple subgraphs owned by different teams. It's powerful and expensive.

| Question | Stay monolithic | Federate |
|---|---|---|
| One team owns the API | ✅ | Overhead |
| 3+ teams, each with their own service & domain | Becomes a coordination tax | ✅ team autonomy |
| Schema needs cross-team types (`User` extended by both Auth & Profile) | Awkward | ✅ entity references |
| You have zero GraphQL ops experience | ✅ start here | ❌ federation amplifies bad practices |
| You need `@requires`, `@provides`, `@key` semantics | Don't | ✅ that's federation's job |

If you need federation: use Apollo Router (Rust-based, the reference impl), publish subgraphs via schema registry, run composition checks in CI. Don't roll your own gateway.

If you don't need federation: a single Apollo Server / Yoga / Mercurius / GraphQL.js schema serves remarkably large APIs. GitHub's public GraphQL API is monolithic.

## Security: Depth, Complexity, Persisted Queries

A public GraphQL endpoint without limits is a DoS vector. A query like `{ user { posts { author { posts { author { ... } } } } } }` can recursively expand to millions of nodes.

```ts
// Apollo Server with depth + complexity + persisted-query plugins
import { ApolloServer } from '@apollo/server';
import depthLimit from 'graphql-depth-limit';
import { createComplexityLimitRule } from 'graphql-validation-complexity';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [
    depthLimit(8),                                // reject queries nested deeper than 8
    createComplexityLimitRule(1000, {
      scalarCost: 1,
      objectCost: 10,
      listFactor: 10,                             // a list of 10 multiplies its children
    }),
  ],
  // For public APIs: enable Automatic Persisted Queries (APQ) so clients send a hash,
  // not the full query string — server only executes pre-registered queries.
  persistedQueries: { ttl: 900 },
});
```

Recommended posture for public endpoints:
- **Depth limit** (~8–10) — kills accidentally pathological introspection
- **Complexity limit** with weighted scalars / lists — kills "big lists everywhere" queries
- **Persisted queries** — only allow queries the client has pre-registered; reject arbitrary text from the wire
- **Disable introspection in prod** *only if* you also publish the schema separately — otherwise clients can't generate types
- **Rate limit per identity AND per query hash** — see `skill-auth` for the identity, `skill-api-rest` for the rate-limit pattern

## Caching

GraphQL undermines HTTP caching (one URL, POST body). Strategies:
- **Per-field caching** at the resolver (DataLoader cache) — only valid within a request
- **Apollo Server response cache** with `@cacheControl(maxAge: 60)` directives — tricky because one query mixes public and private fields
- **Persisted queries + `GET`** — recover URL-based CDN caching for public queries
- **Client-side normalized cache** (Apollo Client, urql) — usually does more for perceived perf than server cache

Don't slap Redis in front of arbitrary GraphQL responses; the cache key would have to include the full query, variables, and identity — at which point you've reinvented APQ.

## Common Failure Modes

| Pattern | Why it fails / consequence |
|---|---|
| Resolver loops over parent and queries DB per child | Classic N+1; one list of 100 = 101 queries |
| One DataLoader shared across requests | User A's data leaks into User B's response |
| Throwing `new Error('not found')` for expected misses | Client sees `errors: [...]` and can't tell programmer-bug from missing-row |
| Public endpoint with introspection on, no depth limit | DoS via deeply nested introspection query |
| Federation with no schema-check CI | Subgraph adds breaking change → router can't compose → outage |
| Subscription with no authorization on each emitted event | User loses access to a channel mid-subscription, still receives events |
| `String!` everywhere because "it's always set today" | Schema lies; clients break when reality diverges |
| Mutations return the entity directly (no result union) | No place for typed errors; client gets generic `errors[]` for validation |
| Pagination via `posts(offset: Int)` on a busy list | Same problems as REST offset pagination — see `skill-api-rest` |
| Hand-rolled gateway in front of multiple subgraphs | You've started writing Apollo Router, badly |

## GraphQL Review Checklist

- [ ] Every list field uses DataLoader (or the framework's batching equivalent)
- [ ] DataLoaders are built per request and not memoized at module scope
- [ ] Mutations return result unions with typed errors for expected failures
- [ ] Nullability matches reality (don't mark non-null without a constraint)
- [ ] Pagination is cursor-based with `pageInfo`
- [ ] Field-level authorization runs in resolvers, not only at the gateway
- [ ] Public endpoints have depth + complexity limits and rate limiting
- [ ] Persisted queries (or APQ) are enabled in production
- [ ] Subscriptions authorize on subscribe AND on each event
- [ ] Schema deprecations use `@deprecated(reason: "...")` with a removal plan
- [ ] Federation subgraph composition runs in CI before deploy

## Integration

- `domains/webdev/skill-api-rest` — REST is often the better choice; this skill defers when it is
- `domains/webdev/skill-api-realtime` — non-query-shaped push (presence, cursors, OT) belongs there
- `domains/webdev/skill-validation` — input shape validation libraries (Zod/Yup/Pydantic) feeding mutation resolvers
- `domains/webdev/skill-auth` — `ctx.user`, role/attribute checks, JWT/session handling for resolvers
- `domains/webdev/skill-database` — the joined queries DataLoader fans out to
- `domains/webdev/skill-error-handling` — uncaught resolver errors flow through the global handler
- `domains/webdev/skill-observability` — Apollo tracing, OpenTelemetry, per-resolver duration metrics
- `domains/webdev/skill-deployment` — federation composition checks belong in the pipeline
- `superpowers:requesting-code-review` — schema PRs deserve structured review

## Resources

- [Apollo Federation v2 docs](https://www.apollographql.com/docs/federation/) — the federation reference
- [DataLoader](https://github.com/graphql/dataloader) — Facebook's original; same pattern in every language
- [GraphQL Spec](https://spec.graphql.org/) — the actual contract
- [Production-Ready GraphQL (Marc-André Giroux)](https://book.productionreadygraphql.com/) — best operational guide
- [Apollo Router](https://www.apollographql.com/docs/router/) — Rust-based federation gateway
- [graphql-ws](https://github.com/enisdenjo/graphql-ws) — current subscription protocol (replaces deprecated `subscriptions-transport-ws`)
- [GraphQL Security Cheatsheet (OWASP)](https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html)
