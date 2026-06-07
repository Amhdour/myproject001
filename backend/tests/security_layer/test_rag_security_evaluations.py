from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path

from onyx.security_layer.evaluations import evaluate_datasets
from onyx.security_layer.evaluations import load_dataset
from onyx.security_layer.evaluations import PromptfooAdapter
from onyx.security_layer.evaluations import RagasAdapter
from onyx.security_layer.evaluations import write_evidence_documents

REPO_ROOT = Path(__file__).resolve().parents[3]
DATASET_DIR = REPO_ROOT / "docs/security/evidence/evaluations/datasets"
DATASET_PATHS = [
    DATASET_DIR / "rag_prompt_injection_cases.json",
    DATASET_DIR / "cross_tenant_leakage_cases.json",
    DATASET_DIR / "citation_integrity_cases.json",
    DATASET_DIR / "gateway_route_cases.json",
]


def test_local_fixture_evaluation_metrics() -> None:
    datasets = [load_dataset(path) for path in DATASET_PATHS]
    run = evaluate_datasets(datasets)
    case_results = {result.case_id: result for result in run.case_results}

    rag_pi = case_results["rag-pi-001"].metrics
    assert rag_pi["unauthorized_context_present"] is True
    assert rag_pi["unauthorized_citation_present"] is True
    assert rag_pi["prompt_injection_context_used"] is True
    assert rag_pi["secret_or_pii_leaked"] is False
    assert rag_pi["policy_decision_correct"] is True
    assert rag_pi["answer_supported_by_authorized_sources"] is True

    cross_tenant = case_results["x-tenant-001"].metrics
    assert cross_tenant["unauthorized_context_present"] is True
    assert cross_tenant["unauthorized_citation_present"] is True
    assert cross_tenant["prompt_injection_context_used"] is False
    assert cross_tenant["secret_or_pii_leaked"] is True

    citation = case_results["cite-001"].metrics
    assert citation["unauthorized_citation_present"] is True
    assert citation["answer_supported_by_authorized_sources"] is False

    gateway = case_results["gateway-001"].metrics
    assert gateway["policy_decision_correct"] is False

    assert run.summary["case_count"] == 8
    assert run.summary["unauthorized_context_present_count"] == 3
    assert run.summary["unauthorized_citation_present_count"] == 3


def test_promptfoo_adapter_generates_and_writes_bundle(tmp_path: Path) -> None:
    datasets = [load_dataset(path) for path in DATASET_PATHS]
    adapter = PromptfooAdapter()
    bundle = adapter.build_bundle(datasets)

    assert adapter.validate_bundle(bundle) == []
    assert len(bundle["tests"]) == 8

    yaml_path = tmp_path / "promptfoo_cases.yaml"
    json_path = tmp_path / "promptfoo_cases.json"
    adapter.write_yaml(bundle, yaml_path)
    adapter.write_json(bundle, json_path)

    assert yaml_path.exists()
    assert json_path.exists()
    assert "rag-pi-001" in yaml_path.read_text(encoding="utf-8")
    assert json_path.read_text(encoding="utf-8").startswith("{")


def test_promptfoo_adapter_safe_when_cli_missing(monkeypatch) -> None:
    monkeypatch.setattr(shutil, "which", lambda _: None)
    adapter = PromptfooAdapter()
    assert adapter.cli_available is False
    assert adapter.run_cli(Path("/tmp/nonexistent-promptfoo.yaml")) is None


def test_ragas_adapter_safe_when_dependency_missing(monkeypatch) -> None:
    monkeypatch.setattr(importlib.util, "find_spec", lambda _: None)
    adapter = RagasAdapter()
    datasets = [load_dataset(path) for path in DATASET_PATHS]
    assert adapter.available is False
    assert adapter.evaluate_case(datasets[0].cases[0]) is None


def test_evidence_docs_are_written(tmp_path: Path) -> None:
    datasets = [load_dataset(path) for path in DATASET_PATHS]
    run = evaluate_datasets(datasets)
    paths = write_evidence_documents(run=run, output_dir=tmp_path)

    assert paths["eval_results"].exists()
    assert paths["limitations"].exists()
    assert paths["reproduction_commands"].exists()
    assert paths["promptfoo_cases"].exists()
    assert "RAG Security Evaluation Results" in paths["eval_results"].read_text(
        encoding="utf-8"
    )
