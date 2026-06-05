from __future__ import annotations

from pathlib import Path


PIPELINE_PATH = Path("backend/onyx/context/search/pipeline.py")
EVIDENCE_PATH = Path("docs/security/evidence/bundle_j_default_off_noop_seam_hook.md")


def test_noop_hook_target_seam_remains_visible() -> None:
    source = PIPELINE_PATH.read_text(encoding="utf-8")

    assert "def search_pipeline(" in source
    assert "retrieved_chunks = search_chunks(" in source
    assert "return censored_chunks" in source


def test_noop_hook_evidence_preserves_no_live_patch_boundary() -> None:
    assert EVIDENCE_PATH.exists()
    content = EVIDENCE_PATH.read_text(encoding="utf-8")

    assert "apply_retrieval_acl_search_pipeline_noop_hook" in content
    assert "backend/onyx/context/search/pipeline.py" in content
    assert "return censored_chunks" in content
    assert "does not modify live Onyx" in content
    assert "Production readiness remains `NO-GO`" in content
    assert "Enterprise readiness remains `NO-GO`" in content
