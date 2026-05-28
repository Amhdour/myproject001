# Shadow-Deny Feature Flags (Step 25A)

Status: planned only
Owner: AI Trust & Security Readiness Engineer
Default for all flags: disabled

| flag name | purpose | default value | allowed values | owner | rollout gate | rollback behavior | required tests | current implementation status |
|---|---|---|---|---|---|---|---|---|
| SECURITY_SHADOW_DENY_ENABLED | global shadow-deny master switch | disabled | disabled/enabled | AI Trust & Security Readiness Engineer | SD-2,SD-10 | set disabled | SDP-001,SDP-020 | planned only |
| RETRIEVAL_SHADOW_DENY_ENABLED | retrieval family simulation control | disabled | disabled/enabled | same | SD-2 | set disabled | SDP-013 | planned only |
| VECTOR_SHADOW_DENY_ENABLED | vector family simulation control | disabled | disabled/enabled | same | SD-2 | set disabled | SDP-014 | planned only |
| CACHE_SHADOW_DENY_ENABLED | cache family simulation control | disabled | disabled/enabled | same | SD-2 | set disabled | SDP-015 | planned only |
| TOOL_SHADOW_DENY_ENABLED | tool family simulation control | disabled | disabled/enabled | same | SD-2 | set disabled | SDP-016 | planned only |
| MCP_SHADOW_DENY_ENABLED | MCP family simulation control | disabled | disabled/enabled | same | SD-2 | set disabled | SDP-017 | planned only |
| ARTIFACT_SHADOW_DENY_ENABLED | artifact family simulation control | disabled | disabled/enabled | same | SD-2 | set disabled | SDP-018 | planned only |
| INGESTION_SHADOW_DENY_ENABLED | ingestion family simulation control | disabled | disabled/enabled | same | SD-2 | set disabled | SDP-019 | planned only |
| SHADOW_DENY_DECISION_RECORDING_ENABLED | decision record emission | disabled | disabled/enabled | same | SD-6 | set disabled | SDP-004,SDP-012 | planned only |
| SHADOW_DENY_COMPARE_MONITOR_ONLY_ENABLED | comparison mode records | disabled | disabled/enabled | same | SD-1,SD-6 | set disabled | SDP-006 | planned only |
| SHADOW_DENY_FAIL_OPEN_ENABLED | explicit fail-open safety control | disabled | disabled/enabled | same | SD-5 | set disabled | SDP-002,SDP-003 | planned only |
| SHADOW_DENY_ROLLBACK_ENABLED | rollback operation toggle | disabled | disabled/enabled | same | SD-3 | set disabled after rollback complete | SDP-012 | planned only |
