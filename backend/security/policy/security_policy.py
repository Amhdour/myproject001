from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter

from pydantic import ValidationError

from backend.security.policy.policy_decision import PolicyDecision
from backend.security.policy.policy_decision import SecurityDecisionValue
from backend.security.policy.policy_decision import SecurityRiskLevel
from backend.security.policy.policy_schema import SUPPORTED_ACTIONS
from backend.security.policy.policy_schema import SecurityContext

DEFAULT_POLICY_VERSION = "portfolio-readiness-mvp-v1"


@dataclass(frozen=True)
class SecurityPolicy:
    policy_version: str = DEFAULT_POLICY_VERSION

    def evaluate(
        self,
        raw_context: SecurityContext | dict[str, object],
        *,
        enforcement_point: str = "security_policy.evaluate",
    ) -> tuple[PolicyDecision, float]:
        started = perf_counter()
        try:
            context = (
                raw_context
                if isinstance(raw_context, SecurityContext)
                else SecurityContext.model_validate(raw_context)
            )
        except ValidationError as exc:
            decision = self._decision_from_invalid_context(
                raw_context,
                reason=f"invalid_security_context:{exc.errors()[0]['type']}",
                enforcement_point=enforcement_point,
            )
            return decision, (perf_counter() - started) * 1000

        decision = self._evaluate_valid_context(context, enforcement_point)
        return decision, (perf_counter() - started) * 1000

    def _evaluate_valid_context(
        self, context: SecurityContext, enforcement_point: str
    ) -> PolicyDecision:
        if context.monitor_only:
            return self._decision(
                context,
                SecurityDecisionValue.MONITOR_ONLY,
                "monitor_only_mode_observed",
                enforcement_point,
            )
        if not context.user_id:
            return self._decision(
                context,
                SecurityDecisionValue.DENY,
                "missing_user_id_default_deny",
                enforcement_point,
            )
        if not context.tenant_id:
            return self._decision(
                context,
                SecurityDecisionValue.DENY,
                "missing_tenant_id_default_deny",
                enforcement_point,
            )
        if context.action not in SUPPORTED_ACTIONS:
            return self._decision(
                context,
                SecurityDecisionValue.DENY,
                "unknown_action_default_deny",
                enforcement_point,
            )
        if (
            context.resource_tenant_id
            and context.resource_tenant_id != context.tenant_id
        ):
            return self._decision(
                context,
                SecurityDecisionValue.DENY,
                "cross_tenant_access_default_deny",
                enforcement_point,
            )
        if (
            context.action in {"tool.execute", "sandbox.execute"}
            and context.risk_level in {SecurityRiskLevel.HIGH, SecurityRiskLevel.CRITICAL}
            and not context.approved
        ):
            return self._decision(
                context,
                SecurityDecisionValue.APPROVAL_REQUIRED,
                "high_risk_action_requires_approval",
                enforcement_point,
            )
        return self._decision(
            context,
            SecurityDecisionValue.ALLOW,
            "policy_allow_same_tenant_known_action",
            enforcement_point,
        )

    def _decision(
        self,
        context: SecurityContext,
        decision: SecurityDecisionValue,
        reason: str,
        enforcement_point: str,
    ) -> PolicyDecision:
        return PolicyDecision(
            decision=decision,
            reason=reason,
            policy_version=self.policy_version,
            risk_level=context.risk_level,
            correlation_id=context.correlation_id,
            enforcement_point=enforcement_point,
            action=context.action,
            resource_type=context.resource_type,
            resource_id=context.resource_id,
            user_id=context.user_id,
            tenant_id=context.tenant_id,
        )

    def _decision_from_invalid_context(
        self,
        raw_context: SecurityContext | dict[str, object],
        *,
        reason: str,
        enforcement_point: str,
    ) -> PolicyDecision:
        context = (
            raw_context if isinstance(raw_context, dict) else raw_context.model_dump()
        )
        return PolicyDecision(
            decision=SecurityDecisionValue.DENY,
            reason=reason,
            policy_version=self.policy_version,
            risk_level=SecurityRiskLevel.CRITICAL,
            correlation_id=str(
                context.get("correlation_id") or "missing-correlation-id"
            ),
            enforcement_point=enforcement_point,
            action=str(context.get("action") or "unknown"),
            resource_type=str(context.get("resource_type") or "unknown"),
            resource_id=str(context.get("resource_id") or "unknown"),
            user_id=str(context["user_id"]) if context.get("user_id") else None,
            tenant_id=str(context["tenant_id"]) if context.get("tenant_id") else None,
        )
