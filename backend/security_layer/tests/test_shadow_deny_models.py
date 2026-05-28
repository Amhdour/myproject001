from backend.security_layer.shadow_deny.simulator import build_shadow_deny_simulation_context
from backend.security_layer.shadow_deny.models import ShadowDenyControlFamily, ShadowDenyStage

def test_simulation_context_creation():
    ctx=build_shadow_deny_simulation_context(decision_id='d1',control_family=ShadowDenyControlFamily.RETRIEVAL,stage=ShadowDenyStage.DECISION,tenant_id_hash_or_safe_id='t',workspace_id_hash_or_safe_id='w',subject_id_hash_or_safe_id='s',deny_reason_code='r',safe_denial_category='cat',flags={})
    assert ctx.mode.value=='shadow_simulation_only'
