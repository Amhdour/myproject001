# Shadow-Deny Test Plan (Step 25A)

Status: planned

| test ID | purpose | mapped control family | mapped risk | expected result | required evidence | current status |
|---|---|---|---|---|---|---|
| SDP-001 | shadow-deny flag defaults disabled | shared runtime | R-SD-006 | all shadow-deny flags default disabled | test output + config snapshot | planned |
| SDP-002 | shadow-deny cannot block live response | shared runtime | R-SD-001 | live response unaffected | behavior comparison log | planned |
| SDP-003 | shadow-deny cannot filter live response | retrieval/vector/cache/tool/mcp/artifact/ingestion | R-SD-002 | live payload unchanged | diff report | planned |
| SDP-004 | shadow-deny records deny decision separately | audit/finding/metric sink | R-SD-007 | separate decision record emitted | decision schema artifacts | planned |
| SDP-005 | shadow-deny preserves monitor-only behavior | shared runtime | R-SD-001 | monitor-only output unchanged | monitor-only regression evidence | planned |
| SDP-006 | shadow-deny compares against monitor-only decision | shared runtime | R-SD-007 | correlated comparison record present | comparison report | planned |
| SDP-007 | shadow-deny safe denial output is non-leaking | safe denial shared runtime | R-SD-003 | no sensitive content in deny outputs | non-leakage validation report | planned |
| SDP-008 | shadow-deny audit event emitted | audit sink | R-SD-007 | audit event with correlation IDs | audit log extract | planned |
| SDP-009 | shadow-deny finding emitted | finding sink | R-SD-004 | finding created for deny-only divergence | finding artifact | planned |
| SDP-010 | shadow-deny metric emitted | metric sink | R-SD-007 | metric counters/tags emitted | metric artifact | planned |
| SDP-011 | shadow-deny false-positive review recorded | approval/review process | R-SD-004 | FP review record exists | review ticket evidence | planned |
| SDP-012 | shadow-deny rollback flag disables decision recording | rollback workflow | R-SD-005 | no new decision records post-rollback | rollback evidence | planned |
| SDP-013 | retrieval shadow-deny simulation only | Retrieval ACL | R-SD-001 | simulated deny, no live effect | family test report | planned |
| SDP-014 | vector shadow-deny simulation only | Vector DB security | R-SD-001 | simulated deny, no live effect | family test report | planned |
| SDP-015 | cache shadow-deny simulation only | Cache security | R-SD-002 | simulated deny, no live effect | family test report | planned |
| SDP-016 | tool shadow-deny simulation only | Tool authorization | R-SD-001 | simulated deny, no live effect | family test report | planned |
| SDP-017 | MCP shadow-deny simulation only | MCP hardening | R-SD-001 | simulated deny, no live effect | family test report | planned |
| SDP-018 | artifact shadow-deny simulation only | Artifact safety | R-SD-002 | simulated deny, no live effect | family test report | planned |
| SDP-019 | ingestion shadow-deny simulation only | Secure ingestion | R-SD-002 | simulated deny, no live effect | family test report | planned |
| SDP-020 | enforce mode remains disabled | shared runtime | R-SD-008 | enforce flag remains disabled | runtime flag snapshot | planned |
| SDP-021 | production behavior remains unchanged | all families | R-SD-001,R-SD-002 | no behavior delta in production path | no-change attestation | planned |

## Step 25B Status
- Isolated simulation tests implemented under backend/security_layer/tests.

## Step 25C - Shadow-Deny Simulation Validation (2026-05-28)

- Completed validation on branch `shadow-deny-simulation-validation`.
- Evidence folder: `docs/security/evidence/shadow_deny_simulation_validation/`.
- Focused and full security-layer test suites passed.
- Confirmed simulation-only operation (no enforce mode, no live blocking/filtering, no application behavior change).
