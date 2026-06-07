from __future__ import annotations

import json
import shutil
import subprocess
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from onyx.security_layer.evaluations.models import RagSecurityCase
from onyx.security_layer.evaluations.models import RagSecurityDataset


class PromptfooAdapter:
    def __init__(self) -> None:
        self._cli_path = shutil.which("promptfoo")

    @property
    def cli_available(self) -> bool:
        return self._cli_path is not None

    def build_case(
        self, case: RagSecurityCase, *, dataset_name: str
    ) -> dict[str, Any]:
        return {
            "description": case.case_id,
            "vars": {
                "case_id": case.case_id,
                "dataset_name": dataset_name,
                "question": case.question,
                "answer": case.answer,
                "retrieved_contexts": [
                    {
                        "source_id": context.source_id,
                        "tenant_id": context.tenant_id,
                        "authorized": context.authorized,
                        "prompt_injection": context.prompt_injection,
                        "contains_secret_or_pii": context.contains_secret_or_pii,
                        "text": context.text,
                        "citation_id": context.citation_id,
                    }
                    for context in case.retrieved_contexts
                ],
                "citations": case.citations,
                "authorized_source_ids": case.authorized_source_ids,
                "support_phrases": case.support_phrases,
                "expected_policy_decision": case.expected_policy_decision,
                "observed_policy_decision": case.observed_policy_decision,
                "route_target": case.route_target,
            },
            "assert": [
                {
                    "type": "equals",
                    "value": {
                        "authorized_source_ids": case.authorized_source_ids,
                    },
                }
            ],
        }

    def build_bundle(self, datasets: Sequence[RagSecurityDataset]) -> dict[str, Any]:
        tests = [
            self.build_case(case, dataset_name=dataset.dataset_name)
            for dataset in datasets
            for case in dataset.cases
        ]
        return {
            "description": "Onyx RAG security regression cases",
            "tests": tests,
            "metadata": {
                "dataset_names": [dataset.dataset_name for dataset in datasets],
                "claim_boundary": (
                    "Fixture-based promptfoo-style cases only; promptfoo CLI execution is optional."
                ),
            },
        }

    def validate_bundle(self, bundle: dict[str, Any]) -> list[str]:
        errors: list[str] = []
        if not isinstance(bundle.get("tests"), list):
            errors.append("bundle.tests must be a list")
            return errors
        for index, test in enumerate(bundle["tests"]):
            if not isinstance(test, dict):
                errors.append(f"test[{index}] must be a mapping")
                continue
            if "description" not in test:
                errors.append(f"test[{index}] is missing description")
            if not isinstance(test.get("vars"), dict):
                errors.append(f"test[{index}].vars must be a mapping")
        return errors

    def write_yaml(self, bundle: dict[str, Any], output_path: Path) -> Path:
        output_path.write_text(
            json.dumps(bundle, indent=2, sort_keys=False), encoding="utf-8"
        )
        return output_path

    def write_json(self, bundle: dict[str, Any], output_path: Path) -> Path:
        output_path.write_text(
            json.dumps(bundle, indent=2, sort_keys=True), encoding="utf-8"
        )
        return output_path

    def run_cli(self, bundle_path: Path) -> subprocess.CompletedProcess[str] | None:
        if not self.cli_available:
            return None
        assert self._cli_path is not None
        return subprocess.run(
            [self._cli_path, "eval", str(bundle_path)],
            check=False,
            capture_output=True,
            text=True,
        )
