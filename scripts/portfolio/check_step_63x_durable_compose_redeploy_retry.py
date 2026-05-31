#!/usr/bin/env python3
"""Validate Step 63X durable Compose redeploy retry evidence package."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "docs/security/evidence/step_63x_durable_compose_redeploy_retry"
REQUIRED_FILES = [
    "README.md",
    "operator_command_bundle.md",
    "classification_rules.md",
    "redaction_note.md",
]
REQUIRED_REPO_FILES = [
    "docs/security/step_63x_durable_compose_redeploy_retry.md",
]
REQUIRED_MARKERS = {
    "README.md": [
        "ORACLE_DURABLE_COMPOSE_REDEPLOY_RETRY_READY_PENDING_OUTPUT",
        "Step 62X",
        "container, image, runtime-code, MinIO, web-health, host-proxy, and status evidence",
        "does not claim that the Oracle VPS commands have been executed",
    ],
    "operator_command_bundle.md": [
        "step63x-durable-compose-retry",
        "BACKGROUND_CONTAINER=$(docker ps --format \"{{.Names}}\" | grep '^onyx-background' | head -1)",
        "DEPLOYED_STEP39X_DIR_FOUND",
        "_apply_step_39x_runtime_enforcement_hook",
        "backend/security_layer/tests/test_step_39x_runtime_enforcement.py -q",
        "onyx-file-store-bucket",
        "WEB_HEALTHCHECK_HOST",
        "ORACLE_DURABLE_COMPOSE_REDEPLOY_VERIFIED",
        "ORACLE_DURABLE_COMPOSE_REDEPLOY_PARTIAL_GO_OR_NO_GO",
    ],
    "classification_rules.md": [
        "ORACLE_DURABLE_COMPOSE_REDEPLOY_VERIFIED",
        "ORACLE_DURABLE_COMPOSE_REDEPLOY_PARTIAL_GO_OR_NO_GO",
        "Do not upgrade a partial result based on intent",
        "production readiness",
        "compliance certification",
    ],
    "redaction_note.md": [
        "<REDACTED>",
        "Do not commit raw `.env` files",
        "MinIO root credentials",
        "Authorization",
    ],
}
FORBIDDEN_UNSUPPORTED_CLAIMS = [
    "ORACLE_DURABLE_COMPOSE_REDEPLOY_VERIFIED_ON_VPS",
    "all required checks passed on Oracle VPS",
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
        for marker in REQUIRED_MARKERS[file_name]:
            if marker not in text:
                failures.append(f"missing marker {marker!r} in {path.relative_to(ROOT)}")

    for file_name in REQUIRED_REPO_FILES:
        path = ROOT / file_name
        if not path.is_file():
            failures.append(f"missing repository file: {file_name}")

    docs_text = "\n".join(
        read(EVIDENCE_DIR / file_name)
        for file_name in REQUIRED_FILES
        if (EVIDENCE_DIR / file_name).is_file()
    )
    docs_text += "\n".join(
        read(ROOT / file_name)
        for file_name in REQUIRED_REPO_FILES
        if (ROOT / file_name).is_file()
    )
    for claim in FORBIDDEN_UNSUPPORTED_CLAIMS:
        if claim.lower() in docs_text.lower():
            failures.append(f"unsupported Step 63X claim found: {claim}")

    if failures:
        print("FAIL: Step 63X durable Compose redeploy retry package check failed.")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: Step 63X durable Compose redeploy retry package is complete and claim-bounded.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
