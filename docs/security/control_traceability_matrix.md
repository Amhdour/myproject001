# Control Traceability Matrix (Step 6)

Status: Planning artifact only; no controls implemented.

| Risk ID | Requirement ID | Patch Points | Planned Controls | Tests | Demo Attacks | Evidence Files | Status |
|---|---|---|---|---|---|---|---|
| R-001 | SR-RET-001, SR-VEC-001, SR-CACHE-001 | PP-RET-01/02, PP-VEC-01, PP-CACHE-01 | ACL filter enforcement + tenant partitioning | Retrieval isolation integration tests | Cross-tenant query attempt | docs/security/evidence/requirements_risk_traceability/traceability_summary.md | Draft |
| R-002 | SR-TOOL-001, SR-APPROVAL-001 | PP-TOOL-01/02, PP-APPROVAL-01 | Tool policy enforcement and approval gate | Authorization deny/allow tests | Unauthorized tool call simulation | docs/security/evidence/requirements_risk_traceability/traceability_summary.md | Draft |
| R-003 | SR-MCP-001, SR-AUDIT-001 | PP-MCP-01/02, PP-AUDIT-01 | Capability-bound MCP invocation | MCP confused deputy tests | Delegated privilege misuse scenario | docs/security/evidence/requirements_risk_traceability/traceability_summary.md | Draft |
| R-004 | SR-PROMPT-001, SR-RET-001 | PP-PROMPT-01/02, PP-RET-01 | Prompt trust segmentation | Prompt-injection red-team tests | Retrieved content override attempt | docs/security/evidence/requirements_risk_traceability/traceability_summary.md | Draft |
| R-005 | SR-ING-001, SR-DLP-001 | PP-ING-01/02, PP-DLP-01 | Ingestion provenance checks | Connector ingestion validation tests | Poisoned document injection | docs/security/evidence/requirements_risk_traceability/traceability_summary.md | Draft |
| R-006 | SR-ART-001, SR-DLP-001 | PP-ART-01, PP-DLP-01 | Artifact secret scan policy | Seeded secret detection tests | Artifact exfiltration simulation | docs/security/evidence/requirements_risk_traceability/traceability_summary.md | Draft |
| R-007 | SR-SBX-001, SR-APPROVAL-001 | PP-SBX-01/02, PP-APPROVAL-01 | Sandboxed command policy | Sandbox command restriction tests | Escape/breakout attempt | docs/security/evidence/requirements_risk_traceability/traceability_summary.md | Draft |
| R-008 | SR-AUDIT-001, SR-EVIDENCE-001 | PP-AUDIT-01/02, PP-EVIDENCE-01 | Structured audit event framework | Audit coverage tests | Missing-log forensic replay | docs/security/evidence/requirements_risk_traceability/traceability_summary.md | Draft |
| R-009 | SR-ADMIN-001, SR-APPROVAL-001 | PP-ADMIN-01, PP-APPROVAL-01 | Privileged action controls | Admin role boundary tests | Unauthorized admin mutation | docs/security/evidence/requirements_risk_traceability/traceability_summary.md | Draft |
| R-010 | SR-CACHE-001, SR-RET-001 | PP-CACHE-01, PP-RET-02 | ACL versioned cache invalidation | Stale permission regression tests | Post-revoke access attempt | docs/security/evidence/requirements_risk_traceability/traceability_summary.md | Draft |
| R-011 | SR-MODEL-001 | PP-MODEL-01 | Provider/model allowlist policy | Route policy enforcement tests | Unapproved provider route attempt | docs/security/evidence/requirements_risk_traceability/traceability_summary.md | Draft |
| R-012 | SR-APPROVAL-001, SR-EVIDENCE-001 | PP-APPROVAL-01, PP-EVIDENCE-01 | Mandatory approvals with immutable logs | Approval bypass tests | Direct-execution bypass attempt | docs/security/evidence/requirements_risk_traceability/traceability_summary.md | Draft |
| R-013 | SR-VEC-001, SR-RET-001 | PP-VEC-01/02, PP-RET-01 | Namespace/metadata query guardrails | Namespace bypass tests | Filter-stripping query scenario | docs/security/evidence/requirements_risk_traceability/traceability_summary.md | Draft |
| R-014 | SR-ING-001, SR-RET-001 | PP-ING-02, PP-RET-02 | Permission reconciliation checks | Connector entitlement sync tests | Source permission drift simulation | docs/security/evidence/requirements_risk_traceability/traceability_summary.md | Draft |
| R-015 | SR-EVIDENCE-001, SR-CI-001 | PP-EVIDENCE-01, PP-CI-01 | Launch evidence gates | Readiness gate completeness checks | Unsupported readiness claim review | docs/security/evidence/requirements_risk_traceability/traceability_summary.md | Draft |
| R-016 | SR-CI-001, SR-EVIDENCE-001 | PP-CI-01, PP-EVIDENCE-01 | Baseline dependency restoration plan | Baseline rerun once dependency available | N/A (blocker tracking) | docs/security/evidence/requirements_risk_traceability/prerequisite_check.txt | Open blocker |
| R-017 | SR-EVIDENCE-001 | PP-EVIDENCE-01 | Remote verification fallback process | Git remote/fetch verification check | N/A (environment limitation) | docs/security/evidence/requirements_risk_traceability/remote_sync_limitation.txt | Open limitation |

