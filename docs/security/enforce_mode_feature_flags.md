# Enforce Mode Feature Flags (Step 26A)

All flags are **planned only** and default-disabled.

| Flag name | Purpose | Default value | Allowed values | Owner | Activation gate | Rollback behavior | Required tests | Current implementation status |
|---|---|---|---|---|---|---|---|---|
| SECURITY_ENFORCE_MODE_ENABLED | Global future enforce switch | disabled | disabled/enabled | Security readiness owner | EM-12 | set disabled to stop enforce | EM-T-001..003 | planned only |
| RETRIEVAL_ENFORCE_ENABLED | Future retrieval enforce | disabled | disabled/enabled | Retrieval control owner | EM-12 + family approval | disable retrieval enforce path | EM-T-019 | planned only |
| VECTOR_ENFORCE_ENABLED | Future vector enforce | disabled | disabled/enabled | Vector control owner | EM-12 + family approval | disable vector enforce path | EM-T-020 | planned only |
| CACHE_ENFORCE_ENABLED | Future cache enforce | disabled | disabled/enabled | Cache control owner | EM-12 + family approval | disable cache enforce path | EM-T-021 | planned only |
| TOOL_ENFORCE_ENABLED | Future tool enforce | disabled | disabled/enabled | Tool control owner | EM-12 + family approval | disable tool enforce path | EM-T-022 | planned only |
| MCP_ENFORCE_ENABLED | Future MCP enforce | disabled | disabled/enabled | MCP control owner | EM-12 + family approval | disable MCP enforce path | EM-T-023 | planned only |
| ARTIFACT_ENFORCE_ENABLED | Future artifact enforce | disabled | disabled/enabled | Artifact control owner | EM-12 + family approval | disable artifact enforce path | EM-T-024 | planned only |
| INGESTION_ENFORCE_ENABLED | Future ingestion enforce | disabled | disabled/enabled | Ingestion control owner | EM-12 + family approval | disable ingestion enforce path | EM-T-025 | planned only |
| ENFORCE_APPROVAL_GATE_ENABLED | Require approval gate checks | disabled | disabled/enabled | Security governance owner | EM-3 | disable returns to monitor-only | EM-T-002..003 | planned only |
| ENFORCE_ROLLBACK_ENABLED | Enables rollback workflow | disabled | disabled/enabled | Ops owner | EM-4 | if disabled, activation blocked | EM-T-005, EM-T-017 | planned only |
| ENFORCE_KILL_SWITCH_ENABLED | Enables emergency disable | disabled | disabled/enabled | Ops owner | EM-4 | immediate disable when switched | EM-T-006, EM-T-018 | planned only |
| ENFORCE_BLAST_RADIUS_LIMIT_ENABLED | Enforces pilot scope constraints | disabled | disabled/enabled | Security + SRE | EM-4, EM-9 | disable enforce if limit checks unavailable | EM-T-012 | planned only |
| ENFORCE_SAFE_DENIAL_REQUIRED | Requires safe-denial pass before enforce | disabled | disabled/enabled | Safe denial owner | EM-5, EM-6 | disable activation on safe-denial mismatch | EM-T-010, EM-T-011, EM-T-013 | planned only |
| ENFORCE_TELEMETRY_REQUIRED | Requires audit/finding/metric emission | disabled | disabled/enabled | Observability owner | EM-7 | disable activation if telemetry missing | EM-T-014..016 | planned only |
