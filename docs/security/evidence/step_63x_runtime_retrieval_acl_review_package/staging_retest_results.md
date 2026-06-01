# Staging Retest Results

## Purpose

Record whether Step 63X runtime retrieval ACL proof is present and executable in the Oracle/Coolify/Compose staging path.

## Expected retest commands

```bash
docker compose -f deployment/docker_compose/docker-compose.yml \
  -f deployment/docker_compose/docker-compose.oracle-staging.override.yml config

docker ps
docker logs <api_container> --tail=100
docker exec <api_container> python -c "import backend.security_layer.runtime_enforcement.telemetry; print('runtime retrieval acl telemetry present')"
docker exec <api_container> python demo_attacks/runtime_retrieval_acl_cross_tenant_attack.py
```

## Expected result

- Compose config renders.
- API container is running.
- Runtime retrieval ACL modules are present in the container.
- Cross-tenant retrieval demo attack exits `0`.
- Logs are captured and redacted before publication.

## Current status

`RETEST_PENDING`

This file does not claim staging GO. It must be updated with real Oracle/VPS command output after retest.
