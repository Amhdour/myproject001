#!/usr/bin/env bash
set -euo pipefail

# Security scan helper for Oracle VPS staging-prep files.
# Runs public-safe checks against repository deployment templates.
# This script does not scan live secrets and does not prove production readiness.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DEPLOY_DIR="${ROOT_DIR}/deploy/oracle-vps"
OUT_DIR="${OUT_DIR:-${ROOT_DIR}/docs/security/evidence/oracle_vps_staging_foundation/raw_scan_outputs}"
TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
EXIT_CODE=0

grep_excludes=(
  --exclude="validate_staging_prep.sh"
  --exclude="security_scan_staging_prep.sh"
)

log_pass() { echo "PASS $*"; }
log_fail() { echo "FAIL $*"; EXIT_CODE=1; }
log_info() { echo "INFO $*"; }
log_warn() { echo "WARN $*"; }
log_skip() { echo "SKIP $*"; }

mkdir -p "${OUT_DIR}"

log_info "== Oracle VPS staging-prep security scan =="
log_info "Output directory: ${OUT_DIR}"

# Lightweight built-in secret-pattern scan.
SECRET_SCAN_FILE="${OUT_DIR}/secret_pattern_scan_${TIMESTAMP}.txt"
if grep -RInE "${grep_excludes[@]}" "(BEGIN (RSA|OPENSSH|EC|DSA) PRIVATE KEY|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9_]{36,}|github_pat_[A-Za-z0-9_]{22,}|xox[baprs]-|sk-[A-Za-z0-9_-]{20,}|-----BEGIN CERTIFICATE-----)" "${DEPLOY_DIR}" > "${SECRET_SCAN_FILE}"; then
  log_fail "possible secret-like pattern found; review ${SECRET_SCAN_FILE}"
else
  log_pass "built-in secret-pattern scan found no common private-key/API-token patterns"
fi

# Check that example env contains placeholders, not empty real-looking values.
ENV_EXAMPLE="${DEPLOY_DIR}/.env.staging.example"
ENV_SCAN_FILE="${OUT_DIR}/env_placeholder_scan_${TIMESTAMP}.txt"
if [[ -f "${ENV_EXAMPLE}" ]]; then
  if grep -En "PASSWORD=CHANGE_ME|API_KEY=CHANGE_ME|STAGING_DOMAIN=staging.example.com" "${ENV_EXAMPLE}" > "${ENV_SCAN_FILE}"; then
    log_pass "env example uses placeholder values"
  else
    log_warn "env example placeholder expectations not fully matched; review ${ENV_SCAN_FILE}"
  fi
else
  log_fail "env example missing"
fi

# Optional gitleaks if available.
if command -v gitleaks >/dev/null 2>&1; then
  GITLEAKS_FILE="${OUT_DIR}/gitleaks_${TIMESTAMP}.json"
  if gitleaks detect --source "${ROOT_DIR}" --no-git --redact --report-format json --report-path "${GITLEAKS_FILE}"; then
    log_pass "gitleaks scan passed"
  else
    log_fail "gitleaks scan failed; review ${GITLEAKS_FILE}"
  fi
else
  log_skip "gitleaks unavailable"
fi

# Optional trivy config scan if available.
if command -v trivy >/dev/null 2>&1; then
  TRIVY_FILE="${OUT_DIR}/trivy_config_${TIMESTAMP}.txt"
  if trivy config --severity HIGH,CRITICAL "${DEPLOY_DIR}" > "${TRIVY_FILE}"; then
    log_pass "trivy config scan completed without HIGH/CRITICAL failure"
  else
    log_fail "trivy config scan reported findings; review ${TRIVY_FILE}"
  fi
else
  log_skip "trivy unavailable"
fi

# Optional semgrep if available.
if command -v semgrep >/dev/null 2>&1; then
  SEMGREP_FILE="${OUT_DIR}/semgrep_${TIMESTAMP}.txt"
  if semgrep --config auto "${DEPLOY_DIR}" > "${SEMGREP_FILE}"; then
    log_pass "semgrep scan completed"
  else
    log_fail "semgrep scan reported findings; review ${SEMGREP_FILE}"
  fi
else
  log_skip "semgrep unavailable"
fi

if [[ "${EXIT_CODE}" -eq 0 ]]; then
  echo "RESULT: PASS staging-prep security scan"
else
  echo "RESULT: FAIL staging-prep security scan"
fi

exit "${EXIT_CODE}"
