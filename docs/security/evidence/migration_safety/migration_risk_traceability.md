# Migration Risk Traceability (Step 10)

## Added Risks
- R-MIG-001 migration breaks existing data
- R-MIG-002 rollback unavailable or untested
- R-MIG-003 schema drift causes authorization bypass
- R-MIG-004 seed/demo data leaks into non-demo environment
- R-MIG-005 migration evidence missing

## Traceability Mapping
Each migration risk maps to:
1. Security requirements (CI/evidence/admin/retrieval where relevant).
2. Planned checks (dry-run, rollback, clean/existing DB migration, schema drift, seed checks, backup/restore).
3. Evidence outputs under `docs/security/evidence/migration_safety/`.

## Result
Migration-safety risks are now documented in risk register and control traceability matrix as planned controls.
