# Enforce Mode Test Plan (Step 26A)

Status for all tests: **planned**.

| Test ID | Purpose | Mapped control family | Mapped risk | Expected result | Required evidence | Current status |
|---|---|---|---|---|---|---|
| EM-T-001 | enforce flag defaults disabled | Shared/global | R-ENF-001 | enforce remains disabled by default | config evidence + test log | planned |
| EM-T-002 | enforce cannot activate without global approval | Shared/global | R-ENF-001 | activation blocked | gate evidence | planned |
| EM-T-003 | enforce cannot activate without control-family approval | Shared/global | R-ENF-001,R-ENF-010 | activation blocked | approval evidence | planned |
| EM-T-004 | enforce cannot activate without shadow-deny evidence | Shared/global | R-ENF-001,R-ENF-006 | activation blocked | shadow-deny evidence | planned |
| EM-T-005 | enforce cannot activate without rollback flag | Shared/global | R-ENF-004 | activation blocked | rollback flag evidence | planned |
| EM-T-006 | enforce cannot activate without kill switch | Shared/global | R-ENF-004 | activation blocked | kill-switch evidence | planned |
| EM-T-007 | enforce cannot activate without CI evidence | Shared/global | R-ENF-006 | activation blocked | CI evidence | planned |
| EM-T-008 | enforce cannot activate without staging dry-run evidence | Shared/global | R-ENF-006 | activation blocked | staging evidence | planned |
| EM-T-009 | enforce cannot activate without false-positive review | Shared/global | R-ENF-007 | activation blocked | FP review record | planned |
| EM-T-010 | enforce cannot activate if non-leakage tests fail | Safe denial | R-ENF-003 | activation blocked | non-leakage report | planned |
| EM-T-011 | enforce cannot activate if safe-denial tests fail | Safe denial | R-ENF-003 | activation blocked | safe-denial report | planned |
| EM-T-012 | enforce blocks only approved low-risk scenario in future test | Shared/global | R-ENF-002,R-ENF-005 | deny limited to allowlisted case | pilot evidence | planned |
| EM-T-013 | enforce never exposes raw secret/context in denial | Safe denial | R-ENF-003 | no sensitive leakage | denial content evidence | planned |
| EM-T-014 | enforce emits audit event | A/F/M sink | R-ENF-008 | audit emitted for deny | audit evidence | planned |
| EM-T-015 | enforce emits finding | A/F/M sink | R-ENF-008 | finding emitted for deny | finding evidence | planned |
| EM-T-016 | enforce emits metric | A/F/M sink | R-ENF-008 | metric emitted for deny | metric evidence | planned |
| EM-T-017 | enforce rollback disables blocking | Shared/global | R-ENF-004 | blocking disabled after rollback | rollback drill evidence | planned |
| EM-T-018 | enforce kill switch disables blocking | Shared/global | R-ENF-004 | blocking disabled immediately | kill-switch drill evidence | planned |
| EM-T-019 | retrieval enforce future test remains blocked | Retrieval ACL | R-ENF-001 | activation remains blocked | retrieval gate evidence | planned |
| EM-T-020 | vector enforce future test remains blocked | Vector DB security | R-ENF-001 | activation remains blocked | vector gate evidence | planned |
| EM-T-021 | cache enforce future test remains blocked | Cache security | R-ENF-001 | activation remains blocked | cache gate evidence | planned |
| EM-T-022 | tool enforce future test remains blocked | Tool authorization | R-ENF-001 | activation remains blocked | tool gate evidence | planned |
| EM-T-023 | MCP enforce future test remains blocked | MCP hardening | R-ENF-001 | activation remains blocked | MCP gate evidence | planned |
| EM-T-024 | artifact enforce future test remains blocked | Artifact safety | R-ENF-001 | activation remains blocked | artifact gate evidence | planned |
| EM-T-025 | ingestion enforce future test remains blocked | Secure ingestion | R-ENF-001 | activation remains blocked | ingestion gate evidence | planned |
| EM-T-026 | production behavior remains unchanged now | All families | R-ENF-001..R-ENF-010 | no behavior change in current runtime | regression + no-change evidence | planned |
