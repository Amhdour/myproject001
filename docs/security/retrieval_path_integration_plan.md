# Retrieval Path Integration Plan (Step 17B)

## Purpose
Define the minimal, phased integration approach for wiring previously isolated retrieval ACL controls into retrieval execution paths under strict feature-flag control.

## Scope
Planning-only integration design, sequencing, and verification requirements for future implementation. No live retrieval runtime patching is performed in this step.

## Status
planned/integration-plan

## Owner
AI Trust & Security Readiness Engineer

## Non-Claim Statement
This document does not claim production wiring, live enforcement, control effectiveness, or release readiness.

## Relationship to Isolated Retrieval ACL Controls
This plan consumes isolated controls in `backend/security_layer/retrieval/{models,validators,controls}.py` as upstream dependencies and defines how they are introduced into runtime paths incrementally.

## Relationship to Retrieval Path Patching Design
This plan operationalizes Step 17A (`docs/security/retrieval_path_patching.md`) by defining implementation phases, gates, rollback criteria, and evidence expectations.

## Minimal Integration Principle
Only the smallest patch set needed per phase will be allowed, with default-safe behavior and explicit rollback for every phase.

## Feature Flag Plan
Introduce dedicated retrieval ACL integration flags with explicit defaults, mode selection (`disabled`, `monitor_only`, `shadow_deny`, `enforce`), and per-environment override controls.

## Monitor-only Default Plan
Default startup mode remains `disabled` or `monitor_only` only; no blocking actions occur until enforce promotion criteria are met.

## Shadow-deny Promotion Plan
Promote from monitor-only after audit and metric stability checks; shadow mode computes deny outcomes and records diffs without blocking users.

## Enforce-mode Promotion Plan
Enable enforce mode only after evidence package completion, traceability closure, rollback rehearsal, and explicit security approval.

## Rollback Plan
Every phase includes a reversible flag path; primary rollback is mode reversion to `disabled`/`monitor_only`, with hook neutralization if required.

## Fail-closed Boundaries
Fail-closed behavior is limited to explicit enforce-mode decision points where policy/context cannot be trusted.

## Safe Denial Boundaries
Any enforce denial must use safe denial taxonomy without leaking unauthorized source, chunk, or tenant details.

## Audit/Finding/Metric Integration Plan
Runtime decision hooks will emit structured audit events, findings for unsafe patterns, and metrics for mode behavior and deny rates.

## Context Extraction Plan
Add a minimal retrieval context builder that extracts subject/tenant/request metadata with safe handling for missing/partial identity attributes.

## Compatibility Plan
Integration must preserve existing retrieval behavior in `disabled`/`monitor_only` modes and avoid changing unrelated search flows.

## Performance Risk Plan
Track latency overhead and candidate volume impact from decision hooks; enforce mode rollout requires measured thresholds.

## Test Strategy
Execution follows `docs/security/retrieval_path_integration_test_plan.md` with phase-mapped tests before promotion.

## Evidence Requirements
Evidence must include prerequisite verification, phase inventory, checklist status, traceability mapping, planned tests, and rollout gating rationale.

## Implementation Sequencing
Phases are strictly ordered from configuration scaffolding to CI/security-gate coverage.

## Known Limitations
- Planning only in Step 17B.
- No live retrieval path is patched in this step.
- Feature flags are planned but not implemented.
- Rollback mechanics are planned but not implemented.
- Production enforcement remains inactive.

---

## Exact Minimal Patch Sequence

### Phase 1 — add config/feature-flag placeholders
- **Phase ID:** RPIP-P1
- **Purpose:** Define retrieval ACL integration mode/config placeholders.
- **Candidate files/functions:** retrieval config module(s), runtime settings surface, environment parsing helpers.
- **Planned code change type:** additive config constants/types/placeholders.
- **Required context fields:** mode, tenant_id, request_id.
- **Mapped patch candidates:** RPC-001, RPC-002.
- **Mapped risks:** R-RINT-002, R-RINT-004.
- **Mapped requirements:** SR-RET-001, SR-CI-001.
- **Planned tests:** RPIT-001, RPIT-014.
- **Rollback note:** revert mode default to `disabled`.
- **Evidence required:** config default capture + test output.
- **Implementation status:** planned.

