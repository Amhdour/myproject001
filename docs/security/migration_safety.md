# Migration Safety Plan (Step 10)

## Purpose
Define the documentation-only safety plan for future security-layer schema and data migrations.

## Scope
- Planning for schema/data migrations tied to future security controls.
- Applies to migration planning, validation, rollback readiness, and evidence requirements.
- No migration code or runtime behavior changes are included in this step.

## Status
planned

## Owner
AI Trust & Security Readiness Engineer

## Non-Claim Statement
This document is a planning artifact only and does **not** claim migration safety implementation, control effectiveness, or production readiness.

## Migration Risk Principles
1. Safety over speed: block release when migration evidence is incomplete.
2. Reproducibility: every migration path must be replayable in clean and existing database contexts.
3. Reversibility: rollback paths must be tested, not assumed.
4. Isolation: tenant, user, document, ACL, tool, and MCP data boundaries must be preserved.
5. Evidence first: no readiness claim without migration evidence.

## Migration Types
- Schema-only migrations (DDL changes).
- Data-only migrations (DML transformations).
- Hybrid schema+data migrations.
- Backfill and cleanup migrations.
- Tenant-scoped migration phases.

## Migration Naming Convention
Planned naming convention:
- Migration identifier: `ms_<YYYYMMDD>_<domain>_<short_action>`
- Example pattern only: `ms_20260526_acl_add_scope_index`
- Domain tags should align to security areas (`acl`, `audit`, `policy`, `tool`, `mcp`, `tenant`).

## Migration Dry-Run Requirements
- Every migration must support dry-run execution in CI/staging-equivalent contexts.
- Dry-run must include pre-checks, migration execution, post-checks, and log capture.
- Dry-run output must be attached as evidence prior to approval.

## Rollback Requirements
- Each migration must define rollback strategy and tested rollback command path.
- Rollback test must validate schema state and critical data integrity after reversal.
- Rollback outcomes must be recorded in evidence artifacts.

## Clean-Database Migration Test Plan
Planned checks:
1. Provision empty database instance.
2. Apply full migration chain from baseline.
3. Validate expected schema objects and constraints.
4. Seed planned test entities and verify integrity.
5. Capture logs/artifacts as evidence.

## Existing-Database Migration Test Plan
Planned checks:
1. Start from representative pre-migration snapshot.
2. Apply migration incrementally.
3. Validate preserved data semantics and access boundaries.
4. Validate post-migration query behavior for tenant/user/document/ACL/tool/MCP records.
5. Capture drift and integrity evidence.

## Schema Drift Detection Plan
- Run schema diff between expected migration state and actual database state.
- Gate on unexpected object deltas (tables, columns, indexes, constraints, policies).
- Record drift outputs for review and signoff.

## Seed Data Plan
Security-migration test seed sets must be synthetic and reproducible.

### Seed Requirements
- **Tenant seeds:** multiple tenants with isolated namespaces.
- **User seeds:** admin/member/viewer user roles across tenants.
- **Document seeds:** tenant-scoped documents with mixed ACL visibility.
- **ACL seeds:** explicit allow/deny entries and inheritance edge cases.
- **Tool seeds:** policy-scoped tools with authorized and unauthorized mappings.
- **MCP seeds:** capability-scoped MCP servers/resources with least-privilege coverage.
- **Demo attack seeds:** synthetic attack scenarios for migration regression checks.

## Backup-Before-Migration Requirement
- A verified backup/snapshot must be completed before applying migration in shared or persistent environments.
- Backup metadata (timestamp, source, checksum/location) must be logged as evidence.

## Restore-After-Migration Validation
- Perform restore drill on a target environment using pre-migration backup.
- Validate recovered schema version, critical row counts, and ACL boundary expectations.
- Record restore validation output as required evidence.

## Evidence Requirements
Required evidence categories for migration safety:
- Prerequisite verification output.
- Dry-run execution logs.
- Rollback test output.
- Clean database migration output.
- Existing database migration output.
- Schema drift reports.
- Seed data verification output.
- Backup and restore validation artifacts.
- Limitation notes when remote/main verification is unavailable.

## CI Gate Requirements
Planned CI gates for migration safety must include:
1. Migration dry-run check.
2. Migration rollback test.
3. Clean database migration test.
4. Existing database migration test.
5. Schema drift detection check.
6. Seed tenants check.
7. Seed users check.
8. Seed documents check.
9. Seed ACLs check.
10. Seed tools check.
11. Seed MCP data check.
12. Seed demo attacks check.
13. Backup before migration check.
14. Restore validation after migration check.

## Production Blocker Criteria
Production readiness remains blocked when any of the following apply:
- Any planned migration safety gate is not implemented or failing.
- Rollback path is missing or untested.
- Backup/restore validation evidence is missing.
- Schema drift is detected and unresolved.
- Seed/demo data separation controls are unverified.
- Required migration evidence is incomplete.

## Known Limitations
- Migration safety is documented as planned only.
- No migration code changes are implemented in this step.
- Migration checks are not yet automated.
- Remote/main verification may be limited by environment access constraints.
