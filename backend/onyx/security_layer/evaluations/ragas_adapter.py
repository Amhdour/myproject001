from __future__ import annotations

import importlib.util
from dataclasses import dataclass
from typing import Any

from onyx.security_layer.evaluations.models import RagSecurityCase
from onyx.security_layer.evaluations.models import RagSecurityDataset


def _ragas_available() -> bool:
    return importlib.util.find_spec("ragas") is not None


@dataclass(frozen=True)
class RagasCaseResult:
    available: bool
    metrics: dict[str, float]
    error: str | None = None


class RagasAdapter:
    def __init__(self) -> None:
        self._available = _ragas_available()

    @property
    def available(self) -> bool:
        return self._available

    def evaluate_case(self, case: RagSecurityCase) -> RagasCaseResult | None:
        if not self.available:
            return None
        try:
            from ragas import evaluate  # type: ignore[import-not-found]
            from ragas import EvaluationDataset  # type: ignore[import-not-found]
            from ragas import SingleTurnSample  # type: ignore[import-not-found]
            from ragas.metrics import Faithfulness  # type: ignore[import-not-found]
            from ragas.metrics import (
                ResponseRelevancy,  # type: ignore[import-not-found]
            )
        except Exception as exc:  # pragma: no cover - dependency-specific
            return RagasCaseResult(available=False, metrics={}, error=str(exc))

        contexts = [context.text for context in case.retrieved_contexts if context.authorized]
        reference = " ".join(case.support_phrases) or None
        sample = SingleTurnSample(
            user_input=case.question,
            retrieved_contexts=contexts,
            response=case.answer,
            reference=reference,
        )
        dataset = EvaluationDataset([sample])
        try:
            result: Any = evaluate(dataset, metrics=[ResponseRelevancy(), Faithfulness()])
        except Exception as exc:  # pragma: no cover - dependency-specific
            return RagasCaseResult(available=False, metrics={}, error=str(exc))
        metrics: dict[str, float] = {}
        for metric_name in ("answer_relevancy", "faithfulness"):
            value: object | None = None
            if isinstance(result, dict):
                value = result.get(metric_name)
            elif hasattr(result, metric_name):
                value = getattr(result, metric_name)
            elif hasattr(result, "scores"):
                scores = getattr(result, "scores")
                if isinstance(scores, dict):
                    value = scores.get(metric_name)
            if isinstance(value, (int, float)):
                metrics[metric_name] = float(value)
        return RagasCaseResult(available=True, metrics=metrics)

    def evaluate_dataset(
        self, dataset: RagSecurityDataset
    ) -> list[RagasCaseResult | None]:
        return [self.evaluate_case(case) for case in dataset.cases]
