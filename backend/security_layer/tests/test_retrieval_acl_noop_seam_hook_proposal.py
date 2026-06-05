from __future__ import annotations

from pathlib import Path


PIPELINE_PATH = Path("backend/onyx/context/search/pipeline.py")
EVIDENCE_PATH = Path("docs/security/evidence/bundle_j_default_off_noop_seam_hook.md")
BUNDLE_K_EVIDENCE_PATH = Path("docs/security/evidence/bundle_k_real_search_pipeline_noop_hook.md")
NOOP_HOOK_RETURN = "return apply_retrieval_acl_search_pipeline_noop_hook(chunks=censored_chunks)"


def test_noop_hook_target_seam_remains_visible() -> None:
    source = PIPELINE_PATH.read_text(encoding="utf-8")

    assert "def search_pipeline(" in source
    assert "retrieved_chunks = search_chunks(" in source
    assert NOOP_HOOK_RETURN in source


def test_noop_hook_evidence_preserves_no_live_enforcement_boundary() -> None:
    assert EVIDENCE_PATH.exists()
    assert BUNDLE_K_EVIDENCE_PATH.exists()
    bundle_j_content = EVIDENCE_PATH.read_text(encoding="utf-8")
    bundle_k_content = BUNDLE_K_EVIDENCE_PATH.read_text(encoding="utf-8")

    assert "apply_retrieval_acl_search_pipeline_noop_hook" in bundle_j_content
    assert "backend/onyx/context/search/pipeline.py" in bundle_j_content
    assert "return censored_chunks" in bundle_j_content
    assert "apply_retrieval_acl_search_pipeline_noop_hook" in bundle_k_content
    assert "does not prove live retrieval enforcement" in bundle_k_content
    assert "Production readiness remains `NO-GO`" in bundle_k_content
    assert "Enterprise readiness remains `NO-GO`" in bundle_k_content
