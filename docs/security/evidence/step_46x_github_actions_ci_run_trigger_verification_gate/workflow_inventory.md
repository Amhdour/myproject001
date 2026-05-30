# Step 46X Workflow Inventory

## Exact inventory command output

```text
### find .github/workflows -maxdepth 1 -type f -print || true
.github/workflows/evidence-integrity.yml
.github/workflows/security-layer-tests.yml
.github/workflows/portfolio-claim-boundary.yml
### sed -n '1,220p' .github/workflows/security-layer-tests.yml || true
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
### sed -n '1,220p' .github/workflows/portfolio-claim-boundary.yml || true
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
### sed -n '1,220p' .github/workflows/evidence-integrity.yml || true
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

## Workflow summary

| Filename | Workflow name | Trigger events | Branch filters | Jobs | Commands run | Should run on Step 46X PR? | Should run on push to main? | `workflow_dispatch`? |
|---|---|---|---|---|---|---|---|---|
| `.github/workflows/security-layer-tests.yml` | `Security Layer Tests` | `pull_request`, `workflow_dispatch` | None found | `security-layer-tests` / `Isolated security-layer tests` | Install `pytest` and `pydantic==2.11.7`; run `python -m pytest backend/security_layer/tests -q` | Yes, if a GitHub PR is created and Actions are enabled. | No; no `push` trigger is configured. | Yes |
| `.github/workflows/portfolio-claim-boundary.yml` | `Portfolio Claim Boundary` | `pull_request`, `workflow_dispatch` | None found | `portfolio-claim-boundary` / `Portfolio claim-boundary checks` | Run `python scripts/portfolio/check_claim_boundary.py` and `python scripts/portfolio/check_no_fake_claims.py` | Yes, if a GitHub PR is created and Actions are enabled. | No; no `push` trigger is configured. | Yes |
| `.github/workflows/evidence-integrity.yml` | `Evidence Integrity` | `pull_request`, `workflow_dispatch` | None found | `evidence-integrity` / `Reviewer evidence integrity` | Run `python scripts/portfolio/check_evidence_links.py` | Yes, if a GitHub PR is created and Actions are enabled. | No; no `push` trigger is configured. | Yes |

## Claim boundary

This inventory proves local workflow configuration only. It does not prove that GitHub Actions actually ran, passed, failed, or were enabled on GitHub.
