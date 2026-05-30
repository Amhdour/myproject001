#!/usr/bin/env python3
"""Validate Step 50X Oracle staging evidence and claim boundaries."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "docs/security/evidence/step_50x_oracle_staging_evidence_healthcheck_decision"
REQUIRED_FILES = [
    "README.md",
    "oracle_vps_environment.md",
    "docker_compose_readiness.md",
    "container_inventory.md",
    "minio_file_store_fix.md",
    "api_health_recovery.md",
    "web_healthcheck_mismatch.md",
    "host_proxy_curl_results.md",
    "log_summary.md",
    "rollback_notes.md",
    "go_no_go.md",
    "remaining_limitations.md",
    "redaction_note.md",
    "decision_record.md",
]
REQUIRED_BOUNDARIES = [
    "ORACLE_ONYX_STAGING_PARTIAL_GO",
    "Production readiness | NO-GO",
    "Enterprise production-candidate | NO-GO",
    "External validation | PENDING",
    "Compliance certification | NOT CLAIMED",
    "healthcheck target mismatch",
    "MinIO",
    "Do not publish raw env dumps",
]
UNSUPPORTED_POSITIVE_CLAIMS = [
    "Production readiness | GO",
    "Enterprise production-candidate | GO",
    "Production readiness: GO",
    "Enterprise production-candidate readiness: GO",
    "Live full app GO: GO",
    "Full live app staging | GO",
    "Compliance certification | CLAIMED",
    "External validation | COMPLETE",
    "ORACLE_ONYX_STAGING_GO",
]


def read_required_text(relative_path: str) -> str:
    path = EVIDENCE_DIR / relative_path
    if not path.is_file():
        raise AssertionError(f"Missing required Step 50X evidence file: {path}")
    return path.read_text(encoding="utf-8")


def assert_contains(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise AssertionError(f"Missing required Step 50X text for {label}: {needle}")


def main() -> int:
    missing = [name for name in REQUIRED_FILES if not (EVIDENCE_DIR / name).is_file()]
    if missing:
        raise AssertionError(f"Missing required Step 50X files: {missing}")

    combined = "\n".join(read_required_text(name) for name in REQUIRED_FILES)
    go_no_go = read_required_text("go_no_go.md")
    web_mismatch = read_required_text("web_healthcheck_mismatch.md")
    minio_fix = read_required_text("minio_file_store_fix.md")
    redaction_note = read_required_text("redaction_note.md")

    if go_no_go.count("ORACLE_ONYX_STAGING_PARTIAL_GO") != 1:
        raise AssertionError("go_no_go.md must contain exactly one Step 50X classification")

    for needle in REQUIRED_BOUNDARIES:
        assert_contains(combined, needle, needle)

    assert_contains(web_mismatch, "127.0.0.1:3000", "web healthcheck target")
    assert_contains(web_mismatch, "ECONNREFUSED", "loopback probe failure")
    assert_contains(web_mismatch, "HTTP `200`", "hostname/IP web reachability")
    assert_contains(minio_fix, "onyx-file-store-bucket", "MinIO bucket creation")
    assert_contains(minio_fix, "staging diagnostic evidence only", "MinIO architecture boundary")
    assert_contains(redaction_note, "SSH private key", "SSH key redaction warning")

    for claim in UNSUPPORTED_POSITIVE_CLAIMS:
        if claim in combined:
            raise AssertionError(f"Unsupported Step 50X positive claim found: {claim}")

    print("PASS: Step 50X Oracle staging evidence package is complete.")
    print("PASS: Classification is ORACLE_ONYX_STAGING_PARTIAL_GO.")
    print("PASS: Production, enterprise, external validation, compliance, web healthcheck, MinIO, and redaction claim boundaries are preserved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
