# Step 39X Runtime Enforcement Proof

## Scope

Step 39X adds one minimal runtime-facing retrieval authorization proof. The hook is wired into `backend/onyx/context/search/retrieval/search_runner.py` after the existing retrieval ACL guard has produced candidate chunks and before chunks are returned from `search_chunks()`.

## Runtime hook chosen

- Hook: `_apply_step_39x_runtime_enforcement_hook()` in `backend/onyx/context/search/retrieval/search_runner.py`.
- Adapter: `backend/security_layer/runtime_enforcement/retrieval_adapter.py`.
- Decision helper: `backend/security_layer/runtime_enforcement/decision.py`.
- Audit sink: `backend/security_layer/runtime_enforcement/audit.py`.

## Why this hook was chosen

The retrieval search runner is a real backend retrieval path, but the Step 39X proof remains narrow and feature-flagged. The hook can be exercised without cloud, VPS, K3s, Rancher, Coolify, or external network services by unit-testing the adapter with deterministic retrieval chunk metadata.

## Mode behavior

`STEP_39X_RUNTIME_ENFORCEMENT_MODE` supports:

- `disabled` — default; no audit event is emitted and chunks are preserved.
- `monitor_only` — evaluates and audits allow/deny decisions, but preserves chunks.
- `enforce` — evaluates and audits; denied chunks are filtered from the runtime hook output and a safe denial payload is available from the adapter.

## Claim boundary

This is a Step 39X runtime enforcement proof only. It is not enterprise production readiness, not full Onyx-wide enforcement, not complete RAG/agent security coverage, not external validation, not compliance certification, and not proof of live staging/cloud deployment.
