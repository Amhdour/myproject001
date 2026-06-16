#!/usr/bin/env bash
set -euo pipefail

# Oracle VPS Ubuntu staging bootstrap.
# Review before running. Do not paste secrets into this script.

if [[ "${EUID}" -ne 0 ]]; then
  echo "Run as root or with sudo: sudo bash deploy/oracle-vps/bootstrap_ubuntu.sh"
  exit 1
fi

DEPLOY_USER="${DEPLOY_USER:-deploy}"
STAGING_DIR="${STAGING_DIR:-/opt/myproject001-staging}"

export DEBIAN_FRONTEND=noninteractive

apt-get update
apt-get install -y \
  ca-certificates \
  curl \
  gnupg \
  lsb-release \
  ufw \
  git \
  jq

install -m 0755 -d /etc/apt/keyrings
if [[ ! -f /etc/apt/keyrings/docker.gpg ]]; then
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
  chmod a+r /etc/apt/keyrings/docker.gpg
fi

. /etc/os-release

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu ${VERSION_CODENAME} stable" \
  > /etc/apt/sources.list.d/docker.list

apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

if ! id "${DEPLOY_USER}" >/dev/null 2>&1; then
  useradd --create-home --shell /bin/bash "${DEPLOY_USER}"
fi

usermod -aG docker "${DEPLOY_USER}"

mkdir -p "${STAGING_DIR}"
chown -R "${DEPLOY_USER}:${DEPLOY_USER}" "${STAGING_DIR}"
chmod 750 "${STAGING_DIR}"

ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

systemctl enable docker
systemctl start docker

docker --version
docker compose version
ufw status verbose

echo "Bootstrap complete. Log out/in for docker group membership to apply for ${DEPLOY_USER}."
echo "Next: copy compose/Caddy examples into ${STAGING_DIR} and create a real .env.staging outside git."
