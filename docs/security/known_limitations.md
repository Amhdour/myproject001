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

8. **Fixture implementation limitation:** fixtures are planned only in documentation and no fixture code has been implemented yet.
9. **Test-data governance limitation:** no real tenant, user, or customer data may be used for fixture work; synthetic data rules are mandatory.

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


10. **Migration safety planning-only limitation:** migration safety is documented as planned only; implementation has not started.
11. **Migration code limitation:** no migration code has been implemented in this step.
12. **Migration automation limitation:** migration safety checks are planned but not yet automated.

## Step 11 Additional Limitations
- Policy files under `docs/security/policies/` are draft-only planning artifacts.
- Policy validation automation is not implemented.
- Runtime policy engine is not implemented.
- Runtime enforcement is not active.

## Step 12A Additional Limitations
- Policy engine is design-only in this step; no runtime enforcement integration exists.
- Policy engine test plan is planned-only and not yet executed.
- Policy hash/integrity and decision-audit checks are not yet implemented in runtime code.

## Step 12B Additional Limitations

- Minimal policy engine is isolated only.
- Runtime integration is not implemented.
- Production enforcement is not active.

## Step 12C Additional Limitations
- Policy engine remains isolated to `backend/security_layer/policies`.
- Runtime enforcement is not active.
- Backend API/request path integration has not started.

## Step 13A Runtime Wrapper Limitations

- runtime wrappers are designed only.
- wrapper implementation is not active.
- wrappers are not wired into application paths.
- enforcement remains inactive.

- Runtime wrappers are isolated-only.
- Runtime wrappers are not wired into application paths.
- Audit/finding/metric helpers are in-memory test-only.
- Enforcement remains inactive.

## Step 13C Additional Limitations
- Runtime wrappers remain isolated under `backend/security_layer/runtime`.
- Runtime enforcement is not active.
- Application-path integration has not started.

## Step 14A Additional Limitations
- Safe denial behavior is documented only; runtime enforcement wiring is not implemented.
- Denial taxonomy is planned and not yet enforced across backend/UI/streaming surfaces.
- Denial metrics/findings/audit mappings are planning metadata pending implementation.

## Step 14B Additional Limitations
- Safe denial helpers are isolated only.
- Denial behavior is not globally wired into application paths.
- Streaming/tool/MCP/artifact denial behavior is not integrated into live flows.
- Production enforcement remains inactive.

## Step 14C Additional Limitations
- Safe denial behavior remains isolated under `backend/security_layer/runtime`.
- Denial behavior is not globally wired into backend/runtime application paths.
- Live streaming/tool/MCP/artifact/sandbox denial integrations are not implemented.
- Production enforcement remains inactive.

## Step 15A Additional Limitations
- secure ingestion is design-only.
- no live ingestion enforcement wired.
- connector/file-upload/parser/chunking/vector-write controls are not integrated.
- malware/DLP checks are placeholders unless later implemented.
- production enforcement remains inactive.

## Step 15B Additional Limitations
- isolated ingestion controls only.
- not wired into live ingestion.
- no real malware scanner.
- no real DLP scanner.
- no production parser/chunker/embedder/vector-write enforcement.
