# Evidence Summary

## README positioning

- Evidence links: [`../../../../README.md`](../../../../README.md), [`../../../../PORTFOLIO_CASE_STUDY.md`](../../../../PORTFOLIO_CASE_STUDY.md), [`../../../../CLAIM_BOUNDARY.md`](../../../../CLAIM_BOUNDARY.md).
- What it proves: the repository has clear top-level positioning as a production-style portfolio project with explicit NO-GO / PENDING / NOT CLAIMED language.
- What it does not prove: production readiness, enterprise readiness, full live staging, external validation, or compliance certification.

## Portfolio package

- Evidence links: [`../../../../portfolio/README.md`](../../../../portfolio/README.md), [`../../../../portfolio/evidence_index.md`](../../../../portfolio/evidence_index.md), [`../../../../portfolio/claim_boundary.md`](../../../../portfolio/claim_boundary.md).
- What it proves: reviewers have a structured path through architecture, quickstart, demo, evidence, and claim-boundary materials.
- What it does not prove: live runtime control activation or production security.

## CI gates

- Evidence links: [`../../../../.github/workflows/security-layer-tests.yml`](../../../../.github/workflows/security-layer-tests.yml), [`../../../../.github/workflows/portfolio-claim-boundary.yml`](../../../../.github/workflows/portfolio-claim-boundary.yml), [`../../../../.github/workflows/evidence-integrity.yml`](../../../../.github/workflows/evidence-integrity.yml).
- What it proves: the repo contains CI definitions for security-layer tests, claim-boundary checks, and evidence-integrity checks.
- What it does not prove: that every production path is protected or that an external auditor approved the project.

## Demo attack runner

- Evidence links: [`../../../../demo_attacks/README.md`](../../../../demo_attacks/README.md), [`../../../../demo_attacks/attack_matrix.md`](../../../../demo_attacks/attack_matrix.md), [`../../../../demo_attacks/run_demo_attacks.py`](../../../../demo_attacks/run_demo_attacks.py), [`../demo_attack_runner/README.md`](../demo_attack_runner/README.md), [`../demo_attack_runner/expected_results.md`](../demo_attack_runner/expected_results.md).
- What it proves: the repository includes repeatable synthetic attack scenarios for reviewer demonstration.
- What it does not prove: live application enforcement, real-world attack coverage, or production blocking/filtering.

## Existing security documentation

- Evidence links: [`../../README.md`](../../README.md), [`../../execution_tracker.md`](../../execution_tracker.md), [`../../evidence_report.md`](../../evidence_report.md), [`../../known_limitations.md`](../../known_limitations.md), [`../../partner_safe_claims.md`](../../partner_safe_claims.md).
- What it proves: the project has a security-readiness documentation tree with evidence reporting, limitations, and partner-safe claim language.
- What it does not prove: production operational maturity or compliance certification.

## Existing isolated controls/tests

- Evidence links: [`../../../../backend/security_layer/tests`](../../../../backend/security_layer/tests), [`../../../../backend/security_layer`](../../../../backend/security_layer).
- What it proves: security-layer helpers and tests exist for isolated validation and portfolio review.
- What it does not prove: all helpers are integrated into live Onyx request paths or that enforce mode is active.

## Minimal staging evidence where documented

- Evidence links: [`../step_34x_oracle_free_vps/README.md`](../step_34x_oracle_free_vps/README.md), [`../step_34x_oracle_free_vps/go_no_go.md`](../step_34x_oracle_free_vps/go_no_go.md), [`../step_34x_oracle_free_vps/full_onyx_resource_blocker.md`](../step_34x_oracle_free_vps/full_onyx_resource_blocker.md), [`../coolify_staging_evidence_bundle/go_no_go_summary.md`](../coolify_staging_evidence_bundle/go_no_go_summary.md).
- What it proves: the repository documents limited Oracle/Coolify/minimal staging planning and constraints.
- What it does not prove: full Onyx live staging, production deployment, or enterprise operations.

## Known limitations and NO-GO decisions

- Evidence links: [`../../known_limitations.md`](../../known_limitations.md), [`../../final_claim_boundary.md`](../../final_claim_boundary.md), [`../../partner_safe_claims.md`](../../partner_safe_claims.md), [`remaining_gaps.md`](remaining_gaps.md).
- What it proves: limitations and non-claims are documented rather than hidden.
- What it does not prove: that the limitations have been remediated.
