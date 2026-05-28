# Shadow-Deny Decision Schema (Planned)

Status: planned

| field name | purpose | required/optional | allowed type | forbidden content | validation rule | mapped tests | current status |
|---|---|---|---|---|---|---|---|
| schema_version | schema tracking | required | string | empty | semantic version pattern | SDP-004 | planned |
| decision_id | unique decision key | required | UUID string | duplicates | UUID v4 | SDP-004 | planned |
| timestamp | decision evaluation time | required | RFC3339 datetime | non-UTC ambiguity | parseable UTC | SDP-004 | planned |
| control_family | family source | required | enum string | unknown families | one of 9 listed families | SDP-013..019 | planned |
| stage | internal stage label | required | string | secret payloads | allowlist stage names | SDP-004 | planned |
| tenant_id_hash_or_safe_id | tenant correlation | required | string | raw tenant identifiers | hashed/safe ID format | SDP-007 | planned |
| workspace_id_hash_or_safe_id | workspace correlation | optional | string | raw workspace identifiers | hashed/safe ID format | SDP-007 | planned |
| subject_id_hash_or_safe_id | subject correlation | optional | string | raw user identifiers | hashed/safe ID format | SDP-007 | planned |
| decision_status | simulated decision outcome | required | enum string | unknown status | allowlist {allow,deny,inconclusive} | SDP-004 | planned |
| simulated_effect | what shadow-deny would do | required | enum string | live action claims | allowlist {would_allow,would_deny,unknown} | SDP-004 | planned |
| live_effect | actual live result | required | enum string | blocked/filtered live claims | must be no_change | SDP-002,SDP-003 | planned |
| monitor_only_decision_id | monitor correlation key | optional | UUID string | malformed IDs | UUID format when present | SDP-006 | planned |
| deny_reason_code | normalized reason | optional | string | freeform secrets | allowlist code set | SDP-007 | planned |
| safe_denial_category | safe denial taxonomy | optional | string | sensitive context excerpts | allowlist category | SDP-007 | planned |
| finding_ids | linked findings | optional | array[string] | non-finding IDs | each ID matches finding pattern | SDP-009 | planned |
| metric_names | linked metrics | optional | array[string] | ad hoc PII metric labels | allowlist metrics | SDP-010 | planned |
| audit_event_id | linked audit event | optional | string | empty/malformed IDs | audit ID regex | SDP-008 | planned |
| evidence_ref | evidence pointer | optional | string | external secret URLs | relative docs/security path | SDP-004 | planned |
| rollback_flag_state | rollback state snapshot | required | enum string | unknown values | allowlist {enabled,disabled} | SDP-012 | planned |
| feature_flag_state | evaluated flags snapshot | required | object | unregistered flags | keys subset of planned flags | SDP-001 | planned |
| non_leakage_validated | leakage check result | required | boolean | null | true/false required | SDP-007 | planned |
| created_at | record creation timestamp | required | RFC3339 datetime | non-parseable values | parseable UTC | SDP-004 | planned |
