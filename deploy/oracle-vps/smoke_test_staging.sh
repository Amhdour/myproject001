#!/usr/bin/env bash
set -euo pipefail

# Oracle VPS staging smoke tests.
# Run after compose services are started on the VPS.
# Do not paste secrets into this script or output.

STAGING_URL="${STAGING_URL:-}"
COMPOSE_FILE="${COMPOSE_FILE:-compose.staging.yml}"
ENV_FILE="${ENV_FILE:-.env.staging}"
EXIT_CODE=0

log_pass() { echo "PASS $*"; }
log_fail() { echo "FAIL $*"; EXIT_CODE=1; }
log_info() { echo "INFO $*"; }
log_skip() { echo "SKIP $*"; }

log_info "== Oracle VPS staging smoke tests =="

if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  log_pass "docker compose available"
else
  log_fail "docker compose unavailable"
fi

if [[ -f "${COMPOSE_FILE}" ]]; then
  log_pass "compose file exists: ${COMPOSE_FILE}"
else
  log_fail "compose file missing: ${COMPOSE_FILE}"
fi

if [[ -f "${ENV_FILE}" ]]; then
  log_pass "env file exists outside git context: ${ENV_FILE}"
else
  log_fail "env file missing: ${ENV_FILE}"
fi

if [[ -f "${COMPOSE_FILE}" && -f "${ENV_FILE}" ]] && command -v docker >/dev/null 2>&1; then
  if docker compose --env-file "${ENV_FILE}" -f "${COMPOSE_FILE}" config >/tmp/myproject001-staging-compose-rendered.yml; then
    log_pass "compose config renders"
  else
    log_fail "compose config does not render"
  fi

  if docker compose --env-file "${ENV_FILE}" -f "${COMPOSE_FILE}" ps >/tmp/myproject001-staging-compose-ps.txt; then
    log_pass "compose ps command works"
  else
    log_fail "compose ps command failed"
  fi
else
  log_skip "compose runtime checks skipped because compose/env/docker is unavailable"
fi

if [[ -n "${STAGING_URL}" ]]; then
  if command -v curl >/dev/null 2>&1; then
    if curl --fail --silent --show-error --max-time 15 "${STAGING_URL}" >/tmp/myproject001-staging-http-response.txt; then
      log_pass "staging URL reachable: ${STAGING_URL}"
    else
      log_fail "staging URL not reachable: ${STAGING_URL}"
    fi
  else
    log_fail "curl unavailable for URL smoke test"
  fi
else
  log_skip "STAGING_URL not set; HTTPS reachability check skipped"
fi

if [[ -f /tmp/myproject001-staging-compose-rendered.yml ]]; then
  if grep -E "(POSTGRES_PASSWORD|QDRANT_API_KEY|GRAFANA_ADMIN_PASSWORD)" /tmp/myproject001-staging-compose-rendered.yml >/dev/null 2>&1; then
    log_info "compose rendered output contains secret variable names; review before publishing evidence"
  fi
fi

if [[ "${EXIT_CODE}" -eq 0 ]]; then
  echo "RESULT: PASS staging smoke tests"
else
  echo "RESULT: FAIL staging smoke tests"
fi

exit "${EXIT_CODE}"
