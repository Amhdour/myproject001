# Retrieval Path Patching (Step 17A)

## Purpose / Scope / Status
Design-only documentation for retrieval path patching. No runtime wiring is included in Step 17A.

## Non-Claim
This step does **not** enable live retrieval enforcement.

## Rollout Modes
- Observe-only
- Enforce-deny

## Expectations
- Fail-closed behavior for indeterminate patch decisions
- Safe-denial behavior for disallowed retrieval paths

## Feature Flag and Rollback
Future implementation must include explicit flag gating and rollback controls.

## Patch Candidate Catalog
RPC-001, RPC-002, RPC-003, RPC-004, RPC-005, RPC-006, RPC-007, RPC-008, RPC-009, RPC-010, RPC-011, RPC-012, RPC-013, RPC-014, RPC-015, RPC-016, RPC-017.

## Step 17B Integration-Plan Note (2026-05-27)
- Integration plan created: `docs/security/retrieval_path_integration_plan.md`.
- No live retrieval path patching performed in Step 17B.
- Feature-flag, rollback, and test sequencing are documented for future implementation.
\n## Step 17C Update\n- Isolated feature-flag helper implemented.\n- Isolated retrieval context builder implemented.\n- Isolated monitor/shadow/enforce hook helper implemented.\n- No live retrieval path patched; production enforcement remains inactive.

## Step 17C Note (2026-05-27)
- Added isolated retrieval integration helpers (feature flags, context builder, and hook helpers).
- No live retrieval path patching or production/runtime wiring was performed.

## Step 17D Readiness Review Reference (2026-05-27)
- Readiness review: `docs/security/retrieval_path_readiness_review.md`.
- Go/no-go decision: `docs/security/retrieval_path_live_patch_go_no_go.md`.
- Live patch target inventory: `docs/security/retrieval_path_live_patch_file_targets.md`.
- Enforce mode remains no-go; next live patch scope is monitor-only only.
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
