# Portfolio Release Candidate

## Purpose

This package prepares the repository for professional portfolio review as `v0.1.0-portfolio-review`. It gives AI agencies, potential clients, partners, employers, and technical reviewers a concise final path through the RAG and autonomous-agent security-readiness evidence.

This release candidate prepares the portfolio for professional review. It does not prove production readiness, enterprise readiness, external validation, compliance certification, full Onyx staging, live enforcement, live blocking, or live filtering.

## Scope

The release-candidate package is documentation, reviewer navigation, final status language, and a lightweight file-presence validation script only. It covers:

- release-candidate notes and status markers;
- final GO/NO-GO language;
- reviewer reading path;
- commands reviewers can run locally;
- manual review checklist;
- evidence-side release-candidate map.

No runtime application behavior is changed by this package.

## What release candidate means

For this repository, release candidate means the portfolio artifacts are organized for professional review and can be checked for expected files, claim boundaries, and demo/test commands. It is a reviewer-readiness milestone for a portfolio project.

## What release candidate does NOT mean

This release candidate does not mean:

- production readiness;
- enterprise readiness;
- compliance certification;
- external validation;
- a real GitHub release or git tag;
- full Onyx live staging;
- live enforce-mode security;
- live shadow-deny runtime;
- live blocking;
- live filtering;
- deployment evidence beyond existing repository artifacts.

## Reviewer entry points

- [`README.md`](../../README.md) for the top-level portfolio positioning.
- [`PORTFOLIO_CASE_STUDY.md`](../../PORTFOLIO_CASE_STUDY.md) for the final case study.
- [`CLAIM_BOUNDARY.md`](../../CLAIM_BOUNDARY.md) for safe and forbidden claims.
- [`portfolio/README.md`](../README.md) for reviewer navigation.
- [`portfolio/evidence_index.md`](../evidence_index.md) for evidence mapping.
- [`final_reviewer_path.md`](final_reviewer_path.md) for the final review order.
- [`docs/security/evidence/final_reviewer_status_snapshot.md`](../../docs/security/evidence/final_reviewer_status_snapshot.md) for the shortest current proof-state and NO-GO boundary snapshot.
- [`docs/security/evidence/reviewer_ci_proof_chain.md`](../../docs/security/evidence/reviewer_ci_proof_chain.md) for recent CI-backed portfolio proof chain evidence.
- [`docs/security/evidence/release_candidate/final_evidence_map.md`](../../docs/security/evidence/release_candidate/final_evidence_map.md) for evidence-side mapping.

## Required commands

Run these from the repository root:

```bash
python demo_attacks/run_demo_attacks.py
python scripts/portfolio/check_claim_boundary.py
python scripts/portfolio/check_no_fake_claims.py
python scripts/portfolio/check_evidence_links.py
python scripts/portfolio/check_public_sharing_readiness.py
python scripts/portfolio/check_release_candidate.py
python -m pytest backend/security_layer/tests -q
```

See [`final_commands.md`](final_commands.md) for what each command proves and does not prove.

## Manual review requirements

Before public sharing or reviewer outreach, manually confirm:

- previous portfolio PRs are merged in the local repository history;
- CI is green for the current branch or target branch;
- all release-candidate commands pass in the target environment;
- no secrets, credentials, private URLs, customer data, or real infrastructure details are present;
- no fake screenshots, videos, deployment proof, or live evidence are added;
- claim-boundary language remains visible;
- release notes remain draft documentation only.

## Claim boundary

Safe claims are limited to portfolio, production-style, evidence-based security-readiness work for RAG and autonomous-agent systems. Production readiness, enterprise readiness, compliance certification, external validation, full Onyx live staging, live enforcement, live blocking, and live filtering remain NO-GO, PENDING, or NOT CLAIMED unless future real repository evidence proves otherwise.
