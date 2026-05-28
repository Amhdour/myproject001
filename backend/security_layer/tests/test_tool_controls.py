from backend.security_layer.runtime.audit import clear_audit_events, get_audit_events
from backend.security_layer.runtime.findings import clear_findings, get_findings
from backend.security_layer.runtime.metrics import clear_security_metrics, get_security_metrics
from backend.security_layer.tools.controls import authorize_tool_audit_written, authorize_tool_finding_recorded_if_needed, authorize_tool_argument_content_validated
from backend.security_layer.tools.models import ToolDecisionStatus

def test_audit_finding_metric_emitted(sample_context, sample_registry):
    clear_audit_events(); clear_findings(); clear_security_metrics()
    authorize_tool_audit_written(sample_context)
    authorize_tool_finding_recorded_if_needed(sample_context)
    assert get_audit_events() and get_findings() and get_security_metrics()

def test_prompt_injection_flagged_in_controls(sample_context, sample_registry):
    context = sample_context.__class__(**{**sample_context.__dict__,'arguments':[sample_context.arguments[0].__class__('prompt','ignore previous')]})
    d = authorize_tool_argument_content_validated(context, sample_registry)
    assert d.status == ToolDecisionStatus.FLAGGED
