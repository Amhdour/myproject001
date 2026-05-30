#!/usr/bin/env python3
"""Validate Step 46X GitHub Actions CI evidence and claim boundaries."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "docs/security/evidence/step_46x_github_actions_ci_run_trigger_verification_gate"
REQUIRED_FILES = [
    "README.md",
    "workflow_inventory.md",
    "ci_trigger_attempt.md",
    "ci_run_results.md",
    "pr_107_visibility.md",
    "local_verification_results.md",
    "secret_hygiene.md",
    "go_no_go.md",
    "remaining_limitations.md",
]
VALID_CLASSIFICATIONS = {
    "CI_ACTIONS_VERIFIED_PASS",
    "CI_ACTIONS_VERIFIED_FAIL",
    "CI_ACTIONS_NOT_TRIGGERED",
    "CI_ACTIONS_BLOCKED",
    "NO_GO",
}


def read_required_text(relative_path: str) -> str:
    path = EVIDENCE_DIR / relative_path
    if not path.is_file():
        raise AssertionError(f"Missing required Step 46X evidence file: {path}")
    return path.read_text(encoding="utf-8")


def assert_contains(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise AssertionError(f"Missing required text for {label}: {needle}")


def main() -> int:
    missing = [name for name in REQUIRED_FILES if not (EVIDENCE_DIR / name).is_file()]
    if missing:
        raise AssertionError(f"Missing required Step 46X files: {missing}")

    combined = "\n".join(read_required_text(name) for name in REQUIRED_FILES)
    go_no_go = read_required_text("go_no_go.md")
    ci_results = read_required_text("ci_run_results.md")

    classifications = [value for value in VALID_CLASSIFICATIONS if value in go_no_go]
    if len(classifications) != 1:
        raise AssertionError(
            "Step 46X go_no_go.md must contain exactly one GO/NO-GO classification; "
            f"found {classifications}"
        )
    classification = classifications[0]

    assert_contains(read_required_text("workflow_inventory.md"), "Workflow summary", "workflow inventory")
    assert_contains(ci_results, "CI Actions evidence", "CI status classification")

    if classification in {"CI_ACTIONS_BLOCKED", "CI_ACTIONS_NOT_TRIGGERED"} and not (
        EVIDENCE_DIR / "ci_blockers.md"
    ).is_file():
        raise AssertionError("ci_blockers.md is required when CI is blocked or unavailable")

    if classification == "CI_ACTIONS_VERIFIED_FAIL" and not (
        EVIDENCE_DIR / "ci_failure_analysis.md"
    ).is_file():
        raise AssertionError("ci_failure_analysis.md is required when CI failed")

    unsupported_success_claims = [
        "CI passed",
        "Actions passed",
        "GitHub Actions passed",
        "CI success is verified",
        "CI Actions evidence: VERIFIED PASS",
    ]
    if classification != "CI_ACTIONS_VERIFIED_PASS":
        for claim in unsupported_success_claims:
            if claim in combined:
                raise AssertionError(f"Unsupported CI success claim found: {claim}")

    if classification == "CI_ACTIONS_VERIFIED_PASS":
        assert_contains(ci_results, "conclusion", "successful CI conclusion evidence")
        assert_contains(ci_results, "success", "successful CI conclusion value")
        assert_contains(ci_results, "job", "CI job result evidence")

    assert_contains(combined, "Live staging/cloud validation", "live staging boundary")
    assert_contains(combined, "PENDING", "pending boundary")
    assert_contains(combined, "Enterprise production-candidate readiness", "enterprise boundary")
    assert_contains(combined, "NO-GO / 5%", "enterprise readiness value")
    assert_contains(combined, "External validation", "external validation boundary")
    assert_contains(combined, "Compliance certification", "compliance boundary")
    assert_contains(combined, "NOT CLAIMED", "compliance not-claimed boundary")

    print(f"PASS: Step 46X evidence package is complete with classification {classification}.")
    print(
        "PASS: CI success, live staging, enterprise, external validation, and compliance "
        "claim boundaries are preserved."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
