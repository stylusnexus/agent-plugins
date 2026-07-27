---
name: db-truth
description: Ground every database claim in the live database. Repo-agnostic — pre-work verification before any spec, plan, or code that touches tables (schema shape, M2M vs scalar, RLS/permissions, function properties), and post-apply verification that migrations actually landed (ledger, object existence, type regen). Defers to a repo-local db-truth skill when one exists. Use BEFORE designing anything DB-touching and AFTER every migration apply.
---

# DB Truth — the database is the only schema authority (repo-agnostic)

## Overview

Types, specs, docs, ORMs, and memory are NOT schema truth. Only the database is. The incident record behind this skill: a spec ratified by six agent reviewers assumed a column that didn't exist (reality was a many-to-many junction); a type regen against a stale local DB deleted 211 real production type keys; migration tools have exited success without applying, and applied without recording.

**If the current repo has its own `.claude/skills/db-truth/` or `.agents/skills/db-truth/`, that version is authoritative — follow it instead.** This global version is the fallback.

**Announce at start:** "Running /db-truth <pre-work | post-apply> verification."

## Part A — Pre-work (before any DB-touching spec, plan, or code)

1. **Dump the real schema for EVERY table you'll reference.** Postgres: `\d <table>` via psql, or `SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name='<t>'`. Supabase repos: local stack creds via `eval "$(npx supabase status -o env)"`; prod read-only via the MCP/dashboard. Paste relevant output into the spec/plan as canonical context — especially for junction tables.
2. **Label every relationship M2M or scalar.** If you're writing a singular possessive ("the record's parent") about a junction-linked entity, you have the wrong model. The spec's data-model section must mark each relationship explicitly.
3. **Check the invisible properties.** Row-level security policies and table GRANTs for the operation you're adding (Supabase: new public tables need explicit GRANTs — auto-grants are being phased out). For functions: `CREATE OR REPLACE` resets EVERY unrestated property, including security settings like `SET search_path` — your replacement must restate them or you silently un-harden production.
4. **Nested JSON writes:** `jsonb_set`-style patches silently no-op when the parent key is missing. Verify the parent is seeded before targeting a nested key.
5. **Verify claimed call sites.** If a plan says "the call happens in X", grep it and cite `file:line`. Plans have named wrong injection sites; implementers propagate the error.

## Part B — Post-apply (after every migration)

1. **Confirm the ledger.** `npx supabase migration list --linked` (or the stack's equivalent). Exit codes are NOT proof — pushes have succeeded without applying, and MCP-style apply tools have run DDL without recording it (reconcile the ledger manually if so).
2. **Probe the object itself.** SELECT from the new table / call the new function in the environment you think you changed. A ledger row is a claim; a returned row is evidence.
3. **Regenerate types the safe way.** Regenerate against the LINKED/production schema, never a possibly-stale local DB. If the regen diff is larger than your change, STOP — you are probably about to commit a mass deletion. Surgical hand-edits are often safer for small changes.

## Standing rules

- Migrations go only in the path the deploy tooling actually applies — verify which directory that is before authoring; legacy migration dirs exist in some repos and are silently ignored.
- Migrations are idempotent (`IF NOT EXISTS` / `DROP ... IF EXISTS`); no non-IMMUTABLE functions (`NOW()`) in index predicates.
- DB-writing tests must be host-gated: test runners commonly load the env file that points at PRODUCTION. Gate on localhost or refuse to run.
- Production mutations require a confirmed recent backup first.

## Stop conditions

- Live schema contradicts the spec/plan/issue → stop and report with the schema dump; don't proceed on the spec's version.
- Regen diff deletes fields you didn't touch → stop, don't commit, investigate drift.
- Ledger and database disagree → reconcile before any further migration work.