### Phase 2 — add retrieval context builder helper
- **Phase ID:** RPIP-P2
- **Purpose:** Build normalized subject/tenant retrieval decision context.
- **Candidate files/functions:** retrieval context helper module(s), request-context wrapper adapters.
- **Planned code change type:** additive helper function/class.
- **Required context fields:** request_id, subject_id, subject_groups, subject_roles, tenant_id, workspace_id.
- **Mapped patch candidates:** RPC-003, RPC-004.
- **Mapped risks:** R-RINT-001, R-RINT-006.
- **Mapped requirements:** SR-RET-001.
- **Planned tests:** RPIT-002, RPIT-003, RPIT-004, RPIT-005.
- **Rollback note:** bypass helper and return neutral context.
- **Evidence required:** context field matrix + missing-field behavior logs.
- **Implementation status:** planned.

### Phase 3 — add monitor-only retrieval decision hook
- **Phase ID:** RPIP-P3
- **Purpose:** Run retrieval ACL decisions without request blocking.
- **Candidate files/functions:** retrieval orchestration hook points from Step 17A candidate map.
- **Planned code change type:** additive hook invocation behind monitor-only flag.
- **Required context fields:** mode, request_id, subject_id, tenant_id, candidate_doc_id/chunk_id.
- **Mapped patch candidates:** RPC-005, RPC-006, RPC-007.
- **Mapped risks:** R-RINT-001, R-RINT-003.
- **Mapped requirements:** SR-RET-001, SR-AUDIT-001.
- **Planned tests:** RPIT-006, RPIT-010.
- **Rollback note:** disable hook via flag.
- **Evidence required:** monitor decision samples proving non-blocking behavior.
- **Implementation status:** planned.

### Phase 4 — add audit/finding/metric recording hook
- **Phase ID:** RPIP-P4
- **Purpose:** Persist monitor/shadow/enforce telemetry for decisions.
- **Candidate files/functions:** audit emitter, findings recorder, metrics counters around retrieval decision hook.
- **Planned code change type:** additive observability integration.
- **Required context fields:** event_type, mode, decision, deny_reason, tenant_id, subject_hash.
- **Mapped patch candidates:** RPC-008, RPC-009.
- **Mapped risks:** R-RINT-001, R-RINT-004.
- **Mapped requirements:** SR-AUDIT-001, SR-EVIDENCE-001.
- **Planned tests:** RPIT-007, RPIT-008, RPIT-009.
- **Rollback note:** keep hook, disable emission path by config.
- **Evidence required:** sample audit/finding/metric artifacts.
- **Implementation status:** planned.

### Phase 5 — add shadow-deny support
- **Phase ID:** RPIP-P5
- **Purpose:** Compute would-deny outcomes and compare to live allow path.
- **Candidate files/functions:** mode switch inside hook, shadow diff recorder.
- **Planned code change type:** additive mode branch.
- **Required context fields:** mode, decision, shadow_decision, candidate_id.
- **Mapped patch candidates:** RPC-010.
- **Mapped risks:** R-RINT-003, R-RINT-004.
- **Mapped requirements:** SR-RET-001, SR-EVIDENCE-001.
- **Planned tests:** RPIT-010.
- **Rollback note:** revert mode to monitor-only.
- **Evidence required:** shadow diff reports.
- **Implementation status:** planned.

