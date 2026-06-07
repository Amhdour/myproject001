# Partner Demo Readme

## Audience

This document is for a partner or demo reviewer who wants a fast, safe walkthrough of the portfolio without interpreting it as a production attestation.

## 5-minute demo flow

1. Open the root `README.md` and confirm the NO-GO / PENDING / NOT CLAIMED status language.
2. Open `PORTFOLIO_CASE_STUDY.md` for the final narrative.
3. Open `CLAIM_BOUNDARY.md` before reviewing any readiness claim.
4. Open `portfolio/evidence_index.md` and the final evidence package.
5. Run the local demo and portfolio checks listed below.

## Where to click/read

- Root orientation: `README.md`.
- Final case study: `PORTFOLIO_CASE_STUDY.md`.
- Client view: `CLIENT_README.md`.
- Employer view: `EMPLOYER_README.md`.
- Claim boundary: `CLAIM_BOUNDARY.md` and `portfolio/claim_boundary.md`.
- Evidence index: `portfolio/evidence_index.md`.
- Final package: `docs/security/evidence/final_portfolio_package/README.md`.
- Demo attacks: `demo_attacks/README.md` and `demo_attacks/attack_matrix.md`.

## Commands to run

```bash
python demo_attacks/run_demo_attacks.py
PYTHONPATH=. pytest backend/security_layer/tests/test_retrieved_content_prompt_injection.py -q
python scripts/portfolio/check_claim_boundary.py
python scripts/portfolio/check_no_fake_claims.py
python scripts/portfolio/check_evidence_links.py
python -m pytest backend/security_layer/tests -q
```

## What PASS means

PASS means the local synthetic demo attacks, retrieved-content prompt-injection detector tests, claim-boundary checks, fake-claim checks, evidence-link presence checks, and isolated security-layer tests completed successfully in the current environment.

## What PASS does not mean

PASS does not mean production readiness, enterprise readiness, compliance certification, external validation, full Onyx live staging, live enforce-mode behavior, live shadow-deny runtime behavior, live blocking, or live filtering.

## Status matrix

| Area | Status |
|---|---|
| Portfolio presentation readiness | 94% |
| Technical portfolio proof readiness | 88% |
| Client demo readiness | 85% |
| Production-style runtime proof readiness | 70% for bounded retrieval/context hook proof only |
| Enterprise production-candidate readiness | 20% / NO-GO |
| Real production readiness | 8% / NO-GO |
| Production readiness | NO-GO |
| Enterprise readiness | NO-GO |
| External validation | PENDING |
| Compliance certification | NOT CLAIMED |
| Full Onyx live staging | NOT CLAIMED |
| Live enforcement/blocking/filtering | NOT CLAIMED |
| Live shadow-deny runtime | NOT CLAIMED |
