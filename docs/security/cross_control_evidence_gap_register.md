# Cross-Control Evidence Gap Register

| Gap ID | Description | Impacted Controls | Severity | Required Remediation | Required Evidence | Recommended Next Phase | Current Status |
|---|---|---|---|---|---|---|---|
| CEG-001 | missing remote/main verification | all cross-control families | high | restore remote access and verify lineage | fetch log + merge-base proof | next integration readiness cycle | open |
| CEG-002 | missing CI workflow evidence | all families | high | run CI security-layer suite | CI artifacts and statuses | CI security gates phase | open |
| CEG-003 | missing staging deployment evidence | monitor-only candidates | high | run staged deployment validation | staging run report | controlled staging phase | open |
| CEG-004 | missing production-like telemetry sink evidence | retrieval monitor-only + future candidates | medium | validate sink durability/availability | sink SLO report | telemetry hardening phase | open |
| CEG-005 | missing feature-flag evidence | future live integrations | high | document and test flags/defaults | flag matrix + tests | rollout controls phase | open |
| CEG-006 | missing rollback evidence | monitor-only expansion candidates | high | test rollback disable path | rollback drill output | rollout controls phase | open |
| CEG-007 | missing load/performance evidence | retrieval/vector/cache/tool/MCP/artifact candidates | medium | run perf/load tests | benchmark report | non-prod performance phase | open |
| CEG-008 | missing live monitor-only dry-run evidence | non-retrieval candidates | high | execute dry-run in non-prod | dry-run logs | monitor-only expansion phase | open |
| CEG-009 | missing shadow-deny simulation evidence | retrieval/tool/MCP families | medium | create simulation-only tests | simulation reports | shadow-deny planning (still blocked) | open |
| CEG-010 | missing incident-response drill evidence | all families | medium | run tabletop + technical drill | IR drill report | operations readiness phase | open |
| CEG-011 | missing backup/restore evidence | telemetry/evidence stores | medium | validate backup/restore | restore drill logs | operations readiness phase | open |
| CEG-012 | missing external validation evidence | all families | low | independent review/audit | assessor report | pre-launch governance phase | open |
