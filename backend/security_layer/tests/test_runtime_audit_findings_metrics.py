from backend.security_layer.runtime.audit import AuditEvent, clear_audit_events, get_audit_events, write_audit_event
from backend.security_layer.runtime.findings import SecurityFinding, clear_findings, get_findings, record_finding
from backend.security_layer.runtime.metrics import clear_security_metrics, emit_security_metric, get_security_metrics


def test_audit_findings_metrics_helpers() -> None:
    clear_audit_events(); clear_findings(); clear_security_metrics()
    write_audit_event(AuditEvent(action="retrieval", decision="allow", mode="enforce", request_id="r1"))
    record_finding(SecurityFinding(action="retrieval", reason_code="denied", request_id="r1"))
    emit_security_metric("retrieval", "allow", "enforce")
    assert len(get_audit_events()) == 1
    assert len(get_findings()) == 1
    assert len(get_security_metrics()) == 1
