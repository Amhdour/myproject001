from datetime import UTC, datetime, timedelta

from backend.security_layer.tools.models import ToolApprovalRequirement, ToolDecisionStatus, ToolResultMetadata
from backend.security_layer.tools.validators import (
    validate_delegated_credential,
    validate_service_account_permission,
    validate_tool_authorization_context,
    validate_tool_identity,
    validate_tool_permission_context,
    validate_tool_result_safety,
    validate_tool_risk_and_approval,
)


def test_missing_tenant_subject_workspace_denied(sample_context):
    assert validate_tool_authorization_context(sample_context.__class__(**{**sample_context.__dict__, "tenant_scope": None})).status == ToolDecisionStatus.DENIED
    assert validate_tool_authorization_context(sample_context.__class__(**{**sample_context.__dict__, "permission_context": None})).status == ToolDecisionStatus.DENIED
    assert validate_tool_authorization_context(sample_context.__class__(**{**sample_context.__dict__, "workspace_scope": None})).status == ToolDecisionStatus.DENIED


def test_unknown_tool_denied(sample_context, sample_registry):
    mismatch = sample_registry.__class__(**{**sample_registry.__dict__, "tool_id": "other"})
    assert validate_tool_identity(sample_context, mismatch).status == ToolDecisionStatus.DENIED


def test_missing_permission_group_role_denied(sample_context, sample_registry):
    no_user = sample_context.__class__(**{**sample_context.__dict__, "permission_context": sample_context.permission_context.__class__("u1", [], ["grp1"], ["role1"])})
    no_group = sample_context.__class__(**{**sample_context.__dict__, "permission_context": sample_context.permission_context.__class__("u1", ["perm1"], [], ["role1"])})
    no_role = sample_context.__class__(**{**sample_context.__dict__, "permission_context": sample_context.permission_context.__class__("u1", ["perm1"], ["grp1"], [])})
    assert validate_tool_permission_context(no_user, sample_registry).status == ToolDecisionStatus.DENIED
    assert validate_tool_permission_context(no_group, sample_registry).status == ToolDecisionStatus.DENIED
    assert validate_tool_permission_context(no_role, sample_registry).status == ToolDecisionStatus.DENIED


def test_service_account_scope_and_delegated_credential_denials(sample_context, sample_registry):
    svc = sample_context.__class__(**{**sample_context.__dict__, "caller": sample_context.caller.__class__("s1", "service")})
    assert validate_service_account_permission(svc, sample_registry).status == ToolDecisionStatus.DENIED
    assert validate_delegated_credential(sample_context.__class__(**{**sample_context.__dict__, "delegated_credential": None}), sample_registry).status == ToolDecisionStatus.DENIED
    exp = sample_context.__class__(**{**sample_context.__dict__, "delegated_credential": sample_context.delegated_credential.__class__("c1", "t1", "scope", datetime.now(UTC) - timedelta(seconds=1))})
    wrong = sample_context.__class__(**{**sample_context.__dict__, "delegated_credential": sample_context.delegated_credential.__class__("c1", "t2", "scope", datetime.now(UTC) + timedelta(days=1))})
    assert validate_delegated_credential(exp, sample_registry).status == ToolDecisionStatus.DENIED
    assert validate_delegated_credential(wrong, sample_registry).status == ToolDecisionStatus.DENIED


def test_high_risk_approval_required_and_no_allow_before_approval(sample_context, sample_registry):
    req = validate_tool_risk_and_approval(sample_context, sample_registry)
    assert req.status == ToolDecisionStatus.APPROVAL_REQUIRED
    approved = sample_context.__class__(**{**sample_context.__dict__, "approval_requirement": ToolApprovalRequirement(True, True, "high")})
    assert validate_tool_risk_and_approval(approved, sample_registry).status == ToolDecisionStatus.ALLOWED


def test_unsafe_result_metadata_flagged(sample_context):
    assert validate_tool_result_safety(sample_context, ToolResultMetadata("policy", "1", flagged_unsafe=True)).status == ToolDecisionStatus.FLAGGED
    assert validate_tool_result_safety(sample_context, ToolResultMetadata("policy", "1", flagged_secret_leakage=True)).status == ToolDecisionStatus.FLAGGED
