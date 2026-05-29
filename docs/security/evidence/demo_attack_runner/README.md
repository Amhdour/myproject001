# Demo Attack Runner Evidence

## Purpose

This evidence package helps reviewers inspect how the portfolio evaluates common RAG and autonomous-agent security risks with deterministic synthetic cases.

## Scope

The package covers five synthetic demo attacks: prompt injection, retrieval cross-tenant leakage, unsafe tool call, MCP confused deputy, and sensitive data exposure. It is documentation and deterministic demo evidence only.

## Command

```bash
python demo_attacks/run_demo_attacks.py
```

## Expected result

The command should exit with code `0` and report `PASS` for all five cases with the expected decision `denied_or_flagged`.

## Evidence interpretation

A passing result means the synthetic portfolio demo runner produced the expected deterministic outcomes for the five documented cases. It should be interpreted as reviewer-friendly evaluation coverage, not as proof of deployed protection.

## Claim boundary

This evidence proves portfolio-level security evaluation coverage only. It does not prove production protection, live blocking, live filtering, live enforcement, external validation, or compliance.

## What it proves

- The demo runner contains the five required synthetic demo attack cases.
- Each case has an expected deterministic outcome of `denied_or_flagged`.
- The runner can be executed without network, tool, MCP, or runtime application calls.

## What it does NOT prove

- It does not prove production readiness or enterprise readiness.
- It does not prove live Onyx staging, live request-path integration, or runtime enforcement.
- It does not prove external validation, compliance certification, or customer deployment evidence.
