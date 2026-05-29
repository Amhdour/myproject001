#!/usr/bin/env python3
"""Verify required reviewer evidence files are present."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
REQUIRED_FILES = [
    "README.md",
    "portfolio/README.md",
    "portfolio/architecture.md",
    "portfolio/reviewer_quickstart.md",
    "portfolio/demo_script.md",
    "portfolio/claim_boundary.md",
    "portfolio/evidence_index.md",
    "docs/security/README.md",
    "docs/security/execution_tracker.md",
    "docs/security/evidence_report.md",
    "docs/security/known_limitations.md",
    "docs/security/partner_safe_claims.md",
]
OPTIONAL_FILES = [
    "docs/security/final_claim_boundary.md",
    "docs/security/final_evidence_package_index.md",
    "docs/security/evidence/step_34x_oracle_free_vps/go_no_go.md",
    "deployment/docker_compose/docker-compose.step34x-minimal.yml",
]


def print_group(title: str, files: list[str]) -> None:
    print(f"\n{title} ({len(files)}):")
    if not files:
        print("  - none")
        return
    for file_path in files:
        print(f"  - {file_path}")


def main() -> int:
    required_present = [file_path for file_path in REQUIRED_FILES if (ROOT / file_path).is_file()]
    required_missing = [file_path for file_path in REQUIRED_FILES if not (ROOT / file_path).is_file()]
    optional_present = [file_path for file_path in OPTIONAL_FILES if (ROOT / file_path).is_file()]
    optional_absent = [file_path for file_path in OPTIONAL_FILES if not (ROOT / file_path).is_file()]

    print_group("Required files present", required_present)
    print_group("Required files missing", required_missing)
    print_group("Optional files present", optional_present)
    print_group("Optional files absent", optional_absent)

    if required_missing:
        print("\nFAIL: required reviewer evidence files are missing.")
        return 1

    print("\nPASS: all required reviewer evidence files are present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
