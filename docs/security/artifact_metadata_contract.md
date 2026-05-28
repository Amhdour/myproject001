# Artifact Metadata Contract (Planned)

Status: planned

## artifact_metadata_schema_version
- **Field name:** artifact_metadata_schema_version
- **Purpose:** Carry safe metadata for artifact safety decisions and evidence.
- **Required/optional:** required
- **Allowed type:** string
- **Forbidden content:** raw secrets, tenant internals, policy internals, raw unauthorized document/chunk text.
- **Validation rule:** non-empty when required, format-safe, and consistent with tenant/workspace/subject context.
- **Mapped tests:** ART-TEST-001
- **Implementation status:** planned

## artifact_id_hash_or_safe_id
- **Field name:** artifact_id_hash_or_safe_id
- **Purpose:** Carry safe metadata for artifact safety decisions and evidence.
- **Required/optional:** required
- **Allowed type:** string
- **Forbidden content:** raw secrets, tenant internals, policy internals, raw unauthorized document/chunk text.
- **Validation rule:** non-empty when required, format-safe, and consistent with tenant/workspace/subject context.
- **Mapped tests:** ART-TEST-002
- **Implementation status:** planned

## artifact_type
- **Field name:** artifact_type
- **Purpose:** Carry safe metadata for artifact safety decisions and evidence.
- **Required/optional:** required
- **Allowed type:** string
- **Forbidden content:** raw secrets, tenant internals, policy internals, raw unauthorized document/chunk text.
- **Validation rule:** non-empty when required, format-safe, and consistent with tenant/workspace/subject context.
- **Mapped tests:** ART-TEST-003
- **Implementation status:** planned

## artifact_purpose
- **Field name:** artifact_purpose
- **Purpose:** Carry safe metadata for artifact safety decisions and evidence.
- **Required/optional:** required
- **Allowed type:** string
- **Forbidden content:** raw secrets, tenant internals, policy internals, raw unauthorized document/chunk text.
- **Validation rule:** non-empty when required, format-safe, and consistent with tenant/workspace/subject context.
- **Mapped tests:** ART-TEST-004
- **Implementation status:** planned

## tenant_id_hash_or_safe_id
- **Field name:** tenant_id_hash_or_safe_id
- **Purpose:** Carry safe metadata for artifact safety decisions and evidence.
- **Required/optional:** required
- **Allowed type:** string
- **Forbidden content:** raw secrets, tenant internals, policy internals, raw unauthorized document/chunk text.
- **Validation rule:** non-empty when required, format-safe, and consistent with tenant/workspace/subject context.
- **Mapped tests:** ART-TEST-005
- **Implementation status:** planned

## workspace_id_hash_or_safe_id
- **Field name:** workspace_id_hash_or_safe_id
- **Purpose:** Carry safe metadata for artifact safety decisions and evidence.
- **Required/optional:** required
- **Allowed type:** string
- **Forbidden content:** raw secrets, tenant internals, policy internals, raw unauthorized document/chunk text.
- **Validation rule:** non-empty when required, format-safe, and consistent with tenant/workspace/subject context.
- **Mapped tests:** ART-TEST-006
- **Implementation status:** planned

## subject_id_hash_or_safe_id
- **Field name:** subject_id_hash_or_safe_id
- **Purpose:** Carry safe metadata for artifact safety decisions and evidence.
- **Required/optional:** required
- **Allowed type:** string
- **Forbidden content:** raw secrets, tenant internals, policy internals, raw unauthorized document/chunk text.
- **Validation rule:** non-empty when required, format-safe, and consistent with tenant/workspace/subject context.
- **Mapped tests:** ART-TEST-007
- **Implementation status:** planned

## subject_group_hashes_or_safe_ids
- **Field name:** subject_group_hashes_or_safe_ids
- **Purpose:** Carry safe metadata for artifact safety decisions and evidence.
- **Required/optional:** required
- **Allowed type:** string
- **Forbidden content:** raw secrets, tenant internals, policy internals, raw unauthorized document/chunk text.
- **Validation rule:** non-empty when required, format-safe, and consistent with tenant/workspace/subject context.
- **Mapped tests:** ART-TEST-008
- **Implementation status:** planned

