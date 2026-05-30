#!/usr/bin/env python3
"""Validate Step 61X web healthcheck mismatch evidence boundaries."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "docs/security/evidence/step_61x_patch_web_healthcheck_mismatch"
REQUIRED_FILES = [
    "README.md",
    "root_cause.md",
    "patch_decision.md",
    "healthcheck_patch.md",
    "oracle_vps_test_plan.md",
    "test_results.md",
    "rollback_plan.md",
    "go_no_go.md",
    "remaining_limitations.md",
    "redaction_note.md",
]

REQUIRED_MARKERS = {
    "root_cause.md": ["Root cause", "127.0.0.1:3000", "container hostname/IP"],
    "patch_decision.md": ["Option B", "require('os').hostname()", "WEB_HEALTHCHECK_HOST"],
    "rollback_plan.md": ["Rollback", "docker inspect"],
    "go_no_go.md": [
        "WEB_HEALTHCHECK_PATCH_READY_RETEST_PENDING",
        "Production-style portfolio readiness | 92%",
        "Enterprise production-candidate | NO-GO / 7–9%",
        "simulated response only / real validation pending",
        "Compliance certification | NOT CLAIMED",
    ],
    "test_results.md": ["PENDING_USER_EXECUTION"],
}

FORBIDDEN_UNLESS_ORACLE_VERIFIED = [
    "WEB_HEALTHCHECK_FIXED_ORACLE_VERIFIED",
    "STAGING_HEALTHCHECK_GO",
    "full staging GO",
    "full live app GO",
]

FORBIDDEN_POSITIVE_CLAIMS = [
    "production readiness achieved",
    "enterprise production-candidate achieved",
    "real external validation complete",
    "externally validated",
    "compliance certified",
]

SAFE_CONTEXT_MARKERS = [
    "not claim",
    "not claimed",
    "no ",
    "pending",
    "must not",
    "without",
    "forbidden",
]


def read_required_file(relative_path: str) -> str | None:
    path = EVIDENCE_DIR / relative_path
    if not path.is_file():
        print(f"FAIL: missing {path.relative_to(ROOT)}")
        return None
    return path.read_text(encoding="utf-8")


def line_is_safe(line: str) -> bool:
    normalized = " ".join(line.lower().split())
    return any(marker in normalized for marker in SAFE_CONTEXT_MARKERS)


def main() -> int:
    failures: list[str] = []

    for relative_path in REQUIRED_FILES:
        if not (EVIDENCE_DIR / relative_path).is_file():
            failures.append(f"missing required file: {relative_path}")

    for relative_path, markers in REQUIRED_MARKERS.items():
        text = read_required_file(relative_path)
        if text is None:
            failures.append(f"cannot inspect missing file: {relative_path}")
            continue
        for marker in markers:
            if marker not in text:
                failures.append(f"{relative_path} missing marker: {marker}")

    combined_lines: list[tuple[str, int, str]] = []
    for relative_path in REQUIRED_FILES:
        path = EVIDENCE_DIR / relative_path
        if not path.is_file():
            continue
        for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            combined_lines.append((relative_path, index, line))

    for relative_path, line_number, line in combined_lines:
        normalized = " ".join(line.lower().split())
        for phrase in FORBIDDEN_UNLESS_ORACLE_VERIFIED:
            if phrase.lower() in normalized and not line_is_safe(line):
                failures.append(
                    f"{relative_path}:{line_number} unsupported Oracle-verified/full-staging claim: {phrase}"
                )
        for phrase in FORBIDDEN_POSITIVE_CLAIMS:
            if phrase in normalized and not line_is_safe(line):
                failures.append(
                    f"{relative_path}:{line_number} unsupported readiness/validation/certification claim: {phrase}"
                )

    if failures:
        print("FAIL: Step 61X evidence boundary check failed.")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        "PASS: Step 61X evidence files exist and preserve NO-GO, simulated/pending, "
        "and NOT CLAIMED boundaries."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
