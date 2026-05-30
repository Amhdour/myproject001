#!/usr/bin/env python3
"""Validate Step 52X custom image evidence and claim boundaries."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "docs/security/evidence/step_52x_custom_onyx_image_runtime_enforcement_deploy"
REQUIRED_FILES = [
    "README.md",
    "source_verification.md",
    "build_strategy.md",
    "build_results.md",
    "image_runtime_code_check.md",
    "deployment_attempt.md",
    "deployed_container_verification.md",
    "runtime_hook_verification.md",
    "health_after_deploy.md",
    "rollback_notes.md",
    "go_no_go.md",
    "remaining_limitations.md",
    "redaction_note.md",
]
BLOCKED_CLASSIFICATIONS = {
    "ORACLE_CUSTOM_IMAGE_BUILD_BLOCKED",
    "ORACLE_CUSTOM_IMAGE_DEPLOYMENT_BLOCKED",
}
REQUIRED_BOUNDARIES = [
    "Production-style portfolio readiness | remains 90%",
    "Enterprise production-candidate readiness | NO-GO / 6-8%",
    "External validation | PENDING",
    "Compliance certification | NOT CLAIMED",
    "Runtime enforcement behavior smoke test | NOT EXECUTED",
    "Oracle runtime-code deployment status | NOT DEPLOYED / NOT VERIFIED",
]
REQUIRED_DOC_TEXT = [
    "Step 39X source",
    "backend/security_layer/runtime_enforcement",
    "_apply_step_39x_runtime_enforcement_hook",
    "Build strategy selected | D",
    "docker: command not found",
    "rollback",
    "No private keys",
]
UNSUPPORTED_CLAIMS = [
    "Production readiness | GO",
    "Enterprise production-candidate readiness | GO",
    "External validation | COMPLETE",
    "Compliance certification | CLAIMED",
    "Runtime enforcement behavior smoke test | PASS",
    "Oracle runtime-code deployment status | VERIFIED",
    "runtime enforcement is active in Oracle staging",
]
DOCS_TO_CHECK = [
    "docs/security/execution_tracker.md",
    "docs/security/evidence_report.md",
    "docs/security/known_limitations.md",
    "portfolio/evidence_index.md",
    "portfolio/release_candidate/final_go_no_go.md",
    "PORTFOLIO_CASE_STUDY.md",
]


def read(path: Path) -> str:
    if not path.is_file():
        raise AssertionError(f"Missing required file: {path}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    missing = [name for name in REQUIRED_FILES if not (EVIDENCE_DIR / name).is_file()]
    if missing:
        raise AssertionError(f"Missing required Step 52X evidence files: {missing}")

    combined = "\n".join(read(EVIDENCE_DIR / name) for name in REQUIRED_FILES)
    go_no_go = read(EVIDENCE_DIR / "go_no_go.md")

    classification_found = [item for item in BLOCKED_CLASSIFICATIONS if item in go_no_go]
    if not classification_found:
        raise AssertionError("Step 52X blocked classification is missing from go_no_go.md")

    if any(item in go_no_go for item in BLOCKED_CLASSIFICATIONS) and not (EVIDENCE_DIR / "blockers.md").is_file():
        raise AssertionError("blockers.md is required when Step 52X is blocked")
    if (EVIDENCE_DIR / "blockers.md").is_file():
        combined += "\n" + read(EVIDENCE_DIR / "blockers.md")

    for needle in REQUIRED_BOUNDARIES + REQUIRED_DOC_TEXT:
        if needle not in combined:
            raise AssertionError(f"Missing required Step 52X evidence text: {needle}")

    docs_combined = "\n".join(read(ROOT / path) for path in DOCS_TO_CHECK)
    for required in [
        "production-style portfolio readiness remains 90%",
        "enterprise production-candidate readiness remains NO-GO / 6-8%",
        "external validation remains PENDING",
        "compliance certification remains NOT CLAIMED",
    ]:
        if required.lower() not in docs_combined.lower():
            raise AssertionError(f"Missing required Step 52X portfolio boundary: {required}")

    for claim in UNSUPPORTED_CLAIMS:
        if claim in combined:
            raise AssertionError(f"Unsupported Step 52X positive claim found: {claim}")

    print("PASS: Step 52X custom image evidence package is complete for blocked build/deploy status.")
    print("PASS: Classification is ORACLE_CUSTOM_IMAGE_BUILD_BLOCKED.")
    print("PASS: Production, enterprise, deployment, runtime behavior, external validation, compliance, rollback, and redaction claim boundaries are preserved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
