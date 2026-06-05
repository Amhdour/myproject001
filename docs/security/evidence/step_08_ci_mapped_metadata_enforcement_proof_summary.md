# Step 08 — CI Mapped-Metadata Enforcement Proof Summary

## What changed

Step 08 extends the focused retrieval ACL GitHub Actions workflow so reviewers can verify the Step 07 mapped-metadata enforcement proof in CI alongside the existing enforcement-hook and real-path shadow-observation tests.

## Workflow

- Workflow name: `Retrieval ACL Real-Path CI Proof Tests`
- Workflow path: `.github/workflows/retrieval-acl-real-path-shadow-observation-tests.yml`
- Artifact name: `retrieval-acl-real-path-ci-proof-test-evidence`

## Exact tests included

- `backend/security_layer/tests/test_retrieval_acl_real_path_mapped_metadata.py`
- `backend/security_layer/tests/test_retrieval_acl_enforce_hook.py`
- `backend/security_layer/tests/test_retrieval_acl_real_path_shadow_observation.py`

## Exact commands

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_real_path_mapped_metadata.py -q
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_enforce_hook.py -q
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_real_path_shadow_observation.py -q
python scripts/portfolio/check_claim_boundary.py
```

## CI status

- CI status: `PENDING_CI`
- No GitHub Actions pass is claimed until the workflow has run on the branch or pull request.

## Safe claims

- The workflow now includes mapped-metadata enforcement tests.
- The workflow still includes enforcement-hook and real-path shadow-observation proof tests.
- Off mode and shadow mode preservation boundaries remain covered by the focused tests.
- Enforce mode remains opt-in behind `ONYX_SECURITY_RETRIEVAL_ACL_MODE=enforce`.
- Production readiness and enterprise readiness remain `NO-GO`.

## Forbidden claims

Do not claim production readiness, enterprise readiness, staging validation, full Onyx-wide enforcement, live filtering, live blocking, compliance certification, or CI success while the status remains `PENDING_CI`.

## Remaining blockers

- GitHub Actions result is still pending.
- This step does not add new runtime controls.
- This step does not add staging validation.
- This step does not prove full real retrieval tenant metadata coverage.

## Updated readiness percentages

These percentages are portfolio-review estimates only, not production readiness claims.

- Production-style portfolio coverage: remains about `99%` as a reviewer artifact only.
- Retrieval ACL mapped-metadata CI proof: `PENDING_CI`.
- Production readiness: `NO-GO / 0%`.
- Enterprise production-candidate readiness: `NO-GO / 7–9%`.
- Staging validation for this step: not claimed / `0%`.
