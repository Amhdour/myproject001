from backend.security_layer.enforce_mode.blast_radius import (
    evaluate_automatic_rollback_conditions,
)
from backend.security_layer.enforce_mode.blast_radius import (
    sanitize_blast_radius_summary,
)
from backend.security_layer.enforce_mode.blast_radius import validate_blast_radius_scope
from backend.security_layer.enforce_mode.blast_radius import (
    validate_deny_rate_threshold,
)
from backend.security_layer.enforce_mode.blast_radius import (
    validate_error_rate_threshold,
)
from backend.security_layer.enforce_mode.blast_radius import (
    validate_false_positive_threshold,
)
from backend.security_layer.enforce_mode.blast_radius import validate_latency_threshold
from backend.security_layer.enforce_mode.models import EnforceBlastRadiusStatus
from backend.security_layer.enforce_mode.models import EnforceControlFamily
from backend.security_layer.enforce_mode.models import EnforceReadinessStage


def test_default_initial_allowed_scope_is_none() -> None:
    assert validate_blast_radius_scope() == EnforceBlastRadiusStatus.NONE_ALLOWED


def test_limited_scope_allowed_for_future_pilot() -> None:
    assert (
        validate_blast_radius_scope(
            tenant_safe_ids=("tenant-placeholder",),
            workspace_safe_ids=("workspace-placeholder",),
            subject_safe_ids=("subject-placeholder",),
            control_families=(EnforceControlFamily.RETRIEVAL_ACL,),
            stages=(EnforceReadinessStage.SIMULATED,),
        )
        == EnforceBlastRadiusStatus.LIMITED
    )


def test_broad_blast_radius_blocks_activation() -> None:
    assert (
        validate_blast_radius_scope(
            tenant_safe_ids=("tenant-1", "tenant-2"),
        )
        == EnforceBlastRadiusStatus.TOO_BROAD
    )


def test_threshold_breach_blocks_activation_and_triggers_rollback() -> None:
    assert not validate_deny_rate_threshold(0.2)
    assert not validate_false_positive_threshold(0.1)
    assert not validate_error_rate_threshold(0.2)
    assert not validate_latency_threshold(200.0)
    assert evaluate_automatic_rollback_conditions(
        deny_rate=0.2,
        false_positive_rate=0.0,
        error_rate=0.0,
        latency_added_ms=0.0,
    )


def test_sanitized_summary_has_no_raw_details() -> None:
    summary = sanitize_blast_radius_summary(EnforceBlastRadiusStatus.LIMITED)
    assert "placeholder" in summary
    assert "user@example.com" not in summary
