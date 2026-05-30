#!/usr/bin/env python3
"""Validate Step 44X repository recovery evidence and claim boundaries."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "docs/security/evidence/step_44x_local_repository_recovery_branch_commit_integrity_gate"
REQUIRED_FILES = [
    "README.md",
    "codespaces_environment.md",
    "remote_origin_check.md",
    "branch_inventory.md",
    "commit_integrity_map.md",
    "evidence_folder_inventory.md",
    "pr_chain_verification.md",
    "ci_visibility.md",
    "local_verification_results.md",
    "secret_hygiene.md",
    "go_no_go.md",
    "remaining_limitations.md",
    "recovery_gaps.md",
]
REQUIRED_PHRASES = [
    "REPOSITORY_RECOVERY_BLOCKED",
    "GitHub repository integrity: **BLOCKED**",
    "Live staging/cloud validation: **PENDING**",
    "Enterprise production-candidate readiness after Step 44X: **NO-GO / 5%**",
    "External validation: **PENDING**",
    "Compliance certification: **NOT CLAIMED**",
]
UNSUPPORTED_PHRASES = [
    "REPOSITORY_CHAIN_VERIFIED",
    "GitHub repository integrity: **VERIFIED**",
    "CI pass: **YES**",
    "GitHub Actions passed: **YES**",
    "Live staging/cloud validation: **VERIFIED**",
    "External validation: **VERIFIED**",
    "Compliance certification: **CERTIFIED**",
    "Enterprise production-candidate readiness after Step 44X: **GO",
]


def main() -> int:
    missing = [name for name in REQUIRED_FILES if not (EVIDENCE_DIR / name).is_file()]
    if missing:
        print("FAIL: missing Step 44X evidence files:")
        for name in missing:
            print(f"  - {name}")
        return 1

    combined = "\n".join((EVIDENCE_DIR / name).read_text(encoding="utf-8") for name in REQUIRED_FILES)
    missing_phrases = [phrase for phrase in REQUIRED_PHRASES if phrase not in combined]
    if missing_phrases:
        print("FAIL: missing required Step 44X classification phrases:")
        for phrase in missing_phrases:
            print(f"  - {phrase}")
        return 1

    found_unsupported = [phrase for phrase in UNSUPPORTED_PHRASES if phrase in combined]
    if found_unsupported:
        print("FAIL: unsupported positive Step 44X claim found:")
        for phrase in found_unsupported:
            print(f"  - {phrase}")
        return 1

    print(f"PASS: Step 44X evidence package is complete in {EVIDENCE_DIR.relative_to(ROOT)}")
    print("PASS: repository recovery remains explicitly blocked, with claim boundaries preserved.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
