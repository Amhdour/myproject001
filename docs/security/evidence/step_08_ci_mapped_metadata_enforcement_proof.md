# Step 08 — CI Mapped-Metadata Enforcement Proof Evidence

## Scope

Step 08 adds a GitHub Actions CI proof path for the Step 07 mapped-metadata Retrieval ACL Enforcement v1 tests and the adjacent enforcement and shadow observation tests.

This evidence records that the workflow is configured. It does not claim that GitHub Actions has already completed on this branch.

## Workflow

- Workflow name: `Retrieval ACL Real-Path CI Proof Tests`
- Workflow path: `.github/workflows/retrieval-acl-real-path-shadow-observation-tests.yml`
- Job name: `Real-path mapped metadata enforcement proof tests`
- Trigger: pull requests touching the focused retrieval ACL proof files, plus manual `workflow_dispatch`
- Artifact name: `retrieval-acl-real-path-ci-proof-test-evidence`

## Exact tests included

- `backend/security_layer/tests/test_retrieval_acl_real_path_mapped_metadata.py`
- `backend/security_layer/tests/test_retrieval_acl_enforce_hook.py`
- `backend/security_layer/tests/test_retrieval_acl_real_path_shadow_observation.py`

## Exact CI commands

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_real_path_mapped_metadata.py -q
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_enforce_hook.py -q
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_real_path_shadow_observation.py -q
python scripts/portfolio/check_claim_boundary.py
```

The workflow pipes each command to a focused evidence log under the uploaded artifact directory.

## CI status

- CI status: `PENDING_CI`
- Reason: the workflow configuration has been added on this branch, but no GitHub Actions result is available inside this local repository session.
- No CI pass claim is made in this evidence file.

## Local proof commands for this step

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_real_path_mapped_metadata.py -q
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_enforce_hook.py -q
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_real_path_shadow_observation.py -q
python scripts/portfolio/check_claim_boundary.py
git diff --check
```

## Safe claims

- The focused GitHub Actions workflow now includes the mapped-metadata enforcement test file.
- The same focused workflow includes the existing enforcement-hook and real-path shadow-observation proof tests.
- The workflow records explicit NO-GO claim-boundary metadata in its evidence artifact.
- Off mode behavior remains a preserve-chunks test boundary.
- Shadow mode behavior remains an observe-only, preserve-chunks test boundary.
- Enforce mode remains behind `ONYX_SECURITY_RETRIEVAL_ACL_MODE=enforce`.
- The workflow runs claim-boundary validation with `python scripts/portfolio/check_claim_boundary.py`.

## Forbidden claims

Do not claim:

- production readiness;
- enterprise readiness;
- staging validation;
- compliance certification;
- full Onyx-wide enforcement;
- live filtering;
- live blocking;
- completed GitHub Actions success while CI status is `PENDING_CI`;
- complete tenant metadata guarantees for every real retrieval chunk.

## Remaining blockers

- GitHub Actions must run on this branch or pull request before this evidence can move from `PENDING_CI` to `CI_PASSED` or `CI_FAILED`.
- This step does not add integration or staging evidence.
- This step does not prove that every real `InferenceChunk.metadata` carries trusted tenant metadata.
- Production readiness remains blocked by the broader launch-gate, staging, monitoring, operational, and external-review requirements outside this focused CI proof.
- Enterprise readiness remains blocked by the same broader requirements plus enterprise deployment, tenant, compliance, and operational evidence not covered here.

## Updated readiness percentages

These percentages are reviewer-facing portfolio estimates only; they are not production-system readiness claims.

- Production-style portfolio coverage: remains about `current separated readiness matrix` as a reviewer artifact only.
- Retrieval ACL mapped-metadata CI proof status: `PENDING_CI` until GitHub Actions completes.
- Production readiness: `NO-GO / 0%`.
- Enterprise production-candidate readiness: `NO-GO`.
- Staging validation: not claimed / `0%` for this step.
- External validation: pending.

## Merge guidance

- Safe to merge: not yet; wait for required local checks and the pull-request GitHub Actions run.
- If GitHub Actions passes, update this evidence from `PENDING_CI` to `CI_PASSED` only with the real workflow result.
- If GitHub Actions fails, update this evidence to `CI_FAILED` and keep production and enterprise readiness as `NO-GO`.
