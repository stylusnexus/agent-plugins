---
name: backup-verify
description: Confirm database backups exist AND actually restore, by enumerating Neon branch snapshots / Supabase scheduled backups / pg_dump artifacts, restoring into a scratch branch, running smoke queries, and recording timestamped evidence. Use before any risky migration or production mutation, and on a monthly cadence regardless.
---

# Backup Verify

## Overview

"A backup exists" and "a backup restores cleanly" are different claims, and only the second one matters during an incident. This skill does the actual restore drill — not just checking a dashboard says backups are enabled. Untested backups are a belief, not a fact.

This is the mandatory gate referenced by [[db-migration-safety]] before any production mutation, and should also run standalone on a monthly cadence so a restore is never being attempted for the first time during a real emergency.

## Workflow

1. **Enumerate what backup mechanism the target database actually uses** — don't assume:
   - Neon: point-in-time restore (PITR) window + snapshots. Check the restore window in the console (it varies by plan) and list snapshots with `neon snapshots list`.
   - Supabase: daily backups on Pro, Team, and Enterprise plans only, kept for 7, 14, and up to 30 days respectively (confirm against the current [Supabase backups docs](https://supabase.com/docs/guides/platform/backups)); PITR is a paid add-on. Free-plan projects get no automatic backups. List them with `supabase backups list --project-ref <ref>` or Dashboard → Database → Backups.
   - Manual `pg_dump`: if neither managed backup exists, this is the fallback — confirm one has actually been run and stored somewhere durable (not just on a laptop).

2. **Confirm the most recent backup's timestamp** and compare it against acceptable staleness for the task at hand — "backup from 6 days ago" is not acceptable evidence before a migration touching the `Subscription` table today.

3. **Restore into a scratch branch/environment** — never restore over the original:
   - Neon: restore a snapshot into a new branch with `neon snapshots restore <snapshot-id> --name backup-drill-<date>` — never pass `--finalize` (it swaps the restored data in for the target branch) or a `--target-branch` that is production. Or branch from a point in time: `neon branches create --parent <timestamp> --name backup-drill-<date>`.
   - Supabase: Dashboard → Database → Backups → **Restore to a New Project** (paid plans with physical backups). Do **not** use `supabase backups restore` for a drill — it restores the live project itself, in place.
   - Custom-format or directory dump (`pg_dump -Fc` / `-Fd`): `createdb backup_drill_<date> && pg_restore --no-owner -d backup_drill_<date> <dump_file>` against a local or scratch Postgres instance.
   - Plain SQL dump (default `pg_dump` output, or `supabase db dump`): `psql -d backup_drill_<date> -f <dump.sql>` — `pg_restore` only reads custom and directory formats. `supabase db dump` writes the schema only by default; a full copy also needs a `--data-only` dump.

4. **Run smoke queries** against the restored copy to confirm data integrity, not just that the restore command exited 0:
   ```sql
   -- Row counts on the tables that matter most (auth, billing)
   SELECT 'User' AS table_name, COUNT(*) FROM "User"
   UNION ALL SELECT 'Subscription', COUNT(*) FROM "Subscription"
   UNION ALL SELECT 'Customer', COUNT(*) FROM "Customer";

   -- Spot-check a known recent row exists and looks right
   SELECT * FROM "Subscription" ORDER BY "updatedAt" DESC LIMIT 5;

   -- Confirm referential integrity wasn't silently broken
   SELECT COUNT(*) FROM "Subscription" s
   LEFT JOIN "Customer" c ON c.id = s."customerId"
   WHERE c.id IS NULL;  -- should be 0
   ```
   Compare row counts against the live database's counts at drill time (they should be close — some drift is expected if traffic occurred between backup and drill).

5. **Tear down the scratch branch/database** after recording evidence — don't leave restore drills lying around accumulating cost or confusion about which environment is "real."

6. **Record evidence with timestamps** — a one-paragraph log entry is enough, but it must include: backup mechanism, backup timestamp, restore-drill timestamp, row-count comparison, and pass/fail.

## Pass/fail criteria

- **Pass:** the restore completes; every key table exists and is non-empty; counts differ from production only by writes made after the backup timestamp; the newest row's timestamp is at or just before the backup time; the integrity query returns 0.
- **Fail:** the restore errors; any key table is empty or missing; counts differ by more than writes since the backup can explain; the integrity query returns non-zero.

## Monthly cadence checklist

- [ ] Neon: PITR window still covers required retention; latest branch snapshot timestamp noted
- [ ] Supabase: scheduled backup ran in last 24–48h; plan tier still includes it
- [ ] Restore drill executed into a scratch branch this month
- [ ] Smoke queries passed (row counts sane, referential integrity intact, recent row present)
- [ ] Scratch branch/database torn down
- [ ] Evidence logged with date

## Common mistakes

- Checking that backups are "enabled" without restoring one.
- Restoring onto the production Neon branch or Supabase project instead of a new one.
- Feeding a plain-SQL dump to `pg_restore`, or treating a schema-only `supabase db dump` as a full backup.
- Comparing counts against production hours later and blaming drift for a real gap.
- Leaving the drill branch or project running.

Sources: [Neon backup and restore](https://neon.com/docs/guides/backup-restore), [Supabase backups](https://supabase.com/docs/guides/platform/backups), PostgreSQL [`pg_restore`](https://www.postgresql.org/docs/current/app-pgrestore.html).

## Output / Evidence

Report to the user: backup mechanism + timestamp of the backup used, the restore command run, smoke query results (row counts, integrity check), and confirmation the scratch environment was cleaned up. This evidence is what unblocks a migration gated by [[db-migration-safety]] — link back to it rather than re-describing.

## Stop Conditions

- No backup mechanism found at all (no PITR, no scheduled backup, no recent `pg_dump`) — stop, surface this to the user immediately, this is a standing risk independent of whatever task prompted the check.
- Restore drill fails (restore errors out, or smoke queries show missing/corrupted data) — stop, do not proceed with any pending migration, escalate as its own incident since it means backups are not actually protecting the business.
- Row counts in the restored copy are wildly inconsistent with production (e.g., off by an order of magnitude) — stop and investigate before treating the backup as valid.
