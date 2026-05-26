# Known Limitations

## Step 7 Status
Step 7 (Evidence Standardization) is completed as documentation-only work. No runtime controls were implemented.

## Active Limitations / Blockers
1. **Baseline dependency blocker:** backend unit test collection fails due to missing `fastapi_users` in current environment.
2. **Remote verification limitation:** remote/main verification remains unavailable because git remote access is not configured/accessible in this environment (`fatal: 'origin' does not appear to be a git repository`).
3. **Evidence standard maturity limitation:** `docs/security/evidence_standard.md` is currently a draft and may require refinement after control implementation begins.
4. **Evidence sanitization limitation:** raw evidence artifacts may require a later sanitization review before external distribution.
5. **Production-readiness limitation:** no production-readiness claim is supported at this stage.
6. **Execution tracker remote metadata limitation:** PR links may remain `TBD` when remote fetch is unavailable.
7. **Execution tracker lineage limitation:** commit lineage may require GitHub UI verification when remote/main is inaccessible.


## Operational Impact
- Full baseline verification remains incomplete until dependency and/or environment issues are resolved.
- Remote/main branch parity cannot be confirmed from the current environment.
- Evidence structure is defined, but implementation-phase artifacts are still pending.

## Required Follow-up
- Restore or configure dependencies for unit collection and rerun baseline checks.
- Reconfigure/restore remote `origin` access and rerun fetch/verification.
- Execute sanitization review on raw evidence bundles before sharing outside the core team.
- Continue control design and implementation in later steps before any readiness decision.

## No-Readiness-Claim Statement
This documentation set does not claim production readiness.
