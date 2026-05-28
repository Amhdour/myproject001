import pytest
from backend.security_layer.shadow_deny.decision_schema import *

def _record(**ov):
    base=dict(decision_id='d1',timestamp='2026-01-01T00:00:00Z',control_family='retrieval',stage='decision',tenant_id_hash_or_safe_id='tenant_safe',workspace_id_hash_or_safe_id='workspace_safe',subject_id_hash_or_safe_id='subject_safe',decision_status='noop',simulated_effect='no_change',live_effect='no_change',monitor_only_decision_id='m1',deny_reason_code='r',safe_denial_category='category_safe',finding_ids=[],metric_names=[],audit_event_id='a1',evidence_ref='e1',rollback_flag_state='disabled',feature_flag_state='disabled',non_leakage_validated=True,created_at='2026-01-01T00:00:00Z')
    base.update(ov)
    return build_shadow_deny_decision_record(**base)

def test_all_22_fields_present():
    r=_record()
    assert len(r.__dict__)==22

def test_forbidden_content_rejected():
    with pytest.raises(ValueError): _record(safe_denial_category='password leak')
    with pytest.raises(ValueError): _record(safe_denial_category='a@example.com')
