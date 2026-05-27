from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from enum import Enum
from typing import Any


class DenialCategory(str, Enum):
    ACCESS_DENIED = "access_denied"
    POLICY_DENIED = "policy_denied"
    APPROVAL_REQUIRED = "approval_required"
    UNSAFE_ARTIFACT_BLOCKED = "unsafe_artifact_blocked"
    UNSAFE_TOOL_BLOCKED = "unsafe_tool_blocked"
    UNSAFE_MCP_BLOCKED = "unsafe_mcp_blocked"
    UNSAFE_SANDBOX_BLOCKED = "unsafe_sandbox_blocked"
    RETRIEVAL_DENIED = "retrieval_denied"
    TENANT_CONTEXT_MISSING = "tenant_context_missing"
    SUBJECT_CONTEXT_MISSING = "subject_context_missing"
    POLICY_ENGINE_UNAVAILABLE = "policy_engine_unavailable"
    VALIDATION_FAILED = "validation_failed"
    RATE_OR_QUOTA_BLOCKED = "rate_or_quota_blocked"
    ADMIN_ACTION_DENIED = "admin_action_denied"


class SafeErrorCode(str, Enum):
    SECURITY_ACCESS_DENIED = "security_access_denied"
    SECURITY_POLICY_DENIED = "security_policy_denied"
    SECURITY_APPROVAL_REQUIRED = "security_approval_required"
    SECURITY_UNSAFE_ARTIFACT_BLOCKED = "security_unsafe_artifact_blocked"
    SECURITY_UNSAFE_TOOL_BLOCKED = "security_unsafe_tool_blocked"
    SECURITY_UNSAFE_MCP_BLOCKED = "security_unsafe_mcp_blocked"
    SECURITY_UNSAFE_SANDBOX_BLOCKED = "security_unsafe_sandbox_blocked"
    SECURITY_RETRIEVAL_DENIED = "security_retrieval_denied"
    SECURITY_TENANT_CONTEXT_MISSING = "security_tenant_context_missing"
    SECURITY_SUBJECT_CONTEXT_MISSING = "security_subject_context_missing"
    SECURITY_POLICY_ENGINE_UNAVAILABLE = "security_policy_engine_unavailable"
    SECURITY_VALIDATION_FAILED = "security_validation_failed"
    SECURITY_RATE_OR_QUOTA_BLOCKED = "security_rate_or_quota_blocked"
    SECURITY_ADMIN_ACTION_DENIED = "security_admin_action_denied"


_CATEGORY_TO_CODE: dict[DenialCategory, SafeErrorCode] = {
    DenialCategory.ACCESS_DENIED: SafeErrorCode.SECURITY_ACCESS_DENIED,
    DenialCategory.POLICY_DENIED: SafeErrorCode.SECURITY_POLICY_DENIED,
    DenialCategory.APPROVAL_REQUIRED: SafeErrorCode.SECURITY_APPROVAL_REQUIRED,
    DenialCategory.UNSAFE_ARTIFACT_BLOCKED: SafeErrorCode.SECURITY_UNSAFE_ARTIFACT_BLOCKED,
    DenialCategory.UNSAFE_TOOL_BLOCKED: SafeErrorCode.SECURITY_UNSAFE_TOOL_BLOCKED,
    DenialCategory.UNSAFE_MCP_BLOCKED: SafeErrorCode.SECURITY_UNSAFE_MCP_BLOCKED,
    DenialCategory.UNSAFE_SANDBOX_BLOCKED: SafeErrorCode.SECURITY_UNSAFE_SANDBOX_BLOCKED,
    DenialCategory.RETRIEVAL_DENIED: SafeErrorCode.SECURITY_RETRIEVAL_DENIED,
    DenialCategory.TENANT_CONTEXT_MISSING: SafeErrorCode.SECURITY_TENANT_CONTEXT_MISSING,
    DenialCategory.SUBJECT_CONTEXT_MISSING: SafeErrorCode.SECURITY_SUBJECT_CONTEXT_MISSING,
    DenialCategory.POLICY_ENGINE_UNAVAILABLE: SafeErrorCode.SECURITY_POLICY_ENGINE_UNAVAILABLE,
    DenialCategory.VALIDATION_FAILED: SafeErrorCode.SECURITY_VALIDATION_FAILED,
    DenialCategory.RATE_OR_QUOTA_BLOCKED: SafeErrorCode.SECURITY_RATE_OR_QUOTA_BLOCKED,
    DenialCategory.ADMIN_ACTION_DENIED: SafeErrorCode.SECURITY_ADMIN_ACTION_DENIED,
}

