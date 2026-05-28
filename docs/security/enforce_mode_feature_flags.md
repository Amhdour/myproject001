# Enforce-Mode Feature Flags

All flags are planned only and default disabled. They must not enable runtime behavior in this step.

## SECURITY_ENFORCE_MODE_ENABLED
- Flag name: `SECURITY_ENFORCE_MODE_ENABLED`
- Purpose: Planned enforce-mode readiness control for future isolated approval gates.
- Default value: disabled
- Allowed values: disabled, enabled
- Owner: Security engineering owner
- Activation gate: EM-3 plus EM-12 and all applicable evidence gates
- Rollback behavior: disabling this flag or using the kill switch must force no blocking/no filtering.
- Required tests: default-disabled, invalid value rejection, activation blocked when missing, rollback/kill-switch no-op behavior.
- Current implementation status: planned only.

## RETRIEVAL_ENFORCE_ENABLED
- Flag name: `RETRIEVAL_ENFORCE_ENABLED`
- Purpose: Planned enforce-mode readiness control for future isolated approval gates.
- Default value: disabled
- Allowed values: disabled, enabled
- Owner: Security engineering owner
- Activation gate: EM-3 plus EM-12 and all applicable evidence gates
- Rollback behavior: disabling this flag or using the kill switch must force no blocking/no filtering.
- Required tests: default-disabled, invalid value rejection, activation blocked when missing, rollback/kill-switch no-op behavior.
- Current implementation status: planned only.

## VECTOR_ENFORCE_ENABLED
- Flag name: `VECTOR_ENFORCE_ENABLED`
- Purpose: Planned enforce-mode readiness control for future isolated approval gates.
- Default value: disabled
- Allowed values: disabled, enabled
- Owner: Security engineering owner
- Activation gate: EM-3 plus EM-12 and all applicable evidence gates
- Rollback behavior: disabling this flag or using the kill switch must force no blocking/no filtering.
- Required tests: default-disabled, invalid value rejection, activation blocked when missing, rollback/kill-switch no-op behavior.
- Current implementation status: planned only.

## CACHE_ENFORCE_ENABLED
- Flag name: `CACHE_ENFORCE_ENABLED`
- Purpose: Planned enforce-mode readiness control for future isolated approval gates.
- Default value: disabled
- Allowed values: disabled, enabled
- Owner: Security engineering owner
- Activation gate: EM-3 plus EM-12 and all applicable evidence gates
- Rollback behavior: disabling this flag or using the kill switch must force no blocking/no filtering.
- Required tests: default-disabled, invalid value rejection, activation blocked when missing, rollback/kill-switch no-op behavior.
- Current implementation status: planned only.

## TOOL_ENFORCE_ENABLED
- Flag name: `TOOL_ENFORCE_ENABLED`
- Purpose: Planned enforce-mode readiness control for future isolated approval gates.
- Default value: disabled
- Allowed values: disabled, enabled
- Owner: Security engineering owner
- Activation gate: EM-3 plus EM-12 and all applicable evidence gates
- Rollback behavior: disabling this flag or using the kill switch must force no blocking/no filtering.
- Required tests: default-disabled, invalid value rejection, activation blocked when missing, rollback/kill-switch no-op behavior.
- Current implementation status: planned only.

## MCP_ENFORCE_ENABLED
- Flag name: `MCP_ENFORCE_ENABLED`
- Purpose: Planned enforce-mode readiness control for future isolated approval gates.
- Default value: disabled
- Allowed values: disabled, enabled
- Owner: Security engineering owner
- Activation gate: EM-3 plus EM-12 and all applicable evidence gates
- Rollback behavior: disabling this flag or using the kill switch must force no blocking/no filtering.
- Required tests: default-disabled, invalid value rejection, activation blocked when missing, rollback/kill-switch no-op behavior.
- Current implementation status: planned only.

## ARTIFACT_ENFORCE_ENABLED
- Flag name: `ARTIFACT_ENFORCE_ENABLED`
- Purpose: Planned enforce-mode readiness control for future isolated approval gates.
- Default value: disabled
- Allowed values: disabled, enabled
- Owner: Security engineering owner
- Activation gate: EM-3 plus EM-12 and all applicable evidence gates
- Rollback behavior: disabling this flag or using the kill switch must force no blocking/no filtering.
- Required tests: default-disabled, invalid value rejection, activation blocked when missing, rollback/kill-switch no-op behavior.
- Current implementation status: planned only.

