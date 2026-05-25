---
name: skill-database
description: Database design discipline — type selection (SQL vs NoSQL vs key-value vs graph), schema design, normalization, indexing strategy, query optimization, migrations, transactions, and data integrity. Use when designing a schema, writing or optimizing queries, planning a migration, choosing a database type, or debugging slow queries. For ORM setup in backend code see skill-backend; for API-level pagination see skill-api-rest; for connection pooling metrics see skill-observability.
---

# Database — Design & Query Discipline

The hardest database bugs come from the wrong type for the workload, missing indexes on query paths, or migrations that lock tables under traffic. Choose the right database, normalize thoughtfully, index for actual query patterns, and never deploy a migration without a rollback plan.

## When to Activate

Use when:
- Choosing between SQL, document, key-value, or graph databases
- Designing a schema (tables, relationships, constraints)
- Writing or optimizing SQL / NoSQL queries
- Planning a database migration
- Debugging slow queries or lock contention
- Setting up indexing strategy

**Trigger phrases:** "database design", "schema design", "slow query", "N+1", "index", "migration", "normalize", "denormalize", "PostgreSQL", "MongoDB", "Redis", "transaction", "foreign key"

## When NOT to Use

| Situation | Use instead |
|---|---|
| ORM setup, repository pattern, connection in code | `skill-backend` |
| API-level pagination (cursor, offset) | `skill-api-rest` |
| Connection pool metrics, query latency monitoring | `skill-observability` |
| Database backup infra, replication | `skill-devops` |

## Iron Laws

1. **Choose the database for the workload, not the resume.** A key-value store doesn't replace a relational DB for transactional data; a graph DB is overkill for a user table.
2. **Index for query patterns, not for tables.** Every index you add speeds one read and slows every write. Profile first, index second.
3. **Migrations are code — version-controlled, reviewed, reversible.** No console-click schema changes in production.
4. **Transactions protect invariants.** If two operations must succeed or fail together, they belong in a transaction. "We'll fix it later" means data corruption now.

## Database Type Selection

| Workload | Choose | Why |
|---|---|---|
| Structured data, relationships, ACID | PostgreSQL, MySQL | Joins, constraints, transactions |
| Flexible schema, nested documents | MongoDB, Firestore | Rapid iteration, hierarchical data |
| High-speed caching, sessions | Redis, Memcached | In-memory, sub-ms latency |
| Highly connected data (social, recommendations) | Neo4j, ArangoDB | Graph traversals |
| Time-series (metrics, IoT) | TimescaleDB, InfluxDB | Optimized for time-range queries |
| Full-text search | Elasticsearch, Meilisearch | Inverted index, relevance scoring |

Default: **PostgreSQL.** It handles 90% of workloads, has JSON support for flexible fields, and scales further than most teams need.

## Schema Design

### Relational — normalize, then denormalize where measured

```sql
-- Normalized: separate tables, foreign keys, no duplication
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now(),
    is_active BOOLEAN DEFAULT true
);

CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    total DECIMAL(10, 2) NOT NULL CHECK (total >= 0),
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Many-to-many with junction table
CREATE TABLE order_items (
    order_id UUID REFERENCES orders(id) ON DELETE CASCADE,
    product_id UUID REFERENCES products(id),
    quantity INT NOT NULL CHECK (quantity > 0),
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    PRIMARY KEY (order_id, product_id)
);
```

### Document — embed for one-to-few, reference for one-to-many

```javascript
// Embedded — address always accessed with user, max ~3 addresses
{
  _id: ObjectId("..."),
  email: "jane@example.com",
  addresses: [
    { street: "123 Main St", city: "New York", zip: "10001" }
  ]
}

// Referenced — orders accessed independently, can be thousands
// Users collection:  { _id, email }
// Orders collection: { _id, userId: ObjectId("..."), total, items: [...] }
```

## Indexing Strategy

```sql
-- Index columns used in WHERE, JOIN, ORDER BY
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status_created ON orders(status, created_at DESC);

-- Partial index — only active users (smaller, faster)
CREATE INDEX idx_active_users_email ON users(email) WHERE is_active = true;

-- Covering index — all columns needed without table lookup
CREATE INDEX idx_orders_covering ON orders(user_id, created_at DESC)
  INCLUDE (total, status);
```

**Profile before indexing:**

```sql
EXPLAIN ANALYZE
SELECT id, total, status FROM orders
WHERE user_id = $1 ORDER BY created_at DESC LIMIT 20;
```

Look for: `Seq Scan` on large tables (missing index), `Sort` without index support, high `actual rows` vs `rows removed by filter`.

## Query Optimization

