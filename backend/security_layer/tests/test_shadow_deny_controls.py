from backend.security_layer.shadow_deny.controls import *
from backend.security_layer.shadow_deny.simulator import build_shadow_deny_simulation_context
from backend.security_layer.shadow_deny.models import ShadowDenyControlFamily, ShadowDenyStage

def _ctx():
    return build_shadow_deny_simulation_context(decision_id='d3',control_family=ShadowDenyControlFamily.RETRIEVAL,stage=ShadowDenyStage.DECISION,tenant_id_hash_or_safe_id='t',workspace_id_hash_or_safe_id='w',subject_id_hash_or_safe_id='s',deny_reason_code='r',safe_denial_category='safe',flags={'SECURITY_SHADOW_DENY_ENABLED':True})

def test_family_disabled_noop():
    assert simulate_retrieval_shadow_deny(_ctx()).decision_record.simulated_effect=='no_change'

def test_each_family_simulation_only():
    c=_ctx(); c.flags.update({'RETRIEVAL_SHADOW_DENY_ENABLED':True}); assert simulate_retrieval_shadow_deny(c).decision_record.live_effect=='no_change'
    c=_ctx(); c.flags.update({'VECTOR_SHADOW_DENY_ENABLED':True}); assert simulate_vector_shadow_deny(c).decision_record.live_effect=='no_change'
    c=_ctx(); c.flags.update({'CACHE_SHADOW_DENY_ENABLED':True}); assert simulate_cache_shadow_deny(c).decision_record.live_effect=='no_change'
    c=_ctx(); c.flags.update({'TOOL_SHADOW_DENY_ENABLED':True}); assert simulate_tool_shadow_deny(c).decision_record.live_effect=='no_change'
    c=_ctx(); c.flags.update({'MCP_SHADOW_DENY_ENABLED':True}); assert simulate_mcp_shadow_deny(c).decision_record.live_effect=='no_change'
    c=_ctx(); c.flags.update({'ARTIFACT_SHADOW_DENY_ENABLED':True}); assert simulate_artifact_shadow_deny(c).decision_record.live_effect=='no_change'
    c=_ctx(); c.flags.update({'INGESTION_SHADOW_DENY_ENABLED':True}); assert simulate_ingestion_shadow_deny(c).decision_record.live_effect=='no_change'
