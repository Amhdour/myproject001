# Baseline Validation Record (Step 2)

## Scope
Baseline validation only. No security controls implemented, no refactors, and no behavior changes.

## Baseline Identity
- Requested branch: `security-layer-mvp`
- Actual branch observed: `work`
- Starting commit SHA: `502239d50c41172ae14759fe3cc31780ace71b98`
- Required baseline context SHA: `f647b54` (not found locally)

## Evidence Files
- `docs/security/evidence/baseline/01_repo_state.log`
- `docs/security/evidence/baseline/02_stack_discovery.log`
- `docs/security/evidence/baseline/03_env_checks.log`
- `docs/security/evidence/baseline/04_backend_checks.log`
- `docs/security/evidence/baseline/05_frontend_checks.log`
- `docs/security/evidence/baseline/06_docker_codespaces_checks.log`

## Stack/Service Detection Summary
- Backend framework: FastAPI (`uvicorn onyx.main:app`) with Celery workers (primary, light, docprocessing, docfetching, heavy, monitoring, user_file_processing). Startup evidence from compose files and `backend/scripts/dev_run_background_jobs.py`.
- Frontend framework: Next.js (`next dev`, `next build`, `next start`) with React and TypeScript via `web/package.json`.
- Required services detected: PostgreSQL (`relational_db`), Redis (`cache`), Vespa (`index`), MinIO/object storage (`minio`), model server (`model_server`/`inference_model_server`), plus API/web/celery services via compose and devcontainer env.
- Dependency installation:
  - Python: requirements in `backend/requirements/`.
  - Frontend: `npm install` in `web/`.
- Docker Compose files detected under `deployment/docker_compose/` and `profiling/docker-compose.yml`.
- Devcontainer present: `.devcontainer/devcontainer.json` and docs present.

## Command Matrix
| Command | Expected result | Actual result | Status | Reason (fail/skip) |
|---|---|---|---|---|
| `git branch --show-current` | `security-layer-mvp` | `work` | FAIL | On different branch than requested. |
| `git rev-parse HEAD` | SHA at/after baseline context | `502239d50c...` | PASS | SHA retrieved successfully. |
| `git merge-base --is-ancestor f647b54 HEAD` | exit 0 if baseline ancestor | fatal: invalid object `f647b54` | FAIL | Baseline commit object unavailable locally. |
| `find . -maxdepth 2 -type d \| sort` | repo structure listing | directory tree emitted | PASS | N/A |
| stack discovery (`rg`, `cat web/package.json`, compose/devcontainer discovery) | identify frameworks, startup, services | completed with evidence | PASS | N/A |
| `python --version` | available | `Python 3.14.4` | PASS | N/A |
| `node --version` | available | `v24.15.0` | PASS | N/A |
| `npm --version` | available | `11.4.2` | PASS | N/A |
| `pnpm --version` | available or explicit miss | `10.28.1` | PASS | N/A |
| `yarn --version` | available or explicit miss | `4.14.1` | PASS | N/A |
| `docker --version` | Docker CLI available | command not found | FAIL | Docker not installed in current environment. |
| `docker compose version` | Compose available | command not found | FAIL | Docker not installed in current environment. |
| `source .venv/bin/activate && python -m compileall -q backend/onyx backend/model_server` | backend compile pass | unicode compile error in `backend/onyx/natural_language_processing/utils.py` | FAIL | Existing source/env issue; not remediated. |
| `source .venv/bin/activate && pytest --collect-only backend/tests/unit -q` | collect tests | `ModuleNotFoundError: fastapi_users` | FAIL | Missing backend dependency in current env. |
| `source .venv/bin/activate && pytest -xv backend/tests/unit -q` | run unit tests | same import failure | FAIL | Missing backend dependency in current env. |
| `cd web && npm install --dry-run` | install check pass | up to date | PASS | N/A |
| `cd web && npm run lint` | lint pass | passed | PASS | N/A |
| `cd web && npm run types:check` | typecheck pass | `TS2503 Cannot find namespace 'JSX'` | FAIL | Existing type issue. |
| `cd web && npm test -- --watch=false` | tests pass | 35/35 suites passed | PASS | N/A |
| `cd web && npx playwright test --list` | list/smoke available | fails on missing MCP OAuth env vars | FAIL | Required env vars not set. |
| `docker compose -f deployment/docker_compose/docker-compose.yml config` | validate compose | docker not found | FAIL | Docker unavailable. |
| `docker compose -f deployment/docker_compose/docker-compose.dev.yml config` | validate compose | docker not found | FAIL | Docker unavailable. |
| `.devcontainer` inspection (`cat .devcontainer/devcontainer.json`, `cat .devcontainer/README.md`) | inspect readiness | files present and readable | PASS | N/A |

## Codespaces/Devcontainer Readiness Gaps
- Docker CLI unavailable in this execution environment, blocking local compose validation.
- Playwright MCP OAuth test discovery is blocked unless the following are configured: `MCP_OAUTH_CLIENT_ID`, `MCP_OAUTH_CLIENT_SECRET`, `MCP_OAUTH_ISSUER`, `MCP_OAUTH_JWKS_URI`, `MCP_OAUTH_USERNAME`, `MCP_OAUTH_PASSWORD`.
- Backend test collection blocked by missing Python package `fastapi_users` in current environment.

## Constraints Honored
- No fixes applied.
- No refactors.
- No behavior changes.