## INGESTION_ENFORCE_ENABLED
- Flag name: `INGESTION_ENFORCE_ENABLED`
- Purpose: Planned enforce-mode readiness control for future isolated approval gates.
- Default value: disabled
- Allowed values: disabled, enabled
- Owner: Security engineering owner
- Activation gate: EM-3 plus EM-12 and all applicable evidence gates
- Rollback behavior: disabling this flag or using the kill switch must force no blocking/no filtering.
- Required tests: default-disabled, invalid value rejection, activation blocked when missing, rollback/kill-switch no-op behavior.
- Current implementation status: planned only.

## ENFORCE_APPROVAL_GATE_ENABLED
- Flag name: `ENFORCE_APPROVAL_GATE_ENABLED`
- Purpose: Planned enforce-mode readiness control for future isolated approval gates.
- Default value: disabled
- Allowed values: disabled, enabled
- Owner: Security engineering owner
- Activation gate: EM-3 plus EM-12 and all applicable evidence gates
- Rollback behavior: disabling this flag or using the kill switch must force no blocking/no filtering.
- Required tests: default-disabled, invalid value rejection, activation blocked when missing, rollback/kill-switch no-op behavior.
- Current implementation status: planned only.

## ENFORCE_ROLLBACK_ENABLED
- Flag name: `ENFORCE_ROLLBACK_ENABLED`
- Purpose: Planned enforce-mode readiness control for future isolated approval gates.
- Default value: disabled
- Allowed values: disabled, enabled
- Owner: Security engineering owner
- Activation gate: EM-3 plus EM-12 and all applicable evidence gates
- Rollback behavior: disabling this flag or using the kill switch must force no blocking/no filtering.
- Required tests: default-disabled, invalid value rejection, activation blocked when missing, rollback/kill-switch no-op behavior.
- Current implementation status: planned only.

## ENFORCE_KILL_SWITCH_ENABLED
- Flag name: `ENFORCE_KILL_SWITCH_ENABLED`
- Purpose: Planned enforce-mode readiness control for future isolated approval gates.
- Default value: disabled
- Allowed values: disabled, enabled
- Owner: Security engineering owner
- Activation gate: EM-3 plus EM-12 and all applicable evidence gates
- Rollback behavior: disabling this flag or using the kill switch must force no blocking/no filtering.
- Required tests: default-disabled, invalid value rejection, activation blocked when missing, rollback/kill-switch no-op behavior.
- Current implementation status: planned only.

## ENFORCE_BLAST_RADIUS_LIMIT_ENABLED
- Flag name: `ENFORCE_BLAST_RADIUS_LIMIT_ENABLED`
- Purpose: Planned enforce-mode readiness control for future isolated approval gates.
- Default value: disabled
- Allowed values: disabled, enabled
- Owner: Security engineering owner
- Activation gate: EM-3 plus EM-12 and all applicable evidence gates
- Rollback behavior: disabling this flag or using the kill switch must force no blocking/no filtering.
- Required tests: default-disabled, invalid value rejection, activation blocked when missing, rollback/kill-switch no-op behavior.
- Current implementation status: planned only.

## ENFORCE_SAFE_DENIAL_REQUIRED
- Flag name: `ENFORCE_SAFE_DENIAL_REQUIRED`
- Purpose: Planned enforce-mode readiness control for future isolated approval gates.
- Default value: disabled
- Allowed values: disabled, enabled
- Owner: Security engineering owner
- Activation gate: EM-3 plus EM-12 and all applicable evidence gates
- Rollback behavior: disabling this flag or using the kill switch must force no blocking/no filtering.
- Required tests: default-disabled, invalid value rejection, activation blocked when missing, rollback/kill-switch no-op behavior.
- Current implementation status: planned only.

## ENFORCE_TELEMETRY_REQUIRED
- Flag name: `ENFORCE_TELEMETRY_REQUIRED`
- Purpose: Planned enforce-mode readiness control for future isolated approval gates.
- Default value: disabled
- Allowed values: disabled, enabled
- Owner: Security engineering owner
- Activation gate: EM-3 plus EM-12 and all applicable evidence gates
- Rollback behavior: disabling this flag or using the kill switch must force no blocking/no filtering.
- Required tests: default-disabled, invalid value rejection, activation blocked when missing, rollback/kill-switch no-op behavior.
- Current implementation status: planned only.

