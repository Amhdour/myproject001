from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator

from backend.security.policy.policy_decision import SecurityRiskLevel


SUPPORTED_ACTIONS = frozenset(
    {
        "retrieval.read",
        "document.access",
        "tool.execute",
        "artifact.download",
        "sandbox.execute",
    }
)


class SecurityContext(BaseModel):
    model_config = ConfigDict(extra="allow")

    user_id: str | None
    tenant_id: str | None
    resource_type: str
    resource_id: str
    action: str
    source: str
    risk_level: SecurityRiskLevel
    correlation_id: str
    resource_tenant_id: str | None = None
    approved: bool = False
    monitor_only: bool = False
    redacted_details: dict[str, str | int | float | bool | None] = Field(
        default_factory=dict
    )

    @field_validator("resource_type", "resource_id", "action", "source", "correlation_id")
    @classmethod
    def required_string_must_not_be_blank(cls, value: str) -> str:
        if not value or value.strip() == "":
            raise ValueError("required security context value must not be blank")
        return value
