#!/usr/bin/env bash
set -euo pipefail

# Oracle VPS staging rollback helper.
# Run from /opt/myproject001-staging after reviewing values.
# This script is a helper only; it does not prove rollback until executed and evidenced.

COMPOSE_FILE="${COMPOSE_FILE:-compose.staging.yml}"
ENV_FILE="${ENV_FILE:-.env.staging}"
PREVIOUS_IMAGE_TAG="${PREVIOUS_IMAGE_TAG:-}"
APP_SERVICE="${APP_SERVICE:-app}"
BACKUP_DIR="${BACKUP_DIR:-./backups}"
TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
EXIT_CODE=0

log_pass() { echo "PASS $*"; }
log_fail() { echo "FAIL $*"; EXIT_CODE=1; }
log_info() { echo "INFO $*"; }
log_skip() { echo "SKIP $*"; }

log_info "== Oracle VPS staging rollback helper =="

if [[ ! -f "${COMPOSE_FILE}" ]]; then
  log_fail "compose file missing: ${COMPOSE_FILE}"
fi

if [[ ! -f "${ENV_FILE}" ]]; then
  log_fail "env file missing: ${ENV_FILE}"
fi

if ! command -v docker >/dev/null 2>&1 || ! docker compose version >/dev/null 2>&1; then
  log_fail "docker compose unavailable"
fi

mkdir -p "${BACKUP_DIR}"
chmod 700 "${BACKUP_DIR}"

if [[ "${EXIT_CODE}" -eq 0 ]]; then
  log_info "capturing pre-rollback compose state"
  docker compose --env-file "${ENV_FILE}" -f "${COMPOSE_FILE}" ps > "${BACKUP_DIR}/pre_rollback_compose_ps_${TIMESTAMP}.txt" || true
  docker compose --env-file "${ENV_FILE}" -f "${COMPOSE_FILE}" config > "${BACKUP_DIR}/pre_rollback_compose_config_${TIMESTAMP}.yml" || true
  log_pass "pre-rollback state captured under ${BACKUP_DIR}"
fi

if [[ -z "${PREVIOUS_IMAGE_TAG}" ]]; then
  log_skip "PREVIOUS_IMAGE_TAG not set; image rollback not executed"
else
  log_info "requested rollback target for ${APP_SERVICE}: ${PREVIOUS_IMAGE_TAG}"
  log_info "manual step required: update ${APP_SERVICE} image tag in ${COMPOSE_FILE}, then run docker compose pull/up"
  log_skip "automatic compose file mutation intentionally not performed"
fi

if [[ "${EXIT_CODE}" -eq 0 ]]; then
  log_info "recommended manual rollback commands after compose file is reviewed:"
  echo "docker compose --env-file ${ENV_FILE} -f ${COMPOSE_FILE} pull ${APP_SERVICE}"
  echo "docker compose --env-file ${ENV_FILE} -f ${COMPOSE_FILE} up -d ${APP_SERVICE}"
  echo "docker compose --env-file ${ENV_FILE} -f ${COMPOSE_FILE} ps"
  echo "RESULT: PASS rollback helper prechecks"
else
  echo "RESULT: FAIL rollback helper prechecks"
fi

exit "${EXIT_CODE}"
