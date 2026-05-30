# Release Preparation Package

## Purpose

This package prepares the portfolio for professional review and public sharing by collecting the final reviewer-facing release materials in one place. It is intended to help reviewers, agencies, employers, and portfolio evaluators understand what to inspect, what can be demonstrated locally, and which claims remain explicitly out of scope.

This package prepares the portfolio for professional review/public sharing. It does not prove production readiness, enterprise readiness, external validation, compliance certification, full Onyx staging, live enforcement, live blocking, or live filtering.

## Scope

The release-prep package is documentation-only. It covers:

- manual screenshot planning,
- an optional video walkthrough script,
- a draft GitHub release note for a future portfolio-review tag,
- final reviewer checklist items,
- publication-readiness checks,
- sanitization checks before sharing any repository, screenshots, logs, or walkthrough videos.

It does not modify runtime application behavior, activate security controls, enable live enforcement, or create deployment evidence.

## What This Release-Prep Package Is

This package is a reviewer-readiness bundle for the existing portfolio evidence room. It helps a reviewer move through the repository in a safe order:

1. Confirm the claim boundary.
2. Review the portfolio package.
3. Run the demo and validation commands.
4. Inspect CI and evidence artifacts.
5. Decide whether the repository is ready to be shared as a portfolio artifact.

## What This Release-Prep Package Is Not

This package is not:

- a production readiness assessment,
- an enterprise readiness assessment,
- an external audit,
- a compliance certification package,
- proof of full Onyx live staging,
- evidence of live enforcement,
- evidence of shadow-deny runtime activation,
- evidence of live blocking,
- evidence of live filtering,
- a source of fabricated screenshots, logs, or deployment claims.

## Required Reviewer Artifacts

The release-prep reviewer path includes these artifacts:

- [`screenshot_checklist.md`](screenshot_checklist.md) — manual screenshot capture plan and sanitization warnings.
- [`video_walkthrough_script.md`](video_walkthrough_script.md) — seven-minute reviewer walkthrough script with safe language.
- [`github_release_notes_draft.md`](github_release_notes_draft.md) — draft release notes for a future `v0.1.0-portfolio-review` tag.
- [`final_reviewer_checklist.md`](final_reviewer_checklist.md) — final review sequence and validation checklist.
- [`publication_readiness_checklist.md`](publication_readiness_checklist.md) — checklist before public sharing or employer/agency sharing.
- [`sanitization_checklist.md`](sanitization_checklist.md) — secret, screenshot, deployment, log, and public-sharing sanitization checklist.
- [`../../docs/security/evidence/release_prep/release_go_no_go.md`](../../docs/security/evidence/release_prep/release_go_no_go.md) — release-prep GO/NO-GO matrix.

## How To Use The Checklist

Use this package immediately before public sharing or reviewer delivery:

1. Read the root [`README.md`](../../README.md) and portfolio [`README.md`](../README.md).
2. Confirm the claim boundary in [`../claim_boundary.md`](../claim_boundary.md) and [`../../CLAIM_BOUNDARY.md`](../../CLAIM_BOUNDARY.md).
3. Run the demo and validation commands listed in the draft release notes.
4. Complete the final reviewer checklist.
5. Complete the publication-readiness checklist.
6. Complete the sanitization checklist before adding optional screenshots or recording an optional video.
7. Do not publish screenshots, logs, URLs, or deployment evidence unless they were captured manually and sanitized.

## Claim Boundary

Safe description: this is a production-style portfolio project for RAG and autonomous-agent security readiness.

Forbidden interpretation: this package must not be used to claim production readiness, enterprise readiness, external validation, compliance certification, full Onyx live staging, live enforcement, live blocking, or live filtering.

The repository's NO-GO / PENDING / NOT CLAIMED language remains authoritative.
