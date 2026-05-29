# CI Security Gates Evidence

## Purpose

This evidence note documents the accelerated CI gates added for the portfolio reviewer package. The gates make the security-readiness documentation and isolated security-layer tests easier for reviewers to evaluate automatically in GitHub Actions.

## Scope

The scope is limited to CI workflows and lightweight validation scripts. This step does not change runtime application behavior, activate security controls, deploy infrastructure, or enable live enforcement.

## Workflows Added

- `.github/workflows/security-layer-tests.yml` runs the isolated `backend/security_layer/tests` pytest suite.
- `.github/workflows/portfolio-claim-boundary.yml` runs portfolio claim-boundary and fake-claim wording checks.
- `.github/workflows/evidence-integrity.yml` verifies that required reviewer evidence files are present.

## What CI Proves

CI passing proves automated portfolio/security-layer checks passed in GitHub Actions for the workflow run under review. In particular, it shows that:

- the isolated security-layer pytest suite completed successfully in CI;
- reviewer-facing claim-boundary checks did not find unsafe positive readiness claims in the scanned files;
- fake or unsupported evidence-claim checks did not find unsafe wording in the scanned files; and
- required reviewer evidence files were present when the evidence-integrity workflow ran.

## What CI Does NOT Prove

CI passing does not prove production readiness.
CI passing does not prove enterprise readiness.
CI passing does not prove compliance certification.
CI passing does not prove external validation.
CI passing does not prove live enforcement, live blocking, live filtering, live shadow-deny runtime protection, or full Onyx staging.

## Claim Boundary

These workflows are portfolio-hardening gates only. They preserve the existing NO-GO, PENDING, and NOT CLAIMED language and are intended to catch unsafe positive claims before review. They must not be interpreted as certification, external audit evidence, production security proof, or live runtime protection evidence.

## Expected Reviewer Interpretation

Reviewers should treat these CI gates as automated consistency checks around the portfolio package. Passing gates increase confidence that the repository maintained its stated claim boundary and that isolated tests ran, but reviewers should not infer operational production security, enterprise deployment readiness, compliance status, or live enforcement from CI success.
