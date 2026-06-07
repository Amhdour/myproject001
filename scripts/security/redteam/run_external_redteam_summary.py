from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
BACKEND_PATH = REPO_ROOT / "backend"
if str(BACKEND_PATH) not in sys.path:
    sys.path.insert(0, str(BACKEND_PATH))

from onyx.security_layer.redteam import build_redteam_summary  # noqa: E402
from onyx.security_layer.redteam import REDTEAM_CLAIM_BOUNDARY  # noqa: E402
from onyx.security_layer.redteam import (  # noqa: E402
    render_findings_to_controls_markdown,
)
from onyx.security_layer.redteam.models import RedteamSummary  # noqa: E402

DEFAULT_FIXTURE_DIR = REPO_ROOT / "docs/security/evidence/redteam/fixtures"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "docs/security/evidence/redteam"
DEFAULT_PYRIT_FIXTURES = [
    DEFAULT_FIXTURE_DIR / "pyrit_prompt_injection_campaign.json",
    DEFAULT_FIXTURE_DIR / "pyrit_tool_abuse_campaign.json",
]
DEFAULT_GARAK_FIXTURES = [
    DEFAULT_FIXTURE_DIR / "garak_prompt_injection_report.json",
    DEFAULT_FIXTURE_DIR / "garak_data_leakage_report.json",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build optional PyRIT + garak fixture-based red-team evidence summary."
    )
    parser.add_argument(
        "--pyrit-fixtures",
        nargs="*",
        type=Path,
        default=DEFAULT_PYRIT_FIXTURES,
        help="PyRIT-style fixture campaign JSON files to parse.",
    )
    parser.add_argument(
        "--garak-fixtures",
        nargs="*",
        type=Path,
        default=DEFAULT_GARAK_FIXTURES,
        help="garak-style fixture report JSON files to parse.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory where red-team evidence docs should be written.",
    )
    return parser.parse_args()


def render_readme_markdown() -> str:
    return "\n".join(
        [
            "# Optional External Red-team Evidence Foundation",
            "",
            "This directory contains a lightweight, fixture-based evidence foundation for optional PyRIT and garak red-team tooling.",
            "It does not make PyRIT or garak hard dependencies and does not claim production readiness.",
            "",
            "## Contents",
            "",
            "- `fixtures/`: sanitized PyRIT-style campaign and garak-style report inputs.",
            "- `redteam_summary.md`: generated fixture-based findings summary.",
            "- `findings_to_controls.md`: generated mapping from finding categories to existing controls.",
            "- `reproduction_commands.md`: local commands for reproducing fixture parsing.",
            "- `limitations.md`: explicit limitations and claim boundary.",
            "",
            "## Evidence boundary",
            "",
            REDTEAM_CLAIM_BOUNDARY,
            "Raw prompts, retrieved context, model outputs, tenant content, and secrets are intentionally not exported in these artifacts.",
        ]
    ) + "\n"


def render_reproduction_commands_markdown() -> str:
    return "\n".join(
        [
            "# Reproduction Commands",
            "",
            "Run from the repository root:",
            "",
            "```bash",
            "python scripts/security/redteam/run_external_redteam_summary.py",
            "python -m pytest --confcutdir=backend/tests/security_layer backend/tests/security_layer/test_redteam_evidence.py",
            "```",
            "",
            "Optional dependency-backed red-team tools are not invoked by default. True PyRIT or garak execution is not proven unless those dependencies are installed and explicit dependency-backed runs occur outside the fixture parser.",
        ]
    ) + "\n"


def render_limitations_markdown(summary: RedteamSummary) -> str:
    return "\n".join(
        [
            "# Red-team Evidence Limitations",
            "",
            "- This is a lightweight fixture-based evidence foundation only.",
            "- PyRIT and garak remain optional and are not hard dependencies.",
            "- If PyRIT or garak are unavailable, fixture-based campaign/report parsing still works and documents that limitation.",
            "- True PyRIT execution is not proven unless a dependency-backed PyRIT campaign run is executed in an environment with PyRIT installed.",
            "- True garak execution is not proven unless a dependency-backed garak scanner run is executed in an environment with garak installed.",
            "- This change does not alter OPA, scanner, tool governance, MCP governance, gateway governance, or evaluation behavior.",
            "- This evidence does not claim production readiness.",
            "- Raw prompts, retrieved context, tenant content, model outputs, and secrets are intentionally not exported.",
            "",
            "## Adapter status at generation time",
            "",
            f"- PyRIT dependency available: `{summary.pyrit_status.dependency_available}`",
            f"- garak dependency available: `{summary.garak_status.dependency_available}`",
            f"- Raw evidence exported: `{summary.raw_evidence_exported}`",
        ]
    ) + "\n"