## subject_role_hashes_or_safe_ids
- **Field name:** subject_role_hashes_or_safe_ids
- **Purpose:** Carry safe metadata for artifact safety decisions and evidence.
- **Required/optional:** required
- **Allowed type:** string
- **Forbidden content:** raw secrets, tenant internals, policy internals, raw unauthorized document/chunk text.
- **Validation rule:** non-empty when required, format-safe, and consistent with tenant/workspace/subject context.
- **Mapped tests:** ART-TEST-009
- **Implementation status:** planned

## provenance_id
- **Field name:** provenance_id
- **Purpose:** Carry safe metadata for artifact safety decisions and evidence.
- **Required/optional:** required
- **Allowed type:** string
- **Forbidden content:** raw secrets, tenant internals, policy internals, raw unauthorized document/chunk text.
- **Validation rule:** non-empty when required, format-safe, and consistent with tenant/workspace/subject context.
- **Mapped tests:** ART-TEST-010
- **Implementation status:** planned

## source_type
- **Field name:** source_type
- **Purpose:** Carry safe metadata for artifact safety decisions and evidence.
- **Required/optional:** required
- **Allowed type:** string
- **Forbidden content:** raw secrets, tenant internals, policy internals, raw unauthorized document/chunk text.
- **Validation rule:** non-empty when required, format-safe, and consistent with tenant/workspace/subject context.
- **Mapped tests:** ART-TEST-011
- **Implementation status:** planned

## source_id_hash_or_safe_id
- **Field name:** source_id_hash_or_safe_id
- **Purpose:** Carry safe metadata for artifact safety decisions and evidence.
- **Required/optional:** required
- **Allowed type:** string
- **Forbidden content:** raw secrets, tenant internals, policy internals, raw unauthorized document/chunk text.
- **Validation rule:** non-empty when required, format-safe, and consistent with tenant/workspace/subject context.
- **Mapped tests:** ART-TEST-012
- **Implementation status:** planned

## related_document_ids_hash_or_safe_ids
- **Field name:** related_document_ids_hash_or_safe_ids
- **Purpose:** Carry safe metadata for artifact safety decisions and evidence.
- **Required/optional:** required
- **Allowed type:** string
- **Forbidden content:** raw secrets, tenant internals, policy internals, raw unauthorized document/chunk text.
- **Validation rule:** non-empty when required, format-safe, and consistent with tenant/workspace/subject context.
- **Mapped tests:** ART-TEST-013
- **Implementation status:** planned

## related_chunk_ids_hash_or_safe_ids
- **Field name:** related_chunk_ids_hash_or_safe_ids
- **Purpose:** Carry safe metadata for artifact safety decisions and evidence.
- **Required/optional:** required
- **Allowed type:** string
- **Forbidden content:** raw secrets, tenant internals, policy internals, raw unauthorized document/chunk text.
- **Validation rule:** non-empty when required, format-safe, and consistent with tenant/workspace/subject context.
- **Mapped tests:** ART-TEST-014
- **Implementation status:** planned

## tool_id_hash_or_safe_id
- **Field name:** tool_id_hash_or_safe_id
- **Purpose:** Carry safe metadata for artifact safety decisions and evidence.
- **Required/optional:** required
- **Allowed type:** string
- **Forbidden content:** raw secrets, tenant internals, policy internals, raw unauthorized document/chunk text.
- **Validation rule:** non-empty when required, format-safe, and consistent with tenant/workspace/subject context.
- **Mapped tests:** ART-TEST-015
- **Implementation status:** planned

## mcp_server_id_hash_or_safe_id
- **Field name:** mcp_server_id_hash_or_safe_id
- **Purpose:** Carry safe metadata for artifact safety decisions and evidence.
- **Required/optional:** required
- **Allowed type:** string
- **Forbidden content:** raw secrets, tenant internals, policy internals, raw unauthorized document/chunk text.
- **Validation rule:** non-empty when required, format-safe, and consistent with tenant/workspace/subject context.
- **Mapped tests:** ART-TEST-016
- **Implementation status:** planned

