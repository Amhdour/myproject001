# Step 42X Smoke Test Results

## Summary
Deployment smoke tests that require a running app were blocked. Local portfolio/security checks that do not require Docker or a running staging target passed under the system Python environment.

| Required Smoke Test | Command | Result |
|---|---|---|
| App/container/process starts | `docker compose ... up -d --wait` | **BLOCKED**: `/bin/bash: line 6: docker: command not found`; exit `127`. |
| Basic health endpoint | `curl -sS -i http://localhost:3000/api/health` | **BLOCKED**: connection failed; exit `7`. |
| Step 39X runtime enforcement test | `python -m pytest backend/security_layer/tests/test_step_39x_runtime_enforcement.py -q` | **PASS**: `6 passed, 12 warnings in 0.17s`; exit `0`. |
| Full security-layer tests | `python -m pytest backend/security_layer/tests -q` | **PASS**: `274 passed, 8 skipped, 288 warnings in 1.97s`; exit `0`. |
| Demo attack runner | `python demo_attacks/run_demo_attacks.py` | **PASS**: all five synthetic demo attacks passed; exit `0`. |
| Claim-boundary check | `python scripts/portfolio/check_claim_boundary.py` | **PASS**: no unsafe positive readiness claims across 729 reviewer-facing files; exit `0`. |
| No fake claims check | `python scripts/portfolio/check_no_fake_claims.py` | **PASS**: no unsupported positive evidence claims across 729 reviewer-facing files; exit `0`. |
| Evidence links check | `python scripts/portfolio/check_evidence_links.py` | **PASS**: all required reviewer evidence files present; exit `0`. |
| Release-candidate check | `python scripts/portfolio/check_release_candidate.py` | **PASS**: all required release-candidate and prerequisite files present; exit `0`. |

## Demo Attack Output Summary
The demo attack runner reported `Overall result: PASS` for prompt injection, retrieval cross-tenant leakage, unsafe tool call, MCP confused deputy, and sensitive data exposure cases. It also stated that runtime behavior was not modified, live enforcement was not claimed or enabled, and no network/tool/MCP calls were performed.

## Notes
- `source .venv/bin/activate && python -m pytest ...` was attempted first for the Step 39X test, but the virtual environment reported `No module named pytest`. The same test passed with the system Python environment.
- These smoke tests support portfolio evidence integrity only. They do not prove live cloud staging or production readiness.
