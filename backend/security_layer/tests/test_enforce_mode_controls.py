from backend.security_layer.enforce_mode.controls import CONTROL_SIMULATORS
from backend.security_layer.enforce_mode.controls import simulate_artifact_enforce_gate
from backend.security_layer.enforce_mode.controls import (
    simulate_audit_metric_enforce_gate,
)
from backend.security_layer.enforce_mode.controls import simulate_cache_enforce_gate
from backend.security_layer.enforce_mode.controls import simulate_ingestion_enforce_gate
from backend.security_layer.enforce_mode.controls import simulate_mcp_enforce_gate
from backend.security_layer.enforce_mode.controls import simulate_retrieval_enforce_gate
from backend.security_layer.enforce_mode.controls import (
    simulate_safe_denial_enforce_gate,
)
from backend.security_layer.enforce_mode.controls import simulate_tool_enforce_gate
from backend.security_layer.enforce_mode.controls import simulate_vector_enforce_gate
from backend.security_layer.enforce_mode.models import EnforceActivationDecisionStatus
from backend.security_layer.enforce_mode.models import EnforceControlFamily
from backend.security_layer.enforce_mode.models import EnforceLiveEffect
from backend.security_layer.enforce_mode.simulator import (
    build_enforce_readiness_context,
)


def _assert_simulation_only(family: EnforceControlFamily, simulator) -> None:
    context = build_enforce_readiness_context(family)
    decision = simulator(context)
    assert decision.status == EnforceActivationDecisionStatus.BLOCKED
    assert decision.live_effect == EnforceLiveEffect.NO_CHANGE
    assert decision.findings
    assert decision.simulation_records
    combined = str(decision).lower()
    for forbidden in (
        "raw query",
        "raw prompt",
        "raw document",
        "raw chunk",
        "secret-value",
    ):
        assert forbidden not in combined


def test_all_9_control_families_have_simulators() -> None:
    assert len(CONTROL_SIMULATORS) == 9


def test_retrieval_enforce_gate_simulation_only() -> None:
    _assert_simulation_only(
        EnforceControlFamily.RETRIEVAL_ACL, simulate_retrieval_enforce_gate
    )


def test_vector_enforce_gate_simulation_only() -> None:
    _assert_simulation_only(
        EnforceControlFamily.VECTOR_DB_SECURITY, simulate_vector_enforce_gate
    )


def test_cache_enforce_gate_simulation_only() -> None:
    _assert_simulation_only(
        EnforceControlFamily.CACHE_SECURITY, simulate_cache_enforce_gate
    )


def test_tool_enforce_gate_simulation_only() -> None:
    _assert_simulation_only(
        EnforceControlFamily.TOOL_AUTHORIZATION, simulate_tool_enforce_gate
    )


def test_mcp_enforce_gate_simulation_only() -> None:
    _assert_simulation_only(
        EnforceControlFamily.MCP_HARDENING, simulate_mcp_enforce_gate
    )


def test_artifact_enforce_gate_simulation_only() -> None:
    _assert_simulation_only(
        EnforceControlFamily.ARTIFACT_SAFETY, simulate_artifact_enforce_gate
    )


def test_ingestion_enforce_gate_simulation_only() -> None:
    _assert_simulation_only(
        EnforceControlFamily.SECURE_INGESTION, simulate_ingestion_enforce_gate
    )


def test_safe_denial_enforce_gate_simulation_only() -> None:
    _assert_simulation_only(
        EnforceControlFamily.SAFE_DENIAL, simulate_safe_denial_enforce_gate
    )


def test_audit_metric_enforce_gate_simulation_only() -> None:
    _assert_simulation_only(
        EnforceControlFamily.AUDIT_FINDING_METRIC, simulate_audit_metric_enforce_gate
    )


def test_no_live_app_integration_and_shadow_deny_runtime_remains_inactive() -> None:
    for family, simulator in CONTROL_SIMULATORS.items():
        decision = simulator(build_enforce_readiness_context(family))
        assert decision.live_effect == EnforceLiveEffect.NO_CHANGE
        assert decision.status == EnforceActivationDecisionStatus.BLOCKED
