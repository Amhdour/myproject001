#!/usr/bin/env python3
"""Check that release-candidate portfolio artifacts are present."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]

RELEASE_CANDIDATE_FILES = [
    "portfolio/release_candidate/README.md",
    "portfolio/release_candidate/v0.1.0_portfolio_review.md",
    "portfolio/release_candidate/final_go_no_go.md",
    "portfolio/release_candidate/final_reviewer_path.md",
    "portfolio/release_candidate/final_commands.md",
    "portfolio/release_candidate/final_status_badges.md",
    "portfolio/release_candidate/final_outreach_pack.md",
    "portfolio/release_candidate/final_manual_review_checklist.md",
    "docs/security/evidence/release_candidate/README.md",
    "docs/security/evidence/release_candidate/release_candidate_go_no_go.md",
    "docs/security/evidence/release_candidate/final_evidence_map.md",
]

EXISTING_PACKAGE_FILES = [
    "README.md",
    "PORTFOLIO_CASE_STUDY.md",
    "CLAIM_BOUNDARY.md",
    "portfolio/README.md",
    "portfolio/evidence_index.md",
    "portfolio/release_prep/README.md",
    "portfolio/public_sharing_audit/README.md",
    "demo_attacks/README.md",
    "demo_attacks/run_demo_attacks.py",
    "scripts/portfolio/check_public_sharing_readiness.py",
    "scripts/portfolio/check_claim_boundary.py",
    "scripts/portfolio/check_no_fake_claims.py",
    "scripts/portfolio/check_evidence_links.py",
]


def split_present_missing(file_paths: list[str]) -> tuple[list[str], list[str]]:
    present = [file_path for file_path in file_paths if (ROOT / file_path).is_file()]
    missing = [file_path for file_path in file_paths if not (ROOT / file_path).is_file()]
    return present, missing


def print_group(title: str, present: list[str], missing: list[str]) -> None:
    status = "PASS" if not missing else "FAIL"
    print(f"\n{status}: {title}")
    print(f"  Present ({len(present)}):")
    if present:
        for file_path in present:
            print(f"    - {file_path}")
    else:
        print("    - none")

    print(f"  Missing ({len(missing)}):")
    if missing:
        for file_path in missing:
            print(f"    - {file_path}")
    else:
        print("    - none")


def main() -> int:
    groups = [
        ("Required release-candidate files", RELEASE_CANDIDATE_FILES),
        ("Required existing portfolio packages", EXISTING_PACKAGE_FILES),
    ]

    missing_total = 0
    for title, file_paths in groups:
        present, missing = split_present_missing(file_paths)
        missing_total += len(missing)
        print_group(title, present, missing)

    if missing_total:
        print(f"\nFAIL: {missing_total} required release-candidate file(s) missing.")
        return 1

    print("\nPASS: all required release-candidate and prerequisite files are present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
