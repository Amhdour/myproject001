import pytest
from backend.security_layer.shadow_deny.feature_flags import *

def test_defaults_disabled():
    assert len(DEFAULT_SHADOW_DENY_FLAG_STATE)==12
    assert all(v is False for v in DEFAULT_SHADOW_DENY_FLAG_STATE.values())

def test_invalid_flag_rejected():
    with pytest.raises(ValueError):
        validate_shadow_deny_flags({'BAD':True})

def test_rollback_disables_recording():
    f=build_shadow_deny_flag_state({'SHADOW_DENY_DECISION_RECORDING_ENABLED':True,'SHADOW_DENY_ROLLBACK_ENABLED':True})
    assert not shadow_deny_decision_recording_enabled(f)
