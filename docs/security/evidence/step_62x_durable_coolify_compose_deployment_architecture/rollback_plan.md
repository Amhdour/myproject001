# Rollback Plan

## Image Rollback

Restore the backend image variable to the upstream image:

```bash
export ONYX_BACKEND_IMAGE=onyxdotapp/onyx-backend:latest
```

Then redeploy using the selected prior compose path.

## MinIO Rollback Boundary

Stop durable MinIO only if the operator intentionally wants to remove the staging file-store service. Preserve the `minio_data` volume unless intentionally deleting staging test data.

## Redeploy Previous Compose

```bash
docker compose -f deployment/docker_compose/docker-compose.yml up -d
```

If Coolify owns the deployment, revert the Coolify configuration to the previous compose file/variables and redeploy through Coolify.

## Verification After Rollback

- Verify the previous partial-go state is restored.
- Record API health, web health, container images, and host/proxy behavior.
- Document rollback evidence in a new dated evidence note.

## Claim Boundary

Rollback does not create production readiness, enterprise production-candidate readiness, external validation, or compliance certification.
