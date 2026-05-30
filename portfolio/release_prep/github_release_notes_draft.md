# Draft GitHub Release Notes

> Draft only. Do not create a tag from this file. Suggested future tag: `v0.1.0-portfolio-review`.

## Summary

This draft release packages the repository as a production-style portfolio review artifact for RAG and autonomous-agent security readiness. It is designed for professional review, agency/employer screening, and evidence-room navigation.

This release would not claim production readiness, enterprise readiness, external validation, compliance certification, full Onyx live staging, live enforcement, live blocking, or live filtering.

## What Is Included

- Root security-readiness portfolio README.
- Reviewer-facing `/portfolio` package.
- Final portfolio case study and audience-specific guides.
- Claim-boundary documentation.
- Synthetic demo attack runner and expected-results documentation.
- Security-layer CI gates and portfolio validation scripts.
- Final release-prep package for screenshots, video walkthrough, reviewer checks, release notes, publication readiness, and sanitization.

## Evidence Package

Review these evidence entry points:

- `portfolio/README.md`
- `portfolio/evidence_index.md`
- `portfolio/claim_boundary.md`
- `docs/security/evidence/final_portfolio_package/README.md`
- `docs/security/evidence/release_prep/README.md`
- `docs/security/evidence/release_prep/release_go_no_go.md`

## Demo Commands

Run from the repository root:

```bash
python demo_attacks/run_demo_attacks.py
python scripts/portfolio/check_claim_boundary.py
python scripts/portfolio/check_no_fake_claims.py
python scripts/portfolio/check_evidence_links.py
python -m pytest backend/security_layer/tests -q
```

## Safe Claims

Safe wording:

- This is a production-style portfolio project for AI security readiness.
- The repository demonstrates documentation, evidence discipline, claim boundaries, synthetic demo attacks, and isolated security-layer tests.
- The demo runner uses synthetic data and deterministic expected outcomes.
- CI gates can validate the configured repository-scope checks when they pass at a specific commit.

## Forbidden Claims

Do not claim:

- production readiness,
- enterprise readiness,
- external validation,
- compliance certification,
- full Onyx live staging,
- live enforce-mode protection,
- live shadow-deny runtime protection,
- live blocking,
- live filtering,
- real customer deployment evidence,
- fake screenshots, fake logs, or fake deployment proof.

## Known Limitations

- Production readiness remains NO-GO.
- Enterprise readiness remains NO-GO.
- External validation remains PENDING.
- Compliance certification remains NOT CLAIMED.
- Full Onyx live staging remains NOT CLAIMED unless real future repository evidence proves otherwise.
- Live enforcement, live blocking, and live filtering remain NOT CLAIMED.
- Optional screenshots and optional video walkthrough remain manual artifacts and must be sanitized if created.

## Reviewer Instructions

1. Start with the root README.
2. Read `portfolio/README.md`.
3. Review the claim boundary before interpreting evidence.
4. Run the demo and validation commands locally.
5. Review CI workflow results for the commit under review.
6. Inspect the final portfolio package and release-prep GO/NO-GO matrix.
7. Confirm no production, enterprise, compliance, external-validation, live-enforcement, live-blocking, or live-filtering claim has been added.
