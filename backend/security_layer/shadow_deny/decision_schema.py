from dataclasses import asdict
import re
from backend.security_layer.shadow_deny.models import ShadowDenyDecisionRecord

SHADOW_DENY_DECISION_SCHEMA_VERSION = "v1"
REQUIRED_SHADOW_DENY_DECISION_FIELDS = [
"schema_version","decision_id","timestamp","control_family","stage","tenant_id_hash_or_safe_id","workspace_id_hash_or_safe_id","subject_id_hash_or_safe_id","decision_status","simulated_effect","live_effect","monitor_only_decision_id","deny_reason_code","safe_denial_category","finding_ids","metric_names","audit_event_id","evidence_ref","rollback_flag_state","feature_flag_state","non_leakage_validated","created_at",
]
FORBIDDEN_SHADOW_DENY_DECISION_FIELDS = ["query","prompt","document","chunk","secret","api_key","token","credential","private_key","password","tenant_internal","source_internal","policy_internal"]

_PATTERNS=[re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",re.I),re.compile(r"api[_-]?key",re.I),re.compile(r"private[_-]?key",re.I),re.compile(r"password",re.I),re.compile(r"token",re.I)]

def build_shadow_deny_decision_record(**kwargs) -> ShadowDenyDecisionRecord:
    kwargs.setdefault("schema_version", SHADOW_DENY_DECISION_SCHEMA_VERSION)
    rec = ShadowDenyDecisionRecord(**kwargs)
    validate_shadow_deny_decision_record(rec)
    return rec

def validate_shadow_deny_decision_schema_version(record: ShadowDenyDecisionRecord) -> None:
    if record.schema_version != SHADOW_DENY_DECISION_SCHEMA_VERSION:
        raise ValueError("Invalid schema version")

def validate_no_forbidden_shadow_deny_content(record: ShadowDenyDecisionRecord) -> None:
    raw = str(asdict(record))
    for word in FORBIDDEN_SHADOW_DENY_DECISION_FIELDS:
        if word in raw.lower():
            raise ValueError(f"Forbidden content token: {word}")
    for p in _PATTERNS:
        if p.search(raw):
            raise ValueError("Forbidden sensitive content")

def validate_shadow_deny_decision_record(record: ShadowDenyDecisionRecord) -> None:
    data = asdict(record)
    for f in REQUIRED_SHADOW_DENY_DECISION_FIELDS:
        if f not in data:
            raise ValueError(f"Missing field: {f}")
    validate_shadow_deny_decision_schema_version(record)
    validate_no_forbidden_shadow_deny_content(record)

def sanitize_shadow_deny_decision_record(record: ShadowDenyDecisionRecord) -> ShadowDenyDecisionRecord:
    data = asdict(record)
    for k,v in data.items():
        if isinstance(v,str):
            data[k]=v.replace("@","[at]")
    sanitized=ShadowDenyDecisionRecord(**data)
    validate_shadow_deny_decision_record(sanitized)
    return sanitized