## Step 9 Fixture/Test-Data Coverage (Planned)
| Risk ID | Planned Fixture Coverage |
|---|---|
| R-001 | FX-TENANT-001, FX-USER-001, FX-XTENANT-001 |
| R-002 | FX-TOOL-001, FX-UNAUTH-TOOL-001, FX-APPROVAL-001 |
| R-003 | FX-MCPSRV-001, FX-MCPRES-001, FX-UNAUTH-MCP-001 |
| R-004 | FX-PROMPT-001, FX-POISONCHUNK-001 |
| R-005 | FX-CONN-001, FX-DOC-001, FX-MALDOC-001 |
| R-006 | FX-ART-001, FX-SECRETA-001 |
| R-007 | FX-SBXCFG-001, FX-POLICY-001 |
| R-008 | FX-AUDIT-001 |
| R-009 | FX-ADMIN-001, FX-ROLE-001 |
| R-010 | FX-ACL-001, FX-CACHE-001, FX-STALEACL-001, FX-EXPACL-001 |
| R-011 | FX-MODEL-001 |
| R-012 | FX-APPROVAL-001, FX-APPBYPASS-001 |
| R-013 | FX-VNS-001, FX-EMBED-001, FX-CHUNK-001, FX-POISONCHUNK-001 |
| R-014 | FX-GROUP-001, FX-DELDOC-001 |
| R-015 | FX-FINDING-001 |
| R-016 | N/A (dependency blocker tracking) |
| R-017 | N/A (remote verification limitation tracking) |

Reference artifact: `docs/security/test_data_factories.md`.


| R-MIG-001 | SR-RET-001, SR-ADMIN-001, SR-CI-001 | PP-RET-02, PP-ADMIN-01, PP-CI-01 | Existing-data migration integrity safeguards (planned) | Existing DB migration test; seed users/documents/ACL checks | Data-corruption migration simulation | docs/security/evidence/migration_safety/migration_risk_traceability.md | Planned |
| R-MIG-002 | SR-CI-001, SR-EVIDENCE-001 | PP-CI-01, PP-EVIDENCE-01 | Rollback readiness and validation gates (planned) | Migration rollback test | Failed-migration rollback drill | docs/security/evidence/migration_safety/migration_risk_traceability.md | Planned |
| R-MIG-003 | SR-RET-001, SR-CI-001, SR-EVIDENCE-001 | PP-RET-01, PP-CI-01, PP-EVIDENCE-01 | Schema-drift detection and blocker policy (planned) | Schema drift detection check | Drift-induced ACL bypass simulation | docs/security/evidence/migration_safety/migration_risk_traceability.md | Planned |
| R-MIG-004 | SR-ADMIN-001, SR-CI-001, SR-EVIDENCE-001 | PP-ADMIN-01, PP-CI-01, PP-EVIDENCE-01 | Seed/demo environment isolation checks (planned) | Seed tenants/users/documents/ACL/tools/MCP/demo-attacks checks | Seed leakage simulation | docs/security/evidence/migration_safety/migration_risk_traceability.md | Planned |
| R-MIG-005 | SR-EVIDENCE-001, SR-CI-001 | PP-EVIDENCE-01, PP-CI-01 | Migration evidence completeness gates (planned) | Evidence completeness verification | Missing-evidence gate bypass attempt | docs/security/evidence/migration_safety/migration_risk_traceability.md | Planned |

