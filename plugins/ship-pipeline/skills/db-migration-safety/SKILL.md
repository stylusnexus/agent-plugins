---
name: db-migration-safety
description: Write or review Prisma and Supabase database migrations safely using the expand-contract pattern, idempotent SQL, and batched backfills. Use when adding/changing columns or tables, writing a migration PR, or reviewing one before merge — especially against Neon Postgres or Supabase in production.
---

# DB Migration Safety

## Overview

The two failure modes this guards against: a migration that locks a large table for the duration of a deploy (site goes down), and a migration that succeeds but corrupts or loses data because it wasn't idempotent or wasn't backed up. Neither is recoverable by "just re-running the migration" — the first needs the expand-contract pattern, the second needs a MANDATORY backup confirmation before anything touches production.

## The expand-contract pattern

Never do add-column + backfill + make-required in one migration against a live table with real traffic. Split into phases, each independently deployable:

1. **Expand** — add the new column/table as *nullable* or with a default, additive only. Old code keeps working unmodified.
2. **Backfill** — populate the new column for existing rows, in batches (see below), running alongside live traffic.
3. **Migrate reads/writes** — deploy application code that writes to (and eventually reads from) the new shape. Both old and new columns may coexist briefly.
4. **Contract** — once all app instances are on the new code path and backfill is confirmed complete, drop the old column / add the `NOT NULL` constraint / drop the old table.

Each phase is its own migration and its own deploy. Collapsing steps 1 and 4 into one migration is the single most common cause of an avoidable outage.

## Workflow

1. **Classify the migration** before writing it:
   - Additive (new nullable column, new table, new index `CONCURRENTLY`) → generally safe, low risk.
   - Constraint-adding (`NOT NULL`, `UNIQUE`, FK) → needs expand-contract, do last, after backfill confirmed.
   - Destructive (`DROP COLUMN`, `DROP TABLE`, type change) → needs expand-contract *and* a deprecation window (keep the old column at least one deploy cycle after the last read of it is removed from code).