## generation_run_id
- **Field name:** generation_run_id
- **Purpose:** Carry safe metadata for artifact safety decisions and evidence.
- **Required/optional:** required
- **Allowed type:** string
- **Forbidden content:** raw secrets, tenant internals, policy internals, raw unauthorized document/chunk text.
- **Validation rule:** non-empty when required, format-safe, and consistent with tenant/workspace/subject context.
- **Mapped tests:** ART-TEST-017
- **Implementation status:** planned

## content_hash
- **Field name:** content_hash
- **Purpose:** Carry safe metadata for artifact safety decisions and evidence.
- **Required/optional:** required
- **Allowed type:** string
- **Forbidden content:** raw secrets, tenant internals, policy internals, raw unauthorized document/chunk text.
- **Validation rule:** non-empty when required, format-safe, and consistent with tenant/workspace/subject context.
- **Mapped tests:** ART-TEST-018
- **Implementation status:** planned

## content_size_bytes
- **Field name:** content_size_bytes
- **Purpose:** Carry safe metadata for artifact safety decisions and evidence.
- **Required/optional:** required
- **Allowed type:** string
- **Forbidden content:** raw secrets, tenant internals, policy internals, raw unauthorized document/chunk text.
- **Validation rule:** non-empty when required, format-safe, and consistent with tenant/workspace/subject context.
- **Mapped tests:** ART-TEST-019
- **Implementation status:** planned

## content_type
- **Field name:** content_type
- **Purpose:** Carry safe metadata for artifact safety decisions and evidence.
- **Required/optional:** required
- **Allowed type:** string
- **Forbidden content:** raw secrets, tenant internals, policy internals, raw unauthorized document/chunk text.
- **Validation rule:** non-empty when required, format-safe, and consistent with tenant/workspace/subject context.
- **Mapped tests:** ART-TEST-020
- **Implementation status:** planned

## sensitivity_label_placeholder
- **Field name:** sensitivity_label_placeholder
- **Purpose:** Carry safe metadata for artifact safety decisions and evidence.
- **Required/optional:** required
- **Allowed type:** string
- **Forbidden content:** raw secrets, tenant internals, policy internals, raw unauthorized document/chunk text.
- **Validation rule:** non-empty when required, format-safe, and consistent with tenant/workspace/subject context.
- **Mapped tests:** ART-TEST-021
- **Implementation status:** planned

## secret_scan_status
- **Field name:** secret_scan_status
- **Purpose:** Carry safe metadata for artifact safety decisions and evidence.
- **Required/optional:** required
- **Allowed type:** string
- **Forbidden content:** raw secrets, tenant internals, policy internals, raw unauthorized document/chunk text.
- **Validation rule:** non-empty when required, format-safe, and consistent with tenant/workspace/subject context.
- **Mapped tests:** ART-TEST-022
- **Implementation status:** planned

## sensitive_data_scan_status
- **Field name:** sensitive_data_scan_status
- **Purpose:** Carry safe metadata for artifact safety decisions and evidence.
- **Required/optional:** required
- **Allowed type:** string
- **Forbidden content:** raw secrets, tenant internals, policy internals, raw unauthorized document/chunk text.
- **Validation rule:** non-empty when required, format-safe, and consistent with tenant/workspace/subject context.
- **Mapped tests:** ART-TEST-023
- **Implementation status:** planned

## unauthorized_content_scan_status
- **Field name:** unauthorized_content_scan_status
- **Purpose:** Carry safe metadata for artifact safety decisions and evidence.
- **Required/optional:** required
- **Allowed type:** string
- **Forbidden content:** raw secrets, tenant internals, policy internals, raw unauthorized document/chunk text.
- **Validation rule:** non-empty when required, format-safe, and consistent with tenant/workspace/subject context.
- **Mapped tests:** ART-TEST-024
- **Implementation status:** planned

