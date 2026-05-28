import pytest
from backend.security_layer.tools.registry_contract import REQUIRED_TOOL_REGISTRY_FIELDS, build_safe_tool_registry_entry, validate_tool_registry_entry

def _entry():
    return {k: [] if 'scope' in k or 'permissions' in k else False if k in {'service_account_allowed','delegated_credential_required','approval_required','audit_required','finding_required_on_violation','metric_required'} else 'x' for k in REQUIRED_TOOL_REGISTRY_FIELDS} | {'tool_category':'internal','tool_risk_tier':'low','tool_status':'active','default_effect':'deny','metadata_schema_version':'1.0'}

def test_required_fields_present():
    e=_entry(); validate_tool_registry_entry(e)

def test_forbidden_field_rejected():
    e=_entry(); e['api_key']='secret';
    with pytest.raises(ValueError): validate_tool_registry_entry(e)

def test_secret_and_email_and_url_secret_rejected():
    for v in ['sk-aaaaaaaaaaaa','a@b.com','https://u:p@example.com']:
        e=_entry(); e['tool_description_placeholder']=v
        with pytest.raises(ValueError): validate_tool_registry_entry(e)

def test_safe_registry_entry_creation():
    assert build_safe_tool_registry_entry(**_entry())['tool_id']=='x'
