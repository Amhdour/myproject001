# Public Sharing Audit

## Purpose

This package is the seventh accelerated portfolio-hardening step. It prepares the repository for professional sharing with AI agencies, employers, partners, or clients by making the reviewer path, hygiene checks, attribution boundaries, and safe public claims easy to inspect.

## Scope

The scope is documentation, audit checklists, and a lightweight validation script only. It does not change runtime application behavior, activate security controls, enable enforcement, or create new live deployment evidence.

## What Public-Sharing Audit Means

A public-sharing audit means the repository has a final manual-review package for:

- confirming reviewer-facing files are present;
- confirming portfolio positioning is clear;
- confirming claim boundaries are visible;
- confirming known limitations and NO-GO / PENDING / NOT CLAIMED language remain visible;
- confirming upstream Onyx attribution and license separation are preserved;
- preparing safe outreach language for agencies, partners, employers, and hiring managers.

## What Public-Sharing Audit Does Not Mean

This audit prepares the repository for professional sharing. It does not prove production readiness, enterprise readiness, external validation, compliance certification, full Onyx staging, live enforcement, live blocking, or live filtering.

It also does not prove that every future public share has been manually sanitized. A human must still review the repository, screenshots, logs, and any linked media before sharing.

## Required Checks Before Sharing

Before sharing the repository publicly or privately with reviewers, run and review:

```bash
python demo_attacks/run_demo_attacks.py
python scripts/portfolio/check_claim_boundary.py
python scripts/portfolio/check_no_fake_claims.py
python scripts/portfolio/check_evidence_links.py
python scripts/portfolio/check_public_sharing_readiness.py
python -m pytest backend/security_layer/tests -q
git diff --check
git diff --stat
```

Manual checks are still required for secrets, private data, screenshots, videos, deployment URLs, customer names, IPs, tokens, SSH keys, private keys, and any real infrastructure details.

## Claim Boundary

Safe public sharing must preserve these boundaries:

- Production readiness: NO-GO.
- Enterprise readiness: NO-GO.
- External validation: PENDING.
- Compliance certification: NOT CLAIMED.
- Full Onyx live staging: NOT CLAIMED unless real repository evidence proves otherwise.
- Live enforcement/blocking/filtering: NOT CLAIMED.

Use this package as a final public-sharing readiness check, not as a production attestation.