## Step 11 Policy File Traceability

| Policy File | Risks | Requirements | Patch Points | Future Controls | Planned Tests | Planned Evidence |
|---|---|---|---|---|---|---|
| docs/security/policies/ingestion_policy.yaml | RISK-POLICY-DRIFT; RISK-UNENFORCED-CONTROL | SR-POLICY-SCHEMA-001; SR-TRACEABILITY-001 | PP-POLICY-MODEL; PP-LAUNCH-GATE | Future policy engine ingestion checks | Schema + linkage checks | policy inventory + traceability summary |
| docs/security/policies/retrieval_policy.yaml | RISK-POLICY-DRIFT; RISK-UNENFORCED-CONTROL | SR-POLICY-SCHEMA-001; SR-TRACEABILITY-001 | PP-POLICY-MODEL; PP-LAUNCH-GATE | Future retrieval policy evaluation | Schema + linkage checks | policy inventory + traceability summary |
| docs/security/policies/vector_db_policy.yaml | RISK-POLICY-DRIFT; RISK-UNENFORCED-CONTROL | SR-POLICY-SCHEMA-001; SR-TRACEABILITY-001 | PP-POLICY-MODEL; PP-LAUNCH-GATE | Future vector DB guardrails | Schema + linkage checks | policy inventory + traceability summary |
| docs/security/policies/cache_policy.yaml | RISK-POLICY-DRIFT; RISK-UNENFORCED-CONTROL | SR-POLICY-SCHEMA-001; SR-TRACEABILITY-001 | PP-POLICY-MODEL; PP-LAUNCH-GATE | Future cache policy checks | Schema + linkage checks | policy inventory + traceability summary |
| docs/security/policies/tools_policy.yaml | RISK-POLICY-DRIFT; RISK-UNENFORCED-CONTROL | SR-POLICY-SCHEMA-001; SR-TRACEABILITY-001 | PP-POLICY-MODEL; PP-LAUNCH-GATE | Future tool authorization controls | Schema + linkage checks | policy inventory + traceability summary |
| docs/security/policies/mcp_policy.yaml | RISK-POLICY-DRIFT; RISK-UNENFORCED-CONTROL | SR-POLICY-SCHEMA-001; SR-TRACEABILITY-001 | PP-POLICY-MODEL; PP-LAUNCH-GATE | Future MCP hardening controls | Schema + linkage checks | policy inventory + traceability summary |
| docs/security/policies/artifacts_policy.yaml | RISK-POLICY-DRIFT; RISK-UNENFORCED-CONTROL | SR-POLICY-SCHEMA-001; SR-TRACEABILITY-001 | PP-POLICY-MODEL; PP-LAUNCH-GATE | Future artifact safety controls | Schema + linkage checks | policy inventory + traceability summary |
| docs/security/policies/sandbox_policy.yaml | RISK-POLICY-DRIFT; RISK-UNENFORCED-CONTROL | SR-POLICY-SCHEMA-001; SR-TRACEABILITY-001 | PP-POLICY-MODEL; PP-LAUNCH-GATE | Future sandbox constraints | Schema + linkage checks | policy inventory + traceability summary |
| docs/security/policies/approvals_policy.yaml | RISK-POLICY-DRIFT; RISK-UNENFORCED-CONTROL | SR-POLICY-SCHEMA-001; SR-TRACEABILITY-001 | PP-POLICY-MODEL; PP-LAUNCH-GATE | Future approval gates | Schema + linkage checks | policy inventory + traceability summary |
| docs/security/policies/admin_policy.yaml | RISK-POLICY-DRIFT; RISK-UNENFORCED-CONTROL | SR-POLICY-SCHEMA-001; SR-TRACEABILITY-001 | PP-POLICY-MODEL; PP-LAUNCH-GATE | Future admin operation controls | Schema + linkage checks | policy inventory + traceability summary |
| docs/security/policies/audit_policy.yaml | RISK-POLICY-DRIFT; RISK-UNENFORCED-CONTROL | SR-POLICY-SCHEMA-001; SR-TRACEABILITY-001 | PP-POLICY-MODEL; PP-LAUNCH-GATE | Future audit event requirements | Schema + linkage checks | policy inventory + traceability summary |
| docs/security/policies/model_provider_policy.yaml | RISK-POLICY-DRIFT; RISK-UNENFORCED-CONTROL | SR-POLICY-SCHEMA-001; SR-TRACEABILITY-001 | PP-POLICY-MODEL; PP-LAUNCH-GATE | Future provider controls | Schema + linkage checks | policy inventory + traceability summary |
| docs/security/policies/prompt_policy.yaml | RISK-POLICY-DRIFT; RISK-UNENFORCED-CONTROL | SR-POLICY-SCHEMA-001; SR-TRACEABILITY-001 | PP-POLICY-MODEL; PP-LAUNCH-GATE | Future prompt safety controls | Schema + linkage checks | policy inventory + traceability summary |
| docs/security/policies/dlp_policy.yaml | RISK-POLICY-DRIFT; RISK-UNENFORCED-CONTROL | SR-POLICY-SCHEMA-001; SR-TRACEABILITY-001 | PP-POLICY-MODEL; PP-LAUNCH-GATE | Future DLP checks | Schema + linkage checks | policy inventory + traceability summary |
| docs/security/policies/launch_gate_policy.yaml | RISK-POLICY-DRIFT; RISK-UNENFORCED-CONTROL | SR-POLICY-SCHEMA-001; SR-TRACEABILITY-001 | PP-POLICY-MODEL; PP-LAUNCH-GATE | Future launch gate control | Schema + linkage checks | policy inventory + traceability summary |
| docs/security/policies/default_deny_policy.yaml | RISK-POLICY-DRIFT; RISK-UNENFORCED-CONTROL | SR-POLICY-SCHEMA-001; SR-TRACEABILITY-001 | PP-POLICY-MODEL; PP-LAUNCH-GATE | Global baseline deny behavior | Schema + linkage checks | policy inventory + traceability summary |
| R-PE-001 | SR-POL-001 | PP-AUDIT-01 | Policy schema+validator strictness for engine startup | PE-T-001..PE-T-006, PE-T-018 | Invalid policy acceptance simulation | docs/security/evidence/policy_engine_design/policy_engine_traceability_summary.md | Planned |
| R-PE-002 | SR-POL-001, SR-APPROVAL-001 | PP-AUDIT-01 | Default-deny and context-required decision logic | PE-T-007..PE-T-011 | Default-deny bypass simulation | docs/security/evidence/policy_engine_design/policy_engine_traceability_summary.md | Planned |
| R-PE-003 | SR-POL-001 | PP-AUDIT-01 | Fail-closed failure-mode handling | PE-T-014, PE-T-018, PE-T-019 | Engine failure fail-open simulation | docs/security/evidence/policy_engine_design/policy_engine_traceability_summary.md | Planned |
| R-PE-004 | SR-AUDIT-001, SR-POL-001 | PP-AUDIT-01, PP-AUDIT-02 | Policy decision audit/event recording | PE-T-012, PE-T-015, PE-T-017 | Missing audit trail simulation | docs/security/evidence/policy_engine_design/policy_engine_traceability_summary.md | Planned |
| R-PE-005 | SR-POL-001, SR-CI-001 | PP-CI-01, PP-EVIDENCE-01 | Policy version/hash drift detection and replay checks | PE-T-013, PE-T-016, PE-T-020, PE-T-021 | Policy drift regression simulation | docs/security/evidence/policy_engine_design/policy_engine_traceability_summary.md | Planned |

