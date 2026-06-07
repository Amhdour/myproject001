# Reviewer Commands

These commands are intentionally scoped to fast, local, reviewer-facing checks. They do not require a full production deployment and do not prove production readiness, enterprise readiness, external validation, compliance certification, live blocking, or live filtering.

| Purpose | Status | Command | Expected result | Output / evidence path |
|---|---|---|---|---|
| Setup / environment check | Verified | `python --version && pytest --version` | Prints Python and pytest versions available to the reviewer. | `docs/security/evidence/step_64x_retrieved_content_prompt_injection_proof/reviewer_command_output.md` |
| Focused security tests | Verified | `PYTHONPATH=. pytest backend/security_layer/tests/test_retrieved_content_prompt_injection.py backend/security_layer/tests/test_demo_attack_runner.py -q` | Focused retrieved-content detector and demo-runner tests pass. | `docs/security/evidence/step_64x_retrieved_content_prompt_injection_proof/retrieval_context_hook_test_result.md` |
| Prompt-injection tests | Verified | `PYTHONPATH=. pytest backend/security_layer/tests/test_retrieved_content_prompt_injection.py -q` | Retrieved-content prompt-injection detector, mode behavior, negative case, and hook-wiring proof pass. | `docs/security/evidence/step_64x_retrieved_content_prompt_injection_proof/prompt_injection_detector_test_result.md` |
| Demo attack command | Verified | `python demo_attacks/run_demo_attacks.py` | Six synthetic demo attacks, including retrieved-content prompt injection, return `denied_or_flagged`. | `docs/security/evidence/step_64x_retrieved_content_prompt_injection_proof/demo_attack_result.md` |
| Evidence validation | Verified | `python scripts/security/validate_security_evidence.py` | Required security evidence paths exist and are non-empty. | `docs/security/evidence/step_64x_retrieved_content_prompt_injection_proof/reviewer_command_output.md` |
| Claim-boundary validation | Verified | `python scripts/portfolio/check_claim_boundary.py && python scripts/portfolio/check_no_fake_claims.py` | No unsupported positive production, enterprise, compliance, external-validation, or live-enforcement claims are found. | `docs/security/evidence/step_64x_retrieved_content_prompt_injection_proof/reviewer_command_output.md` |
| Evidence-link validation | Verified | `python scripts/portfolio/check_evidence_links.py` | Required reviewer evidence files are present. | `docs/security/evidence/step_64x_retrieved_content_prompt_injection_proof/reviewer_command_output.md` |
| Full project dependency sync | Blocked in this workspace | `uv run --group backend --group dev -- python -m pytest backend/security_layer/tests/test_retrieved_content_prompt_injection.py -q` | Expected on a compatible Python 3.11 environment; blocked here because the current CPython 3.14 environment cannot install the locked `onnxruntime==1.20.1` wheel. | `docs/security/evidence/step_64x_retrieved_content_prompt_injection_proof/limitations.md` |

## Interpretation

- `Verified` means the command was run in this workspace and evidence is included under the listed path.
- `Blocked` means the command exists but was blocked by an environment/dependency limitation, not by a known control failure.
- Passing commands support only bounded portfolio/demo/test claims. They do not prove full prompt-injection defense, production readiness, enterprise readiness, staging proof, external validation, or compliance certification.
