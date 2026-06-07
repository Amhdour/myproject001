from __future__ import annotations

from pathlib import Path

REQUIRED_PATHS = [
    Path("docs/security/evidence_report.md"),
    Path("docs/security/known_limitations.md"),
    Path("docs/security/evidence/audit/sample_security_audit_events.jsonl"),
    Path("docs/security/evidence/telemetry/sample_security_metrics.json"),
    Path("docs/security/evidence/demo_attacks/demo_attack_results.md"),
    Path("docs/security/evidence/demo_attacks/demo_attack_results.json"),
    Path("backend/tests/security/test_policy_decision.py"),
    Path("backend/tests/security/test_security_enforcer.py"),
    Path("backend/tests/security/test_security_audit_logger.py"),
    Path("backend/tests/security/test_security_metrics.py"),
    Path("backend/tests/security/demo_attacks/test_cross_tenant_retrieval_attack.py"),
    Path("backend/tests/security/demo_attacks/test_high_risk_tool_without_approval.py"),
    Path("docs/security/reviewer_commands.md"),
    Path("docs/security/live_hook_gap_report.md"),
    Path("docs/security/evidence/step_64x_retrieved_content_prompt_injection_proof/README.md"),
    Path("docs/security/evidence/step_64x_retrieved_content_prompt_injection_proof/prompt_injection_detector_test_result.md"),
    Path("docs/security/evidence/step_64x_retrieved_content_prompt_injection_proof/retrieval_context_hook_test_result.md"),
    Path("docs/security/evidence/step_64x_retrieved_content_prompt_injection_proof/demo_attack_result.md"),
    Path("docs/security/evidence/step_64x_retrieved_content_prompt_injection_proof/audit_sample.json"),
    Path("docs/security/evidence/step_64x_retrieved_content_prompt_injection_proof/telemetry_sample.json"),
    Path("docs/security/evidence/step_64x_retrieved_content_prompt_injection_proof/reviewer_command_output.md"),
    Path("docs/security/evidence/step_64x_retrieved_content_prompt_injection_proof/ci_status.md"),
    Path("docs/security/evidence/step_64x_retrieved_content_prompt_injection_proof/limitations.md"),
]


def main() -> int:
    missing = [str(path) for path in REQUIRED_PATHS if not path.exists()]
    empty = [str(path) for path in REQUIRED_PATHS if path.exists() and path.is_file() and path.stat().st_size == 0]
    if missing or empty:
        if missing:
            print("Missing required evidence paths:")
            for path in missing:
                print(f"- {path}")
        if empty:
            print("Empty required evidence paths:")
            for path in empty:
                print(f"- {path}")
        return 1
    print(f"Security evidence validation passed for {len(REQUIRED_PATHS)} required paths.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
