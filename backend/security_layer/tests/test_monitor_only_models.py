from backend.security_layer.monitor_only.models import MonitorOnlyCandidate
from backend.security_layer.monitor_only.models import MonitorOnlyDecision
from backend.security_layer.monitor_only.models import MonitorOnlyObservation
from backend.security_layer.monitor_only.models import SELECTED_MONITOR_ONLY_CANDIDATES
from backend.security_layer.monitor_only.models import reviewed_candidate_count
from backend.security_layer.monitor_only.models import selected_candidate_count


def test_monitor_only_candidate_inventory_has_eight_reviewed_and_two_selected() -> None:
    assert reviewed_candidate_count() == 8
    assert selected_candidate_count() == 2
    assert SELECTED_MONITOR_ONLY_CANDIDATES == (
        MonitorOnlyCandidate.SHARED_SINK_CONSOLIDATION,
        MonitorOnlyCandidate.CACHE_DRY_RUN_ADAPTER,
    )


def test_monitor_only_observation_is_telemetry_only() -> None:
    observation = MonitorOnlyObservation(
        candidate=MonitorOnlyCandidate.CACHE_DRY_RUN_ADAPTER,
        decision=MonitorOnlyDecision.OBSERVED,
        request_id="req-1",
        notes=("no blocking", "no filtering"),
    )

    assert observation.decision is MonitorOnlyDecision.OBSERVED
    assert "no blocking" in observation.notes
    assert "no filtering" in observation.notes
