# Demo Attack Runner

## Purpose

This package gives reviewers a quick, deterministic way to inspect how this portfolio evaluates common RAG and autonomous-agent security risks using synthetic fixtures only.

## Scope

The runner and case notes are documentation-and-evidence artifacts. They do not modify application runtime behavior, enable security controls, call tools, call MCP servers, access network resources, or access secret stores.

## Synthetic-data-only statement

All demo inputs are synthetic. The package uses synthetic tenant IDs, synthetic user IDs, synthetic document labels, fake tool names, fake MCP server names, and fake secret placeholders. It includes no real customer data, real secrets, real tokens, real infrastructure details, or private credentials.

## What demo attacks prove

- The portfolio includes reviewer-friendly coverage for direct prompt injection, retrieved-content prompt injection, retrieval cross-tenant leakage, unsafe tool calls, MCP confused-deputy risk, and sensitive data exposure.
- The deterministic runner can classify the six synthetic demo attacks as `denied_or_flagged`.
- The case files explain expected evidence and claim boundaries for each scenario.

## What demo attacks do NOT prove

- They do not prove production protection, live blocking, live filtering, live enforcement, external validation, compliance, or enterprise readiness.
- They do not prove that any live Onyx request path is protected by these simulated decisions.
- They do not prove deployment evidence, customer evidence, or security-control activation.

## How to run

```bash
python demo_attacks/run_demo_attacks.py
```

## Optional test command

```bash
python -m pytest backend/security_layer/tests/test_demo_attack_runner.py -q
```

## Claim boundary

Demo attacks prove portfolio-level security evaluation coverage only. They do not prove production protection, live blocking, live filtering, live enforcement, external validation, or compliance.
