# Step 45X Merge Commit Map

## Local merge commits

| PR | Local merge commit | Local object type | Local containing branches | Verification status |
|---:|---|---|---|---|
| #102 | `ad43304445bf99fa3811e5cef3a01724112a2472` | `commit` | `step-45x-github-pr-chain-ci-actions-verification`, `work` | Local object verified; GitHub metadata unavailable |
| #103 | `401d342d61a2fad984ca0b9b4df41433696c56fb` | `commit` | `step-45x-github-pr-chain-ci-actions-verification`, `work` | Local object verified; GitHub metadata unavailable |
| #104 | `d03aca0d5f6a5c09518e3187d21cf62654ee214f` | `commit` | `step-45x-github-pr-chain-ci-actions-verification`, `work` | Local object verified; GitHub metadata unavailable |
| #105 | `bd5dd3805906f84153600b4a6c2d835cb93b8be0` | `commit` | `step-45x-github-pr-chain-ci-actions-verification`, `work` | Local object verified; GitHub metadata unavailable |
| #106 | `45d1e02f496a09979870a5fa4c5f82c210689c11` | `commit` | `step-45x-github-pr-chain-ci-actions-verification`, `work` | Local object verified; GitHub metadata unavailable |

## Verification commands

The following command family was run for each local merge commit:

```text
git cat-file -t <merge_commit_sha> || true
git show --stat --oneline --decorate <merge_commit_sha> || true
git branch --contains <merge_commit_sha> || true
```

All five local merge commits resolved as git commit objects and were contained by the current Step 45X branch and `work`.

## Important limitation

This map is a **local object map**, not a GitHub PR metadata map. GitHub API/CLI access was unavailable, so Step 45X does not independently prove GitHub merged state, GitHub merge-commit assignment, PR URLs, review status, or CI checks.
