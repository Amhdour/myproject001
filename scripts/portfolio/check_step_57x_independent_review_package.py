#!/usr/bin/env python3
"""Validate Step 57X independent reviewer package and claim boundaries."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "docs/security/evidence/step_57x_independent_reviewer_package_request"
CLASSIFICATION = "INDEPENDENT_REVIEW_PACKAGE_READY_EXTERNAL_VALIDATION_REQUEST_PENDING"
REQUIRED_FILES = [
    "README.md",
    "reviewer_package_summary.md",
    "evidence_map_for_reviewer.md",
    "claims_to_validate.md",
    "claims_not_made.md",
    "reviewer_questions.md",
    "reviewer_checklist.md",
    "reproduction_guide.md",
    "review_request_email.md",
    "reviewer_response_template.md",
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
    "External validation | REQUEST PACKAGE READY / NOT YET COMPLETED",
    "Production readiness after Step 57X | NO-GO",
    "Enterprise production-candidate readiness after Step 57X | NO-GO / 7–9%",
    "Compliance certification after Step 57X | NOT CLAIMED",
    "reviewer_questions.md",
    "reviewer_response_template.md",
    "redaction_note.md",
]
REQUIRED_QUESTIONS = [
    "Does the evidence support the stated 92% production-style portfolio readiness?",
    "Are the claim boundaries honest?",
    "Is the Oracle staging PARTIAL GO classification justified?",
    "Is the runtime enforcement PARTIAL GO classification justified?",
    "Is the Step 39X runtime hook actually deployed in the diagnostic custom API container?",
    "Does the smoke test prove enough for a portfolio-level claim?",
    "What evidence is still missing for a client-facing pilot?",
    "What evidence is still missing for enterprise production-candidate?",
    "Are redaction and secret-handling practices acceptable?",
    "What should be fixed before showing this to an AI agency or client?",
    "What should be fixed before public portfolio publication?",
    "What should be fixed before paid consulting use?",
]
DOC_BOUNDARIES = [
    "Production readiness after Step 57X | NO-GO",
    "Enterprise production-candidate readiness after Step 57X | NO-GO / 7–9%",
    "External validation: REQUEST PACKAGE READY / NOT YET COMPLETED",
    "Compliance certification: NOT CLAIMED",
]
UNSUPPORTED_POSITIVE_CLAIMS = [
    "external validation is complete",
    "external validation complete",
    "independent review is complete",
    "independent review has happened",
    "third-party approval",
    "production readiness is achieved",
    "enterprise production-candidate readiness is achieved",
    "compliance certified",
    "security certified",
    "externally validated",
]
SAFE_CONTEXT_MARKERS = [
    "not",
    "no ",
    "must not",
    "does not",
    "do not",
    "until",
    "not yet completed",
    "not claimed",
    "request package ready",
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


def main() -> int:
    missing = [name for name in REQUIRED_FILES if not (EVIDENCE_DIR / name).is_file()]
    if missing:
        raise AssertionError(f"Missing required Step 57X files: {missing}")

    combined = "\n".join(read(EVIDENCE_DIR / name) for name in REQUIRED_FILES)
    docs_combined = "\n".join(read(ROOT / path) for path in REQUIRED_DOCS)

    for needle in REQUIRED_TEXT:
        if needle not in combined:
            raise AssertionError(f"Missing required Step 57X package text: {needle}")

    questions = read(EVIDENCE_DIR / "reviewer_questions.md")
    for question in REQUIRED_QUESTIONS:
        if question not in questions:
            raise AssertionError(f"Missing reviewer question: {question}")

    for needle in [
        "Reviewer name",
        "Overall Decision",
        "Evidence supports claims",
        "Evidence partially supports claims",
        "Evidence does not support claims",
        "Recommended Fixes",
    ]:
        if needle not in read(EVIDENCE_DIR / "reviewer_response_template.md"):
            raise AssertionError(f"Missing reviewer response template text: {needle}")

    for needle in [
        "Do not send raw env dumps",
        "Do not send SSH keys",
        "Do not send OCI secrets",
        "Do not send cookies",
        "Do not send passwords",
        "Do not send access tokens",
    ]:
        if needle not in read(EVIDENCE_DIR / "redaction_note.md"):
            raise AssertionError(f"Missing redaction note text: {needle}")

    for needle in DOC_BOUNDARIES:
        if needle.lower() not in docs_combined.lower():
            raise AssertionError(f"Missing required Step 57X doc boundary: {needle}")

    assert_no_unsupported_positive_claims("Step 57X package", combined)
    assert_no_unsupported_positive_claims("Step 57X updated docs", docs_combined)

    print("PASS: Step 57X independent reviewer package files are complete.")
    print(f"PASS: Classification is {CLASSIFICATION}.")
    print("PASS: External validation is request-package ready and not claimed complete.")
    print("PASS: Production readiness and enterprise production-candidate readiness remain NO-GO.")
    print("PASS: Compliance certification remains NOT CLAIMED.")
    print("PASS: Reviewer questions, response template, and redaction note are present.")
    print("PASS: No unsupported external-validation, production, enterprise, or certification claims found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
