#!/usr/bin/env python3
"""Validate Step 47X Docker/local compose staging evidence and claim boundaries."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "docs/security/evidence/step_47x_docker_local_compose_staging_proof"
REQUIRED_FILES = [
    "README.md",
    "environment_check.md",
    "docker_availability.md",
    "deployment_file_inventory.md",
    "compose_config_validation.md",
    "local_staging_attempt.md",
    "health_check_results.md",
    "runtime_enforcement_mode.md",
    "log_capture.md",
    "rollback_evidence.md",
    "smoke_test_results.md",
    "go_no_go.md",
    "remaining_limitations.md",
]
VALID_CLASSIFICATIONS = {
    "LOCAL_DOCKER_STAGING_GO",
    "COMPOSE_CONFIG_VERIFIED_STARTUP_BLOCKED",
    "DOCKER_STAGING_BLOCKED",
    "LOCAL_STAGING_NO_GO",
    "NO_GO",
}
BLOCKED_CLASSIFICATIONS = {
    "DOCKER_STAGING_BLOCKED",
    "COMPOSE_CONFIG_VERIFIED_STARTUP_BLOCKED",
}
STARTUP_FAILURE_CLASSIFICATIONS = {"LOCAL_STAGING_NO_GO"}


def read_required_text(relative_path: str) -> str:
    path = EVIDENCE_DIR / relative_path
    if not path.is_file():
        raise AssertionError(f"Missing required Step 47X evidence file: {path}")
    return path.read_text(encoding="utf-8")


def assert_contains(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise AssertionError(f"Missing required text for {label}: {needle}")


def main() -> int:
    missing = [name for name in REQUIRED_FILES if not (EVIDENCE_DIR / name).is_file()]
    if missing:
        raise AssertionError(f"Missing required Step 47X files: {missing}")

    combined = "\n".join(read_required_text(name) for name in REQUIRED_FILES)
    go_no_go = read_required_text("go_no_go.md")
    local_attempt = read_required_text("local_staging_attempt.md")
    runtime_mode = read_required_text("runtime_enforcement_mode.md")

    classifications = [value for value in VALID_CLASSIFICATIONS if value in go_no_go]
    if len(classifications) != 1:
        raise AssertionError(
            "Step 47X go_no_go.md must contain exactly one GO/NO-GO classification; "
            f"found {classifications}"
        )
    classification = classifications[0]

    assert_contains(read_required_text("docker_availability.md"), "DOCKER_", "Docker state classification")
    assert_contains(local_attempt, "Path ", "local staging attempt path")
    assert_contains(read_required_text("compose_config_validation.md"), "config", "Compose config result")
    assert_contains(runtime_mode, "STEP_39X_RUNTIME_ENFORCEMENT_MODE", "runtime mode variable")
    assert_contains(runtime_mode, "disabled", "safe default mode")

    if classification in BLOCKED_CLASSIFICATIONS and not (EVIDENCE_DIR / "blockers.md").is_file():
        raise AssertionError("blockers.md is required when Docker/local staging is blocked")

    if classification in STARTUP_FAILURE_CLASSIFICATIONS and not (
        EVIDENCE_DIR / "startup_failure_analysis.md"
    ).is_file():
        raise AssertionError("startup_failure_analysis.md is required when startup begins and fails")

    unsupported_success_claims = [
        "Local Docker staging evidence: VERIFIED",
        "LOCAL_DOCKER_STAGING_GO",
        "Local Docker staging verified",
        "local staging stack started successfully",
        "health endpoint passed",
    ]
    if classification != "LOCAL_DOCKER_STAGING_GO":
        for claim in unsupported_success_claims:
            if claim in combined:
                raise AssertionError(f"Unsupported local staging success claim found: {claim}")

    assert_contains(combined, "Live staging/cloud validation", "live staging boundary")
    assert_contains(combined, "PENDING", "pending boundary")
    assert_contains(combined, "Enterprise production-candidate readiness", "enterprise boundary")
    assert_contains(combined, "NO-GO / 5%", "enterprise readiness value")
    assert_contains(combined, "External validation", "external validation boundary")
    assert_contains(combined, "Compliance certification", "compliance boundary")
    assert_contains(combined, "NOT CLAIMED", "compliance not-claimed boundary")

    print(f"PASS: Step 47X evidence package is complete with classification {classification}.")
    print(
        "PASS: Docker/local staging, live staging, enterprise, external validation, "
        "and compliance claim boundaries are preserved."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
