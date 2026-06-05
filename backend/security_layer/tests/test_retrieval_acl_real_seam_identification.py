from __future__ import annotations

from pathlib import Path


PIPELINE_PATH = Path("backend/onyx/context/search/pipeline.py")
NOOP_HOOK_RETURN = "return apply_retrieval_acl_search_pipeline_noop_hook(chunks=censored_chunks)"


def _pipeline_source() -> str:
    assert PIPELINE_PATH.exists(), "Expected Onyx search pipeline file to exist"
    return PIPELINE_PATH.read_text(encoding="utf-8")


def test_real_retrieval_seam_file_exists() -> None:
    assert PIPELINE_PATH.exists()


def test_search_pipeline_function_and_search_chunks_call_are_stable() -> None:
    source = _pipeline_source()

    assert "def search_pipeline(" in source
    assert "retrieved_chunks = search_chunks(" in source
    assert "query_request=query_request" in source
    assert "document_index=document_index" in source
    assert "db_session=db_session" in source


def test_post_retrieval_censoring_and_return_path_are_stable() -> None:
    source = _pipeline_source()

    assert "censored_chunks: list[InferenceChunk] = fetch_ee_implementation_or_noop(" in source
    assert '"onyx.external_permissions.post_query_censoring"' in source
    assert '"_post_query_chunk_censoring"' in source
    assert "chunks=retrieved_chunks" in source
    assert NOOP_HOOK_RETURN in source


def test_real_seam_is_documented_as_observation_only_or_noop_hook_boundary() -> None:
    bundle_i_evidence = Path(
        "docs/security/evidence/bundle_i_real_retrieval_seam_identification.md"
    )
    bundle_k_evidence = Path(
        "docs/security/evidence/bundle_k_real_search_pipeline_noop_hook.md"
    )
    assert bundle_i_evidence.exists(), "Expected Bundle I seam evidence file to exist"
    assert bundle_k_evidence.exists(), "Expected Bundle K no-op hook evidence file to exist"
    bundle_i_content = bundle_i_evidence.read_text(encoding="utf-8")
    bundle_k_content = bundle_k_evidence.read_text(encoding="utf-8")

    assert "backend/onyx/context/search/pipeline.py" in bundle_i_content
    assert "search_pipeline" in bundle_i_content
    assert "retrieved_chunks = search_chunks(" in bundle_i_content
    assert "return censored_chunks" in bundle_i_content
    assert "backend/onyx/context/search/pipeline.py" in bundle_k_content
    assert "apply_retrieval_acl_search_pipeline_noop_hook" in bundle_k_content
    assert "Production readiness remains `NO-GO`" in bundle_k_content
    assert "Enterprise readiness remains `NO-GO`" in bundle_k_content
