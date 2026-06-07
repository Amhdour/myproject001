from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel
from pydantic import Field


class RagSecurityMetricName(str, Enum):
    UNAUTHORIZED_CONTEXT_PRESENT = "unauthorized_context_present"
    UNAUTHORIZED_CITATION_PRESENT = "unauthorized_citation_present"
    PROMPT_INJECTION_CONTEXT_USED = "prompt_injection_context_used"
    SECRET_OR_PII_LEAKED = "secret_or_pii_leaked"
    POLICY_DECISION_CORRECT = "policy_decision_correct"
    ANSWER_SUPPORTED_BY_AUTHORIZED_SOURCES = (
        "answer_supported_by_authorized_sources"
    )


class RagSecurityContext(BaseModel):
    source_id: str
    tenant_id: str
    text: str
    citation_id: str | None = None
    authorized: bool = True
    prompt_injection: bool = False
    contains_secret_or_pii: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)


class RagSecurityCase(BaseModel):
    case_id: str
    title: str
    question: str
    answer: str
    retrieved_contexts: list[RagSecurityContext]
    citations: list[str] = Field(default_factory=list)
    authorized_source_ids: list[str] = Field(default_factory=list)
    support_phrases: list[str] = Field(default_factory=list)
    expected_policy_decision: str | None = None
    observed_policy_decision: str | None = None
    route_target: str | None = None
    notes: str | None = None


class RagSecurityDataset(BaseModel):
    dataset_name: str
    description: str
    cases: list[RagSecurityCase]


class RagSecurityMetricResult(BaseModel):
    metric_name: RagSecurityMetricName
    passed: bool
    detail: str | None = None


class RagSecurityCaseResult(BaseModel):
    case_id: str
    dataset_name: str
    title: str
    metric_results: list[RagSecurityMetricResult]
    score: float

    @property
    def metrics(self) -> dict[str, bool]:
        return {
            result.metric_name.value: result.passed for result in self.metric_results
        }


class RagSecurityEvaluationRun(BaseModel):
    generated_at_utc: str
    datasets: list[RagSecurityDataset]
    case_results: list[RagSecurityCaseResult]
    summary: dict[str, float | int | str]
