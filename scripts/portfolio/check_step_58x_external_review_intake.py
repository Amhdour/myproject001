#!/usr/bin/env python3
"""Validate Step 58X external reviewer response intake and finding tracker."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "docs/security/evidence/step_58x_external_reviewer_response_intake_finding_tracker"
STEP_57X_DIR = ROOT / "docs/security/evidence/step_57x_independent_reviewer_package_request"
CLASSIFICATION = "EXTERNAL_REVIEW_INTAKE_READY_NO_RESPONSE_YET"
REQUIRED_FILES = [
    "README.md",
    "intake_process.md",
    "reviewer_response_intake_form.md",
    "finding_tracker.md",
    "finding_severity_model.md",
    "evidence_mapping_template.md",
    "remediation_plan_template.md",
    "closure_criteria.md",
    "reviewer_decision_record_template.md",
    "go_no_go.md",
    "remaining_limitations.md",
    "redaction_note.md",
]
REQUIRED_DOCS = [
    "docs/security/execution_tracker.md",
    "docs/security/evidence_report.md",
    "docs/security/known_limitations.md",
    "portfolio/evidence_index.md",
    "portfolio/release_candidate/final_go_no_go.md",
    "PORTFOLIO_CASE_STUDY.md",
]
REQUIRED_TEXT = [
    CLASSIFICATION,
    "Production-style portfolio readiness",
    "92%",
    "Enterprise production-candidate",
    "NO-GO / 7–9%",
    "External validation",
    "REQUEST PACKAGE READY / NO RESPONSE YET",
    "Compliance certification",
    "NOT CLAIMED",
]
REQUIRED_PACKAGE_TEXT = [
    "intake/tracking system only",
    "../step_57x_independent_reviewer_package_request/",
    "Receive reviewer response",
    "Confirm reviewer identity/role, date, and scope",
    "Redact sensitive data",
    "Store response summary",
    "Extract findings",
    "Assign severity",
    "Map finding to evidence",
    "Decide remediation action",
    "Track status",
    "Re-test and collect evidence",
    "Close finding only after evidence exists",
    "Update final validation status",
    "Reviewer name",
    "Reviewer role",
    "Organization, optional",
    "Date received",
    "Review scope",
    "Evidence reviewed",
    "Overall reviewer decision",
    "Reviewer comments",
    "Findings summary",
    "Required fixes",
    "Recommended fixes",
    "Claim-boundary feedback",
    "Permission to quote reviewer? yes/no",
    "Public attribution allowed? yes/no",
    "Confidentiality restrictions",
    "Raw response location",
    "Sanitized response location",
    "Finding ID | Source reviewer | Date | Title | Severity | Category | Evidence path | Affected claim | Status | Owner | Remediation step | Retest evidence | Closure date | Notes",
    "OPEN",
    "TRIAGED",
    "ACCEPTED_RISK",
    "IN_PROGRESS",
    "FIXED_PENDING_RETEST",
    "CLOSED_VERIFIED",
    "REJECTED_WITH_REASON",
    "CRITICAL",
    "HIGH",
    "MEDIUM",
    "LOW",
    "INFO",
    "Findings cannot be closed by assertion only",
    "Closure requires evidence",
    "Critical/high findings require retest evidence",
    "Reviewer approval is not assumed unless explicitly provided",
    "Do not commit raw reviewer email if confidential",
    "Store sanitized summaries in repo",
]
DOC_BOUNDARIES = [
    CLASSIFICATION,
    "Reviewer response received | NO",
    "External validation after Step 58X | REQUEST PACKAGE READY / NO RESPONSE YET",
    "Production readiness after Step 58X | NO-GO",
    "Enterprise production-candidate readiness after Step 58X | NO-GO / 7–9%",
    "Compliance certification after Step 58X | NOT CLAIMED",
]
UNSUPPORTED_POSITIVE_CLAIMS = [
    "reviewed",
    "approved",
    "externally validated",
    "certified",
    "external validation is complete",
    "external validation complete",
    "reviewer response received | yes",
    "reviewer approval received",
    "third-party validation complete",
    "production readiness is achieved",
    "enterprise production-candidate readiness is achieved",
    "compliance certification is complete",
]
SAFE_CONTEXT_MARKERS = [
    "not",
    "no ",
    "must not",
    "does not",
    "do not",
    "unless explicitly",
    "no response yet",
    "not claimed",
    "request package ready",
    "intake",
    "template",
    "future",
    "if ",
    "allowed decision values",
    "evidence reviewed",
    "after step 58x",
    "external validation after step 58x",
]


def read(path: Path) -> str:
    if not path.is_file():
        raise AssertionError(f"Missing required file: {path}")
    return path.read_text(encoding="utf-8")


def assert_no_unsupported_positive_claims(label: str, text: str) -> None:
    for line_number, line in enumerate(text.splitlines(), start=1):
        normalized = " ".join(line.lower().split())
        for phrase in UNSUPPORTED_POSITIVE_CLAIMS:
            if phrase in normalized and not any(marker in normalized for marker in SAFE_CONTEXT_MARKERS):
                raise AssertionError(
                    f"Unsupported positive claim in {label}:{line_number}: {phrase!r}: {line.strip()}"
                )


def assert_contains(text: str, needle: str, label: str) -> None:
    if needle.lower() not in text.lower():
        raise AssertionError(f"Missing required {label}: {needle}")


def main() -> int:
    if not STEP_57X_DIR.is_dir():
        raise AssertionError(f"Step 57X package is unavailable: {STEP_57X_DIR}")

    missing = [name for name in REQUIRED_FILES if not (EVIDENCE_DIR / name).is_file()]
    if missing:
        raise AssertionError(f"Missing required Step 58X files: {missing}")

    combined = "\n".join(read(EVIDENCE_DIR / name) for name in REQUIRED_FILES)
    docs_combined = "\n".join(
        line
        for path in REQUIRED_DOCS
        for line in read(ROOT / path).splitlines()
        if "58X" in line
        or "Step 58X" in line
        or "Reviewer response" in line
        or "NO RESPONSE YET" in line
        or "Enterprise production-candidate readiness" in line
        or "Compliance certification" in line
        or "Production readiness" in line
    )

    for needle in REQUIRED_TEXT:
        assert_contains(combined, needle, "package status text")

    for needle in REQUIRED_PACKAGE_TEXT:
        assert_contains(combined, needle, "package control text")

    for needle in DOC_BOUNDARIES:
        assert_contains(docs_combined, needle, "updated documentation boundary")

    assert_contains(read(EVIDENCE_DIR / "finding_tracker.md"), "| Finding ID | Source reviewer | Date | Title | Severity | Category | Evidence path | Affected claim | Status | Owner | Remediation step | Retest evidence | Closure date | Notes |", "finding tracker table")
    assert_contains(read(EVIDENCE_DIR / "finding_severity_model.md"), "CRITICAL", "severity model")
    assert_contains(read(EVIDENCE_DIR / "closure_criteria.md"), "Closure requires evidence", "closure criteria")
    assert_contains(read(EVIDENCE_DIR / "redaction_note.md"), "Do not commit secrets", "redaction note")

    assert_no_unsupported_positive_claims("Step 58X package", combined)
    assert_no_unsupported_positive_claims("Step 58X updated docs", docs_combined)

    print("PASS: Step 58X required intake files are complete.")
    print(f"PASS: Classification is {CLASSIFICATION}.")
    print("PASS: No reviewer response is claimed.")
    print("PASS: External validation is not claimed complete.")
    print("PASS: Production readiness remains NO-GO.")
    print("PASS: Enterprise production-candidate readiness remains NO-GO / 7–9%.")
    print("PASS: Compliance certification remains NOT CLAIMED.")
    print("PASS: Finding tracker, severity model, closure criteria, and redaction note exist.")
    print("PASS: No unsupported reviewed/approved/externally validated/certified claim detected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
