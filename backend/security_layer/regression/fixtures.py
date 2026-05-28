"""Synthetic fixture builders for isolated regression/demo attacks."""

from __future__ import annotations

from typing import Any

Fixture = dict[str, Any]

BASE_SAFE_IDS: Fixture = {
    "tenant_safe_id": "tenant_alpha",
    "other_tenant_safe_id": "tenant_beta",
    "workspace_safe_id": "workspace_demo",
    "subject_safe_id": "subject_demo",
    "document_safe_id": "doc_hash_demo",
    "chunk_safe_id": "chunk_hash_demo",
    "credential_ref": "credential_ref_demo_redacted",
}


def _fixture(kind: str, markers: tuple[str, ...], **extra: object) -> Fixture:
    return {
        **BASE_SAFE_IDS,
        "fixture_kind": kind,
        "fixture_type": "synthetic_only",
        "contains_real_data": False,
        "contains_raw_prompt_text": False,
        "contains_raw_document_text": False,
        "contains_raw_chunk_text": False,
        "contains_raw_secret": False,
        "attack_markers": markers,
        **extra,
    }


def build_cross_tenant_fixture() -> Fixture:
    return _fixture(
        "cross_tenant_retrieval",
        ("cross_tenant_marker",),
        requested_tenant_safe_id="tenant_alpha",
        resource_tenant_safe_id="tenant_beta",
        expected_flag=True,
    )


def build_stale_acl_fixture() -> Fixture:
    return _fixture(
        "stale_acl_retrieval",
        ("stale_acl_marker",),
        acl_version_requested="acl_v2_demo",
        acl_version_indexed="acl_v1_demo",
        expected_flag=True,
    )


def build_deleted_document_fixture() -> Fixture:
    return _fixture(
        "deleted_document_retrieval",
        ("deleted_document_marker",),
        deletion_state="deleted_marker_only",
        expected_flag=True,
    )


def build_vector_mismatch_fixture() -> Fixture:
    return _fixture(
        "vector_mismatch",
        ("vector_namespace_mismatch_marker", "vector_acl_metadata_mismatch_marker"),
        query_namespace="namespace_alpha_demo",
        vector_namespace="namespace_beta_demo",
        expected_flag=True,
    )


def build_cache_collision_fixture() -> Fixture:
    return _fixture(
        "cache_collision",
        ("cache_tenant_mismatch_marker", "cache_acl_version_mismatch_marker"),
        cache_key="cache_key_hash_demo",
        cache_tenant_safe_id="tenant_beta",
        expected_flag=True,
    )


def build_unauthorized_tool_fixture() -> Fixture:
    return _fixture(
        "unauthorized_tool",
        ("unauthorized_tool_marker", "tool_approval_required_marker"),
        tool_safe_name="tool_demo_write_action",
        isolated_control_can_deny=True,
        expected_flag=True,
    )


def build_mcp_confused_deputy_fixture() -> Fixture:
    return _fixture(
        "mcp_confused_deputy",
        (
            "unknown_mcp_server_marker",
            "confused_deputy_marker",
            "credential_boundary_marker",
        ),
        mcp_server_safe_id="mcp_server_demo_unknown",
        expected_flag=True,
    )


def build_artifact_secret_fixture() -> Fixture:
    return _fixture(
        "artifact_sensitive_marker",
        (
            "artifact_sensitive_value_marker",
            "artifact_unauthorized_document_marker",
            "artifact_prompt_injection_marker",
        ),
        artifact_safe_id="artifact_hash_demo",
        expected_flag=True,
    )


def build_monitor_only_no_block_fixture() -> Fixture:
    return _fixture(
        "monitor_only_no_block",
        ("monitor_only_no_block_marker", "monitor_only_no_filter_marker"),
        live_effect="no_change",
        behavior_preserved=True,
    )


def build_shadow_deny_no_block_fixture() -> Fixture:
    return _fixture(
        "shadow_deny_no_block",
        ("shadow_deny_simulated_deny_marker",),
        simulated_effect="deny",
        live_effect="no_change",
        behavior_preserved=True,
    )


def build_enforce_gate_block_fixture() -> Fixture:
    return _fixture(
        "enforce_gate_block",
        ("enforce_missing_gate_marker", "kill_switch_no_change_marker"),
        activation_state="blocked_by_missing_gates",
        simulation_only=True,
        live_effect="no_change",
    )


def build_safe_denial_non_leakage_fixture() -> Fixture:
    return _fixture(
        "safe_denial_non_leakage",
        ("safe_denial_marker", "audit_finding_metric_marker"),
        denial_summary="Access cannot be granted for this synthetic scenario.",
        non_leakage_expected=True,
    )


def build_regression_demo_fixtures() -> dict[str, Fixture]:
    return {
        "cross_tenant": build_cross_tenant_fixture(),
        "stale_acl": build_stale_acl_fixture(),
        "deleted_document": build_deleted_document_fixture(),
        "vector_mismatch": build_vector_mismatch_fixture(),
        "cache_collision": build_cache_collision_fixture(),
        "unauthorized_tool": build_unauthorized_tool_fixture(),
        "mcp_confused_deputy": build_mcp_confused_deputy_fixture(),
        "artifact_secret": build_artifact_secret_fixture(),
        "monitor_only_no_block": build_monitor_only_no_block_fixture(),
        "shadow_deny_no_block": build_shadow_deny_no_block_fixture(),
        "enforce_gate_block": build_enforce_gate_block_fixture(),
        "safe_denial_non_leakage": build_safe_denial_non_leakage_fixture(),
    }
