# Demo Attacks

## Purpose

Define the intended structure and evidence model for synthetic demo attacks.

## Scope

Demo attacks are reviewer-facing portfolio evidence. They do not modify application runtime behavior, call live tools, call MCP servers, access network resources, access secret stores, or prove live production protection.

## Current status

Status: bounded synthetic demo bundle with local runner and tests.

## Implemented synthetic cases

- Direct prompt injection.
- Retrieved-content prompt injection.
- Retrieval cross-tenant leakage.
- Unsafe tool call.
- MCP confused deputy.
- Sensitive data exposure.

## Commands

```bash
python demo_attacks/run_demo_attacks.py
PYTHONPATH=. pytest backend/security_layer/tests/test_demo_attack_runner.py -q
```

## Evidence

- `demo_attacks/run_demo_attacks.py`
- `demo_attacks/attack_matrix.md`
- `backend/security_layer/tests/test_demo_attack_runner.py`
- `docs/security/evidence/step_64x_retrieved_content_prompt_injection_proof/demo_attack_result.md`

## Non-Claim Statement

The demo bundle supports portfolio-level evaluation coverage only. It does **not** claim implementation completeness, full prompt-injection defense, live blocking/filtering, production readiness, enterprise readiness, external validation, compliance certification, or live Onyx staging proof.
