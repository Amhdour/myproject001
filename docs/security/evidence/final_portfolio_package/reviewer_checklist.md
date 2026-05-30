# Reviewer Checklist

Use this checklist to review the final portfolio package.

- [ ] README reviewed.
- [ ] Portfolio package reviewed.
- [ ] Claim boundary reviewed.
- [ ] Evidence index reviewed.
- [ ] CI workflows reviewed.
- [ ] Demo attack runner executed.
- [ ] Security-layer pytest executed.
- [ ] Known limitations reviewed.
- [ ] NO-GO/PENDING/NOT CLAIMED boundaries understood.

## Suggested commands

```bash
python demo_attacks/run_demo_attacks.py
python scripts/portfolio/check_claim_boundary.py
python scripts/portfolio/check_no_fake_claims.py
python scripts/portfolio/check_evidence_links.py
python -m pytest backend/security_layer/tests -q
```

## Interpretation

A completed checklist supports portfolio review. It does not convert the project into a production system, an enterprise deployment, an externally reviewed security program, or a certified compliance product.
