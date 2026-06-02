#!/usr/bin/env bash
set -euo pipefail

# Validate Oracle VPS staging-prep files without requiring real secrets.
# This script is safe to run in a local clone or on the VPS after copying examples.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DEPLOY_DIR="${ROOT_DIR}/deploy/oracle-vps"
TEMP_ENV_FILE="${DEPLOY_DIR}/.env.staging"
EXIT_CODE=0

cleanup() {
  if [[ -f "${TEMP_ENV_FILE}" && "${MYPROJECT001_CREATED_TEMP_ENV:-0}" == "1" ]]; then
    rm -f "${TEMP_ENV_FILE}"
  fi
}
trap cleanup EXIT

required_files=(
  "${DEPLOY_DIR}/README.md"
  "${DEPLOY_DIR}/bootstrap_ubuntu.sh"
  "${DEPLOY_DIR}/compose.staging.example.yml"
  "${DEPLOY_DIR}/.env.staging.example"
  "${DEPLOY_DIR}/Caddyfile.example"
  "${DEPLOY_DIR}/security_boundary.md"
  "${DEPLOY_DIR}/security_scan_staging_prep.sh"
  "${DEPLOY_DIR}/smoke_test_staging.sh"
  "${DEPLOY_DIR}/rollback_staging.sh"
)

grep_excludes=(
  --exclude="validate_staging_prep.sh"
  --exclude="security_scan_staging_prep.sh"
)

echo "== Oracle VPS staging prep validation =="

for file in "${required_files[@]}"; do
  if [[ -f "${file}" ]]; then
    echo "PASS file exists: ${file#${ROOT_DIR}/}"
  else
    echo "FAIL missing file: ${file#${ROOT_DIR}/}"
    EXIT_CODE=1
  fi
done

if grep -RInE "${grep_excludes[@]}" "(BEGIN (RSA|OPENSSH|EC|DSA) PRIVATE KEY|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9_]{36,}|xox[baprs]-|sk-[A-Za-z0-9_-]{20,})" "${DEPLOY_DIR}"; then
  echo "FAIL possible secret-like value found in deploy/oracle-vps"
  EXIT_CODE=1
else
  echo "PASS no common private-key/API-token patterns found in deploy/oracle-vps"
fi

if grep -RInE "${grep_excludes[@]}" "([0-9]{1,3}\.){3}[0-9]{1,3}" "${DEPLOY_DIR}"; then
  echo "WARN IPv4-like value found; verify it is not a live public IP"
else
  echo "PASS no IPv4-like values found in deploy/oracle-vps"
fi

if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  echo "INFO docker compose available; validating compose skeleton syntax"
  if [[ ! -f "${TEMP_ENV_FILE}" ]]; then
    cp "${DEPLOY_DIR}/.env.staging.example" "${TEMP_ENV_FILE}"
    MYPROJECT001_CREATED_TEMP_ENV=1
  fi
  if docker compose --env-file "${DEPLOY_DIR}/.env.staging.example" -f "${DEPLOY_DIR}/compose.staging.example.yml" config >/tmp/myproject001-compose-config.txt; then
    echo "PASS compose skeleton renders with example env"
  else
    echo "FAIL compose skeleton failed to render"
    EXIT_CODE=1
  fi
else
  echo "SKIP docker compose not available; syntax validation not executed"
fi

if [[ "${EXIT_CODE}" -eq 0 ]]; then
  echo "RESULT: PASS staging prep validation"
else
  echo "RESULT: FAIL staging prep validation"
fi

exit "${EXIT_CODE}"
