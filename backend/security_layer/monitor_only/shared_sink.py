from __future__ import annotations

from backend.security_layer.monitor_only.feature_flags import MonitorOnlyFeatureFlags
from backend.security_layer.monitor_only.feature_flags import is_shared_sink_enabled
from backend.security_layer.monitor_only.models import MonitorOnlyCandidate
from backend.security_layer.monitor_only.models import MonitorOnlyDecision
from backend.security_layer.monitor_only.models import MonitorOnlyObservation
from backend.security_layer.monitor_only.models import MonitorOnlySignal
from backend.security_layer.monitor_only.models import MonitorOnlySignalType
from backend.security_layer.runtime.audit import AuditEvent
from backend.security_layer.runtime.audit import write_audit_event
from backend.security_layer.runtime.findings import SecurityFinding
from backend.security_layer.runtime.findings import record_finding
from backend.security_layer.runtime.metrics import emit_security_metric


def write_monitor_only_signals(
    flags: MonitorOnlyFeatureFlags,
    *,
    request_id: str,
    action: str,
    decision: str = "allow",
    reason_code: str | None = None,
    details: dict[str, object] | None = None,
) -> MonitorOnlyObservation:
    try:
        enabled = is_shared_sink_enabled(flags)
    except ValueError:
        enabled = False
    if not enabled:
        return MonitorOnlyObservation(
            candidate=MonitorOnlyCandidate.SHARED_SINK_CONSOLIDATION,
            decision=MonitorOnlyDecision.SKIPPED_DISABLED,
            request_id=request_id,
            notes=("shared sink disabled or invalid",),
        )

    safe_details = dict(details or {})
    mode = "monitor_only"
    signals = (
        MonitorOnlySignal(
            signal_type=MonitorOnlySignalType.AUDIT,
            action=action,
            decision=decision,
            mode=mode,
            request_id=request_id,
            details=safe_details,
        ),
        MonitorOnlySignal(
            signal_type=MonitorOnlySignalType.METRIC,
            action=action,
            decision=decision,
            mode=mode,
            request_id=request_id,
            details=safe_details,
        ),
    )
    write_audit_event(AuditEvent(action=action, decision=decision, mode=mode, request_id=request_id, details=safe_details))
    emit_security_metric(action, decision, mode)

    if reason_code:
        record_finding(SecurityFinding(action=action, reason_code=reason_code, request_id=request_id))
        signals = signals + (
            MonitorOnlySignal(
                signal_type=MonitorOnlySignalType.FINDING,
                action=action,
                decision=decision,
                mode=mode,
                request_id=request_id,
                reason_code=reason_code,
                details=safe_details,
            ),
        )

    return MonitorOnlyObservation(
        candidate=MonitorOnlyCandidate.SHARED_SINK_CONSOLIDATION,
        decision=MonitorOnlyDecision.OBSERVED,
        request_id=request_id,
        signals=signals,
        notes=("fail-open telemetry only",),
    )
