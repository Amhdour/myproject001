# Coolify Staging Environment Template

> Do not commit real domains, IP addresses, credentials, tokens, private keys,
> passwords, or secrets. Replace these placeholders only inside the approved
> Coolify secret store or another approved secret-management system.

```dotenv
# Application identity
STAGING_APP_NAME=<coolify-staging-app-name>
STAGING_PUBLIC_URL=<https://staging-placeholder.example.invalid>
STAGING_INTERNAL_URL=<http://internal-placeholder.invalid>

# Database and cache
POSTGRES_HOST=<postgres-host-placeholder>
POSTGRES_PORT=<postgres-port-placeholder>
POSTGRES_DB=<postgres-db-placeholder>
POSTGRES_USER=<postgres-user-placeholder>
POSTGRES_PASSWORD=<postgres-password-placeholder>
REDIS_URL=<redis-url-placeholder>

# Search/model dependencies
VESPA_HOST=<vespa-host-placeholder>
MODEL_SERVER_URL=<model-server-url-placeholder>
OPENAI_API_KEY=<openai-api-key-placeholder>

# Security layer runtime boundaries
SECURITY_LAYER_ENFORCE_MODE=false
SECURITY_LAYER_SHADOW_DENY_RUNTIME=false
SECURITY_LAYER_LIVE_BLOCKING=false
SECURITY_LAYER_LIVE_FILTERING=false

# Observability placeholders
STAGING_LOG_SINK=<staging-log-sink-placeholder>
STAGING_METRIC_SINK=<staging-metric-sink-placeholder>
```

## Notes
- Placeholder values are intentionally non-routable examples.
- The template documents expected categories only; it is not a deployable secret
  file.
- Runtime boundary flags remain false for this evidence bundle.
