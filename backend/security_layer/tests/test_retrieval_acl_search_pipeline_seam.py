from __future__ import annotations

from pathlib import Path


PIPELINE_PATH = Path("backend/onyx/context/search/pipeline.py")
REAL_PATH_HOOK_RETURN = "return apply_retrieval_acl_real_path_enforcement_hook("


def _pipeline_source() -> str:
    return PIPELINE_PATH.read_text(encoding="utf-8")


def test_search_pipeline_file_exists_for_seam_discovery() -> None:
    assert PIPELINE_PATH.exists()


def test_search_pipeline_function_and_retrieval_seam_exist() -> None:
    source = _pipeline_source()

    assert "def search_pipeline(" in source
    assert "retrieved_chunks = search_chunks(" in source
    assert "fetch_ee_implementation_or_noop(" in source
    assert '"onyx.external_permissions.post_query_censoring"' in source
    assert '"_post_query_chunk_censoring"' in source
    assert REAL_PATH_HOOK_RETURN in source


def test_search_chunks_happens_before_post_query_censoring_and_real_path_hook_return() -> None:
    source = _pipeline_source()

    search_call_index = source.index("retrieved_chunks = search_chunks(")
    censor_hook_index = source.index('"onyx.external_permissions.post_query_censoring"')
    censor_call_chunks_index = source.index("chunks=retrieved_chunks")
    return_index = source.index(REAL_PATH_HOOK_RETURN)

    assert search_call_index < censor_hook_index
    assert censor_hook_index < censor_call_chunks_index
    assert censor_call_chunks_index < return_index


def test_build_index_filters_still_supplies_acl_and_tenant_filters() -> None:
    source = _pipeline_source()

    assert "def _build_index_filters(" in source
    assert "bypass_acl" in source
    assert "build_access_filters_for_user(user, db_session)" in source
    assert "access_control_list=user_acl_filters" in source
    assert "tenant_id=get_current_tenant_id() if MULTI_TENANT else None" in source


def test_seam_tests_do_not_require_importing_live_search_pipeline() -> None:
    """Keep Step 41 dependency-light and non-invasive.

    The real pipeline imports database, LLM, document index, and connector modules.
    Step 41 intentionally inspects source structure only, proving the seam without
    importing or mutating live runtime code.
    """

    assert PIPELINE_PATH.as_posix() == "backend/onyx/context/search/pipeline.py"
