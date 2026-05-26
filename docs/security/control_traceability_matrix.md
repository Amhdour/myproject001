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
