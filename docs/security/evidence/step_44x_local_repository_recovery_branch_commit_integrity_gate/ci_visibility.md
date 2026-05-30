# CI Visibility

## GitHub Actions Query Output

```text
### gh run list --repo Amhdour/myproject001 --limit 20
/bin/bash: line 6: gh: command not found
### gh pr checks 102 --repo Amhdour/myproject001 || true
/bin/bash: line 7: gh: command not found
### gh pr checks 103 --repo Amhdour/myproject001 || true
/bin/bash: line 7: gh: command not found
### gh pr checks 104 --repo Amhdour/myproject001 || true
/bin/bash: line 7: gh: command not found
### gh pr checks 105 --repo Amhdour/myproject001 || true
/bin/bash: line 7: gh: command not found
```

## Local Workflow File Inventory

```text
### find .github/workflows -maxdepth 1 -type f -print || true
.github/workflows/security-layer-tests.yml
.github/workflows/portfolio-claim-boundary.yml
.github/workflows/evidence-integrity.yml
### sed -n '1,160p' .github/workflows/security-layer-tests.yml || true
name: Security Layer Tests

on:
  pull_request:
  workflow_dispatch:

jobs:
  security-layer-tests:
    name: Isolated security-layer tests
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install minimal test dependencies
        run: |
          python -m pip install --upgrade pip
          # Minimal dependencies for the isolated portfolio security-layer tests; pydantic is pinned from pyproject.toml.
          # This intentionally does not stand up Onyx services and does not prove production security.
          python -m pip install pytest "pydantic==2.11.7"

      - name: Run isolated security-layer tests
        run: |
          # Passing tests prove isolated security-layer helper behavior only.
          # Passing tests do NOT prove production security, live enforcement, or full Onyx staging.
          python -m pytest backend/security_layer/tests -q
### sed -n '1,160p' .github/workflows/portfolio-claim-boundary.yml || true
name: Portfolio Claim Boundary

on:
  pull_request:
  workflow_dispatch:

jobs:
  portfolio-claim-boundary:
    name: Portfolio claim-boundary checks
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Run claim-boundary checks
        run: |
          python scripts/portfolio/check_claim_boundary.py
          python scripts/portfolio/check_no_fake_claims.py
### sed -n '1,160p' .github/workflows/evidence-integrity.yml || true
name: Evidence Integrity

on:
  pull_request:
  workflow_dispatch:

jobs:
  evidence-integrity:
    name: Reviewer evidence integrity
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Check reviewer evidence files
        run: python scripts/portfolio/check_evidence_links.py
```

## Result
- GitHub Actions run list: **UNAVAILABLE** because `gh` is missing.
- PR checks #102-#105: **UNAVAILABLE** because `gh` is missing.
- Local workflow files: **FOUND** for security-layer tests, portfolio claim-boundary checks, and evidence integrity.
- CI pass/fail status: **NOT CLAIMED**.

## Boundary
Local workflow files show CI configuration exists in the repository, but they do not prove that GitHub Actions ran or passed for any PR.
