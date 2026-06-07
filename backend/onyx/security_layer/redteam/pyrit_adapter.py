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

PYRIT_LIMITATION = (
    "PyRIT dependency-backed execution is not proven unless this adapter is run "
    "in an environment with pyrit installed and an explicit dependency-backed "
    "campaign execution is performed. Fixture parsing remains available without pyrit."
)


def pyrit_available() -> bool:
    return importlib.util.find_spec("pyrit") is not None


class PyritAdapter:
    def __init__(self) -> None:
        self._available = pyrit_available()

    @property
    def available(self) -> bool:
        return self._available

    def status(self) -> RedteamAdapterStatus:
        return RedteamAdapterStatus(
            tool_name=RedteamToolName.PYRIT,
            dependency_available=self.available,
            fixture_mode=True,
            limitation=PYRIT_LIMITATION,
        )

    def parse_fixture_campaign(self, fixture_path: Path) -> RedteamEvidenceBundle:
        payload = json.loads(fixture_path.read_text(encoding="utf-8"))
        findings_payload = payload.get("findings", [])
        if not isinstance(findings_payload, list):
            raise ValueError("PyRIT fixture findings must be a list")
        findings = [
            RedteamFinding.model_validate(
                {
                    **finding_payload,
                    "source_tool": RedteamToolName.PYRIT,
                    "source_fixture": fixture_path.name,
                    "raw_evidence_exported": False,
                }
            )
            for finding_payload in findings_payload
            if isinstance(finding_payload, dict)
        ]
        return RedteamEvidenceBundle(
            generated_by="pyrit_fixture_parser",
            claim_boundary=str(
                payload.get(
                    "claim_boundary",
                    "Fixture-based PyRIT-style campaign parsing only; no production-readiness claim.",
                )
            ),
            adapter_status=self.status(),
            findings=map_findings_to_controls(findings),
        )

    def parse_fixture_campaigns(
        self, fixture_paths: list[Path]
    ) -> list[RedteamEvidenceBundle]:
        return [self.parse_fixture_campaign(path) for path in fixture_paths]

    def run_dependency_backed_campaign(self, _campaign_config: dict[str, Any]) -> None:
        if not self.available:
            return None
        return None
