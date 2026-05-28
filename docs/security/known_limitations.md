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


- Step 18D-A note: monitor-only negative coverage expanded; no new runtime limitations introduced.

## Step 18E Additional Limitations (2026-05-27)
- Retrieval negative tests are validated for monitor-only and isolated behavior only.
- Future shadow-deny/enforce tests remain skipped/xfail.
- Shadow-deny/enforce remain blocked.
- Production enforcement remains inactive.
- Live retrieval blocking/filtering remains disabled.

## Step 19A Additional Limitations (2026-05-27)
- vector DB security is design-only.
- no live vector DB enforcement wired.
- no vector write/read/delete controls integrated.
- no namespace/metadata filters integrated into live vector queries.
- production enforcement remains inactive.

## Step 19B Additional Limitations (2026-05-27)
- isolated vector DB security controls only.
- no live vector DB enforcement wired.
- no real vector DB/search/index/cache calls.
- production enforcement remains inactive.

## Step 19C Additional Limitations (2026-05-27)
- isolated vector DB security controls validated only.
- no live vector DB enforcement wired.
- no real vector DB/search/index/cache calls added.
- live vector/retrieval blocking/filtering remains disabled.
- production enforcement remains inactive.

## Step 20A Additional Limitations (2026-05-28)
- cache security is design-only.
- no live cache enforcement wired.
- no cache key contract implemented yet.
- no cache read/write/invalidation controls integrated.
- production enforcement remains inactive.

## Step 20B Limitations
- Isolated cache security controls only.
- No live cache enforcement wiring.
- No real cache backend calls.
- No cache read/write/invalidation controls integrated into live flows.
- Production enforcement remains inactive.

## Step 20C Limitations (2026-05-28)
- isolated cache security controls validated only.
- no live cache enforcement wired.
- no real cache backend calls.
- live cache/vector/retrieval blocking/filtering remains disabled.
- production enforcement remains inactive.

## Step 21A Tool Authorization Limitations
- tool authorization is design-only.
- no live tool enforcement wired.
- no tool registry implementation yet.
- no tool argument validation integrated into live flows.
- production enforcement remains inactive.

## Step 21B Limitations
- Isolated tool authorization controls only.
- No live tool enforcement wired.
- No real tool/MCP/network/filesystem/shell calls.
- No tool argument validation integrated into live flows.
- Production enforcement remains inactive.

## Step 21C Limitations Update (2026-05-28)
- Isolated tool authorization controls validated only.
- No live tool enforcement wired.
- No real tool/MCP/network/filesystem/shell calls in this step scope.
- Tool argument validation is not integrated into live request flows.
- Live tool/cache/vector/retrieval blocking/filtering remains disabled.
- Production enforcement remains inactive.


## Step 22A Additional Limitations
- MCP hardening is design-only.
- no live MCP enforcement wired.
- no MCP registry implementation yet.
- no MCP credential isolation implementation yet.
- no MCP egress enforcement integrated into live flows.
- no MCP request signing/replay protection integrated into live flows.
- production enforcement remains inactive.

## Step 22B Update (2026-05-28)
Implemented minimal isolated MCP hardening helpers/tests only; no live MCP/tool/agent integration and no production enforcement activation.

## Step 22C Update (2026-05-28)
Validation cleanup is isolated-only. No enforce mode, no shadow-deny mode, and no live MCP/tool/cache/vector/retrieval blocking/filtering enabled.

## Step 23A Additional Limitations
- artifact safety is design-only
- no live artifact safety enforcement wired
- no artifact metadata contract implementation yet
- no artifact scan-before-release implementation yet
- no artifact quarantine/redaction/download enforcement integrated into live flows
- production enforcement remains inactive


## Step 23C Update (2026-05-28)
- Isolated artifact safety validation cleanup completed for controls/tests/docs/evidence only.
- No live artifact/export/download/sandbox/tool/MCP/retrieval/vector/cache integration changed.
- Enforce and shadow-deny remain inactive.

