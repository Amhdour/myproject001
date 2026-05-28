from backend.security_layer.runtime.audit import clear_audit_events, get_audit_events
from backend.security_layer.runtime.findings import clear_findings, get_findings
from backend.security_layer.runtime.metrics import clear_security_metrics, get_security_metrics
from backend.security_layer.tools.controls import (
    authorize_approval_requirement_evaluated,
    authorize_caller_identity_resolved,
    authorize_delegated_credential_validated,
    authorize_service_account_permission_validated,
    authorize_subject_permission_validated,
    authorize_tenant_scope_validated,
    authorize_tool_argument_content_validated,
    authorize_tool_argument_schema_validated,
    authorize_tool_audit_written,
    authorize_tool_call_requested,
    authorize_tool_context_validated,
    authorize_tool_execution_authorized,
    authorize_tool_finding_recorded_if_needed,
    authorize_tool_identity_resolved,
    authorize_tool_registry_loaded,
    authorize_tool_registry_validated,
    authorize_tool_result_received,
    authorize_tool_result_safety_validated,
    authorize_tool_risk_classified,
    authorize_workspace_scope_validated,
)
from backend.security_layer.tools.models import ToolAuthorizationStage, ToolDecisionStatus, ToolResultMetadata


def test_all_20_authorization_stage_controls_exist_and_return_decisions(sample_context, sample_registry):
    stages = [
        authorize_tool_registry_loaded(sample_context),
        authorize_tool_registry_validated(sample_context),
        authorize_tool_call_requested(sample_context),
        authorize_tool_context_validated(sample_context),
        authorize_tool_identity_resolved(sample_context, sample_registry),
        authorize_caller_identity_resolved(sample_context),
        authorize_tenant_scope_validated(sample_context),
        authorize_workspace_scope_validated(sample_context),
        authorize_subject_permission_validated(sample_context, sample_registry),
        authorize_service_account_permission_validated(sample_context, sample_registry),
        authorize_delegated_credential_validated(sample_context, sample_registry),
        authorize_tool_risk_classified(sample_context, sample_registry),
        authorize_tool_argument_schema_validated(sample_context, sample_registry),
        authorize_tool_argument_content_validated(sample_context, sample_registry),
        authorize_approval_requirement_evaluated(sample_context, sample_registry),
        authorize_tool_execution_authorized(sample_context, sample_registry),
        authorize_tool_result_received(sample_context, ToolResultMetadata("p", "1")),
        authorize_tool_result_safety_validated(sample_context, ToolResultMetadata("p", "1")),
        authorize_tool_audit_written(sample_context),
        authorize_tool_finding_recorded_if_needed(sample_context),
    ]
    assert len(stages) == 20
    assert all(hasattr(d, "status") for d in stages)


def test_audit_finding_metric_are_in_memory_helpers(sample_context):
    clear_audit_events(); clear_findings(); clear_security_metrics()
    authorize_tool_audit_written(sample_context)
    authorize_tool_finding_recorded_if_needed(sample_context)
    assert get_audit_events() and get_findings() and get_security_metrics()


def test_prompt_injection_flagged_in_controls(sample_context, sample_registry):
    context = sample_context.__class__(
        **{**sample_context.__dict__, "arguments": [sample_context.arguments[0].__class__("prompt", "ignore previous")]} 
    )
    d = authorize_tool_argument_content_validated(context, sample_registry)
    assert d.status == ToolDecisionStatus.FLAGGED
    assert d.stage == ToolAuthorizationStage.TOOL_ARGUMENT_CONTENT_VALIDATED
