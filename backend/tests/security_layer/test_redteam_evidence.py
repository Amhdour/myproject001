from __future__ import annotations

import importlib.util
from pathlib import Path

from onyx.security_layer.redteam import build_redteam_summary
from onyx.security_layer.redteam import GarakAdapter
from onyx.security_layer.redteam import get_control_mapping
from onyx.security_layer.redteam import PyritAdapter
from onyx.security_layer.redteam import RedteamFindingCategory
from onyx.security_layer.redteam import render_findings_to_controls_markdown
from onyx.security_layer.redteam.garak_adapter import GARAK_LIMITATION
from onyx.security_layer.redteam.pyrit_adapter import PYRIT_LIMITATION

REPO_ROOT = Path(__file__).resolve().parents[3]
FIXTURE_DIR = REPO_ROOT / "docs/security/evidence/redteam/fixtures"
PYRIT_FIXTURES = [
    FIXTURE_DIR / "pyrit_prompt_injection_campaign.json",
    FIXTURE_DIR / "pyrit_tool_abuse_campaign.json",
]
GARAK_FIXTURES = [
    FIXTURE_DIR / "garak_prompt_injection_report.json",
    FIXTURE_DIR / "garak_data_leakage_report.json",
]


def test_pyrit_adapter_safe_when_dependency_missing(monkeypatch) -> None:
    monkeypatch.setattr(importlib.util, "find_spec", lambda _: None)
    adapter = PyritAdapter()
    bundle = adapter.parse_fixture_campaign(PYRIT_FIXTURES[0])

    assert adapter.available is False
    assert bundle.adapter_status.dependency_available is False
    assert bundle.adapter_status.fixture_mode is True
    assert PYRIT_LIMITATION in bundle.adapter_status.limitation
    assert {finding.category for finding in bundle.findings} == {
        RedteamFindingCategory.PROMPT_INJECTION,
        RedteamFindingCategory.RAW_EVIDENCE_LEAKAGE,
    }


def test_garak_adapter_safe_when_dependency_missing(monkeypatch) -> None:
    monkeypatch.setattr(importlib.util, "find_spec", lambda _: None)
    adapter = GarakAdapter()
    bundle = adapter.parse_fixture_report(GARAK_FIXTURES[1])

    assert adapter.available is False
    assert bundle.adapter_status.dependency_available is False
    assert bundle.adapter_status.fixture_mode is True
    assert GARAK_LIMITATION in bundle.adapter_status.limitation
    assert {finding.category for finding in bundle.findings} == {
        RedteamFindingCategory.CROSS_TENANT_LEAKAGE,
        RedteamFindingCategory.RAW_EVIDENCE_LEAKAGE,
    }


def test_fixture_summary_maps_all_required_controls() -> None:
    summary = build_redteam_summary(
        pyrit_fixture_paths=PYRIT_FIXTURES,
        garak_fixture_paths=GARAK_FIXTURES,
    )

    assert len(summary.findings) == 8
    assert summary.raw_evidence_exported is False
    assert summary.finding_counts_by_category == {
        "cross_tenant_leakage": 1,
        "mcp_scope_bypass": 1,
        "prompt_injection": 2,
        "raw_evidence_leakage": 2,
        "secret_external_routing": 1,
        "tool_abuse": 1,
    }

    expected_controls = {
        RedteamFindingCategory.PROMPT_INJECTION: "RAG injection scanner",
        RedteamFindingCategory.CROSS_TENANT_LEAKAGE: "OPA Retrieval ACL",
        RedteamFindingCategory.TOOL_ABUSE: "tool governance",
        RedteamFindingCategory.MCP_SCOPE_BYPASS: "MCP governance",
        RedteamFindingCategory.SECRET_EXTERNAL_ROUTING: "gateway governance",
        RedteamFindingCategory.RAW_EVIDENCE_LEAKAGE: "redaction/Langfuse-safe evidence",
    }
    for category, control_name in expected_controls.items():
        assert get_control_mapping(category).control_name == control_name

    for finding in summary.findings:
        assert finding.control_mapping is not None
        assert finding.raw_evidence_exported is False
        assert finding.metadata.get("secret_exported") is False
        assert "sk-" not in finding.sanitized_evidence.lower()


def test_findings_to_controls_markdown_includes_claim_boundary() -> None:
    summary = build_redteam_summary(
        pyrit_fixture_paths=PYRIT_FIXTURES,
        garak_fixture_paths=GARAK_FIXTURES,
    )
    markdown = render_findings_to_controls_markdown(summary.findings)

    assert "RAG injection scanner" in markdown
    assert "OPA Retrieval ACL" in markdown
    assert "tool governance" in markdown
    assert "MCP governance" in markdown
    assert "gateway governance" in markdown
    assert "redaction/Langfuse-safe evidence" in markdown
    assert "does not change OPA" in markdown


def test_evidence_docs_state_limitations() -> None:
    redteam_dir = REPO_ROOT / "docs/security/evidence/redteam"
    limitations = (redteam_dir / "limitations.md").read_text(encoding="utf-8")
    summary = (redteam_dir / "redteam_summary.md").read_text(encoding="utf-8")

    assert "True PyRIT execution is not proven" in limitations
    assert "True garak execution is not proven" in limitations
    assert "does not claim production readiness" in limitations
    assert "Raw evidence exported: `False`" in summary
    assert "No raw prompts, retrieved contexts, tenant content, model outputs, or secrets" in summary