## Step 24A Known Limitations
- Cross-control integration remains documentation-first and monitor-only.
- No enforce mode, no shadow-deny mode, and no live blocking/filtering were enabled.
- Remote PR linkage may remain unavailable when remote sync is restricted.

## Step 24B Additional Limitations (2026-05-28)
- cross-control evidence hardening is documentation/evidence-only.
- no new live enforcement wired.
- no new live blocking/filtering enabled.
- monitor-only remains limited.
- shadow-deny remains blocked.
- enforce mode remains blocked.
- production readiness is not claimed.
- remote/main verification remains limited when remote fetch is unavailable.

## Step 24C Additional Limitations (2026-05-28)
- Cross-control evidence validation is documentation/evidence consistency validation only.
- Remote/mainline/PR linkage verification remains limited when no git remote is configured.
- No live enforcement controls were enabled in this step.

## Step 25A Shadow-Deny Planning Limitations
- shadow-deny rollout is planning-only.
- no shadow-deny runtime activation.
- no live blocking/filtering enabled.
- enforce mode remains blocked.
- production enforcement remains inactive.
- production readiness is not claimed.

## Step 25B Limitations
- Shadow-deny simulation harness is isolated only.
- No runtime shadow-deny activation.
- No live blocking/filtering enabled.
- Enforce mode remains blocked.
- Production enforcement remains inactive.
- Production readiness is not claimed.

## Step 25C - Shadow-Deny Simulation Validation (2026-05-28)

- Completed validation on branch `shadow-deny-simulation-validation`.
- Evidence folder: `docs/security/evidence/shadow_deny_simulation_validation/`.
- Focused and full security-layer test suites passed.
- Confirmed simulation-only operation (no enforce mode, no live blocking/filtering, no application behavior change).

## Step 26X Enforce-Mode Readiness Bundle Limitations
- The enforce-mode readiness bundle is planning/simulation/evidence only.
- No enforce runtime activation is implemented or enabled.
- No live blocking/filtering is enabled.
- Shadow-deny runtime remains inactive.
- Production enforcement remains inactive.
- Production readiness is not claimed.
- Remote/main verification was limited because `origin` was not configured in this environment.

## Step 27X Limited Monitor-Only Integration Limitations

- The bundle is isolated helper scaffolding only and is not wired into live cache/application request paths.
- The shared sink uses in-memory security-layer runtime helpers in tests; production telemetry sink reliability is not validated.
- Remote branch synchronization could not be verified because no git remote is configured in this workspace.
- Enforce mode and shadow-deny runtime activation remain outside Step 27X scope and inactive.
- This step does not claim production readiness.

## Step 28X Regression + Demo Attack Bundle Limitations

- The regression/demo attack bundle is isolated only.
- Demo attacks use synthetic fixtures only.
- No staging execution has occurred yet.
- No live blocking/filtering is enabled.
- No enforce runtime activation is enabled.
- No shadow-deny runtime activation is enabled.
- Production readiness is not claimed.

## Step 29X Coolify Staging Limitations

- No real Coolify deployment was executed from this repository change.
- Live staging smoke validation is pending until an approved operator deploys the
  branch to a staging-only Coolify application and captures sanitized evidence.
- The environment template contains placeholders only and is not a deployable
  secret file.
- Remote Coolify synchronization was not verified from this environment.
- The staging helper package is isolated and does not validate real network,
  routing, secret-store, or runtime service behavior.
- No production-readiness claim is made.

## Step 30X Partner Evidence Room Limitations

- The partner evidence room is a sanitized repository-evidence bundle, not a production-readiness attestation.
- Live staging validation remains **PENDING** unless real staging evidence is collected separately.
- External validation remains **PENDING**.
- Compliance certification is **NOT CLAIMED**.
- No enforce mode, shadow-deny runtime mode, live blocking, or live filtering is enabled by this step.
- No git remote is configured in this workspace, so remote synchronization could not be verified locally.
