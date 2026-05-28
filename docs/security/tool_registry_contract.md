# Tool Registry Contract (Planned)

| Field Name | Purpose | Required/Optional | Allowed Type | Forbidden Content | Validation Rule | Mapped Tests | Implementation Status |
|---|---|---|---|---|---|---|---|
| tool_id | Stable identifier | required | string | empty, whitespace-only | non-empty, unique | TA-001 | planned |
| tool_name | Human-readable name | required | string | control chars | non-empty | TA-001 | planned |
| tool_version | Version pin | required | string | freeform unparseable token | semver-compatible string | TA-001 | planned |
| tool_owner | Ownership mapping | required | string | unknown team ids | must map to known owner list | TA-025 | planned |
| tool_category | Functional class | required | enum string | values outside enum | one of defined categories | TA-012 | planned |
| tool_risk_tier | Risk class | required | enum string | unknown tier | low/medium/high/critical | TA-012 | planned |
| tool_status | Lifecycle state | required | enum string | unknown state | planned/active/deprecated/disabled | TA-001 | planned |
| allowed_tenant_scope | Tenant constraints | required | list[string] or wildcard token | malformed ids | explicit scope or approved wildcard | TA-002 | planned |
| allowed_workspace_scope | Workspace constraints | required | list[string] or wildcard token | malformed ids | explicit scope or approved wildcard | TA-004 | planned |
| required_user_permissions | User perms | optional | list[string] | unknown permission ids | all ids in permission catalog | TA-005 | planned |
| required_group_permissions | Group perms | optional | list[string] | unknown group ids | all ids in group catalog | TA-006 | planned |
| required_role_permissions | Role perms | optional | list[string] | unknown role ids | all ids in role catalog | TA-007 | planned |
| service_account_allowed | SA usage policy | required | boolean | null | explicit true/false | TA-008 | planned |
| delegated_credential_required | Credential requirement | required | boolean | null | explicit true/false | TA-009 | planned |
| delegated_credential_scope | Credential scope | optional | object | invalid tenant/workspace format | matches tenant/workspace scope schema | TA-010,TA-011 | planned |
| approval_required | Approval gating | required | boolean | null | explicit true/false | TA-012 | planned |
| approval_risk_level | Approval level | optional | enum string | unknown level | required when approval_required=true | TA-013 | planned |
| argument_schema_id | Arg schema link | required | string | missing reference | must resolve to known schema | TA-014 | planned |
| result_safety_policy_id | Result policy link | required | string | missing reference | must resolve to known policy | TA-019 | planned |
| audit_required | Audit mandate | required | boolean | null | explicit true/false | TA-025 | planned |
| finding_required_on_violation | Finding mandate | required | boolean | null | explicit true/false | TA-026 | planned |
| metric_required | Metric mandate | required | boolean | null | explicit true/false | TA-027 | planned |
| default_effect | Default decision effect | required | enum string | allow-by-default | must be deny | TA-001 | planned |
| metadata_schema_version | Registry schema version | required | string | unknown version | must equal supported contract version | TA-001 | planned |
