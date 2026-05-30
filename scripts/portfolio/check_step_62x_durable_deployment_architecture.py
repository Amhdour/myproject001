#!/usr/bin/env python3
"""Validate Step 62X durable deployment architecture evidence boundaries."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "docs/security/evidence/step_62x_durable_coolify_compose_deployment_architecture"
REQUIRED_FILES = [
    "README.md",
    "current_diagnostic_gap.md",
    "architecture_decision.md",
    "compose_changes.md",
    "minio_durable_service.md",
    "custom_backend_image_strategy.md",
    "web_healthcheck_preservation.md",
    "oracle_vps_redeploy_plan.md",
    "retest_checklist.md",
    "rollback_plan.md",
    "go_no_go.md",
    "remaining_limitations.md",
    "redaction_note.md",
]
REQUIRED_REPO_FILES = [
    "deployment/docker_compose/docker-compose.oracle-staging.override.yml",
    "docs/security/oracle_staging_durable_deployment_architecture.md",
]
REQUIRED_MARKERS = {
    "README.md": [
        "DURABLE_DEPLOYMENT_ARCHITECTURE_READY_RETEST_PENDING",
        "SIM-F-004",
        "Production-style portfolio readiness | 92%",
        "Enterprise production-candidate | NO-GO / 7–9%",
        "simulated response only / real validation pending",
        "Compliance certification | NOT CLAIMED",
    ],
    "architecture_decision.md": ["Option B", "WEB_HEALTHCHECK_HOST", "require('os').hostname()"],
    "compose_changes.md": ["docker-compose.oracle-staging.override.yml", "ONYX_BACKEND_IMAGE", "--profile s3-filestore"],
    "minio_durable_service.md": ["minio", "onyx-file-store-bucket", "http://minio:9000", "minio_data:/data"],
    "custom_backend_image_strategy.md": ["api_server", "background", "rag-agent-security-onyx-backend:step53x-b77bee6"],
    "web_healthcheck_preservation.md": ["WEB_HEALTHCHECK_HOST", "require('os').hostname()", "10.0.3.11"],
    "oracle_vps_redeploy_plan.md": ["not claimed as executed", "docker compose", "rollback"],
    "retest_checklist.md": ["Step 55X", "no secrets exposed"],
    "go_no_go.md": [
        "DURABLE_DEPLOYMENT_ARCHITECTURE_READY_RETEST_PENDING",
        "PENDING_USER_EXECUTION",
        "Full staging GO | NOT CLAIMED",
        "Production readiness | NO-GO",
        "Enterprise production-candidate | NO-GO / 7–9%",
        "External validation | simulated response only / real validation pending",
        "Compliance certification | NOT CLAIMED",
    ],
    "remaining_limitations.md": ["Oracle VPS redeploy/retest pending", "Real external validation still pending"],
    "redaction_note.md": ["no raw env dumps", "no passwords", "no tokens", "no MinIO root password in repo"],
}
OVERRIDE_MARKERS = [
    "ONYX_BACKEND_IMAGE",
    "FILE_STORE_BACKEND",
    "SERVICE_NAME_MINIO",
    "S3_ENDPOINT_URL",
    "S3_FILE_STORE_BUCKET_NAME",
    "onyx-file-store-bucket",
    "minio_data:/data",
    "WEB_HEALTHCHECK_HOST",
]
FORBIDDEN_UNSUPPORTED_CLAIMS = [
    "DURABLE_DEPLOYMENT_ARCHITECTURE_VERIFIED_ON_VPS",
    "full staging GO achieved",
    "production readiness achieved",
    "enterprise production-candidate achieved",
    "real external validation complete",
    "compliance certification complete",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []

    for file_name in REQUIRED_FILES:
        path = EVIDENCE_DIR / file_name
        if not path.is_file():
            failures.append(f"missing evidence file: {path.relative_to(ROOT)}")
            continue
        text = read(path)
        for marker in REQUIRED_MARKERS.get(file_name, []):
            if marker not in text:
                failures.append(f"missing marker {marker!r} in {path.relative_to(ROOT)}")

    for file_name in REQUIRED_REPO_FILES:
        path = ROOT / file_name
        if not path.is_file():
            failures.append(f"missing repository file: {file_name}")

    override_path = ROOT / "deployment/docker_compose/docker-compose.oracle-staging.override.yml"
    if override_path.is_file():
        override_text = read(override_path)
        for marker in OVERRIDE_MARKERS:
            if marker not in override_text:
                failures.append(f"missing override marker {marker!r}")

    docs_text = "\n".join(read(EVIDENCE_DIR / file_name) for file_name in REQUIRED_FILES if (EVIDENCE_DIR / file_name).is_file())
    for claim in FORBIDDEN_UNSUPPORTED_CLAIMS:
        if claim.lower() in docs_text.lower():
            failures.append(f"unsupported Step 62X claim found: {claim}")

    if failures:
        print("FAIL: Step 62X durable deployment architecture evidence check failed.")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: Step 62X durable deployment architecture evidence is complete and claim-bounded.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