## Step 13A Runtime Context Wrapper Traceability (Planned)

| Control ID | Requirement(s) | Risk(s) | Patch Point(s) | Planned Artifact |
|---|---|---|---|---|
| CTX-WRAP-01 Request/Tenant/Subject context completeness | SR-RET-001, SR-AUDIT-001 | R-WRAP-001 | PP-RET-01 | docs/security/runtime_context_wrappers.md |
| CTX-WRAP-02 Fail-closed wrapper contract | SR-RET-001 | R-WRAP-002 | PP-RET-01, PP-SBX-01 | docs/security/runtime_context_wrappers.md |
| CTX-WRAP-03 Safe denial handling | SR-RET-001, SR-TOOL-001 | R-WRAP-003 | PP-RET-01, PP-TOOL-01 | docs/security/runtime_context_wrappers.md |
| CTX-WRAP-04 Audit/finding/metric emissions | SR-AUDIT-001, SR-EVIDENCE-001 | R-WRAP-004 | PP-AUDIT-01, PP-EVIDENCE-01 | docs/security/runtime_context_wrappers_test_plan.md |
| CTX-WRAP-05 Wrapper-to-patch-point coverage | SR-RET-001, SR-VEC-001, SR-CACHE-001, SR-TOOL-001 | R-WRAP-005 | PP-RET-01, PP-VEC-01, PP-CACHE-01, PP-TOOL-01 | docs/security/runtime_context_wrappers.md |

