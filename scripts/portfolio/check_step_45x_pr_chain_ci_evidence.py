#!/usr/bin/env python3
"""Validate Step 45X PR-chain and CI evidence boundaries."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "docs/security/evidence/step_45x_github_pr_chain_ci_actions_verification"
REQUIRED_FILES = [
    "README.md",
    "reconciliation_summary.md",
    "pr_chain_verification.md",
    "merge_commit_map.md",
    "main_branch_evidence.md",
    "ci_actions_verification.md",
    "local_verification_results.md",
    "secret_hygiene.md",
    "go_no_go.md",
    "remaining_limitations.md",
]
VALID_CLASSIFICATIONS = {
    "PR_CHAIN_AND_CI_VERIFIED",
    "PR_CHAIN_VERIFIED_CI_PENDING",
    "PR_CHAIN_PARTIALLY_VERIFIED",
    "RECONCILIATION_BLOCKED",
    "NO_GO",
}
INCOMPLETE_CLASSIFICATIONS = {
    "PR_CHAIN_PARTIALLY_VERIFIED",
    "RECONCILIATION_BLOCKED",
    "NO_GO",
}


def read_required_text(relative_path: str) -> str:
    path = EVIDENCE_DIR / relative_path
    if not path.is_file():
        raise AssertionError(f"Missing required Step 45X evidence file: {path}")
    return path.read_text(encoding="utf-8")


def assert_contains(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise AssertionError(f"Missing required text for {label}: {needle}")


def main() -> int:
    missing = [name for name in REQUIRED_FILES if not (EVIDENCE_DIR / name).is_file()]
    if missing:
        raise AssertionError(f"Missing required Step 45X files: {missing}")

    combined = "\n".join(read_required_text(name) for name in REQUIRED_FILES)
    go_no_go = read_required_text("go_no_go.md")
    ci_text = read_required_text("ci_actions_verification.md")
    pr_text = read_required_text("pr_chain_verification.md")

    classifications = [value for value in VALID_CLASSIFICATIONS if value in go_no_go]
    if len(classifications) != 1:
        raise AssertionError(
            "Step 45X go_no_go.md must contain exactly one GO/NO-GO classification; "
            f"found {classifications}"
        )
    classification = classifications[0]

    assert_contains(pr_text, "GitHub PR metadata unavailable", "PR metadata boundary")
    assert_contains(ci_text, "PENDING / UNAVAILABLE", "CI status classification")
    assert_contains(combined, "Live staging/cloud validation", "live staging boundary")
    assert_contains(combined, "NO-GO / 5%", "enterprise production-candidate boundary")
    assert_contains(combined, "External validation", "external validation boundary")
    assert_contains(combined, "Compliance certification", "compliance boundary")
    assert_contains(combined, "NOT CLAIMED", "not-claimed boundary")

    unresolved_path = EVIDENCE_DIR / "unresolved_gaps.md"
    if classification in INCOMPLETE_CLASSIFICATIONS and not unresolved_path.is_file():
        raise AssertionError(
            "unresolved_gaps.md is required when PR or CI verification is incomplete"
        )

    forbidden_unsupported_claims = [
        "CI passed",
        "Actions passed",
        "GitHub Actions passed",
        "CI success is verified",
        "CI Actions evidence: VERIFIED",
    ]
    if classification != "PR_CHAIN_AND_CI_VERIFIED":
        for claim in forbidden_unsupported_claims:
            if claim in combined:
                raise AssertionError(f"Unsupported CI success claim found: {claim}")

    print(f"PASS: Step 45X evidence package is complete with classification {classification}.")
    print("PASS: CI, PR metadata, live staging, enterprise, external validation, and compliance boundaries are preserved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
