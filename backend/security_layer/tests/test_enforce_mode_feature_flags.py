import pytest

from backend.security_layer.enforce_mode.feature_flags import DEFAULT_ENFORCE_FLAG_STATE
from backend.security_layer.enforce_mode.feature_flags import (
    ENFORCE_APPROVAL_GATE_ENABLED,
)
from backend.security_layer.enforce_mode.feature_flags import (
    ENFORCE_BLAST_RADIUS_LIMIT_ENABLED,
)
from backend.security_layer.enforce_mode.feature_flags import (
    ENFORCE_KILL_SWITCH_ENABLED,
)
from backend.security_layer.enforce_mode.feature_flags import ENFORCE_MODE_FLAGS
from backend.security_layer.enforce_mode.feature_flags import ENFORCE_ROLLBACK_ENABLED
from backend.security_layer.enforce_mode.feature_flags import RETRIEVAL_ENFORCE_ENABLED
from backend.security_layer.enforce_mode.feature_flags import (
    SECURITY_ENFORCE_MODE_ENABLED,
)
from backend.security_layer.enforce_mode.feature_flags import build_enforce_flag_state
from backend.security_layer.enforce_mode.feature_flags import (
    enforce_approval_gate_enabled,
)
from backend.security_layer.enforce_mode.feature_flags import (
    enforce_blast_radius_enabled,
)
from backend.security_layer.enforce_mode.feature_flags import enforce_family_enabled
from backend.security_layer.enforce_mode.feature_flags import enforce_globally_enabled
from backend.security_layer.enforce_mode.feature_flags import (
    enforce_kill_switch_enabled,
)
from backend.security_layer.enforce_mode.feature_flags import enforce_rollback_enabled
from backend.security_layer.enforce_mode.feature_flags import validate_enforce_flags
from backend.security_layer.enforce_mode.models import EnforceControlFamily
from backend.security_layer.enforce_mode.models import EnforceFeatureFlagState


def test_all_14_enforce_flags_default_disabled() -> None:
    assert len(ENFORCE_MODE_FLAGS) == 14
    assert set(DEFAULT_ENFORCE_FLAG_STATE) == set(ENFORCE_MODE_FLAGS)
    assert all(
        value == EnforceFeatureFlagState.DISABLED
        for value in DEFAULT_ENFORCE_FLAG_STATE.values()
    )


def test_invalid_flag_rejected() -> None:
    with pytest.raises(ValueError):
        build_enforce_flag_state({SECURITY_ENFORCE_MODE_ENABLED: "invalid"})


def test_unknown_flag_rejected() -> None:
    with pytest.raises(ValueError):
        build_enforce_flag_state({"UNKNOWN": EnforceFeatureFlagState.ENABLED})


def test_global_disabled_blocks_family_activation() -> None:
    flags = build_enforce_flag_state(
        {RETRIEVAL_ENFORCE_ENABLED: EnforceFeatureFlagState.ENABLED}
    )
    assert not enforce_globally_enabled(flags)
    assert not enforce_family_enabled(flags, EnforceControlFamily.RETRIEVAL_ACL)


def test_family_disabled_blocks_activation_even_when_global_enabled() -> None:
    flags = build_enforce_flag_state(
        {SECURITY_ENFORCE_MODE_ENABLED: EnforceFeatureFlagState.ENABLED}
    )
    assert enforce_globally_enabled(flags)
    assert not enforce_family_enabled(flags, EnforceControlFamily.RETRIEVAL_ACL)


def test_required_gate_helpers_are_explicit() -> None:
    flags = build_enforce_flag_state(
        {
            ENFORCE_APPROVAL_GATE_ENABLED: EnforceFeatureFlagState.ENABLED,
            ENFORCE_ROLLBACK_ENABLED: EnforceFeatureFlagState.ENABLED,
            ENFORCE_KILL_SWITCH_ENABLED: EnforceFeatureFlagState.ENABLED,
            ENFORCE_BLAST_RADIUS_LIMIT_ENABLED: EnforceFeatureFlagState.ENABLED,
        }
    )
    assert validate_enforce_flags(flags)
    assert enforce_approval_gate_enabled(flags)
    assert enforce_rollback_enabled(flags)
    assert enforce_kill_switch_enabled(flags)
    assert enforce_blast_radius_enabled(flags)