## Step 14A Safe Denial Behavior Traceability Addendum

| Control / Requirement | Risks | Patch Points | Planned Tests | Evidence Artifacts | Status |
|---|---|---|---|---|---|
| SR-DENY-001 Safe denial response standardization | R-DENY-001, R-DENY-002, R-DENY-003, R-DENY-004, R-DENY-005 | PP-DENY-01, PP-DENY-02, PP-DENY-03 | T-DENY-001..T-DENY-024 | docs/security/evidence/safe_denial_behavior_design/denial_category_inventory.md; docs/security/evidence/safe_denial_behavior_design/safe_denial_traceability_summary.md | planned |

## Step 15A Secure Ingestion Traceability Additions

| Control/Stage | Requirement(s) | Risk(s) | Patch Point(s) | Planned Test(s) | Evidence |
|---|---|---|---|---|---|
| Secure ingestion staged controls (SI-01..SI-17) | SR-ING-001, SR-AUDIT-001, SR-DLP-001 | R-ING-001..R-ING-010 | PP-ING-01, PP-ING-02, PP-AUDIT-01, PP-AUDIT-02, PP-DLP-01 | SITP-001..SITP-026 | docs/security/evidence/secure_ingestion_design/ |
| Tenant boundary + ownership + ACL staging | SR-ING-001 | R-ING-001, R-ING-004, R-ING-008 | PP-ING-02 | SITP-003, SITP-004, SITP-008, SITP-009, SITP-015 | secure_ingestion_traceability_summary.md |
| Content/size/provenance admission staging | SR-ING-001 | R-ING-005, R-ING-006, R-ING-007 | PP-ING-01 | SITP-005, SITP-006, SITP-007, SITP-018, SITP-019 | ingestion_stage_inventory.md |

## Step 16A Retrieval ACL Traceability Rows

| Control ID | Requirement IDs | Risk IDs | Patch Points | Design/Test Artifact |
|---|---|---|---|---|
| RACL-01..RACL-04 (request + subject/tenant/scope validation) | SR-RET-001 | R-RET-001 | PP-RET-01 | docs/security/retrieval_acl.md, RET-ACL-T001..T006 |
| RACL-05..RACL-07 (source/doc/chunk ACL) | SR-RET-001 | R-RET-002, R-RET-005, R-RET-009 | PP-RET-02 | docs/security/retrieval_acl.md, RET-ACL-T003..T008, T018 |
| RACL-08..RACL-09 (vector namespace/metadata) | SR-VEC-001, SR-RET-001 | R-RET-003 | PP-VEC-01, PP-VEC-02 | docs/security/retrieval_acl.md, RET-ACL-T009..T010 |
| RACL-10..RACL-14 (hybrid/rerank/citation/context/prompt) | SR-RET-001, SR-PROMPT-001 | R-RET-006, R-RET-007, R-RET-010 | PP-RET-02, PP-PROMPT-01 | docs/security/retrieval_acl.md, RET-ACL-T011..T015 |
| RACL-15 (cache authorization) | SR-CACHE-001, SR-RET-001 | R-RET-008, R-RET-004 | PP-CACHE-01, PP-RET-02 | docs/security/retrieval_acl.md, RET-ACL-T016..T017 |
| RACL-16..RACL-17 (audit/findings/metrics) | SR-AUDIT-001, SR-EVIDENCE-001 | R-RET-004, R-RET-009 | PP-AUDIT-01, PP-AUDIT-02, PP-EVIDENCE-01 | docs/security/retrieval_acl.md, RET-ACL-T019..T025 |

