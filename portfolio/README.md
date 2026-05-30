# RAG & Agent Security Readiness Portfolio

This reviewer package summarizes an Onyx-based RAG/agent security-readiness portfolio for AI agencies, clients, partners, and employers who need a fast, honest overview without reading the full `docs/security/` tree. The upstream Onyx platform provides the RAG and agent foundation; the portfolio contribution is the AI security-readiness layer, evidence package, launch-gate discipline, isolated helpers, tests, and minimal staging evidence where the repository supports it. This package is for professional review, not production attestation.

## Current Status

| Area | Status |
|---|---|
| Portfolio status | In progress |
| Production-style portfolio readiness | 97% portfolio presentation readiness after release-candidate package and checks pass, not production-system readiness |
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

## Release Preparation

The sixth accelerated portfolio-hardening step adds a release-prep folder for reviewer delivery and public-sharing readiness:

- [`release_prep/README.md`](release_prep/README.md)
- [`release_prep/screenshot_checklist.md`](release_prep/screenshot_checklist.md)
- [`release_prep/video_walkthrough_script.md`](release_prep/video_walkthrough_script.md)
- [`release_prep/github_release_notes_draft.md`](release_prep/github_release_notes_draft.md)
- [`release_prep/final_reviewer_checklist.md`](release_prep/final_reviewer_checklist.md)
- [`release_prep/publication_readiness_checklist.md`](release_prep/publication_readiness_checklist.md)
- [`release_prep/sanitization_checklist.md`](release_prep/sanitization_checklist.md)
- [`../docs/security/evidence/release_prep/release_go_no_go.md`](../docs/security/evidence/release_prep/release_go_no_go.md)

The release-prep package is documentation-only and preserves the existing NO-GO / PENDING / NOT CLAIMED claim boundary. It does not create screenshots, video evidence, live deployment evidence, or runtime enforcement.

## Public Sharing Audit

The seventh accelerated portfolio-hardening step adds a public-sharing audit package for final repository hygiene and safe reviewer distribution:

- [`public_sharing_audit/README.md`](public_sharing_audit/README.md)
- [`public_sharing_audit/repo_hygiene_checklist.md`](public_sharing_audit/repo_hygiene_checklist.md)
- [`public_sharing_audit/public_review_path.md`](public_sharing_audit/public_review_path.md)
- [`public_sharing_audit/final_safe_claims.md`](public_sharing_audit/final_safe_claims.md)
- [`public_sharing_audit/final_forbidden_claims.md`](public_sharing_audit/final_forbidden_claims.md)
- [`../docs/security/evidence/public_sharing_audit/public_sharing_go_no_go.md`](../docs/security/evidence/public_sharing_audit/public_sharing_go_no_go.md)

This package is documentation and validation-script support only. It does not add production readiness, enterprise readiness, external validation, compliance certification, full Onyx live staging, live enforcement, live blocking, or live filtering claims.

## Release Candidate

The final accelerated portfolio-release-candidate step adds a `v0.1.0-portfolio-review` documentation package for professional review:

- [`release_candidate/README.md`](release_candidate/README.md)
- [`release_candidate/v0.1.0_portfolio_review.md`](release_candidate/v0.1.0_portfolio_review.md)
- [`release_candidate/final_go_no_go.md`](release_candidate/final_go_no_go.md)
- [`../docs/security/evidence/release_candidate/final_evidence_map.md`](../docs/security/evidence/release_candidate/final_evidence_map.md)

This release candidate is documentation, reviewer navigation, checklist, and validation-script support only. It does not prove production readiness, enterprise readiness, external validation, compliance certification, full Onyx live staging, live enforcement, live blocking, or live filtering.

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