## prompt_injection_flag
- **Field name:** prompt_injection_flag
- **Purpose:** Carry safe metadata for artifact safety decisions and evidence.
- **Required/optional:** optional
- **Allowed type:** string
- **Forbidden content:** raw secrets, tenant internals, policy internals, raw unauthorized document/chunk text.
- **Validation rule:** non-empty when required, format-safe, and consistent with tenant/workspace/subject context.
- **Mapped tests:** ART-TEST-025
- **Implementation status:** planned

## poisoning_flag
- **Field name:** poisoning_flag
- **Purpose:** Carry safe metadata for artifact safety decisions and evidence.
- **Required/optional:** optional
- **Allowed type:** string
- **Forbidden content:** raw secrets, tenant internals, policy internals, raw unauthorized document/chunk text.
- **Validation rule:** non-empty when required, format-safe, and consistent with tenant/workspace/subject context.
- **Mapped tests:** ART-TEST-026
- **Implementation status:** planned

## quarantine_status
- **Field name:** quarantine_status
- **Purpose:** Carry safe metadata for artifact safety decisions and evidence.
- **Required/optional:** optional
- **Allowed type:** string
- **Forbidden content:** raw secrets, tenant internals, policy internals, raw unauthorized document/chunk text.
- **Validation rule:** non-empty when required, format-safe, and consistent with tenant/workspace/subject context.
- **Mapped tests:** ART-TEST-027
- **Implementation status:** planned

## redaction_status
- **Field name:** redaction_status
- **Purpose:** Carry safe metadata for artifact safety decisions and evidence.
- **Required/optional:** optional
- **Allowed type:** string
- **Forbidden content:** raw secrets, tenant internals, policy internals, raw unauthorized document/chunk text.
- **Validation rule:** non-empty when required, format-safe, and consistent with tenant/workspace/subject context.
- **Mapped tests:** ART-TEST-028
- **Implementation status:** planned

## approval_required
- **Field name:** approval_required
- **Purpose:** Carry safe metadata for artifact safety decisions and evidence.
- **Required/optional:** optional
- **Allowed type:** string
- **Forbidden content:** raw secrets, tenant internals, policy internals, raw unauthorized document/chunk text.
- **Validation rule:** non-empty when required, format-safe, and consistent with tenant/workspace/subject context.
- **Mapped tests:** ART-TEST-029
- **Implementation status:** planned

## approval_status
- **Field name:** approval_status
- **Purpose:** Carry safe metadata for artifact safety decisions and evidence.
- **Required/optional:** optional
- **Allowed type:** string
- **Forbidden content:** raw secrets, tenant internals, policy internals, raw unauthorized document/chunk text.
- **Validation rule:** non-empty when required, format-safe, and consistent with tenant/workspace/subject context.
- **Mapped tests:** ART-TEST-030
- **Implementation status:** planned

## retention_policy_id
- **Field name:** retention_policy_id
- **Purpose:** Carry safe metadata for artifact safety decisions and evidence.
- **Required/optional:** optional
- **Allowed type:** string
- **Forbidden content:** raw secrets, tenant internals, policy internals, raw unauthorized document/chunk text.
- **Validation rule:** non-empty when required, format-safe, and consistent with tenant/workspace/subject context.
- **Mapped tests:** ART-TEST-031
- **Implementation status:** planned

## created_at
- **Field name:** created_at
- **Purpose:** Carry safe metadata for artifact safety decisions and evidence.
- **Required/optional:** optional
- **Allowed type:** string
- **Forbidden content:** raw secrets, tenant internals, policy internals, raw unauthorized document/chunk text.
- **Validation rule:** non-empty when required, format-safe, and consistent with tenant/workspace/subject context.
- **Mapped tests:** ART-TEST-032
- **Implementation status:** planned

## expires_at
- **Field name:** expires_at
- **Purpose:** Carry safe metadata for artifact safety decisions and evidence.
- **Required/optional:** optional
- **Allowed type:** string
- **Forbidden content:** raw secrets, tenant internals, policy internals, raw unauthorized document/chunk text.
- **Validation rule:** non-empty when required, format-safe, and consistent with tenant/workspace/subject context.
- **Mapped tests:** ART-TEST-033
- **Implementation status:** planned