| R-RPATCH-001 | SR-RET-001 | PP-RET-01, PP-RET-02 | Retrieval path patch completeness planning | RPT-001, RPT-006, RPT-007 | Missing-hook simulation | docs/security/evidence/retrieval_path_patching_design/retrieval_path_traceability_summary.md | Planned |
| R-RPATCH-002 | SR-RET-001, SR-PROMPT-001 | PP-RET-02, PP-PROMPT-01, PP-PROMPT-02 | Behavior-preserving authorization filtering design | RPT-010, RPT-012, RPT-013, RPT-014, RPT-022 | Unintended behavior change simulation | docs/security/evidence/retrieval_path_patching_design/retrieval_path_traceability_summary.md | Planned |
| R-RPATCH-003 | SR-AUDIT-001 | PP-AUDIT-01 | Monitor-only audit completeness design | RPT-004, RPT-016 | Missing monitor audit simulation | docs/security/evidence/retrieval_path_patching_design/retrieval_path_traceability_summary.md | Planned |
| R-RPATCH-004 | SR-AUDIT-001, SR-EVIDENCE-001 | PP-AUDIT-02, PP-EVIDENCE-01 | Shadow-deny drift detection design | RPT-005, RPT-017, RPT-018 | Undetected shadow drift simulation | docs/security/evidence/retrieval_path_patching_design/retrieval_path_traceability_summary.md | Planned |
| R-RPATCH-005 | SR-CI-001 | PP-CI-01 | Rollback safety planning | RPT-021 | Failed rollback drill | docs/security/evidence/retrieval_path_patching_design/retrieval_path_traceability_summary.md | Planned |
| R-RPATCH-006 | SR-CI-001, SR-RET-001 | PP-CI-01, PP-RET-01 | Feature flag/mode safety planning | RPT-020 | Misconfiguration simulation | docs/security/evidence/retrieval_path_patching_design/retrieval_path_traceability_summary.md | Planned |
| R-RPATCH-007 | SR-RET-001 | PP-RET-01 | Context completeness enforcement planning | RPT-002, RPT-003 | Missing-context simulation | docs/security/evidence/retrieval_path_patching_design/retrieval_path_traceability_summary.md | Planned |
| R-RPATCH-008 | SR-CACHE-001, SR-RET-001 | PP-CACHE-01, PP-RET-02 | Cache ACL revalidation planning | RPT-015 | Cache bypass simulation | docs/security/evidence/retrieval_path_patching_design/retrieval_path_traceability_summary.md | Planned |

## Step 17A Traceability Additions
Mapped controls for R-RPATCH-001 through R-RPATCH-008.

## Step 17B Retrieval Path Integration Traceability Rows

| Control ID | Requirement | Risk | Patch Candidates | Planned Tests | Evidence | Status |
|---|---|---|---|---|---|---|
| CTM-RINT-001 | SR-RET-001 | R-RINT-001 | RPC-005, RPC-011, RPC-014 | RPIT-006, RPIT-011, RPIT-016 | retrieval_path_integration_plan + test evidence | planned |
| CTM-RINT-002 | SR-CI-001 | R-RINT-002 | RPC-001, RPC-002, RPC-017 | RPIT-001, RPIT-014, RPIT-019 | config defaults + CI gate evidence | planned |
| CTM-RINT-003 | SR-RET-001 | R-RINT-003 | RPC-005, RPC-010 | RPIT-006, RPIT-010 | monitor/shadow non-blocking evidence | planned |
| CTM-RINT-004 | SR-EVIDENCE-001 | R-RINT-004 | RPC-011, RPC-013 | RPIT-013 | enforce promotion gate evidence | planned |
| CTM-RINT-005 | SR-EVIDENCE-001 | R-RINT-005 | RPC-015 | RPIT-015 | rollback rehearsal evidence | planned |
| CTM-RINT-006 | SR-RET-001 | R-RINT-006 | RPC-003, RPC-004 | RPIT-002, RPIT-003, RPIT-004, RPIT-005 | context builder evidence | planned |

## Step 18A Retrieval Security Test Traceability
| Control/Test Area | Test Group | Matrix Reference | Status |
|---|---|---|---|
| Tenant/ACL isolation | RST-G01/G04/G05 | `retrieval_security_test_matrix.md` | planned |
| Leakage prevention | RST-G13/G14/G15/G17 | `retrieval_security_test_matrix.md` | planned |
| Mode safety and observability | RST-G16/G18/G19/G20 | `retrieval_security_test_matrix.md` | planned |

## Step 19A Vector DB Security Traceability Rows

