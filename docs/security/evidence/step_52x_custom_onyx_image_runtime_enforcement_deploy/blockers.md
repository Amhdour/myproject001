# Blockers

## Build Blocker

- `docker` is not installed in this workspace.
- `docker compose` is not available because the Docker CLI is missing.
- Result: local custom backend image build and image runtime-code checks are blocked.

## Deployment Blocker

- SSH hostname `rag-agent-security-staging-v2` could not be resolved from this workspace.
- Result: Oracle VPS deployment, container inventory, deployed image verification, runtime directory check, hook grep, logs, and post-deploy health checks are blocked.

## Required Resolution

Run the reserved build and verification commands on a host with Docker and Oracle VPS access, or provide a secure reachable SSH target. Do not claim `ORACLE_CUSTOM_IMAGE_DEPLOYED_RUNTIME_CODE_PRESENT` until deployed-container evidence proves the custom image, runtime directory, and hook are present.
