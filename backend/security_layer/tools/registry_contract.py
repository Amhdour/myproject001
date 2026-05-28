from __future__ import annotations

import re

TOOL_REGISTRY_SCHEMA_VERSION = "1.0"
REQUIRED_TOOL_REGISTRY_FIELDS = [
    "tool_id","tool_name","tool_version","tool_owner","tool_category","tool_risk_tier","tool_status",
    "allowed_tenant_scope","allowed_workspace_scope","required_user_permissions","required_group_permissions",
    "required_role_permissions","service_account_allowed","delegated_credential_required","delegated_credential_scope",
    "approval_required","approval_risk_level","argument_schema_id","result_safety_policy_id","audit_required",
    "finding_required_on_violation","metric_required","default_effect","metadata_schema_version","tool_description_placeholder",
]
OPTIONAL_TOOL_REGISTRY_FIELDS = ["notes"]
FORBIDDEN_TOOL_REGISTRY_FIELDS = ["credential","api_key","token","password","private_key","secret"]


_PATTERNS = [r"sk-[A-Za-z0-9]{10,}", r"-----BEGIN PRIVATE KEY-----", r"password\s*=", r"token\s*=", r"api[_-]?key", r"[\w.-]+@[\w.-]+\.[A-Za-z]{2,}", r"https?://[^\s]*:[^\s]*@"]


def sanitize_tool_registry_entry(entry: dict[str, object]) -> dict[str, object]:
    sanitized = {}
    for k, v in entry.items():
        if k in FORBIDDEN_TOOL_REGISTRY_FIELDS:
            continue
        sanitized[k] = v
    return sanitized


def validate_tool_registry_schema_version(entry: dict[str, object]) -> None:
    if entry.get("metadata_schema_version") != TOOL_REGISTRY_SCHEMA_VERSION:
        raise ValueError("invalid registry schema version")


def validate_no_forbidden_tool_registry_content(entry: dict[str, object]) -> None:
    for key, value in entry.items():
        lower_key = key.lower()
        if lower_key in FORBIDDEN_TOOL_REGISTRY_FIELDS:
            raise ValueError("forbidden registry field")
        text = str(value)
        for pattern in _PATTERNS:
            if re.search(pattern, text, flags=re.IGNORECASE):
                raise ValueError("forbidden registry content")


def validate_tool_registry_entry(entry: dict[str, object]) -> None:
    missing = [f for f in REQUIRED_TOOL_REGISTRY_FIELDS if f not in entry]
    if missing:
        raise ValueError(f"missing required fields: {missing}")
    validate_tool_registry_schema_version(entry)
    validate_no_forbidden_tool_registry_content(entry)


def build_safe_tool_registry_entry(**kwargs: object) -> dict[str, object]:
    entry = sanitize_tool_registry_entry(kwargs)
    validate_tool_registry_entry(entry)
    return entry