| Requirement ID | Risk ID | Control/Design Artifact | Patch Point(s) | Planned Tests | Evidence Artifact |
|---|---|---|---|---|---|
| SR-VEC-001 | R-VEC-001 | vector namespace model + vector_namespace_authorized stage | PP-VEC-01, PP-VEC-02 | VEC-TST-003, VEC-TST-012, VEC-TST-014 | docs/security/evidence/vector_db_security_design/vector_traceability_summary.md |
| SR-VEC-001 | R-VEC-002 | vector metadata validation model + metadata contract | PP-VEC-01, PP-VEC-02 | VEC-TST-007, VEC-TST-013 | docs/security/evidence/vector_db_security_design/vector_metadata_contract_summary.md |
| SR-VEC-001 | R-VEC-003 | ACL snapshot propagation controls | PP-VEC-01, PP-RET-02 | VEC-TST-004, VEC-TST-005 | docs/security/evidence/vector_db_security_design/vector_test_plan_summary.md |
| SR-VEC-001 | R-VEC-004 | stale/deleted candidate handling model | PP-VEC-02, PP-RET-02 | VEC-TST-015, VEC-TST-016 | docs/security/evidence/vector_db_security_design/vector_stage_inventory.md |
| SR-VEC-001 | R-VEC-005 | provenance propagation model | PP-VEC-01, PP-ING-02 | VEC-TST-006, VEC-TST-019 | docs/security/evidence/vector_db_security_design/vector_metadata_contract_summary.md |
| SR-VEC-001 | R-VEC-006 | poisoning marker propagation model | PP-VEC-01, PP-ING-02 | VEC-TST-008, VEC-TST-024 | docs/security/evidence/vector_db_security_design/vector_test_plan_summary.md |
| SR-VEC-001 | R-VEC-007 | prompt-injection marker propagation model | PP-VEC-01, PP-PROMPT-01 | VEC-TST-009 | docs/security/evidence/vector_db_security_design/vector_test_plan_summary.md |
| SR-VEC-001, SR-CACHE-001 | R-VEC-008 | vector cache interaction model | PP-CACHE-01, PP-VEC-02 | VEC-TST-017, VEC-TST-025 | docs/security/evidence/vector_db_security_design/vector_traceability_summary.md |
| SR-VEC-001 | R-VEC-009 | re-embedding authorization continuity model | PP-VEC-01 | VEC-TST-019 | docs/security/evidence/vector_db_security_design/vector_stage_inventory.md |
| SR-VEC-001, SR-AUDIT-001 | R-VEC-010 | safe metadata + safe denial + audit/finding model | PP-VEC-02, PP-AUDIT-01, PP-AUDIT-02 | VEC-TST-023, VEC-TST-026 | docs/security/evidence/vector_db_security_design/vector_traceability_summary.md |

## Step 20A Cache Security Traceability Additions
| Control ID | Requirement | Risk | Patch Point | Design/Test Reference | Status |
|---|---|---|---|---|---|
| CTRL-CACHE-KEY-BIND | SR-CACHE-001 | R-CACHE-001,R-CACHE-002 | PP-CACHE-01 | cache_security.md + cache_key_contract.md + CACHE-001/002 | planned |
| CTRL-CACHE-ACL-BIND | SR-CACHE-001,SR-RET-001 | R-CACHE-003 | PP-CACHE-01,PP-RET-02 | cache_security.md + CACHE-003/009/013 | planned |
| CTRL-CACHE-INVALIDATION | SR-CACHE-001 | R-CACHE-004,R-CACHE-005 | PP-CACHE-01 | cache_security.md + CACHE-010/011 | planned |
| CTRL-CACHE-VECTOR-BOUNDARY | SR-VEC-001 | R-CACHE-006 | PP-VEC-01 | cache_security.md + CACHE-012 | planned |
| CTRL-CACHE-PROMPT-CONTEXT | SR-PROMPT-001 | R-CACHE-007,R-CACHE-008 | PP-PROMPT-01,PP-PROMPT-02 | cache_security.md + CACHE-014/015 | planned |
| CTRL-CACHE-TOOL-BOUNDARY | SR-TOOL-001 | R-CACHE-009 | PP-TOOL-01 | cache_security.md + CACHE-016 | planned |
| CTRL-CACHE-SAFE-METADATA | SR-DLP-001,SR-AUDIT-001 | R-CACHE-010 | PP-DLP-01,PP-AUDIT-01 | cache_key_contract.md + CACHE-019/027 | planned |