```sql
-- BAD: SELECT * fetches all columns
SELECT * FROM users WHERE email = 'jane@example.com';

-- GOOD: only needed columns
SELECT id, name, email FROM users WHERE email = 'jane@example.com';

-- BAD: N+1 in application code
-- SELECT * FROM users;
-- then for each: SELECT * FROM orders WHERE user_id = ?;

-- GOOD: single query with JOIN
SELECT u.id, u.name, COUNT(o.id) as order_count
FROM users u LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;

-- BAD: LIKE '%widget%' can't use index
SELECT * FROM products WHERE name LIKE '%widget%';

-- GOOD: full-text search
SELECT * FROM products WHERE to_tsvector('english', name) @@ to_tsquery('widget');
```

## Migrations

```python
# Alembic (Python/SQLAlchemy) — always write up AND down
def upgrade():
    op.add_column('users', sa.Column('phone', sa.String(20), nullable=True))
    op.create_index('idx_users_phone', 'users', ['phone'])

def downgrade():
    op.drop_index('idx_users_phone', table_name='users')
    op.drop_column('users', 'phone')
```

```javascript
// Knex.js (Node.js)
exports.up = (knex) => knex.schema.table('users', (t) => {
  t.string('phone', 20);
});
exports.down = (knex) => knex.schema.table('users', (t) => {
  t.dropColumn('phone');
});
```

Migration discipline (see also `skill-deployment` for deploy sequence):
- **Additive first** — add columns/tables before code depends on them
- **Never rename in place** — add new, dual-write, migrate data, drop old
- **Test on production-size data** — a migration that takes 10ms on test data may lock a table for 10 minutes on prod
- **Always reversible** — every `up` has a `down`

## Transactions

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
-- If either fails, ROLLBACK; else:
COMMIT;
```

```python
# SQLAlchemy — context manager handles rollback on exception
with Session() as session, session.begin():
    session.execute(update(accounts).where(accounts.c.id == 1).values(balance=balance - 100))
    session.execute(update(accounts).where(accounts.c.id == 2).values(balance=balance + 100))
    # auto-commits if no exception; auto-rollbacks if exception
```

## SQL Injection Prevention

```python
# BAD — string interpolation
query = f"SELECT * FROM users WHERE email = '{user_input}'"

# GOOD — parameterized query
query = "SELECT * FROM users WHERE email = %s"
cursor.execute(query, (user_input,))

# GOOD — ORM (always parameterizes)
user = session.query(User).filter(User.email == user_input).first()
```

## Common Failure Modes

| Pattern | Why it fails / consequence |
|---|---|
| `SELECT *` everywhere | Fetches unused columns; prevents covering indexes |
| N+1 queries | 100 list items = 101 queries; seconds of latency |
| Index on every column | Write performance tanks; storage bloats |
| No index on foreign keys | JOINs scan full tables |
| Migration locks table under traffic | Downtime; blocked writes during ALTER TABLE |
| No foreign key constraints | Orphaned records; referential integrity violated |
| Storing money as FLOAT | Rounding errors; $10.00 becomes $9.999999 |
| Connection pool exhaustion | "Too many connections"; app hangs |
| No transaction around multi-step writes | Partial writes; data corruption |
| `OFFSET 100000` pagination | Reads and discards 100K rows; use cursor/keyset |

## Database Review Checklist

- [ ] Database type matches workload (SQL for relational, document for flexible)
- [ ] Schema has appropriate constraints (NOT NULL, UNIQUE, CHECK, FK)
- [ ] Indexes exist for all WHERE, JOIN, and ORDER BY patterns
- [ ] No `SELECT *` in production queries
- [ ] N+1 queries eliminated (JOINs, eager loading, DataLoader)
- [ ] Migrations are version-controlled with up AND down
- [ ] Migrations tested on production-size data before deploy
- [ ] Money stored as DECIMAL, not FLOAT
- [ ] Multi-step writes wrapped in transactions
- [ ] Parameterized queries used everywhere (no string interpolation)
- [ ] Connection pooling configured with appropriate limits
- [ ] Pagination uses cursor/keyset, not OFFSET on large tables

## Integration

- `domains/webdev/skill-backend` — repository pattern, connection setup
- `domains/webdev/skill-api-rest` — cursor pagination, filtering
- `domains/webdev/skill-api-graphql` — DataLoader batching for N+1
- `domains/webdev/skill-deployment` — migration deploy sequence (additive → dual-write → cleanup)
- `domains/webdev/skill-observability` — query latency metrics, connection pool monitoring
- `domains/webdev/skill-performance` — N+1 detection, index optimization
- `domains/webdev/skill-auth` — user/session schema design

## Resources

- [PostgreSQL docs](https://www.postgresql.org/docs/)
- [Use The Index, Luke](https://use-the-index-luke.com/) — SQL indexing best practices
- [MongoDB Schema Design](https://www.mongodb.com/docs/manual/data-modeling/)
- [Alembic](https://alembic.sqlalchemy.org/) — Python migration tool
- [Knex.js](https://knexjs.org/) — Node.js migration tool