def render_summary_markdown(summary: RedteamSummary) -> str:
    lines = [
        "# External Red-team Evidence Summary",
        "",
        "## Claim boundary",
        "",
        summary.claim_boundary,
        "",
        "## Adapter status",
        "",
        "| Tool | Dependency available | Fixture mode | Limitation |",
        "| --- | --- | --- | --- |",
        f"| PyRIT | {summary.pyrit_status.dependency_available} | {summary.pyrit_status.fixture_mode} | {summary.pyrit_status.limitation} |",
        f"| garak | {summary.garak_status.dependency_available} | {summary.garak_status.fixture_mode} | {summary.garak_status.limitation} |",
        "",
        "## Finding counts",
        "",
        "| Category | Count |",
        "| --- | ---: |",
    ]
    for category, count in summary.finding_counts_by_category.items():
        lines.append(f"| {category} | {count} |")
    lines.extend(
        [
            "",
            "## Findings",
            "",
            "| Finding | Tool | Severity | Category | Sanitized evidence | Control |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for finding in summary.findings:
        control_name = "unmapped"
        if finding.control_mapping is not None:
            control_name = finding.control_mapping.control_name
        lines.append(
            f"| {finding.finding_id} | {finding.source_tool.value} | {finding.severity.value} | "
            f"{finding.category.value} | {finding.sanitized_evidence} | {control_name} |"
        )
    lines.extend(
        [
            "",
            f"Raw evidence exported: `{summary.raw_evidence_exported}`",
            "",
            "No raw prompts, retrieved contexts, tenant content, model outputs, or secrets are included in this summary.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_evidence_documents(summary: RedteamSummary, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "readme": output_dir / "README.md",
        "reproduction_commands": output_dir / "reproduction_commands.md",
        "redteam_summary": output_dir / "redteam_summary.md",
        "findings_to_controls": output_dir / "findings_to_controls.md",
        "limitations": output_dir / "limitations.md",
    }
    paths["readme"].write_text(render_readme_markdown(), encoding="utf-8")
    paths["reproduction_commands"].write_text(
        render_reproduction_commands_markdown(), encoding="utf-8"
    )
    paths["redteam_summary"].write_text(
        render_summary_markdown(summary), encoding="utf-8"
    )
    paths["findings_to_controls"].write_text(
        render_findings_to_controls_markdown(summary.findings), encoding="utf-8"
    )
    paths["limitations"].write_text(
        render_limitations_markdown(summary), encoding="utf-8"
    )
    return paths


def _summary_output(summary: RedteamSummary, paths: dict[str, Path]) -> dict[str, Any]:
    return {
        "claim_boundary": summary.claim_boundary,
        "adapter_status": {
            "pyrit_dependency_available": summary.pyrit_status.dependency_available,
            "garak_dependency_available": summary.garak_status.dependency_available,
            "pyrit_fixture_mode": summary.pyrit_status.fixture_mode,
            "garak_fixture_mode": summary.garak_status.fixture_mode,
        },
        "finding_counts_by_category": summary.finding_counts_by_category,
        "finding_count": len(summary.findings),
        "raw_evidence_exported": summary.raw_evidence_exported,
        "written_paths": {key: str(value) for key, value in paths.items()},
    }


def main() -> int:
    args = parse_args()
    summary = build_redteam_summary(
        pyrit_fixture_paths=args.pyrit_fixtures,
        garak_fixture_paths=args.garak_fixtures,
    )
    paths = write_evidence_documents(summary=summary, output_dir=args.output_dir)
    print(json.dumps(_summary_output(summary, paths), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
