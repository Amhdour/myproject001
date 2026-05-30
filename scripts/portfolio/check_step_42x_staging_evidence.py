#!/usr/bin/env python3
"""Validate that Step 42X staging evidence files and blocked-claim boundaries exist."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "docs/security/evidence/step_42x_live_staging_deployment_evidence"
REQUIRED_FILES = [
    "README.md",
    "environment_check.md",
    "deployment_attempt.md",
    "health_check_results.md",
    "runtime_enforcement_mode.md",
    "smoke_test_results.md",
    "log_capture.md",
    "rollback_notes.md",
    "go_no_go.md",
    "remaining_limitations.md",
    "blockers.md",
]
REQUIRED_PHRASES = {
    "README.md": [
        "DEPLOYMENT_BLOCKED",
        "Live staging validation remains **PENDING**",
        "Compliance certification is **NOT CLAIMED**",
    ],
    "go_no_go.md": [
        "**DEPLOYMENT_BLOCKED**",
        "Live staging/cloud validation: **PENDING**",
        "Enterprise production-candidate readiness: **NO-GO / 5%**",
    ],
    "blockers.md": [
        "Deployment status: **DEPLOYMENT_BLOCKED**",
        "live staging validation remains **PENDING**",
    ],
}


def main() -> int:
    missing = [name for name in REQUIRED_FILES if not (EVIDENCE_DIR / name).is_file()]
    if missing:
        print("FAIL: missing Step 42X evidence files:")
        for name in missing:
            print(f"  - {name}")
        return 1

    phrase_failures: list[str] = []
    for filename, phrases in REQUIRED_PHRASES.items():
        text = (EVIDENCE_DIR / filename).read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                phrase_failures.append(f"{filename}: {phrase}")

    if phrase_failures:
        print("FAIL: missing Step 42X claim-boundary phrases:")
        for failure in phrase_failures:
            print(f"  - {failure}")
        return 1

    print(f"PASS: Step 42X evidence package is complete in {EVIDENCE_DIR.relative_to(ROOT)}")
    print("PASS: blocked-deployment claim boundaries are present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
