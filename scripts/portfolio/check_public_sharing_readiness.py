#!/usr/bin/env python3
"""Check that public-sharing readiness artifacts are present."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]

PUBLIC_SHARING_FILES = [
    "README.md",
    "PORTFOLIO_CASE_STUDY.md",
    "CLAIM_BOUNDARY.md",
    "CLIENT_README.md",
    "EMPLOYER_README.md",
    "PARTNER_DEMO_README.md",
    "portfolio/README.md",
    "portfolio/evidence_index.md",
    "portfolio/release_prep/README.md",
    "demo_attacks/README.md",
    "demo_attacks/run_demo_attacks.py",
    "docs/security/known_limitations.md",
    "docs/security/evidence/final_portfolio_package/README.md",
]

CLAIM_BOUNDARY_FILES = [
    "portfolio/claim_boundary.md",
    "docs/security/partner_safe_claims.md",
]

CI_FILES = [
    ".github/workflows/security-layer-tests.yml",
    ".github/workflows/portfolio-claim-boundary.yml",
    ".github/workflows/evidence-integrity.yml",
]


def present_and_missing(file_paths: list[str]) -> tuple[list[str], list[str]]:
    present = [file_path for file_path in file_paths if (ROOT / file_path).is_file()]
    missing = [file_path for file_path in file_paths if not (ROOT / file_path).is_file()]
    return present, missing


def print_group(title: str, present: list[str], missing: list[str]) -> None:
    status = "PASS" if not missing else "FAIL"
    print(f"\n{status}: {title}")
    print(f"  Present ({len(present)}):")
    for file_path in present:
        print(f"    - {file_path}")
    if not present:
        print("    - none")
    print(f"  Missing ({len(missing)}):")
    for file_path in missing:
        print(f"    - {file_path}")
    if not missing:
        print("    - none")


def main() -> int:
    groups = [
        ("Required public-sharing files", PUBLIC_SHARING_FILES),
        ("Required claim-boundary files", CLAIM_BOUNDARY_FILES),
        ("Required CI files", CI_FILES),
    ]

    missing_total = 0
    for title, file_paths in groups:
        present, missing = present_and_missing(file_paths)
        missing_total += len(missing)
        print_group(title, present, missing)

    if missing_total:
        print(f"\nFAIL: {missing_total} required public-sharing readiness file(s) missing.")
        return 1

    print("\nPASS: all required public-sharing readiness files are present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
