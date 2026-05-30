# Architecture Decision

## Selected Option

Option B — Compose override.

## Rationale

A dedicated Oracle staging override file is the safest path because it avoids aggressively changing the standard compose file while still giving Coolify/Compose a durable, repeatable way to express the staging-specific requirements.

The base compose files already preserve the Step 61X web healthcheck patch and expose `ONYX_BACKEND_IMAGE` for backend image selection. The override file turns the Oracle staging diagnostic assumptions into explicit deployment configuration for:

- `api_server` and `background` backend image selection.
- MinIO file-store service dependency.
- Required S3/MinIO file-store variables.
- The required bucket name, `onyx-file-store-bucket`.
- The service-local MinIO DNS name, `minio`.
- Explicit Compose project/network naming through variables.

## Avoided Unsafe Coupling

The architecture avoids hardcoded one-time container IPs, one-time container hostnames, public IP addresses, raw credentials, SSH details, private OCI identifiers, and Coolify session material. Service discovery uses Compose service names and the `minio` network alias instead of ephemeral runtime identifiers.

## Step 61X Healthcheck Preservation

The Step 61X web healthcheck patch remains in the base compose files. The healthcheck command keeps the `WEB_HEALTHCHECK_HOST` override and falls back to `require('os').hostname()` so the probe remains hostname-compatible without hardcoding `10.0.3.11`, `127.0.0.1:3000`, or an old container hostname.

## Verification Boundary

This decision is ready for Oracle VPS retest, but the durable architecture is not marked verified on VPS in Step 62X.
