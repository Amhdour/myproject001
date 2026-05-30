# Step 45X Main Branch Evidence

## Required `main` verification commands

```text
$ git checkout main || true
error: pathspec 'main' did not match any file(s) known to git
$ git pull origin main || true
fatal: 'origin' does not appear to be a git repository
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
$ git rev-parse HEAD || true
45d1e02f496a09979870a5fa4c5f82c210689c11
```

## Result

`main` could not be checked out or pulled from this workspace. There is no configured `origin`, no local `main` branch, and no remote branch inventory.

Therefore Step 45X does **not** claim that current GitHub `main` contains Step 39X-45X evidence.

## Current-branch fallback inventory

After `main` checkout failed, the requested file/folder checks were run in the current Step 45X branch at `45d1e02f496a09979870a5fa4c5f82c210689c11`:

| Check | Current-branch result |
|---|---|
| `docs/security/evidence/step_39x_runtime_enforcement_proof` | FOUND |
| `docs/security/evidence/step_40x_runtime_enforcement_pr_review_merge_gate` | FOUND |
| `docs/security/evidence/step_42x_live_staging_deployment_evidence` | FOUND |
| `docs/security/evidence/step_43x_github_remote_pr_ci_verification_gate` | FOUND |
| `docs/security/evidence/step_44x_local_repository_recovery_branch_commit_integrity_gate` | FOUND |
| `backend/onyx/context/search/retrieval/search_runner.py` | FOUND |
| `backend/security_layer/runtime_enforcement` | FOUND |
| `backend/security_layer/tests/test_step_39x_runtime_enforcement.py` | FOUND |
| `_apply_step_39x_runtime_enforcement_hook` in `search_runner.py` | FOUND at lines reported by grep: `190` and `235` |

## Step 45X evidence on main

Step 45X evidence is created on branch `step-45x-github-pr-chain-ci-actions-verification`. It cannot be claimed to exist on `main` until this branch is merged and `main` containment is verified by local checkout or GitHub API/CLI evidence.
