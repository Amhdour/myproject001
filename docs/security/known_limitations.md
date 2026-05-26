# Known Limitations

## Step 6 Status
Step 6 (Requirements, Risk, and Traceability) is completed as documentation-only work. No runtime controls were implemented.

## Active Limitations / Blockers
1. **Baseline dependency blocker:** backend unit test collection fails due to missing `fastapi_users` in current environment.
2. **Remote verification limitation:** git remote verification is limited because `origin` fetch is unavailable in this environment (`fatal: 'origin' does not appear to be a git repository`).
3. **Production-readiness limitation:** no production-readiness claim is supported at this stage.

## Operational Impact
- Full baseline verification remains incomplete until dependency and/or environment issues are resolved.
- Remote/main branch parity cannot be confirmed from the current environment.

## Required Follow-up
- Restore or configure dependencies for unit collection and rerun baseline checks.
- Reconfigure/restore remote `origin` access and rerun fetch/verification.
- Continue control design and implementation in later steps before any readiness decision.
