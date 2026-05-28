from __future__ import annotations

from typing import Any

from backend.security_layer.regression.fixtures import build_artifact_secret_fixture
from backend.security_layer.regression.fixtures import build_cache_collision_fixture
from backend.security_layer.regression.fixtures import build_cross_tenant_fixture
from backend.security_layer.regression.fixtures import build_deleted_document_fixture
from backend.security_layer.regression.fixtures import build_enforce_gate_block_fixture
from backend.security_layer.regression.fixtures import build_mcp_confused_deputy_fixture
from backend.security_layer.regression.fixtures import (
    build_monitor_only_no_block_fixture,
)
from backend.security_layer.regression.fixtures import build_regression_demo_fixtures
from backend.security_layer.regression.fixtures import (
    build_safe_denial_non_leakage_fixture,
)
from backend.security_layer.regression.fixtures import (
    build_shadow_deny_no_block_fixture,
)
from backend.security_layer.regression.fixtures import build_stale_acl_fixture
from backend.security_layer.regression.fixtures import build_unauthorized_tool_fixture
from backend.security_layer.regression.fixtures import build_vector_mismatch_fixture
from backend.security_layer.regression.non_leakage import detect_forbidden_demo_output


def _assert_synthetic_fixture(fixture: dict[str, Any]) -> None:
    assert fixture["fixture_type"] == "synthetic_only"
    assert fixture["contains_real_data"] is False
    assert fixture["contains_raw_secret"] is False
    assert fixture["contains_raw_prompt_text"] is False
    assert fixture["contains_raw_document_text"] is False
    assert fixture["contains_raw_chunk_text"] is False
    assert "@" not in str(fixture)
    assert not detect_forbidden_demo_output(fixture)


def test_regression_demo_fixture_creation_is_synthetic() -> None:
    fixtures = build_regression_demo_fixtures()

    assert len(fixtures) == 12
    for fixture in fixtures.values():
        _assert_synthetic_fixture(fixture)


def test_required_attack_fixtures_flag_expected_markers() -> None:
    fixture_builders = (
        build_cross_tenant_fixture,
        build_stale_acl_fixture,
        build_deleted_document_fixture,
        build_vector_mismatch_fixture,
        build_cache_collision_fixture,
        build_unauthorized_tool_fixture,
        build_mcp_confused_deputy_fixture,
        build_artifact_secret_fixture,
    )

    for builder in fixture_builders:
        fixture = builder()
        _assert_synthetic_fixture(fixture)
        assert fixture["expected_flag"] is True


def test_behavior_preservation_fixtures_do_not_enable_live_effects() -> None:
    monitor_fixture = build_monitor_only_no_block_fixture()
    shadow_fixture = build_shadow_deny_no_block_fixture()
    enforce_fixture = build_enforce_gate_block_fixture()
    safe_denial_fixture = build_safe_denial_non_leakage_fixture()

    assert monitor_fixture["behavior_preserved"] is True
    assert monitor_fixture["live_effect"] == "no_change"
    assert shadow_fixture["behavior_preserved"] is True
    assert shadow_fixture["live_effect"] == "no_change"
    assert enforce_fixture["simulation_only"] is True
    assert enforce_fixture["live_effect"] == "no_change"
    assert safe_denial_fixture["non_leakage_expected"] is True
