from __future__ import annotations

from collections import Counter
from pathlib import Path

from onyx.security_layer.redteam.findings_mapper import get_control_mapping
from onyx.security_layer.redteam.findings_mapper import map_findings_to_controls
from onyx.security_layer.redteam.findings_mapper import (
    render_findings_to_controls_markdown,
)
from onyx.security_layer.redteam.garak_adapter import garak_available
from onyx.security_layer.redteam.garak_adapter import GARAK_LIMITATION
from onyx.security_layer.redteam.garak_adapter import GarakAdapter
from onyx.security_layer.redteam.models import RedteamAdapterStatus
from onyx.security_layer.redteam.models import RedteamControlMapping
from onyx.security_layer.redteam.models import RedteamEvidenceBundle
from onyx.security_layer.redteam.models import RedteamFinding
from onyx.security_layer.redteam.models import RedteamFindingCategory
from onyx.security_layer.redteam.models import RedteamSeverity
from onyx.security_layer.redteam.models import RedteamSummary
from onyx.security_layer.redteam.models import RedteamToolName
from onyx.security_layer.redteam.pyrit_adapter import pyrit_available
from onyx.security_layer.redteam.pyrit_adapter import PYRIT_LIMITATION
from onyx.security_layer.redteam.pyrit_adapter import PyritAdapter

REDTEAM_CLAIM_BOUNDARY = (
    "Lightweight fixture-based PyRIT and garak evidence foundation only. "
    "External red-team tooling is optional, no production readiness is claimed, "
    "and true PyRIT/garak execution is not proven unless dependency-backed runs occur."
)


def build_redteam_summary(
    *, pyrit_fixture_paths: list[Path], garak_fixture_paths: list[Path]
) -> RedteamSummary:
    pyrit_adapter = PyritAdapter()
    garak_adapter = GarakAdapter()
    pyrit_bundles = pyrit_adapter.parse_fixture_campaigns(pyrit_fixture_paths)
    garak_bundles = garak_adapter.parse_fixture_reports(garak_fixture_paths)
    findings = [
        finding
        for bundle in [*pyrit_bundles, *garak_bundles]
        for finding in bundle.findings
    ]
    mapped_findings = map_findings_to_controls(findings)
    counts = Counter(finding.category.value for finding in mapped_findings)
    return RedteamSummary(
        claim_boundary=REDTEAM_CLAIM_BOUNDARY,
        pyrit_status=pyrit_adapter.status(),
        garak_status=garak_adapter.status(),
        findings=mapped_findings,
        finding_counts_by_category=dict(sorted(counts.items())),
        raw_evidence_exported=any(
            finding.raw_evidence_exported for finding in mapped_findings
        ),
    )


__all__ = [
    "GARAK_LIMITATION",
    "PYRIT_LIMITATION",
    "REDTEAM_CLAIM_BOUNDARY",
    "GarakAdapter",
    "PyritAdapter",
    "RedteamAdapterStatus",
    "RedteamControlMapping",
    "RedteamEvidenceBundle",
    "RedteamFinding",
    "RedteamFindingCategory",
    "RedteamSeverity",
    "RedteamSummary",
    "RedteamToolName",
    "build_redteam_summary",
    "garak_available",
    "get_control_mapping",
    "map_findings_to_controls",
    "pyrit_available",
    "render_findings_to_controls_markdown",
]
