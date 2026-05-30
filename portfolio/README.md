# RAG & Agent Security Readiness Portfolio

This reviewer package summarizes an Onyx-based RAG/agent security-readiness portfolio for AI agencies, clients, partners, and employers who need a fast, honest overview without reading the full `docs/security/` tree. The upstream Onyx platform provides the RAG and agent foundation; the portfolio contribution is the AI security-readiness layer, evidence package, launch-gate discipline, isolated helpers, tests, and minimal staging evidence where the repository supports it. This package is for professional review, not production attestation.

## Current Status

| Area | Status |
|---|---|
| Portfolio status | In progress |
| Production-style portfolio readiness | 80% |
| Production readiness | NO-GO |
| Enterprise readiness | NO-GO |
| External validation | PENDING |
| Compliance certification | NOT CLAIMED |


## Final Review Package

The fifth accelerated portfolio-hardening step adds a final reviewer-facing package:

- [`../PORTFOLIO_CASE_STUDY.md`](../PORTFOLIO_CASE_STUDY.md)
- [`../CLIENT_README.md`](../CLIENT_README.md)
- [`../EMPLOYER_README.md`](../EMPLOYER_README.md)
- [`../PARTNER_DEMO_README.md`](../PARTNER_DEMO_README.md)
- [`../CLAIM_BOUNDARY.md`](../CLAIM_BOUNDARY.md)
- [`../docs/security/evidence/final_portfolio_package/README.md`](../docs/security/evidence/final_portfolio_package/README.md)

This final package summarizes the project for agencies, clients, partners, and employers while preserving the existing NO-GO / PENDING / NOT CLAIMED boundaries.

## Reviewer Navigation

- **Start here:** this file explains the package scope and claim boundary.
- **Architecture:** [`architecture.md`](architecture.md) separates the upstream platform from the portfolio security-readiness layers.
- **Quickstart:** [`reviewer_quickstart.md`](reviewer_quickstart.md) gives the recommended reading order and local test command.
- **Demo script:** [`demo_script.md`](demo_script.md) provides a five-minute reviewer-safe walkthrough.
- **Claim boundary:** [`claim_boundary.md`](claim_boundary.md) lists safe claims, forbidden claims, and GO / NO-GO / PENDING / NOT CLAIMED status language.
- **Evidence index:** [`evidence_index.md`](evidence_index.md) maps reviewer questions to existing repository evidence and its limits.

## What This Portfolio Package Represents

This repository is built around an Onyx-based RAG and agent system, but the reviewer-facing contribution is the security-readiness work around that system:

- evidence-room organization and evidence-indexing discipline,
- launch-gate and GO / NO-GO decision language,
- claim-boundary controls that preserve NO-GO / PENDING / NOT CLAIMED status,
- isolated helper modules and tests for security-layer behavior,
- demo-attack and readiness narratives for professional review,
- minimal staging evidence only where repository artifacts support it.

Many controls remain isolated, documentation-only, or monitor-only unless existing repository evidence proves otherwise. This package does not claim production readiness, enterprise readiness, compliance certification, external validation, full Onyx live staging, live enforce-mode protection, live shadow-deny runtime, live blocking, or live filtering.

## How Reviewers Should Use This Package

Use `/portfolio` as the entry point, then follow the links into `docs/security/` only when you want detailed evidence. The package is intentionally scoped to help reviewers understand the portfolio quickly while preserving the repository's existing claim boundaries.
