# Step 01 Reproducibility Gate Summary

## Status

**CONDITIONAL** — the evidence files for the Step 01 reproducibility gate were created, and the local frontend lint command passed, but baseline verification remains incomplete because multiple validation paths are blocked or unverified.

## Exact blockers

- `DOCKER_STAGING_BLOCKED`: `docker` was not found, so `docker compose -f deployment/docker_compose/docker-compose.yml config` failed with exit code `127`.
- `TEST_EXECUTION_BLOCKED`: `source .venv/bin/activate && python -m pytest --collect-only backend/tests/unit -q` failed with exit code `1` because `.venv/bin/python` reported `No module named pytest`.
- `CI_ACTIONS_UNVERIFIED`: `.github/workflows` files were inventoried, but GitHub Actions execution was not verified locally.

## Exact proof files

- `docs/security/evidence/step_01_reproducibility_gate.md`
- `docs/security/evidence/step_01_reproducibility_gate_summary.md`

## Validation result snapshot

- Passed: `cd web && npm run lint -- --help` exited `0`.
- Passed: `cd web && npm run lint` exited `0`.
- Failed: `source .venv/bin/activate && python -m pytest --collect-only backend/tests/unit -q` exited `1`.
- Failed: `docker compose -f deployment/docker_compose/docker-compose.yml config` exited `127`.

## Readiness percentages for this evidence snapshot

- Production readiness: **0% / NO-GO**.
- Enterprise readiness: **0% / NO-GO**.
- Live enforcement readiness: **0% / NO-GO**.
- Step 01 reproducibility gate documentation completion: **100% for evidence-file creation only**.
- Step 01 baseline validation completion: **conditional / incomplete** due to the exact blockers above.

## Claim boundary

This step documents reproducibility evidence only. It does not add controls, alter application behavior, prove production readiness, prove enterprise readiness, or prove live enforcement.

## Next recommended step

Re-run this gate in an environment with Docker available and Python test dependencies installed in `.venv`, then attach CI run evidence or workflow logs before advancing to the next portfolio step.
