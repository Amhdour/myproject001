from __future__ import annotations

from pathlib import Path


RUNBOOK_PATH = Path(
    "docs/security/runbooks/retrieval_acl_shadow_observation_non_production.md"
)
EVIDENCE_PATH = Path(
    "docs/security/evidence/bundle_q_shadow_observation_non_production_runbook.md"
)


def test_shadow_observation_runbook_exists() -> None:
    assert RUNBOOK_PATH.exists()


def test_shadow_observation_runbook_requires_non_production_and_shadow_mode() -> None:
    content = RUNBOOK_PATH.read_text(encoding="utf-8")

    assert "non-production" in content
    assert "export ONYX_SECURITY_RETRIEVAL_ACL_MODE=shadow" in content
    assert "export ONYX_SECURITY_RETRIEVAL_ACL_MODE=off" in content
    assert "Mode is `shadow`" in content
    assert "Mode is `enforce`" in content


def test_shadow_observation_runbook_forbids_sensitive_evidence() -> None:
    content = RUNBOOK_PATH.read_text(encoding="utf-8")

    assert "document content" in content
    assert "document IDs" in content
    assert "user prompts" in content
    assert "credentials" in content
    assert "secrets" in content
    assert "API keys" in content
    assert "PII" in content
    assert "production data" in content


def test_shadow_observation_runbook_preserves_claim_boundaries() -> None:
    content = RUNBOOK_PATH.read_text(encoding="utf-8")

    assert "Production readiness remains `NO-GO`" in content
    assert "Enterprise readiness remains `NO-GO`" in content
    assert "Do not claim live retrieval enforcement" in content
    assert "Do not claim live retrieval filtering" in content
    assert "Do not claim live retrieval blocking" in content
    assert "Do not claim compliance certification" in content


def test_shadow_observation_runbook_evidence_file_preserves_boundaries() -> None:
    assert EVIDENCE_PATH.exists()
    content = EVIDENCE_PATH.read_text(encoding="utf-8")

    assert "Bundle Q" in content
    assert "non-production" in content
    assert "Production readiness remains `NO-GO`" in content
    assert "Enterprise readiness remains `NO-GO`" in content
    assert "does not filter, block, or enforce" in content