2. **Avoid long table locks:**
   - Start each DDL migration on an existing table with `SET lock_timeout = '5s';` (tune to the app). Without it, an `ALTER TABLE` queued behind a long-running transaction blocks every query that arrives after it. If it times out, retry at a quieter time; do not raise the timeout to force it through.
   - Prisma: `ALTER TABLE ... ADD COLUMN` with a default on Postgres 11+ is fast (no full rewrite) as long as the default isn't a volatile expression — safe by default in most Prisma migrations.
   - Indexes: always `CREATE INDEX CONCURRENTLY` for existing tables with real data — Prisma's default migration won't do this automatically, hand-edit the generated SQL:
     ```sql
     -- CreateIndex
     CREATE INDEX CONCURRENTLY IF NOT EXISTS "idx_subscription_customer_id" ON "Subscription"("customerId");
     ```
     Note: `CONCURRENTLY` cannot run inside a transaction block, and Prisma Migrate never generates it — you hand-edit it in:
     - **Prisma ORM 7.4.0 and later** (`migration.sql` files applied by `prisma migrate deploy`): Prisma sends `migration.sql` to Postgres one statement at a time instead of as one script, so `CREATE INDEX CONCURRENTLY` works inside the migration file ([prisma-engines#5767](https://github.com/prisma/prisma-engines/pull/5767), shipped in [Prisma 7.4.0](https://github.com/prisma/prisma/releases/tag/7.4.0)). The catch: the file is no longer all-or-nothing. A failure partway through leaves the earlier statements applied, so write every statement to be safe to re-run (`IF NOT EXISTS`, `IF EXISTS`, guarded `DO` blocks) before you retry.
     - **Prisma ORM before 7.4.0**: the file runs as one script, which Postgres wraps in a transaction, so `CONCURRENTLY` fails. Run the statement by hand (`psql`), then record the migration with `prisma migrate resolve --applied <migration_name>`.
     - **Prisma ORM 8** (`migrate deploy` becomes `db migrate`; in CI and production it runs as `npx prisma db migrate --to <ref>` — [Prisma docs, How migrations work](https://www.prisma.io/docs/orm/migrations/how-migrations-work)): Prisma's docs say one `db migrate` run on Postgres is one transaction, so a raw-SQL step cannot run `CREATE INDEX CONCURRENTLY`, and `createIndex` is a plain `CREATE INDEX` that blocks writes while it builds ([Prisma docs, Editing a migration](https://www.prisma.io/docs/orm/migrations/editing-a-migration)). For a large table, build the index outside Prisma with `psql`, then follow the repo's own documented process to keep Prisma's record in sync. Prisma 8 was a release candidate in Prisma's [2026-08-02 changelog](https://www.prisma.io/changelog/2026-08-02) and its behavior may still change, so check the repo's installed Prisma version and the current docs before relying on any of this.
     - Other migration tools: check whether they wrap each file in a transaction before relying on `CONCURRENTLY`.
   - A failed `CONCURRENTLY` build leaves an `INVALID` index behind, and a re-run with `IF NOT EXISTS` silently skips it. Find it with `\d <table>` in `psql` (the index is listed as `INVALID`), `DROP INDEX CONCURRENTLY` it, and rebuild.
   - Constraints on populated tables, without a long exclusive scan:
     - `NOT NULL`: `ADD CONSTRAINT c CHECK (col IS NOT NULL) NOT VALID;` → `VALIDATE CONSTRAINT c;` → `ALTER COLUMN col SET NOT NULL;` (Postgres 12+ uses the validated check and skips the full-table scan) → drop `c`.
     - Foreign key: `ADD CONSTRAINT ... FOREIGN KEY ... NOT VALID`, then `VALIDATE CONSTRAINT` in a separate step.
     - Unique: `CREATE UNIQUE INDEX CONCURRENTLY`, then `ADD CONSTRAINT ... UNIQUE USING INDEX`.

3. **Batch backfills** — never a single `UPDATE` touching the whole table:
   ```sql
   -- Backfill in batches of 1000, sleeping isn't needed on Neon/Supabase managed Postgres
   -- but keep batch size small enough that each statement is sub-second.
   UPDATE "User" SET "normalizedEmail" = LOWER("email")
   WHERE id IN (
     SELECT id FROM "User" WHERE "normalizedEmail" IS NULL LIMIT 1000
   );
   -- repeat until 0 rows affected
   ```
   For large tables, drive this from a script (Node/Prisma or a `uv`-run Python script) with a loop and a small delay between batches, logging progress so it's resumable if interrupted.

4. **Idempotent SQL always** — every migration must be safely re-runnable:
   ```sql
   CREATE TABLE IF NOT EXISTS "WebhookEvent" (...);
   ALTER TABLE "Subscription" ADD COLUMN IF NOT EXISTS "trialEndsAt" TIMESTAMP;
   DROP TABLE IF EXISTS "LegacyBilling";
   CREATE INDEX CONCURRENTLY IF NOT EXISTS ...;
   ```
   Supabase migrations especially — the CLI can partially apply and re-run, so `IF NOT EXISTS` / `IF EXISTS` guards are not optional.

5. **MANDATORY pre-flight backup confirmation** before any migration touches production data (this is a hard gate, not a suggestion):
   - Neon: take a snapshot or a branch at the current head as the safety net — `neon snapshots create --branch main --name pre-migration-<date>` or `neon branches create --parent main --name pre-migration-<date>`.
   - Supabase: confirm the latest daily backup is under 24h old (`supabase backups list --project-ref <ref>`, or Dashboard → Database → Backups). There is no way to trigger a manual backup; if the daily one is stale, take a dump (`supabase db dump`, plus `--data-only` for the rows, or `pg_dump`).
   - Neither available: run `pg_dump` manually and confirm the file is non-empty before proceeding.
   - See [[backup-verify]] for the full drill, including an actual restore test — don't just check a backup *exists*, know it *restores*.

6. **Run in staging/branch first** — Neon and Supabase both support branching; apply the migration to a branch, run the app's test suite and a manual smoke check against it, before applying to production.

## Migration PR review checklist

- [ ] Backup confirmed within the last 24h (link to the snapshot/backup evidence)
- [ ] Migration is idempotent (`IF NOT EXISTS`/`IF EXISTS` on every DDL statement)
- [ ] No `NOT NULL`/`UNIQUE`/FK constraint added in the same migration as the column that needs backfilling
- [ ] `lock_timeout` set before DDL on existing tables
- [ ] Any new index on an existing table uses `CONCURRENTLY`, run outside a transaction
- [ ] `NOT NULL` / FK / `UNIQUE` on a populated table added via `NOT VALID` + `VALIDATE` (or a unique index built `CONCURRENTLY`)
- [ ] Backfill (if any) is batched, not a single table-wide statement
- [ ] Destructive statements (`DROP COLUMN`/`DROP TABLE`) are in a separate, later migration than the code that stops using that column
- [ ] Tested against a Neon/Supabase branch, not applied straight to prod
- [ ] Rollback plan stated in the PR description (down migration, or "expand-only, no rollback needed")

**Pass:** every box ticked. **Fail:** any box left open — fix it, or record in the PR why it does not apply.

## Common mistakes

- Adding a column and its `NOT NULL` constraint in one migration on a table that already has rows.
- Shipping the plain `CREATE INDEX` the ORM generated against a large table.
- Re-running after a failed `CONCURRENTLY` build and trusting `IF NOT EXISTS` to repair the `INVALID` index.
- Treating "Supabase takes daily backups" as a backup taken before this migration.
- Dropping a column in the same deploy that removes its last read; old instances still serving during the rollout will error.

Sources: PostgreSQL docs for [`CREATE INDEX`](https://www.postgresql.org/docs/current/sql-createindex.html#SQL-CREATEINDEX-CONCURRENTLY), [`ALTER TABLE`](https://www.postgresql.org/docs/current/sql-altertable.html) and [`lock_timeout`](https://www.postgresql.org/docs/current/runtime-config-client.html#GUC-LOCK-TIMEOUT); Prisma docs on [editing a migration](https://www.prisma.io/docs/orm/migrations/editing-a-migration) and [coming from Prisma ORM 7](https://www.prisma.io/docs/orm/coming-from-prisma-orm-7); Supabase docs on [database backups](https://supabase.com/docs/guides/platform/backups).

## Output / Evidence

Show the user: the classification (additive/constraint/destructive), the backup confirmation (snapshot ID + timestamp), the branch test result, and — for backfills — row counts before/after and how long the batched run took.

## Stop Conditions

- No backup confirmed within 24h — stop, do not proceed, surface this before any mutation ([[backup-verify]]).
- A single migration combines add-constraint with the column's initial creation on a table with existing rows — stop and split it.
- Migration touches auth/billing tables (`User`, `Customer`, `Subscription`) — escalate to a second reviewer regardless of how small the change looks.
