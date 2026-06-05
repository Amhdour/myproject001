from __future__ import annotations

from pathlib import Path


PIPELINE_PATH = Path("backend/onyx/context/search/pipeline.py")
EVIDENCE_PATH = Path("docs/security/evidence/bundle_k_real_search_pipeline_noop_hook.md")


def _pipeline_source() -> str:
    assert PIPELINE_PATH.exists(), "Expected Onyx search pipeline file to exist"
    return PIPELINE_PATH.read_text(encoding="utf-8")


def test_real_search_pipeline_imports_real_path_enforcement_hook() -> None:
    source = _pipeline_source()

    assert "from backend.security_layer.retrieval_acl.enforce_hook import (" in source
    assert "apply_retrieval_acl_real_path_enforcement_hook," in source


def test_real_search_pipeline_return_path_uses_real_path_hook() -> None:
    source = _pipeline_source()

    assert "censored_chunks: list[InferenceChunk] = fetch_ee_implementation_or_noop(" in source
    assert "return apply_retrieval_acl_real_path_enforcement_hook(" in source
    assert "return censored_chunks" not in source


def test_real_search_pipeline_retrieval_and_censoring_path_remain_visible() -> None:
    source = _pipeline_source()

    assert "def search_pipeline(" in source
    assert "retrieved_chunks = search_chunks(" in source
    assert '"onyx.external_permissions.post_query_censoring"' in source
    assert '"_post_query_chunk_censoring"' in source
    assert "chunks=retrieved_chunks" in source


def test_real_search_pipeline_noop_hook_evidence_preserves_boundaries() -> None:
    assert EVIDENCE_PATH.exists(), "Expected Bundle K evidence file to exist"
    content = EVIDENCE_PATH.read_text(encoding="utf-8")

    assert "backend/onyx/context/search/pipeline.py" in content
    assert "apply_retrieval_acl_search_pipeline_noop_hook" in content
    assert "behavior-preserving" in content
    assert "does not prove live retrieval enforcement" in content
    assert "Production readiness remains `NO-GO`" in content
    assert "Enterprise readiness remains `NO-GO`" in content
