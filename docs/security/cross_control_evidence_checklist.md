# Cross-Control Evidence Checklist

## Sections
- design docs present
- implementation files present
- validation files present
- test files present
- evidence folders present
- test outputs present
- exit-code files present
- no-live-enforcement statements present
- no-shadow-deny statements present
- no-live-blocking statements present
- known limitations present
- risk register mappings present
- traceability mappings present
- PR readiness notes present

| Checklist ID | Control Family | Required Artifact | Expected Path | Verification Result | Evidence Source | Blocker Status | Remediation Needed |
|---|---|---|---|---|---|---|---|
| CEC-001 | Policy engine | Design doc | docs/security/policy_engine.md | present | local repo | none | none |
| CEC-002 | Runtime wrappers | Implementation files | backend/security_layer/runtime/ | present | local repo | none | none |
| CEC-003 | Safe denial | Validation evidence | docs/security/evidence/safe_denial_validation/ | present | local repo | none | none |
| CEC-004 | Secure ingestion | Test files | backend/security_layer/tests/ingestion/ | present | local repo | none | none |
| CEC-005 | Retrieval ACL | Evidence folder | docs/security/evidence/retrieval_acl_validation/ | present | local repo | none | none |
| CEC-006 | Retrieval monitor-only hook | Test output | docs/security/evidence/cross_control_evidence_hardening/test_output.txt | present after run | Step 24B evidence | none | none |
| CEC-007 | Retrieval security tests | Exit code file | docs/security/evidence/cross_control_evidence_hardening/test_exitcode.txt | present after run | Step 24B evidence | none | none |
| CEC-008 | Vector DB security | No-live-enforcement statement | docs/security/cross_control_no_live_enforcement_attestation.md | present | Step 24B attestation | none | none |
| CEC-009 | Cache security | No-shadow-deny statement | docs/security/cross_control_no_live_enforcement_attestation.md | present | Step 24B attestation | none | none |
| CEC-010 | Tool authorization | No-live-blocking statement | docs/security/cross_control_no_live_enforcement_attestation.md | present | Step 24B attestation | none | none |
| CEC-011 | MCP hardening | Known limitations | docs/security/known_limitations.md | present | limitations update | none | none |
| CEC-012 | Artifact safety | Risk register mapping | docs/security/risk_register.md | present | prior artifact | none | none |
| CEC-013 | Cross-control readiness | Traceability mapping | docs/security/control_traceability_matrix.md | present | prior artifact | none | none |
| CEC-014 | Cross-control readiness | PR readiness note | docs/security/README.md | present | Step 24B update | none | none |
