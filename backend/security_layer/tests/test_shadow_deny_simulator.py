from backend.security_layer.shadow_deny.simulator import *
from backend.security_layer.shadow_deny.models import ShadowDenyControlFamily, ShadowDenyStage

def _ctx(flags):
    return build_shadow_deny_simulation_context(decision_id='d2',control_family=ShadowDenyControlFamily.RETRIEVAL,stage=ShadowDenyStage.DECISION,tenant_id_hash_or_safe_id='t',workspace_id_hash_or_safe_id='w',subject_id_hash_or_safe_id='s',deny_reason_code='r',safe_denial_category='safe',flags=flags)

def test_disabled_noop():
    d=simulate_shadow_deny_decision(_ctx({}))
    assert d.decision_record.simulated_effect=='no_change'

def test_recording_and_compare():
    d=simulate_shadow_deny_decision(_ctx({'SECURITY_SHADOW_DENY_ENABLED':True,'RETRIEVAL_SHADOW_DENY_ENABLED':True,'SHADOW_DENY_DECISION_RECORDING_ENABLED':True,'SHADOW_DENY_COMPARE_MONITOR_ONLY_ENABLED':True}),monitor_only_decision={'decision_id':'m'})
    assert d.recorded and d.comparison is not None
    assert validate_shadow_deny_non_blocking(d)
    assert validate_shadow_deny_non_filtering(d)
    assert d.decision_record.live_effect=='no_change'
