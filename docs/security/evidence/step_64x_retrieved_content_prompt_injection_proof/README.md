# Step 64X Retrieved-Content Prompt-Injection Proof

| Field | Value |
|---|---|
| Date | 2026-06-07 |
| Command run | `PYTHONPATH=. pytest backend/security_layer/tests/test_retrieved_content_prompt_injection.py -q`; `python demo_attacks/run_demo_attacks.py`; evidence and claim-boundary commands listed in `docs/security/reviewer_commands.md` |
| Exit code | `0` for focused detector tests and demo attack command in this workspace |
| Result | Bounded retrieved-content prompt-injection detector, monitor/shadow/enforce mode handling, redacted audit sample, telemetry sample, synthetic demo attack, and real search-runner hook wiring are documented. |
| Limitation | This is local/focused proof only. It is not full prompt-injection defense, live production blocking, live filtering, staging validation, external validation, or compliance certification. |
| Safe claim supported | Retrieved-content prompt-injection detection/protection is covered by focused tests and demo evidence in this repository. |

## Evidence included

- `prompt_injection_detector_test_result.md`
- `retrieval_context_hook_test_result.md`
- `demo_attack_result.md`
- `audit_sample.json`
- `telemetry_sample.json`
- `reviewer_command_output.md`
- `ci_status.md`
- `limitations.md`

## Hook boundary

The bounded hook is wired into `backend/onyx/context/search/retrieval/search_runner.py` after Step 39X runtime retrieval enforcement and before retrieved chunks are returned to downstream context construction. The test proves the helper executes and verifies source-level wiring in the real search runner.

## Claim boundary

Do not claim full prompt-injection defense, live production enforcement, live blocking, live filtering, external validation, compliance certification, or enterprise readiness from this evidence.
