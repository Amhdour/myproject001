# Release Preparation GO/NO-GO Matrix

This matrix applies only to portfolio release preparation. It does not approve production use, enterprise use, compliance claims, or live security-control enforcement.

| Item | Status | Evidence / Condition | Boundary |
|---|---:|---|---|
| Portfolio documentation package | GO | Root README, portfolio README, case study, claim boundary, and evidence index are present. | GO for portfolio review only. |
| Reviewer package | GO | `portfolio/` and `portfolio/release_prep/` provide reviewer routes, checklists, and safe release-prep instructions. | GO for professional review/public sharing preparation only. |
| CI gates | GO if passing | GitHub Actions or local commands must pass for the commit being shared. | A passing run is commit-scoped, not production proof. |
| Demo attack runner | GO if passing | `python demo_attacks/run_demo_attacks.py` must pass locally or in CI for the commit being shared. | Synthetic demo only; not live blocking or live filtering proof. |
| Claim boundary | GO if checks passing | `python scripts/portfolio/check_claim_boundary.py` and `python scripts/portfolio/check_no_fake_claims.py` must pass. | Scanner scope only; claim boundary still requires human review. |
| Public release | CONDITIONAL on sanitization | Publication-readiness and sanitization checklists must be completed before sharing. | Do not publish secrets, private infrastructure details, fake screenshots, or fake evidence. |
| Production readiness | NO-GO | No production-readiness evidence is claimed. | Must not be marketed as production-ready. |
| Enterprise readiness | NO-GO | No enterprise-readiness evidence is claimed. | Must not be marketed as enterprise-ready. |
| External validation | PENDING | No external validation evidence is claimed. | Must not claim external validation. |
| Compliance certification | NOT CLAIMED | No certification evidence is claimed. | Must not claim compliance certification. |
| Full Onyx live staging | NOT CLAIMED unless evidence exists | Only real repository evidence can change this status. | Do not infer full live staging from docs or minimal staging plans. |
| Live enforcement/blocking/filtering | NOT CLAIMED | No live enforce-mode, live blocking, or live filtering evidence is claimed. | Do not claim live protection or activation. |