### Phase 6 — add enforce-mode support
- **Phase ID:** RPIP-P6
- **Purpose:** Block unauthorized retrieval candidates under explicit enforce flag.
- **Candidate files/functions:** candidate filtering/citation/context boundary hooks identified in Step 17A patch map.
- **Planned code change type:** gated behavioral change (deny/block).
- **Required context fields:** decision, deny_reason, tenant_id, source_id, chunk_id.
- **Mapped patch candidates:** RPC-011, RPC-012, RPC-013, RPC-014.
- **Mapped risks:** R-RINT-001, R-RINT-004.
- **Mapped requirements:** SR-RET-001, SR-CACHE-001.
- **Planned tests:** RPIT-011, RPIT-012, RPIT-013, RPIT-016, RPIT-017, RPIT-018.
- **Rollback note:** immediate mode fallback to shadow/monitor/disabled.
- **Evidence required:** enforce deny evidence + no-leak safe denial samples.
- **Implementation status:** planned.

### Phase 7 — add rollback verification
- **Phase ID:** RPIP-P7
- **Purpose:** Prove safe rollback/neutralization path before merge/promotion.
- **Candidate files/functions:** mode toggles, hook guard rails, deployment config docs.
- **Planned code change type:** verification and runbook updates.
- **Required context fields:** previous_mode, target_mode, verification_status.
- **Mapped patch candidates:** RPC-015.
- **Mapped risks:** R-RINT-005.
- **Mapped requirements:** SR-EVIDENCE-001, SR-CI-001.
- **Planned tests:** RPIT-015.
- **Rollback note:** N/A (this phase verifies rollback).
- **Evidence required:** rollback rehearsal output.
- **Implementation status:** planned.

### Phase 8 — add CI/security-gate coverage
- **Phase ID:** RPIP-P8
- **Purpose:** Add automated checks for mode defaults, traceability, and enforce safety gates.
- **Candidate files/functions:** CI jobs, security gate scripts, docs evidence checklists.
- **Planned code change type:** additive CI/test gate configuration.
- **Required context fields:** build_id, mode_default, gate_result.
- **Mapped patch candidates:** RPC-016, RPC-017.
- **Mapped risks:** R-RINT-002, R-RINT-004, R-RINT-005.
- **Mapped requirements:** SR-CI-001, SR-EVIDENCE-001.
- **Planned tests:** RPIT-019.
- **Rollback note:** disable gate additions if false positives block critical pipelines.
- **Evidence required:** CI gate pass/fail reports.
- **Implementation status:** planned.
\n## Step 17C Update\n- Isolated feature-flag helper implemented.\n- Isolated retrieval context builder implemented.\n- Isolated monitor/shadow/enforce hook helper implemented.\n- No live retrieval path patched; production enforcement remains inactive.

## Step 17C Implementation Note (2026-05-27)
- Isolated feature-flag helper implemented.
- Isolated retrieval context builder implemented.
- Isolated monitor/shadow/enforce hook helper implemented.
- No live retrieval path patched.

## Step 17D Readiness-Review Note (2026-05-27)
- Readiness review completed: `docs/security/retrieval_path_readiness_review.md`.
- Next live patch scope is limited to monitor-only integration.
- Enforce mode remains explicit no-go pending separate evidence-backed approval.
\n\n## Step 17E Update (2026-05-27)\n- Added first live retrieval monitor-only hook at  after existing retrieval guard result handling.\n- Mode is disabled by default (), and monitor_only is the only live-enabled behavior for this step.\n- Enforce mode remains NO-GO and is not wired into live retrieval path.\n- Hook is non-blocking, non-filtering, fail-open for telemetry errors, and preserves retrieval response unchanged.\n

## Step 17E Update (2026-05-27)
- Added first live retrieval monitor-only hook at `backend/onyx/context/search/retrieval/search_runner.py` after existing retrieval guard result handling.
- Mode is disabled by default (`default_retrieval_integration_config`), and monitor_only is the only live-enabled behavior for this step.
- Enforce mode remains NO-GO and is not wired into live retrieval path.
- Hook is non-blocking, non-filtering, fail-open for telemetry errors, and preserves retrieval response unchanged.
