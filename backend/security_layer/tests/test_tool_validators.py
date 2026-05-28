from datetime import UTC, datetime, timedelta
from backend.security_layer.tools.validators import validate_delegated_credential, validate_tool_authorization_context, validate_tool_permission_context, validate_service_account_permission, validate_tool_risk_and_approval, validate_tool_result_safety, validate_tool_identity
from backend.security_layer.tools.models import ToolDecisionStatus, ToolResultMetadata

def test_unknown_tool_and_missing_context_denied(sample_context, sample_registry):
    bad = validate_tool_identity(sample_context, sample_registry.__class__(**{**sample_registry.__dict__,'tool_id':'other'}))
    assert bad.status == ToolDecisionStatus.DENIED
    c = sample_context.__class__(**{**sample_context.__dict__,'tenant_scope':None})
    assert validate_tool_authorization_context(c).status == ToolDecisionStatus.DENIED

def test_permission_and_service_and_delegated_denials(sample_context, sample_registry):
    c = sample_context.__class__(**{**sample_context.__dict__,'permission_context':sample_context.permission_context.__class__(subject_id='u1',user_permissions=[],group_permissions=[],role_permissions=[])})
    assert validate_tool_permission_context(c,sample_registry).status == ToolDecisionStatus.DENIED
    svc = sample_context.__class__(**{**sample_context.__dict__,'caller':sample_context.caller.__class__(caller_id='s1',caller_type='service')})
    assert validate_service_account_permission(svc,sample_registry).status == ToolDecisionStatus.DENIED
    no_cred = sample_context.__class__(**{**sample_context.__dict__,'delegated_credential':None})
    assert validate_delegated_credential(no_cred,sample_registry).status == ToolDecisionStatus.DENIED

def test_delegated_expired_wrong_tenant_high_risk_and_result_flags(sample_context, sample_registry):
    exp = sample_context.__class__(**{**sample_context.__dict__,'delegated_credential':sample_context.delegated_credential.__class__('c1','t1','scope',datetime.now(UTC)-timedelta(seconds=1))})
    assert validate_delegated_credential(exp,sample_registry).status == ToolDecisionStatus.DENIED
    wrong = sample_context.__class__(**{**sample_context.__dict__,'delegated_credential':sample_context.delegated_credential.__class__('c1','t2','scope',datetime.now(UTC)+timedelta(days=1))})
    assert validate_delegated_credential(wrong,sample_registry).status == ToolDecisionStatus.DENIED
    assert validate_tool_risk_and_approval(sample_context,sample_registry).status == ToolDecisionStatus.APPROVAL_REQUIRED
    assert validate_tool_result_safety(sample_context,ToolResultMetadata('p','1',flagged_unsafe=True)).status == ToolDecisionStatus.FLAGGED
    assert validate_tool_result_safety(sample_context,ToolResultMetadata('p','1',flagged_secret_leakage=True)).status == ToolDecisionStatus.FLAGGED
