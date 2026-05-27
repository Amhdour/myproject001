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

## Step 15C Additional Limitations
- secure ingestion remains isolated.
- live ingestion enforcement is not active.
- connector/file-upload/parser/chunking/embedding/vector-write controls are not integrated into live flows.
- production enforcement remains inactive.

## Step 16A Additional Limitations
- retrieval ACL is design-only.
- no live retrieval enforcement wired.
- document/chunk/vector/cache/rerank/context controls are not integrated.
- production enforcement remains inactive.

## Step 16B Known Limitations (2026-05-27)
- Isolated retrieval ACL controls only.
- Not wired into live retrieval.
- No real vector DB/search/rerank/cache/context/prompt enforcement.
- Production enforcement remains inactive.

## Step 16C Additional Limitations
- retrieval ACL remains isolated.
- live retrieval enforcement is not active.
- document/chunk/vector/cache/rerank/context/prompt controls are not integrated into live flows.
- production enforcement remains inactive.

## step 17A retrieval path patching limitations
- Retrieval path patching is design-only in this step.
- No live retrieval path is patched yet.
- Enforcement remains inactive.
- Feature flags/rollback controls described but not implemented yet.
- Production enforcement remains inactive.

## Step 17A Known Limitations
- Design-only output
- No live patching
- Enforcement inactive
- Feature flags not implemented
- Rollback controls not implemented

## Step 17B Additional Limitations
- retrieval path integration is planned only.
- no live retrieval path patched yet.
- feature flags not implemented yet.
- rollback not implemented yet.
- production enforcement remains inactive.
\n## Step 17C Update\n- Isolated feature-flag helper implemented.\n- Isolated retrieval context builder implemented.\n- Isolated monitor/shadow/enforce hook helper implemented.\n- No live retrieval path patched; production enforcement remains inactive.

## Step 17C Additional Limitations
- retrieval context builder is isolated only.
- feature flags are isolated/test-only.
- live retrieval path is not patched.
- production enforcement remains inactive.

## Step 17D Additions (2026-05-27)
- Live retrieval patching has not started.
- Enforce mode is explicitly no-go.
- Next implementation may only be monitor-only.
- Production enforcement remains inactive.
\n\n## Step 17E Update (2026-05-27)\n- Added first live retrieval monitor-only hook at  after existing retrieval guard result handling.\n- Mode is disabled by default (), and monitor_only is the only live-enabled behavior for this step.\n- Enforce mode remains NO-GO and is not wired into live retrieval path.\n- Hook is non-blocking, non-filtering, fail-open for telemetry errors, and preserves retrieval response unchanged.\n

## Step 17E Update (2026-05-27)
- Added first live retrieval monitor-only hook at `backend/onyx/context/search/retrieval/search_runner.py` after existing retrieval guard result handling.
- Mode is disabled by default (`default_retrieval_integration_config`), and monitor_only is the only live-enabled behavior for this step.
- Enforce mode remains NO-GO and is not wired into live retrieval path.
- Hook is non-blocking, non-filtering, fail-open for telemetry errors, and preserves retrieval response unchanged.


## Step 17F Update (2026-05-27)
- Retrieval monitor-only validation completed.
- Disabled mode preserves retrieval behavior.
- Monitor-only mode preserves retrieval behavior.
- Enforce mode remains NO-GO/inactive.
- Retrieval blocking/filtering/denial remains disabled in live path.

## Step 18A Limitations (2026-05-27)
- Retrieval security tests are designed only.
- Broad retrieval security test suite is not implemented yet.
- Shadow-deny/enforce remain blocked.
- Production enforcement remains inactive.

## Step 18B Additional Limitations (2026-05-27)
- retrieval security tests are partially implemented.
- future shadow-deny/enforce tests are skipped/xfail.
- shadow-deny/enforce remain blocked.
- production enforcement remains inactive.

## Step 18B Limitation Update (2026-05-27)
- Prior pytest-unavailable blocker for Step 18B validation is resolved in current environment via `python -m pytest` execution.
- Shadow-deny/enforce remain intentionally not enabled.

## Step 18C Additional Limitations
- Future shadow-deny/enforce retrieval tests remain skipped/xfail by design.
- Shadow-deny/enforce remain blocked and inactive.
- Production retrieval enforcement remains inactive.
- Retrieval security tests are still skeleton/partial and are not full live-enforcement tests.

## Step 18D Additional Limitations (2026-05-27)
- Retrieval negative tests are implemented for monitor-only and isolated behavior.
- Future shadow-deny/enforce tests remain skipped/xfail.
- Shadow-deny and enforce remain blocked.
- Production enforcement remains inactive.
- Live retrieval blocking/filtering remains disabled.
