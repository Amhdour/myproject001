# Step 07 SearchSettings Runtime Annotation Fix

## Metadata

| Field | Value |
| --- | --- |
| UTC timestamp | 2026-06-04T13:23:54Z |
| Branch name | `step-07-fix-searchsettings-runtime-annotation` |
| Base branch | `step-63x-runtime-retrieval-acl-proof` |
| Commit SHA before fix | `cbde6208299c3efdb0d16afb8e9a291394037094` |

## Confirmed CI artifact failure

The Python Backend Test Collection workflow reached pytest collection after `uv sync --frozen` succeeded and pytest was available. The captured CI artifact showed pytest collection failed with 81 collection errors. The repeated collection-time error was:

```text
NameError: name 'SearchSettings' is not defined
```

## Exact source file

```text
backend/onyx/context/search/models.py
```

## Exact root cause

`backend/onyx/context/search/models.py` imported `SearchSettings` only under `TYPE_CHECKING`, but class methods in the same module referenced `SearchSettings` in annotations that were evaluated at runtime. Because `SearchSettings` was not defined at runtime, importing the module during pytest collection raised `NameError`.

## Fix applied

Added this first line to `backend/onyx/context/search/models.py`:

```python
from __future__ import annotations
```

This postpones annotation evaluation so the existing `TYPE_CHECKING`-only import can remain type-checker-only without creating a runtime dependency on `onyx.db.models.SearchSettings`.

## Why this is minimal

- The change is a single import at the top of the failing module.
- The existing type-checking import is preserved.
- No runtime import of `SearchSettings` was added, avoiding possible circular imports.
- No tests were hidden or narrowed.
- No unrelated code was refactored.
- No security controls were added.

## Commands run

```bash
python -m pytest --collect-only backend/tests/unit -q
source .venv/bin/activate && python -m pytest --collect-only backend/tests/unit -q
git diff --check
python scripts/portfolio/check_claim_boundary.py
python scripts/portfolio/check_no_fake_claims.py
ruby -e 'require "yaml"; Dir[".github/workflows/*.yml"].each { |f| YAML.load_file(f) }; puts "YAML parse passed"'
```

## Local results

- `python -m pytest --collect-only backend/tests/unit -q`: failed locally before collection recovery could be assessed because the ambient Python 3.14 environment is missing `fastapi_users`.
- `source .venv/bin/activate && python -m pytest --collect-only backend/tests/unit -q`: failed locally because `.venv` uses Python 3.14 and does not have pytest installed (`No module named pytest`).
- `git diff --check`: passed with no whitespace errors.
- `python scripts/portfolio/check_claim_boundary.py`: passed.
- `python scripts/portfolio/check_no_fake_claims.py`: passed.
- `ruby -e 'require "yaml"; Dir[".github/workflows/*.yml"].each { |f| YAML.load_file(f) }; puts "YAML parse passed"'`: passed.

## Expected CI result

The Python Backend Test Collection workflow should rerun against this branch. If the only collection blocker was runtime evaluation of `SearchSettings` annotations in `backend/onyx/context/search/models.py`, backend unit-test collection is expected to proceed past this specific `NameError`.

## Safe claims

- The CI artifact exposed a concrete pytest collection root cause.
- The root cause was a runtime-evaluated annotation referencing a `TYPE_CHECKING`-only import.
- Step 07 applies the minimal annotation postponement fix to the failing module.
- Production readiness remains `NO-GO`.
- Enterprise readiness remains `NO-GO`.

## Forbidden claims

- Do not claim backend test collection is fully recovered until CI proves the collection command passes.
- Do not claim production readiness.
- Do not claim enterprise readiness.
- Do not claim full backend test success.
- Do not claim the branch is safe to merge solely from this local fix.

## Next step

Run GitHub Actions for the Python Backend Test Collection workflow and classify the result as either `TEST_COLLECTION_RECOVERED_BY_CI` if backend collection passes or `TEST_COLLECTION_FAILED_IN_CI_NEXT_BLOCKER` if collection fails with a new traceback.
