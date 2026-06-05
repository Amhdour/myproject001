from __future__ import annotations

from pathlib import Path


PIPELINE_PATH = Path("backend/onyx/context/search/pipeline.py")


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
    assert "return censored_chunks" in source


def test_real_seam_is_documented_as_observation_only_not_live_patch() -> None:
    evidence = Path(
        "docs/security/evidence/bundle_i_real_retrieval_seam_identification.md"
    )
    assert evidence.exists(), "Expected Bundle I seam evidence file to exist"
    content = evidence.read_text(encoding="utf-8")

    assert "backend/onyx/context/search/pipeline.py" in content
    assert "search_pipeline" in content
    assert "retrieved_chunks = search_chunks(" in content
    assert "return censored_chunks" in content
    assert "does not modify live Onyx" in content
    assert "Production readiness remains `NO-GO`" in content
    assert "Enterprise readiness remains `NO-GO`" in content
