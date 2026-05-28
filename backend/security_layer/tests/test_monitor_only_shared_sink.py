from backend.security_layer.monitor_only.feature_flags import MonitorOnlyFeatureFlags
from backend.security_layer.monitor_only.feature_flags import MonitorOnlyRuntimeMode
from backend.security_layer.monitor_only.models import MonitorOnlyDecision
from backend.security_layer.monitor_only.models import MonitorOnlySignalType
from backend.security_layer.monitor_only.shared_sink import write_monitor_only_signals
from backend.security_layer.runtime.audit import clear_audit_events
from backend.security_layer.runtime.audit import get_audit_events
from backend.security_layer.runtime.findings import clear_findings
from backend.security_layer.runtime.findings import get_findings
from backend.security_layer.runtime.metrics import clear_security_metrics
from backend.security_layer.runtime.metrics import get_security_metrics


def _enabled_flags() -> MonitorOnlyFeatureFlags:
    return MonitorOnlyFeatureFlags(runtime_mode=MonitorOnlyRuntimeMode.MONITOR_ONLY, shared_sink_enabled=True)


def test_shared_sink_skips_without_emitting_when_disabled() -> None:
    clear_audit_events()
    clear_findings()
    clear_security_metrics()

    observation = write_monitor_only_signals(MonitorOnlyFeatureFlags(), request_id="req-1", action="cache_read_requested")

    assert observation.decision is MonitorOnlyDecision.SKIPPED_DISABLED
    assert not get_audit_events()
    assert not get_findings()
    assert not get_security_metrics()


def test_shared_sink_writes_audit_metric_and_optional_finding() -> None:
    clear_audit_events()
    clear_findings()
    clear_security_metrics()

    observation = write_monitor_only_signals(
        _enabled_flags(),
        request_id="req-1",
        action="cache_read_requested",
        decision="observed",
        reason_code="monitor_only_reason",
        details={"safe": "value"},
    )

    assert observation.decision is MonitorOnlyDecision.OBSERVED
    assert {signal.signal_type for signal in observation.signals} == {
        MonitorOnlySignalType.AUDIT,
        MonitorOnlySignalType.METRIC,
        MonitorOnlySignalType.FINDING,
    }
    assert get_audit_events()[0].mode == "monitor_only"
    assert get_findings()[0].reason_code == "monitor_only_reason"
    assert get_security_metrics()[0].mode == "monitor_only"
