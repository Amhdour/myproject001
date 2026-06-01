# Known Limitations

## Step 63X limitations

1. The proof is bounded to the existing runtime retrieval enforcement adapter and focused tests.
2. It does not prove every Onyx retrieval path is protected.
3. It does not prove every connector, cache, rerank, citation, prompt-construction, or streaming path is protected.
4. The telemetry helper is in-memory proof telemetry, not a production monitoring backend.
5. The audit helper remains reviewer/test evidence and does not prove production-grade audit retention.
6. The staging retest remains pending until real Oracle/Coolify command output is added.
7. The CI workflow is pending until GitHub Actions runs and the result is recorded.
8. External validation remains pending until a real reviewer response is received.
9. The normal focused pytest command is blocked in the minimal Oracle VPS verification venv because repo-wide `backend/tests/conftest.py` imports `fastapi_users` before the Step 63X tests execute.
10. Oracle VPS function-level verification passed by importing and running the Step 63X test functions directly without pytest/conftest.
11. Oracle VPS demo-attack verification passed for the bounded cross-tenant retrieval scenario.

## Verified Step 63X Oracle evidence

- `ORACLE_STEP63X_DEMO_ATTACK_PASS`
- `ORACLE_STEP63X_NO_PYTEST_FUNCTION_VERIFIER_PASS`

## Required non-claims

Production readiness remains NO-GO. Enterprise production-candidate readiness remains NO-GO. Full Onyx-wide enforcement is NOT CLAIMED. Full staging GO is NOT CLAIMED. External validation remains PENDING. Compliance certification is NOT CLAIMED.
