from backend.security_layer.mcp.registry_contract import *


def _entry():
    data={k:([] if 'permissions' in k else False if k in {'service_account_allowed','delegated_credential_required','approval_required','request_signing_required','replay_protection_required','audit_required','finding_required_on_violation','metric_required'} else 'x') for k in REQUIRED_MCP_REGISTRY_FIELDS}
    data['metadata_schema_version']='1.0'
    return build_safe_mcp_registry_entry(**data)


def test_registry_fields_and_forbidden():
    e=_entry(); ok,errs=validate_mcp_registry_entry(e); assert ok
    e['api_key']='abc'; ok,errs=validate_mcp_registry_entry(e); assert not ok
