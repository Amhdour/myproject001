from __future__ import annotations

from dataclasses import dataclass

from backend.security.audit.security_audit_logger import InMemorySecurityAuditLogger
from backend.security.audit.security_audit_logger import SecurityAuditEvent
from backend.security.policy.policy_decision import PolicyDecision
from backend.security.policy.policy_decision import SecurityDecisionValue
from backend.security.policy.policy_schema import SecurityContext
from backend.security.policy.security_policy import SecurityPolicy
from backend.security.telemetry.security_metrics import InMemorySecurityMetrics


class SecurityEnforcementError(RuntimeError):
    def __init__(self, decision: PolicyDecision) -> None:
        super().__init__("Security policy blocked this action.")
        self.decision = decision


@dataclass(frozen=True)
class SecurityEnforcementResult:
    decision: PolicyDecision
    audit_event: SecurityAuditEvent
    blocked: bool


class SecurityEnforcer:
    def __init__(
        self,
        *,
        policy: SecurityPolicy | None = None,
        audit_logger: InMemorySecurityAuditLogger | None = None,
        metrics: InMemorySecurityMetrics | None = None,
    ) -> None:
        self.policy = policy or SecurityPolicy()
        self.audit_logger = audit_logger or InMemorySecurityAuditLogger()
        self.metrics = metrics or InMemorySecurityMetrics()

    def evaluate(
        self,
        context: SecurityContext | dict[str, object],
        *,
        enforcement_point: str,
        details: dict[str, object] | None = None,
        demo_attack: bool = False,
    ) -> SecurityEnforcementResult:
        decision, latency_ms = self.policy.evaluate(
            context, enforcement_point=enforcement_point
        )
        fail_closed = decision.reason.startswith("invalid_security_context")
        event = self.audit_logger.emit(decision, details=details)
        self.metrics.record_decision(
            decision,
            latency_ms=latency_ms,
            fail_closed=fail_closed,
            demo_attack=demo_attack,
        )
        return SecurityEnforcementResult(
            decision=decision,
            audit_event=event,
            blocked=decision.blocks_runtime,
        )

    def enforce(
        self,
        context: SecurityContext | dict[str, object],
        *,
        enforcement_point: str,
        details: dict[str, object] | None = None,
        demo_attack: bool = False,
    ) -> SecurityEnforcementResult:
        result = self.evaluate(
            context,
            enforcement_point=enforcement_point,
            details=details,
            demo_attack=demo_attack,
        )
        if result.decision.decision == SecurityDecisionValue.APPROVAL_REQUIRED:
            approved = (
                context.approved if isinstance(context, SecurityContext) else bool(context.get("approved"))
            )
            if not approved:
                raise SecurityEnforcementError(result.decision)
        elif result.decision.decision == SecurityDecisionValue.DENY:
            raise SecurityEnforcementError(result.decision)
        return result
