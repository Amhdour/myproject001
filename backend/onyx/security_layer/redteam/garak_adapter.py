from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any

from onyx.security_layer.redteam.findings_mapper import map_findings_to_controls
from onyx.security_layer.redteam.models import RedteamAdapterStatus
from onyx.security_layer.redteam.models import RedteamEvidenceBundle
from onyx.security_layer.redteam.models import RedteamFinding
from onyx.security_layer.redteam.models import RedteamToolName

GARAK_LIMITATION = (
    "garak dependency-backed execution is not proven unless this adapter is run "
    "in an environment with garak installed and an explicit dependency-backed "
    "scanner execution is performed. Fixture parsing remains available without garak."
)


def garak_available() -> bool:
    return importlib.util.find_spec("garak") is not None


class GarakAdapter:
    def __init__(self) -> None:
        self._available = garak_available()

    @property
    def available(self) -> bool:
        return self._available

    def status(self) -> RedteamAdapterStatus:
        return RedteamAdapterStatus(
            tool_name=RedteamToolName.GARAK,
            dependency_available=self.available,
            fixture_mode=True,
            limitation=GARAK_LIMITATION,
        )

    def parse_fixture_report(self, fixture_path: Path) -> RedteamEvidenceBundle:
        payload = json.loads(fixture_path.read_text(encoding="utf-8"))
        findings_payload = payload.get("findings", [])
        if not isinstance(findings_payload, list):
            raise ValueError("garak fixture findings must be a list")
        findings = [
            RedteamFinding.model_validate(
                {
                    **finding_payload,
                    "source_tool": RedteamToolName.GARAK,
                    "source_fixture": fixture_path.name,
                    "raw_evidence_exported": False,
                }
            )
            for finding_payload in findings_payload
            if isinstance(finding_payload, dict)
        ]
        return RedteamEvidenceBundle(
            generated_by="garak_fixture_parser",
            claim_boundary=str(
                payload.get(
                    "claim_boundary",
                    "Fixture-based garak-style report parsing only; no production-readiness claim.",
                )
            ),
            adapter_status=self.status(),
            findings=map_findings_to_controls(findings),
        )

    def parse_fixture_reports(
        self, fixture_paths: list[Path]
    ) -> list[RedteamEvidenceBundle]:
        return [self.parse_fixture_report(path) for path in fixture_paths]

    def run_dependency_backed_scan(self, _scan_config: dict[str, Any]) -> None:
        if not self.available:
            return None
        return None