_SAFE_USER_MESSAGES: dict[DenialCategory, str] = {
    DenialCategory.ACCESS_DENIED: "Request blocked by security controls.",
    DenialCategory.POLICY_DENIED: "Request blocked by security policy.",
    DenialCategory.APPROVAL_REQUIRED: "Request requires administrative approval.",
    DenialCategory.UNSAFE_ARTIFACT_BLOCKED: "Request blocked by security policy.",
    DenialCategory.UNSAFE_TOOL_BLOCKED: "Request blocked by security policy.",
    DenialCategory.UNSAFE_MCP_BLOCKED: "Request blocked by security policy.",
    DenialCategory.UNSAFE_SANDBOX_BLOCKED: "Request blocked by security policy.",
    DenialCategory.RETRIEVAL_DENIED: "Request blocked by security policy.",
    DenialCategory.TENANT_CONTEXT_MISSING: "Request cannot be processed securely.",
    DenialCategory.SUBJECT_CONTEXT_MISSING: "Request cannot be processed securely.",
    DenialCategory.POLICY_ENGINE_UNAVAILABLE: "Request cannot be processed securely.",
    DenialCategory.VALIDATION_FAILED: "Request failed security validation.",
    DenialCategory.RATE_OR_QUOTA_BLOCKED: "Request temporarily blocked by security controls.",
    DenialCategory.ADMIN_ACTION_DENIED: "Administrative action denied by security policy.",
}


@dataclass(frozen=True)
class DenialPayload:
    category: DenialCategory
    error_code: SafeErrorCode
    message: str
    admin_summary: str

    def to_dict(self) -> dict[str, str]:
        return {
            "category": self.category.value,
            "error_code": self.error_code.value,
            "message": self.message,
            "admin_summary": self.admin_summary,
        }


@dataclass(frozen=True)
class SecurityDenial(Exception):
    payload: DenialPayload

    @property
    def message(self) -> str:
        return self.payload.message

    @property
    def reason_code(self) -> str:
        return self.payload.error_code.value

    def __str__(self) -> str:
        return self.payload.message


def _normalize_category(category: DenialCategory | str | None) -> DenialCategory:
    if category is None:
        return DenialCategory.ACCESS_DENIED
    if isinstance(category, DenialCategory):
        return category
    legacy_map = {
        "missing_subject": DenialCategory.SUBJECT_CONTEXT_MISSING,
        "missing_tenant": DenialCategory.TENANT_CONTEXT_MISSING,
        "evaluation_error": DenialCategory.POLICY_DENIED,
        "evaluator_unavailable": DenialCategory.POLICY_ENGINE_UNAVAILABLE,
        "security_denied": DenialCategory.POLICY_DENIED,
        "denied": DenialCategory.POLICY_DENIED,
    }
    mapped = legacy_map.get(category, category)
    return DenialCategory(mapped)


def redact_for_denial(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, Exception):
        return "[redacted]"
    if isinstance(value, DenialPayload):
        return "[redacted]"
    if isinstance(value, dict):
        return "[redacted]"
    if hasattr(value, "__dataclass_fields__"):
        return "[redacted]"
    return "[redacted]"


def safe_denial_message(category: DenialCategory | str | None = None) -> str:
    return _SAFE_USER_MESSAGES[_normalize_category(category)]


def safe_admin_summary(category: DenialCategory | str, reason: Any | None = None) -> str:
    normalized = _normalize_category(category)
    reason_fragment = f"; reason={redact_for_denial(reason)}" if reason is not None else ""
    return f"safe_denial:{normalized.value}{reason_fragment}"


def build_denial_payload(category: DenialCategory | str, reason: Any | None = None) -> DenialPayload:
    normalized = _normalize_category(category)
    return DenialPayload(
        category=normalized,
        error_code=_CATEGORY_TO_CODE[normalized],
        message=safe_denial_message(normalized),
        admin_summary=safe_admin_summary(normalized, reason),
    )


def approval_required_payload(reason: Any | None = None) -> dict[str, Any]:
    payload = build_denial_payload(DenialCategory.APPROVAL_REQUIRED, reason)
    response = payload.to_dict()
    response["approval_required"] = True
    response["approval_status"] = "pending"
    return response


def validation_failed_payload(reason: Any | None = None) -> dict[str, Any]:
    return build_denial_payload(DenialCategory.VALIDATION_FAILED, reason).to_dict()


def policy_engine_unavailable_payload(reason: Any | None = None) -> dict[str, Any]:
    return build_denial_payload(DenialCategory.POLICY_ENGINE_UNAVAILABLE, reason).to_dict()


def rate_or_quota_blocked_payload(reason: Any | None = None) -> dict[str, Any]:
    return build_denial_payload(DenialCategory.RATE_OR_QUOTA_BLOCKED, reason).to_dict()


def raise_security_denial(category: DenialCategory | str | None = None, reason: Any | None = None) -> None:
    raise SecurityDenial(payload=build_denial_payload(category or DenialCategory.ACCESS_DENIED, reason))
