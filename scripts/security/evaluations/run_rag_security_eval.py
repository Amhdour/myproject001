from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
BACKEND_PATH = REPO_ROOT / "backend"
if str(BACKEND_PATH) not in sys.path:
    sys.path.insert(0, str(BACKEND_PATH))

from onyx.security_layer.evaluations import load_datasets  # noqa: E402
from onyx.security_layer.evaluations import PromptfooAdapter  # noqa: E402
from onyx.security_layer.evaluations import RagasAdapter  # noqa: E402
from onyx.security_layer.evaluations import run_local_evaluation  # noqa: E402
from onyx.security_layer.evaluations import write_evidence_documents  # noqa: E402

DEFAULT_DATASET_DIR = (
    REPO_ROOT / "docs/security/evidence/evaluations/datasets"
)
DEFAULT_OUTPUT_DIR = REPO_ROOT / "docs/security/evidence/evaluations"
DEFAULT_DATASET_FILES = [
    DEFAULT_DATASET_DIR / "rag_prompt_injection_cases.json",
    DEFAULT_DATASET_DIR / "cross_tenant_leakage_cases.json",
    DEFAULT_DATASET_DIR / "citation_integrity_cases.json",
    DEFAULT_DATASET_DIR / "gateway_route_cases.json",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the local RAG security evaluation foundation."
    )
    parser.add_argument(
        "--datasets",
        nargs="*",
        type=Path,
        default=DEFAULT_DATASET_FILES,
        help="Dataset JSON files to evaluate.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory where evidence docs should be written.",
    )
    parser.add_argument(
        "--run-ragas",
        action="store_true",
        help="Attempt a dependency-backed Ragas evaluation if ragas is installed.",
    )
    parser.add_argument(
        "--run-promptfoo-cli",
        action="store_true",
        help="Attempt to run the promptfoo CLI if it is installed.",
    )
    return parser.parse_args()


def _serialize_ragas_results(results: list[Any]) -> list[dict[str, Any] | None]:
    serialized: list[dict[str, Any] | None] = []
    for result in results:
        if result is None:
            serialized.append(None)
        else:
            serialized.append(
                {
                    "available": result.available,
                    "metrics": result.metrics,
                    "error": result.error,
                }
            )
    return serialized


def main() -> int:
    args = parse_args()
    datasets = load_datasets(args.datasets)
    run, adapter_status = run_local_evaluation(args.datasets)
    promptfoo = PromptfooAdapter()
    paths = write_evidence_documents(
        run=run,
        output_dir=args.output_dir,
        promptfoo_adapter=promptfoo,
    )

    ragas_results: list[Any] = adapter_status["ragas_results"]
    if args.run_ragas:
        ragas_adapter = RagasAdapter()
        ragas_results = [
            ragas_adapter.evaluate_case(case)
            for dataset in datasets
            for case in dataset.cases
        ]
    promptfoo_cli_result = None
    if args.run_promptfoo_cli:
        promptfoo_cli_result = promptfoo.run_cli(paths["promptfoo_cases"])

    output: dict[str, Any] = {
        "claim_boundary": (
            "Local fixture-based evaluation only. This does not claim production readiness."
        ),
        "datasets": [dataset.dataset_name for dataset in datasets],
        "summary": run.summary,
        "adapter_status": {
            "ragas_available": adapter_status["ragas_available"],
            "promptfoo_cli_available": adapter_status["promptfoo_cli_available"],
        },
        "ragas_results": _serialize_ragas_results(ragas_results),
        "promptfoo_cli_returncode": None
        if promptfoo_cli_result is None
        else promptfoo_cli_result.returncode,
        "written_paths": {key: str(value) for key, value in paths.items()},
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
