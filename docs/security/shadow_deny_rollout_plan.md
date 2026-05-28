# Shadow-Deny Rollout Plan (Step 25A)

## Purpose
Define a documentation-only, future-state rollout plan for shadow-deny across security control families without changing live behavior.

## Scope
- Planning, documentation, and evidence-only updates.
- No live runtime integration, no blocking/filtering behavior changes, and no production activation.

## Status
**planned only**

## Owner
AI Trust & Security Readiness Engineer

## Non-Claim Statement
This plan does not claim production readiness, control effectiveness, runtime activation, or enforce-mode eligibility.

## Relationship to Monitor-Only
Shadow-deny is modeled as an additive simulated decision stream compared against existing monitor-only decisions; monitor-only remains authoritative for current observation.

## Relationship to Enforce Mode
Enforce mode remains blocked/inactive. Shadow-deny planning is a prerequisite stage and does not authorize enforce mode.

## Relationship to Cross-Control Readiness
This plan consumes readiness artifacts from Step 24A/24B/24C and defines additional gates before any future activation consideration.

## Relationship to Evidence Validation
All shadow-deny outcomes must be evidenced through audit/finding/metric artifacts and validation records before gate progression.

## Shadow-Deny Definition
Shadow-deny is a non-live, simulation-only denial evaluation path that records what would have been denied, while leaving live responses unchanged.

## What Shadow-Deny May Do
- Compute simulated deny decisions.
- Emit planned audit/finding/metric records in isolated evidence pathways.
- Compare decisions with monitor-only outputs.
- Support false-positive review and rollback rehearsal records.

## What Shadow-Deny Must Not Do
- Block live traffic.
- Filter live results.
- Alter prompt/context assembly or retrieval output.
- Enable enforce mode.
- Claim production readiness.

## Current Shadow-Deny Status
inactive/blocked

## Required Prerequisites Before Activation
- Monitor-only evidence complete and validated.
- Feature-flag inventory and defaults documented.
- Rollback workflow documented and tested in dry-run.
- CI and staging dry-run evidence complete.
- False-positive review process complete.

## Required Feature Flags
See `docs/security/shadow_deny_feature_flags.md`.

## Required Rollout Gates
See `docs/security/shadow_deny_rollout_gates.md`.

## Required Telemetry
- Decision count by control family and decision_status.
- Comparison drift rate between monitor-only and shadow-deny.
- Non-leakage validation pass rate.
- Rollback-flag activation events.

## Required Audit/Finding/Metric Evidence
- Audit event linkage per decision record.
- Finding IDs for suspect deny logic.
- Metrics for deny simulation distribution and FP review outcomes.

## Required Rollback Plan
Rollback requires disabling top-level and per-family shadow-deny flags and decision recording flags; rollback proof must show immediate reversion to monitor-only-only behavior.

## Safe Denial Expectations
All simulated deny outputs must use safe denial categories with no sensitive payload leakage.

## Non-Leakage Expectations
No raw prompt/context/document/tool secrets in decision records or denial categories.

## Fail-Open/Fail-Closed Expectations
Planned default is fail-open for live behavior; simulated decision pipeline may fail-closed internally only for recording integrity while keeping live path unaffected.

## Control-Family Rollout Order
1. Safe denial shared runtime
2. Audit/finding/metric shared sink
3. Retrieval ACL
4. Vector DB security
5. Cache security
6. Tool authorization
7. MCP hardening
8. Artifact safety
9. Secure ingestion

## Dry-Run Decision Recording Model
Dry-run records each simulated decision with correlation IDs to monitor-only and evidence refs; no live action is applied.

## Monitor-Only Comparison Model
Pair each shadow-deny decision to a monitor-only decision ID and calculate divergence classes: match, deny-only, monitor-only-only, inconclusive.

## False-Positive Review Model
All deny-only divergences above threshold require triage ticket, reviewer assignment, and closure reason before gate progression.

## Approval Workflow
Security engineering reviewer -> platform owner -> release approver. Approval is required at SD-10 and does not auto-enable runtime flags.

## Rollback Workflow
Trigger rollback flag, disable family flags, disable decision recording, validate no new shadow-deny records, archive rollback evidence.

## Incident Response Expectations
Unexpected shadow-deny side effects (including any live influence) require immediate rollback workflow execution and incident evidence capture.

## Production-Readiness Non-Claim
Completion of this plan does not indicate production readiness.

## Known Limitations
- Remote/main verification may be limited by environment connectivity.
- Monitor-only evidence coverage is incomplete for activation.
- Staging dry-run evidence not yet complete.

## Control Family Readiness Table
| control family name | current status | monitor-only status | shadow-deny readiness | required prerequisites | required feature flag | decision recording requirement | allowed behavior | forbidden behavior | rollback requirement | required tests | required evidence | readiness decision |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Retrieval ACL | isolated controls exist | limited live hook | planning only | SD-1..SD-9 | RETRIEVAL_SHADOW_DENY_ENABLED | required via decision schema | simulation + record | live blocking/filtering | disable family + global flags | SDP-013, SDP-001..006 | gate + test artifacts | blocked pending monitor-only evidence |
| Vector DB security | isolated controls exist | limited | planning only | SD-1..SD-9 | VECTOR_SHADOW_DENY_ENABLED | required | simulation + record | live blocking/filtering | disable family + global flags | SDP-014 | gate + test artifacts | blocked pending CI/staging evidence |
| Cache security | isolated controls exist | limited | planning only | SD-1..SD-9 | CACHE_SHADOW_DENY_ENABLED | required | simulation + record | live blocking/filtering | disable family + global flags | SDP-015 | gate + test artifacts | blocked pending feature flags |
| Tool authorization | isolated controls exist | limited | planning only | SD-1..SD-9 | TOOL_SHADOW_DENY_ENABLED | required | simulation + record | live blocking/filtering | disable family + global flags | SDP-016 | gate + test artifacts | blocked pending rollback evidence |
| MCP hardening | isolated controls exist | limited | planning only | SD-1..SD-9 | MCP_SHADOW_DENY_ENABLED | required | simulation + record | live blocking/filtering | disable family + global flags | SDP-017 | gate + test artifacts | blocked pending CI/staging evidence |
| Artifact safety | isolated controls exist | limited | planning only | SD-1..SD-9 | ARTIFACT_SHADOW_DENY_ENABLED | required | simulation + record | live blocking/filtering | disable family + global flags | SDP-018 | gate + test artifacts | blocked pending monitor-only evidence |
| Secure ingestion | isolated controls exist | limited | planning only | SD-1..SD-9 | INGESTION_SHADOW_DENY_ENABLED | required | simulation + record | live blocking/filtering | disable family + global flags | SDP-019 | gate + test artifacts | blocked pending monitor-only evidence |
| Safe denial shared runtime | design/minimal isolated components exist | n/a | planning only | SD-2..SD-6 | SECURITY_SHADOW_DENY_ENABLED | required | categorize simulated denial safely | denial leakage | disable global flags | SDP-007, SDP-004, SDP-005 | non-leakage evidence | ready for future shadow-deny planning only |
| Audit/finding/metric shared sink | isolated evidence patterns exist | monitor-only emits partial evidence | planning only | SD-1..SD-7 | SHADOW_DENY_DECISION_RECORDING_ENABLED | required | record-only emissions | missing correlation or raw data leakage | disable recording flag | SDP-008, SDP-009, SDP-010 | correlated evidence records | blocked from activation |
