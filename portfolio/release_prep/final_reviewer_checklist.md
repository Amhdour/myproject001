# Final Reviewer Checklist

Use this checklist to review the portfolio package without expanding its claims beyond the evidence.

- [ ] Read the root `README.md`.
- [ ] Read `portfolio/README.md`.
- [ ] Read `PORTFOLIO_CASE_STUDY.md`.
- [ ] Read the claim boundary in `CLAIM_BOUNDARY.md` and `portfolio/claim_boundary.md`.
- [ ] Run the demo attack runner: `python demo_attacks/run_demo_attacks.py`.
- [ ] Run the portfolio validation scripts:
  - [ ] `python scripts/portfolio/check_claim_boundary.py`
  - [ ] `python scripts/portfolio/check_no_fake_claims.py`
  - [ ] `python scripts/portfolio/check_evidence_links.py`
- [ ] Run or review security-layer tests: `python -m pytest backend/security_layer/tests -q`.
- [ ] Review CI workflows and real run results for the commit under review.
- [ ] Review `portfolio/evidence_index.md` and the evidence package under `docs/security/evidence/final_portfolio_package/`.
- [ ] Review known limitations and remaining gaps.
- [ ] Confirm no production readiness claim was added.
- [ ] Confirm no enterprise readiness claim was added.
- [ ] Confirm no compliance certification claim was added.
- [ ] Confirm no external-validation claim was added.
- [ ] Confirm no full Onyx live staging claim was added unless real evidence exists.
- [ ] Confirm no live enforcement, live blocking, or live filtering claim was added.
