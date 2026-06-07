# Deployment File Inventory

## Selected safest compose path

The safest local staging candidate, if Docker were available, is the documented lite development overlay:

```text
deployment/docker_compose/docker-compose.yml
deployment/docker_compose/docker-compose.onyx-lite.yml
deployment/docker_compose/docker-compose.dev.yml
```

This path was selected because `docker-compose.onyx-lite.yml` explicitly minimizes dependencies by moving vector DB, Redis, model servers, MinIO, and background worker behind profiles, while `docker-compose.dev.yml` exposes local development ports for health/reachability probes.

## Exact discovery output

```text
$ find . -maxdepth 4 \( -iname "*compose*.yml" -o -iname "*compose*.yaml" -o -iname "Dockerfile" -o -iname ".env.example" -o -iname "env.example" \) -print | sort
./.devcontainer/Dockerfile
./backend/Dockerfile
./backend/tests/integration/Dockerfile
./cli/Dockerfile
./deployment/docker_compose/docker-compose.coolify-staging.yml
./deployment/docker_compose/docker-compose.craft.yml
./deployment/docker_compose/docker-compose.dev.yml
./deployment/docker_compose/docker-compose.mcp-api-key-test.yml
./deployment/docker_compose/docker-compose.mcp-oauth-test.yml
./deployment/docker_compose/docker-compose.mcp-per-user-key-test.yml
./deployment/docker_compose/docker-compose.multitenant-dev.yml
./deployment/docker_compose/docker-compose.onyx-lite.yml
./deployment/docker_compose/docker-compose.prod-cloud.yml
./deployment/docker_compose/docker-compose.prod-no-letsencrypt.yml
./deployment/docker_compose/docker-compose.prod.yml
./deployment/docker_compose/docker-compose.resources.yml
./deployment/docker_compose/docker-compose.search-testing.yml
./deployment/docker_compose/docker-compose.step34x-minimal.yml
./deployment/docker_compose/docker-compose.yml
./examples/widget/.env.example
./profiling/docker-compose.yml
./web/Dockerfile
./web/node_modules/ts-unused-exports/Dockerfile
./widget/.env.example
$ find deployment -maxdepth 5 -type f 2>/dev/null | sort || true
deployment/.gitignore
deployment/README.md
deployment/aws_ecs_fargate/cloudformation/README.md
deployment/aws_ecs_fargate/cloudformation/deploy.sh
deployment/aws_ecs_fargate/cloudformation/onyx_acm_template.yaml
deployment/aws_ecs_fargate/cloudformation/onyx_cluster_template.yaml
deployment/aws_ecs_fargate/cloudformation/onyx_config.jsonl
deployment/aws_ecs_fargate/cloudformation/onyx_efs_template.yaml
deployment/aws_ecs_fargate/cloudformation/services/onyx_backend_api_server_service_template.yaml
deployment/aws_ecs_fargate/cloudformation/services/onyx_backend_background_server_service_template.yaml
deployment/aws_ecs_fargate/cloudformation/services/onyx_model_server_indexing_service_template.yaml
deployment/aws_ecs_fargate/cloudformation/services/onyx_model_server_inference_service_template.yaml
deployment/aws_ecs_fargate/cloudformation/services/onyx_nginx_service_template.yaml
deployment/aws_ecs_fargate/cloudformation/services/onyx_postgres_service_template.yaml
deployment/aws_ecs_fargate/cloudformation/services/onyx_redis_service_template.yaml
deployment/aws_ecs_fargate/cloudformation/services/onyx_vespaengine_service_template.yaml
deployment/aws_ecs_fargate/cloudformation/services/onyx_web_server_service_template.yaml
deployment/aws_ecs_fargate/cloudformation/uninstall.sh
deployment/data/nginx/app.conf.template
deployment/data/nginx/app.conf.template.no-letsencrypt
deployment/data/nginx/app.conf.template.prod
deployment/data/nginx/mcp.conf.inc.template
deployment/data/nginx/mcp_upstream.conf.inc.template
deployment/data/nginx/run-nginx.sh
deployment/docker_compose/README.md
deployment/docker_compose/README.step34x-minimal.md
deployment/docker_compose/docker-compose.coolify-staging.yml
deployment/docker_compose/docker-compose.craft.yml
deployment/docker_compose/docker-compose.dev.yml
deployment/docker_compose/docker-compose.mcp-api-key-test.yml
deployment/docker_compose/docker-compose.mcp-oauth-test.yml
deployment/docker_compose/docker-compose.mcp-per-user-key-test.yml
deployment/docker_compose/docker-compose.multitenant-dev.yml
deployment/docker_compose/docker-compose.onyx-lite.yml
deployment/docker_compose/docker-compose.prod-cloud.yml
deployment/docker_compose/docker-compose.prod-no-letsencrypt.yml
deployment/docker_compose/docker-compose.prod.yml
deployment/docker_compose/docker-compose.resources.yml
deployment/docker_compose/docker-compose.search-testing.yml
deployment/docker_compose/docker-compose.step34x-minimal.yml
deployment/docker_compose/docker-compose.yml
deployment/docker_compose/env.nginx.template
deployment/docker_compose/env.prod.template
deployment/docker_compose/env.template
deployment/docker_compose/init-letsencrypt.sh
deployment/docker_compose/install.ps1
deployment/docker_compose/install.sh
deployment/helm/README.md
deployment/helm/charts/onyx/.gitignore
deployment/helm/charts/onyx/.helmignore
deployment/helm/charts/onyx/Chart.lock
deployment/helm/charts/onyx/Chart.yaml
deployment/helm/charts/onyx/ci/ct-values.yaml
deployment/helm/charts/onyx/crds/cnpg-crds.yaml
deployment/helm/charts/onyx/dashboards/indexing-pipeline.json
deployment/helm/charts/onyx/dashboards/indexing-pruning.json
deployment/helm/charts/onyx/dashboards/opensearch-search-latency.json
deployment/helm/charts/onyx/dashboards/redis-queues.json
deployment/helm/charts/onyx/scripts/check-cnpg-crds.sh
deployment/helm/charts/onyx/templates/_helpers.tpl
deployment/helm/charts/onyx/templates/api-deployment.yaml
deployment/helm/charts/onyx/templates/api-hpa.yaml
deployment/helm/charts/onyx/templates/api-scaledobject.yaml
deployment/helm/charts/onyx/templates/api-service.yaml
deployment/helm/charts/onyx/templates/api-servicemonitor.yaml
deployment/helm/charts/onyx/templates/auth-secrets.yaml
deployment/helm/charts/onyx/templates/celery-beat.yaml
deployment/helm/charts/onyx/templates/celery-worker-docfetching-hpa.yaml
deployment/helm/charts/onyx/templates/celery-worker-docfetching-metrics-service.yaml
deployment/helm/charts/onyx/templates/celery-worker-docfetching-scaledobject.yaml
deployment/helm/charts/onyx/templates/celery-worker-docfetching.yaml
deployment/helm/charts/onyx/templates/celery-worker-docprocessing-hpa.yaml
deployment/helm/charts/onyx/templates/celery-worker-docprocessing-metrics-service.yaml
deployment/helm/charts/onyx/templates/celery-worker-docprocessing-scaledobject.yaml
deployment/helm/charts/onyx/templates/celery-worker-docprocessing.yaml
deployment/helm/charts/onyx/templates/celery-worker-heavy-hpa.yaml
deployment/helm/charts/onyx/templates/celery-worker-heavy-metrics-service.yaml
deployment/helm/charts/onyx/templates/celery-worker-heavy-scaledobject.yaml
deployment/helm/charts/onyx/templates/celery-worker-heavy.yaml
deployment/helm/charts/onyx/templates/celery-worker-light-hpa.yaml
deployment/helm/charts/onyx/templates/celery-worker-light-metrics-service.yaml
deployment/helm/charts/onyx/templates/celery-worker-light-scaledobject.yaml
deployment/helm/charts/onyx/templates/celery-worker-light.yaml
deployment/helm/charts/onyx/templates/celery-worker-monitoring-hpa.yaml
deployment/helm/charts/onyx/templates/celery-worker-monitoring-metrics-service.yaml
deployment/helm/charts/onyx/templates/celery-worker-monitoring-scaledobject.yaml
deployment/helm/charts/onyx/templates/celery-worker-monitoring.yaml
deployment/helm/charts/onyx/templates/celery-worker-primary-hpa.yaml
deployment/helm/charts/onyx/templates/celery-worker-primary-metrics-service.yaml
deployment/helm/charts/onyx/templates/celery-worker-primary-scaledobject.yaml
deployment/helm/charts/onyx/templates/celery-worker-primary.yaml
deployment/helm/charts/onyx/templates/celery-worker-scheduled-tasks-hpa.yaml
deployment/helm/charts/onyx/templates/celery-worker-scheduled-tasks-metrics-service.yaml
deployment/helm/charts/onyx/templates/celery-worker-scheduled-tasks-scaledobject.yaml
deployment/helm/charts/onyx/templates/celery-worker-scheduled-tasks.yaml
deployment/helm/charts/onyx/templates/celery-worker-servicemonitors.yaml
deployment/helm/charts/onyx/templates/celery-worker-user-file-processing-hpa.yaml
deployment/helm/charts/onyx/templates/celery-worker-user-file-processing-scaledobject.yaml
deployment/helm/charts/onyx/templates/celery-worker-user-file-processing.yaml
deployment/helm/charts/onyx/templates/configmap.yaml
deployment/helm/charts/onyx/templates/discordbot.yaml
deployment/helm/charts/onyx/templates/external-secret.yaml
deployment/helm/charts/onyx/templates/extra-manifests.yaml
deployment/helm/charts/onyx/templates/grafana-dashboards.yaml
deployment/helm/charts/onyx/templates/indexing-model-deployment.yaml
deployment/helm/charts/onyx/templates/indexing-model-service.yaml
deployment/helm/charts/onyx/templates/inference-model-deployment.yaml
deployment/helm/charts/onyx/templates/inference-model-service.yaml
deployment/helm/charts/onyx/templates/ingress-api.yaml
deployment/helm/charts/onyx/templates/ingress-mcp-oauth-callback.yaml
deployment/helm/charts/onyx/templates/ingress-mcp.yaml
deployment/helm/charts/onyx/templates/ingress-webserver.yaml
deployment/helm/charts/onyx/templates/lets-encrypt.yaml
deployment/helm/charts/onyx/templates/mcp-server-deployment.yaml
deployment/helm/charts/onyx/templates/mcp-server-service.yaml
deployment/helm/charts/onyx/templates/network-policy-sandbox-push.yaml
deployment/helm/charts/onyx/templates/nginx-conf.yaml
deployment/helm/charts/onyx/templates/postgres-cluster.yaml
deployment/helm/charts/onyx/templates/pre-delete-cleanup.yaml
deployment/helm/charts/onyx/templates/sandbox-namespace.yaml
deployment/helm/charts/onyx/templates/serviceaccount.yaml
deployment/helm/charts/onyx/templates/slackbot.yaml
deployment/helm/charts/onyx/templates/tooling-pginto-configmap.yaml
deployment/helm/charts/onyx/templates/webserver-deployment.yaml
deployment/helm/charts/onyx/templates/webserver-hpa.yaml
deployment/helm/charts/onyx/templates/webserver-scaledobject.yaml
deployment/helm/charts/onyx/templates/webserver-service.yaml
deployment/helm/charts/onyx/templates_disabled/background-deployment.yaml
deployment/helm/charts/onyx/templates_disabled/background-hpa.yaml
deployment/helm/charts/onyx/templates_disabled/onyx-secret.yaml
deployment/helm/charts/onyx/values-ci.yaml
deployment/helm/charts/onyx/values-lite.yaml
deployment/helm/charts/onyx/values-localdev.yaml
deployment/helm/charts/onyx/values.yaml
deployment/helm/dev/k8s-down.sh
deployment/helm/dev/k8s-up.sh
deployment/terraform/modules/aws/README.md
deployment/terraform/modules/aws/eks/main.tf
deployment/terraform/modules/aws/eks/outputs.tf
deployment/terraform/modules/aws/eks/variables.tf
deployment/terraform/modules/aws/onyx/main.tf
deployment/terraform/modules/aws/onyx/outputs.tf
deployment/terraform/modules/aws/onyx/variables.tf
deployment/terraform/modules/aws/onyx/versions.tf
deployment/terraform/modules/aws/opensearch/main.tf
deployment/terraform/modules/aws/opensearch/outputs.tf
deployment/terraform/modules/aws/opensearch/variables.tf
deployment/terraform/modules/aws/postgres/main.tf
deployment/terraform/modules/aws/postgres/outputs.tf
deployment/terraform/modules/aws/postgres/variables.tf
deployment/terraform/modules/aws/redis/main.tf
deployment/terraform/modules/aws/redis/outputs.tf
deployment/terraform/modules/aws/redis/variables.tf
deployment/terraform/modules/aws/s3/main.tf
deployment/terraform/modules/aws/s3/variables.tf
deployment/terraform/modules/aws/vpc/main.tf
deployment/terraform/modules/aws/vpc/outputs.tf
deployment/terraform/modules/aws/vpc/variables.tf
deployment/terraform/modules/aws/waf/main.tf
deployment/terraform/modules/aws/waf/outputs.tf
deployment/terraform/modules/aws/waf/variables.tf
$ ls -la deployment || true
total 36
drwxr-xr-x  7 root root 4096 May 30 06:47 .
drwxr-xr-x 24 root root 4096 May 30 12:02 ..
-rw-r--r--  1 root root   19 May 30 06:47 .gitignore
-rw-r--r--  1 root root  114 May 30 06:47 README.md
drwxr-xr-x  3 root root 4096 May 30 06:47 aws_ecs_fargate
drwxr-xr-x  3 root root 4096 May 30 06:47 data
drwxr-xr-x  2 root root 4096 May 30 06:47 docker_compose
drwxr-xr-x  4 root root 4096 May 30 06:47 helm
drwxr-xr-x  3 root root 4096 May 30 06:47 terraform
$ ls -la deployment/docker_compose || true
total 312
drwxr-xr-x 2 root root  4096 May 30 06:47 .
drwxr-xr-x 7 root root  4096 May 30 06:47 ..
-rw-r--r-- 1 root root  3029 May 30 06:47 README.md
-rw-r--r-- 1 root root   850 May 30 06:47 README.step34x-minimal.md
-rw-r--r-- 1 root root 20738 May 30 06:47 docker-compose.coolify-staging.yml
-rw-r--r-- 1 root root  2687 May 30 06:47 docker-compose.craft.yml
-rw-r--r-- 1 root root  1250 May 30 06:47 docker-compose.dev.yml
-rw-r--r-- 1 root root  1082 May 30 06:47 docker-compose.mcp-api-key-test.yml
-rw-r--r-- 1 root root  1454 May 30 06:47 docker-compose.mcp-oauth-test.yml
-rw-r--r-- 1 root root  1195 May 30 06:47 docker-compose.mcp-per-user-key-test.yml
-rw-r--r-- 1 root root 22356 May 30 06:47 docker-compose.multitenant-dev.yml
-rw-r--r-- 1 root root  3156 May 30 06:47 docker-compose.onyx-lite.yml
-rw-r--r-- 1 root root 11662 May 30 06:47 docker-compose.prod-cloud.yml
-rw-r--r-- 1 root root 13037 May 30 06:47 docker-compose.prod-no-letsencrypt.yml
-rw-r--r-- 1 root root 14574 May 30 06:47 docker-compose.prod.yml
-rw-r--r-- 1 root root  2553 May 30 06:47 docker-compose.resources.yml
-rw-r--r-- 1 root root  8642 May 30 06:47 docker-compose.search-testing.yml
-rw-r--r-- 1 root root   267 May 30 06:47 docker-compose.step34x-minimal.yml
-rw-r--r-- 1 root root 22721 May 30 06:47 docker-compose.yml
-rw-r--r-- 1 root root   469 May 30 06:47 env.nginx.template
-rw-r--r-- 1 root root  2370 May 30 06:47 env.prod.template
-rw-r--r-- 1 root root 11044 May 30 06:47 env.template
-rwxr-xr-x 1 root root  4152 May 30 06:47 init-letsencrypt.sh
-rw-r--r-- 1 root root 56409 May 30 06:47 install.ps1
-rwxr-xr-x 1 root root 50729 May 30 06:47 install.sh
$ ls -la .devcontainer || true
total 48
drwxr-xr-x  2 root root 4096 May 30 06:47 .
drwxr-xr-x 24 root root 4096 May 30 12:02 ..
-rw-r--r--  1 root root 2654 May 30 06:47 Dockerfile
-rw-r--r--  1 root root 3150 May 30 06:47 README.md
-rw-r--r--  1 root root 2128 May 30 06:47 devcontainer.json
-rw-r--r--  1 root root 1393 May 30 06:47 dnsmasq.conf
-rw-r--r--  1 root root  828 May 30 06:47 github_known_hosts
-rw-r--r--  1 root root 5249 May 30 06:47 init-dev-user.sh
-rwxr-xr-x  1 root root 4556 May 30 06:47 init-firewall.sh
-rw-r--r--  1 root root  335 May 30 06:47 zshrc
$ find .devcontainer -maxdepth 3 -type f -print 2>/dev/null || true
.devcontainer/dnsmasq.conf
.devcontainer/README.md
.devcontainer/github_known_hosts
.devcontainer/zshrc
.devcontainer/init-firewall.sh
.devcontainer/Dockerfile
.devcontainer/devcontainer.json
.devcontainer/init-dev-user.sh

```

## Selected compose file inspection output

```text
===== deployment/docker_compose/docker-compose.yml sed -n '1,220p' =====
# =============================================================================
# ONYX DOCKER COMPOSE
# =============================================================================
# This is the default configuration for Onyx. This file is fairly configurable,
# also see env.template for possible settings.
#
# PRODUCTION DEPLOYMENT CHECKLIST:
# To convert this setup to a production deployment following best practices,
# follow the checklist below. Note that there are other ways to secure the Onyx
# deployment so these are not strictly necessary for all teams.
#
# 1. SECURITY HARDENING:
#    - Remove all port exposures except nginx (80/443)
#    - Comment out ports for: api_server, relational_db, cache, minio
#
# 2. SSL/TLS SETUP:
#    - Uncomment the certbot service (see below)
#    - Add SSL certificate volumes to nginx service
#    - Change nginx command from app.conf.template to app.conf.template.prod
#
# 3. ENVIRONMENT CONFIGURATION:
#    - Replace env_file with explicit environment variables
#
# 4. AUTHENTICATION:
#    - Select an authentication method like Basic, Google OAuth, OIDC, or SAML
#
# 5. CA CERTIFICATES:
#    - Uncomment custom CA certificate volumes if needed
#
# 6. DOMAIN CONFIGURATION:
#    - Set proper DOMAIN environment variable for nginx
#    - Configure DNS and SSL certificates
#
# For a complete production setup, refer to docker-compose.prod.yml
# =============================================================================

name: onyx

services:
  api_server:
    image: ${ONYX_BACKEND_IMAGE:-onyxdotapp/onyx-backend:${IMAGE_TAG:-latest}}
    build:
      context: ../../backend
      dockerfile: Dockerfile
      args:
        - ENABLE_CRAFT=${ENABLE_CRAFT:-false}
    command: >
      /bin/sh -c "alembic upgrade head &&
      echo \"Starting Onyx Api Server\" &&
      uvicorn onyx.main:app --host 0.0.0.0 --port 8080"
    # Check env.template and copy to .env for env vars
    env_file:
      - path: .env
        required: false
    depends_on:
      relational_db:
        condition: service_started
      opensearch:
        condition: service_started
      cache:
        condition: service_started
      inference_model_server:
        condition: service_started
      minio:
        condition: service_started
        required: false
    restart: unless-stopped
    # DEV: To expose ports, either:
    # 1. Use docker-compose.dev.yml: docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d --wait
    # 2. Uncomment the ports below
    # ports:
    #   - "8080:8080"
    environment:
      # Auth Settings
      - AUTH_TYPE=${AUTH_TYPE:-basic}
      - FILE_STORE_BACKEND=${FILE_STORE_BACKEND:-s3}
      - POSTGRES_HOST=${POSTGRES_HOST:-relational_db}
      - OPENSEARCH_HOST=${OPENSEARCH_HOST:-opensearch}
      - OPENSEARCH_ADMIN_PASSWORD=${OPENSEARCH_ADMIN_PASSWORD:-StrongPassword123!}
      - REDIS_HOST=${REDIS_HOST:-cache}
      - MODEL_SERVER_HOST=${MODEL_SERVER_HOST:-inference_model_server}
      - CODE_INTERPRETER_BASE_URL=${CODE_INTERPRETER_BASE_URL:-http://code-interpreter:8000}
      - S3_ENDPOINT_URL=${S3_ENDPOINT_URL:-http://minio:9000}
      - S3_AWS_ACCESS_KEY_ID=${S3_AWS_ACCESS_KEY_ID:-minioadmin}
      - S3_AWS_SECRET_ACCESS_KEY=${S3_AWS_SECRET_ACCESS_KEY:-minioadmin}
      # Onyx Craft configuration (disabled by default, set ENABLE_CRAFT=true in .env to enable)
      # Use --include-craft with install script, or manually set in .env file
      - ENABLE_CRAFT=${ENABLE_CRAFT:-false}
      - OUTPUTS_TEMPLATE_PATH=${OUTPUTS_TEMPLATE_PATH:-/app/onyx/server/features/build/sandbox/kubernetes/docker/templates/outputs}
      - VENV_TEMPLATE_PATH=${VENV_TEMPLATE_PATH:-/app/onyx/server/features/build/sandbox/kubernetes/docker/templates/venv}
      - WEB_TEMPLATE_PATH=${WEB_TEMPLATE_PATH:-/app/onyx/server/features/build/sandbox/kubernetes/docker/templates/outputs/web}
      - PERSISTENT_DOCUMENT_STORAGE_PATH=${PERSISTENT_DOCUMENT_STORAGE_PATH:-/app/file-system}
    # PRODUCTION: Uncomment the line below to use if IAM_AUTH is true and you are using iam auth for postgres
    # volumes:
    #   - ./bundle.pem:/app/bundle.pem:ro
    extra_hosts:
      - "host.docker.internal:host-gateway"
    logging:
      driver: json-file
      options:
        max-size: "50m"
        max-file: "6"
    healthcheck:
      test:
        [
          "CMD",
          "python",
          "-c",
          "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')",
        ]
      interval: 30s
      timeout: 20s
      retries: 3
      # Generous start_period so that `docker compose up --wait` does not flag
      # the container unhealthy while alembic migrations run on a fresh DB.
      # Healthy is reported as soon as /health responds, so this does not slow
      # down fast boots.
      start_period: 600s
    # Optional, only for debugging purposes
    volumes:
      - api_server_logs:/var/log/onyx
      # Shared volume for persistent document storage (Craft file-system mode)
      - file-system:/app/file-system

  background:
    image: ${ONYX_BACKEND_IMAGE:-onyxdotapp/onyx-backend:${IMAGE_TAG:-latest}}
    build:
      context: ../../backend
      dockerfile: Dockerfile
      args:
        - ENABLE_CRAFT=${ENABLE_CRAFT:-false}
    command: >
      /bin/sh -c "
      if [ -f /app/scripts/setup_craft_templates.sh ]; then
        /app/scripts/setup_craft_templates.sh;
      fi &&
      if [ -f /etc/ssl/certs/custom-ca.crt ]; then
        update-ca-certificates;
      fi &&
      /app/scripts/supervisord_entrypoint.sh"
    env_file:
      - path: .env
        required: false
    depends_on:
      relational_db:
        condition: service_started
      opensearch:
        condition: service_started
      cache:
        condition: service_started
      inference_model_server:
        condition: service_started
      indexing_model_server:
        condition: service_started
    restart: unless-stopped
    environment:
      - FILE_STORE_BACKEND=${FILE_STORE_BACKEND:-s3}
      - POSTGRES_HOST=${POSTGRES_HOST:-relational_db}
      - OPENSEARCH_HOST=${OPENSEARCH_HOST:-opensearch}
      - OPENSEARCH_ADMIN_PASSWORD=${OPENSEARCH_ADMIN_PASSWORD:-StrongPassword123!}
      - REDIS_HOST=${REDIS_HOST:-cache}
      - MODEL_SERVER_HOST=${MODEL_SERVER_HOST:-inference_model_server}
      - INDEXING_MODEL_SERVER_HOST=${INDEXING_MODEL_SERVER_HOST:-indexing_model_server}
      - S3_ENDPOINT_URL=${S3_ENDPOINT_URL:-http://minio:9000}
      - S3_AWS_ACCESS_KEY_ID=${S3_AWS_ACCESS_KEY_ID:-minioadmin}
      - S3_AWS_SECRET_ACCESS_KEY=${S3_AWS_SECRET_ACCESS_KEY:-minioadmin}
      - DISCORD_BOT_TOKEN=${DISCORD_BOT_TOKEN:-}
      - DISCORD_BOT_INVOKE_CHAR=${DISCORD_BOT_INVOKE_CHAR:-!}
      # API Server connection for Discord bot message processing
      - API_SERVER_PROTOCOL=${API_SERVER_PROTOCOL:-http}
      - API_SERVER_HOST=${API_SERVER_HOST:-api_server}
      # Onyx Craft configuration (set up automatically on container startup)
      - ENABLE_CRAFT=${ENABLE_CRAFT:-false}
      - OUTPUTS_TEMPLATE_PATH=${OUTPUTS_TEMPLATE_PATH:-/app/onyx/server/features/build/sandbox/kubernetes/docker/templates/outputs}
      - VENV_TEMPLATE_PATH=${VENV_TEMPLATE_PATH:-/app/onyx/server/features/build/sandbox/kubernetes/docker/templates/venv}
      - WEB_TEMPLATE_PATH=${WEB_TEMPLATE_PATH:-/app/onyx/server/features/build/sandbox/kubernetes/docker/templates/outputs/web}
      - PERSISTENT_DOCUMENT_STORAGE_PATH=${PERSISTENT_DOCUMENT_STORAGE_PATH:-/app/file-system}
    # PRODUCTION: Uncomment the line below to use if IAM_AUTH is true and you are using iam auth for postgres
    # volumes:
    #   - ./bundle.pem:/app/bundle.pem:ro
    extra_hosts:
      - "host.docker.internal:host-gateway"
    # Optional, only for debugging purposes
    volumes:
      - background_logs:/var/log/onyx
      # Shared volume for persistent document storage (Craft file-system mode)
      - file-system:/app/file-system
    logging:
      driver: json-file
      options:
        max-size: "50m"
        max-file: "6"
    # PRODUCTION: Uncomment the following lines if you need to include a custom CA certificate
    # This section enables the use of a custom CA certificate
    # If present, the custom CA certificate is mounted as a volume
    # The container checks for its existence and updates the system's CA certificates
    # This allows for secure communication with services using custom SSL certificates
    # Optional volume mount for CA certificate
    # volumes:
    #   # Maps to the CA_CERT_PATH environment variable in the Dockerfile
    #   - ${CA_CERT_PATH:-./custom-ca.crt}:/etc/ssl/certs/custom-ca.crt:ro

  web_server:
    image: ${ONYX_WEB_SERVER_IMAGE:-onyxdotapp/onyx-web-server:${IMAGE_TAG:-latest}}
    build:
      context: ../../web
      dockerfile: Dockerfile
      args:
        - NEXT_PUBLIC_DISABLE_LOGOUT=${NEXT_PUBLIC_DISABLE_LOGOUT:-}
        - NEXT_PUBLIC_FORGOT_PASSWORD_ENABLED=${NEXT_PUBLIC_FORGOT_PASSWORD_ENABLED:-}
        # Enterprise Edition only
        - NEXT_PUBLIC_THEME=${NEXT_PUBLIC_THEME:-}
        # DO NOT TURN ON unless you have EXPLICIT PERMISSION from Onyx.
        - NEXT_PUBLIC_DO_NOT_USE_TOGGLE_OFF_DANSWER_POWERED=${NEXT_PUBLIC_DO_NOT_USE_TOGGLE_OFF_DANSWER_POWERED:-false}
        - NODE_OPTIONS=${NODE_OPTIONS:-"--max-old-space-size=4096"}
    env_file:
      - path: .env
        required: false
    depends_on:
      - api_server
===== deployment/docker_compose/docker-compose.yml grep key directives =====
41:    image: ${ONYX_BACKEND_IMAGE:-onyxdotapp/onyx-backend:${IMAGE_TAG:-latest}}
42:    build:
52:    env_file:
55:    depends_on:
71:    # ports:
73:    environment:
103:    healthcheck:
126:    image: ${ONYX_BACKEND_IMAGE:-onyxdotapp/onyx-backend:${IMAGE_TAG:-latest}}
127:    build:
141:    env_file:
144:    depends_on:
156:    environment:
204:    image: ${ONYX_WEB_SERVER_IMAGE:-onyxdotapp/onyx-web-server:${IMAGE_TAG:-latest}}
205:    build:
216:    env_file:
219:    depends_on:
222:    environment:
224:    healthcheck:
239:  #   image: ${ONYX_BACKEND_IMAGE:-onyxdotapp/onyx-backend:${IMAGE_TAG:-latest}}
240:  #   build:
250:  #   env_file:
253:  #   depends_on:
257:  #   environment:
278:    image: ${ONYX_MODEL_SERVER_IMAGE:-onyxdotapp/onyx-model-server:${IMAGE_TAG:-latest}}
279:    build:
298:    env_file:
312:    healthcheck:
328:    image: ${ONYX_MODEL_SERVER_IMAGE:-onyxdotapp/onyx-model-server:${IMAGE_TAG:-latest}}
329:    build:
348:    env_file:
352:    environment:
364:    healthcheck:
380:    image: postgres:15.2-alpine
383:    env_file:
388:    environment:
394:    # ports:
396:    healthcheck:
405:    image: opensearchproject/opensearch:3.6.0
411:    environment:
444:    image: nginx:1.25.5-alpine
448:    depends_on:
453:    env_file:
456:    environment:
462:    ports:
488:    healthcheck:
504:    image: redis:7.4-alpine
509:    # ports:
514:    env_file:
522:    image: minio/minio:RELEASE.2025-07-23T15-54-02Z-cpuv1
528:    # ports:
531:    env_file:
534:    environment:
542:    healthcheck:
549:    image: onyxdotapp/code-interpreter:${CODE_INTERPRETER_IMAGE_TAG:-latest}
552:    env_file:
567:  #   image: certbot/certbot
===== deployment/docker_compose/docker-compose.onyx-lite.yml sed -n '1,220p' =====
# =============================================================================
# ONYX LITE — MINIMAL DEPLOYMENT OVERLAY
# =============================================================================
# Overlay to run Onyx in a minimal configuration: no vector database, no Redis,
# no model servers, and no background workers. Only PostgreSQL is required. In
# this mode, connectors and RAG search are disabled, but the core chat
# experience (LLM conversations, tools, user file uploads, Projects, Agent
# knowledge, code interpreter) still works.
#
# Usage:
#   docker compose -f docker-compose.yml -f docker-compose.onyx-lite.yml up -d
#
# With dev ports:
#   docker compose -f docker-compose.yml -f docker-compose.onyx-lite.yml \
#                  -f docker-compose.dev.yml up -d --wait
#
# This overlay:
#   - Moves both model servers, OpenSearch, MinIO, Redis (cache), and the
#     background worker to profiles so they do not start by default
#   - Makes depends_on references to removed services optional
#   - Sets DISABLE_VECTOR_DB=true on the api_server
#   - Uses PostgreSQL for caching and auth instead of Redis
#   - Uses PostgreSQL for file storage instead of S3/MinIO
#
# To selectively bring services back:
#   --profile vectordb          Indexing model server
#   --profile inference         Inference model server
#   --profile background        Background worker (Celery) — also needs redis
#   --profile redis             Redis cache
#   --profile opensearch        OpenSearch
#   --profile s3-filestore      MinIO (S3-compatible file store)
# =============================================================================

name: onyx

services:
  api_server:
    depends_on:
      opensearch:
        condition: service_started
        required: false
      cache:
        condition: service_started
        required: false
      inference_model_server:
        condition: service_started
        required: false
      minio:
        condition: service_started
        required: false
    environment:
      - DISABLE_VECTOR_DB=true
      - FILE_STORE_BACKEND=postgres
      - CACHE_BACKEND=postgres
      - AUTH_BACKEND=postgres

  # Move the background worker to a profile so it does not start by default.
  # The API server handles all background work in lite mode.
  background:
    profiles: ["background"]
    depends_on:
      inference_model_server:
        condition: service_started
        required: false
      indexing_model_server:
        condition: service_started
        required: false

  # Move Redis to a profile so it does not start by default.
  # The Postgres cache backend replaces Redis in lite mode.
  cache:
    profiles: ["redis"]

  # Move indexing model server to a profile so it does not start.
  indexing_model_server:
    profiles: ["vectordb"]

  # Inference model server is only needed for local embeddings, not for LLM chat.
  inference_model_server:
    profiles: ["inference"]

  # OpenSearch is not needed in lite mode (no indexing).
  opensearch:
    profiles: ["opensearch"]

  # MinIO is not needed in lite mode (Postgres handles file storage).
  minio:
    profiles: ["s3-filestore"]
===== deployment/docker_compose/docker-compose.onyx-lite.yml grep key directives =====
13:# With dev ports:
38:    depends_on:
51:    environment:
61:    depends_on:
===== deployment/docker_compose/docker-compose.dev.yml sed -n '1,220p' =====
# Docker Compose Override for Development/Testing
# This file exposes service ports for development and testing purposes
#
# Usage:
#   docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d --wait
#
# Or set COMPOSE_FILE environment variable:
#   export COMPOSE_FILE=docker-compose.yml:docker-compose.dev.yml
#   docker compose up -d --wait

services:
  api_server:
    ports:
      - "8080:8080"
    deploy:
      resources:
        limits:
          cpus: "${API_SERVER_CPU_LIMIT:-0}"
          memory: "${API_SERVER_MEM_LIMIT:-0}"

  # Uncomment the block below to enable the MCP server for Onyx.
  # mcp_server:
  #   ports:
  #     - "8090:8090"

  relational_db:
    ports:
      - "5432:5432"

  opensearch:
    ports:
      - "9200:9200"
    # Rootless Docker can reject the base OpenSearch ulimit settings, so clear
    # the inherited block entirely in the dev override.
    ulimits: !reset null
    environment:
      - bootstrap.memory_lock=false

  inference_model_server:
    ports:
      - "9000:9000"

  cache:
    ports:
      - "6379:6379"

  minio:
    # use different ports to avoid conflicts with model servers
    ports:
      - "9004:9000"
      - "9005:9001"

  code-interpreter:
    ports:
      - "8000:8000"
===== deployment/docker_compose/docker-compose.dev.yml grep key directives =====
13:    ports:
23:  #   ports:
27:    ports:
31:    ports:
36:    environment:
40:    ports:
44:    ports:
49:    ports:
54:    ports:

```

## Environment example/template inspection

No repository root `.env.example` was found by the requested command. Template values under `deployment/docker_compose/` include placeholder/default local development values only; no real `.env` secret values were printed or committed.

```text
$ find . -maxdepth 4 \( -iname ".env.example" -o -iname "env.example" -o -iname "*.env.example" \) -print
./examples/widget/.env.example
./widget/.env.example
$ grep -R "^[A-Z0-9_]*=" -n .env.example deployment .devcontainer 2>/dev/null || true
deployment/helm/charts/onyx/scripts/check-cnpg-crds.sh:14:CHART_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
deployment/helm/charts/onyx/scripts/check-cnpg-crds.sh:15:CRDS_FILE="$CHART_DIR/crds/cnpg-crds.yaml"
deployment/helm/charts/onyx/scripts/check-cnpg-crds.sh:16:SUBCHART_TARBALL="$(find "$CHART_DIR/charts" -maxdepth 1 -name 'cloudnative-pg-*.tgz' -print -quit 2>/dev/null)"
deployment/helm/charts/onyx/scripts/check-cnpg-crds.sh:23:EXPECTED=$(tar -xzOf "$SUBCHART_TARBALL" cloudnative-pg/templates/crds/crds.yaml | sed -e '1{/^{{/d;}' -e '${/^{{/d;}')
deployment/helm/charts/onyx/scripts/check-cnpg-crds.sh:31:ACTUAL=$(cat "$CRDS_FILE")
deployment/helm/dev/k8s-up.sh:21:CLUSTER_NAME="onyx-dev"
deployment/helm/dev/k8s-up.sh:22:NAMESPACE="onyx"
deployment/helm/dev/k8s-up.sh:23:OPENSEARCH_PASSWORD=""
deployment/helm/dev/k8s-up.sh:24:SKIP_CLUSTER_CREATE=0
deployment/helm/dev/k8s-up.sh:25:SKIP_HELM=0
deployment/helm/dev/k8s-up.sh:27:SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
deployment/helm/dev/k8s-up.sh:28:CHART_DIR="$(cd "$SCRIPT_DIR/../charts/onyx" && pwd)"
deployment/helm/dev/k8s-up.sh:29:VALUES_OVERLAY="$CHART_DIR/values-localdev.yaml"
deployment/helm/dev/k8s-up.sh:78:EXPECTED_CTX="kind-$CLUSTER_NAME"
deployment/helm/dev/k8s-up.sh:79:CURRENT_CTX="$(kubectl config current-context)"
deployment/helm/dev/k8s-up.sh:105:HELM_DEV_HOME="$(mktemp -d -t onyx-dev-helm-XXXXXX)"
deployment/helm/dev/k8s-up.sh:125:PW_FLAG=()
deployment/helm/dev/k8s-down.sh:19:CLUSTER_NAME="onyx-dev"
deployment/helm/dev/k8s-down.sh:20:NAMESPACE="onyx"
deployment/helm/dev/k8s-down.sh:21:KEEP_CLUSTER=0
deployment/helm/dev/k8s-down.sh:48:EXPECTED_CTX="kind-$CLUSTER_NAME"
deployment/helm/dev/k8s-down.sh:49:CURRENT_CTX="$(kubectl config current-context)"
deployment/docker_compose/env.nginx.template:2:DOMAIN=
deployment/docker_compose/env.nginx.template:3:EMAIL=
deployment/docker_compose/env.nginx.template:10:SSL_CERT_FILE_NAME=ssl.cert
deployment/docker_compose/env.nginx.template:11:SSL_CERT_KEY_FILE_NAME=ssl.key
deployment/docker_compose/init-letsencrypt.sh:22:COMPOSE_CMD=$(docker_compose_cmd)
deployment/docker_compose/install.sh:6:EXPECTED_DOCKER_RAM_GB=10
deployment/docker_compose/install.sh:7:EXPECTED_DISK_GB=32
deployment/docker_compose/install.sh:10:SHUTDOWN_MODE=false
deployment/docker_compose/install.sh:11:DELETE_DATA_MODE=false
deployment/docker_compose/install.sh:12:INCLUDE_CRAFT=false  # Disabled by default, use --include-craft to enable
deployment/docker_compose/install.sh:13:LITE_MODE=false       # Disabled by default, use --lite to enable
deployment/docker_compose/install.sh:14:USE_LOCAL_FILES=false # Disabled by default, use --local to skip downloading config files
deployment/docker_compose/install.sh:15:NO_PROMPT=false
deployment/docker_compose/install.sh:16:DRY_RUN=false
deployment/docker_compose/install.sh:17:VERBOSE=false
deployment/docker_compose/install.sh:18:NO_WAIT=false  # When false (default), pass --wait to `docker compose up`
deployment/docker_compose/install.sh:19:WAIT_TIMEOUT_SECONDS=600
deployment/docker_compose/install.sh:114:INSTALL_ROOT="${INSTALL_PREFIX:-onyx_data}"
deployment/docker_compose/install.sh:116:LITE_COMPOSE_FILE="docker-compose.onyx-lite.yml"
deployment/docker_compose/install.sh:117:CRAFT_COMPOSE_FILE="docker-compose.craft.yml"
deployment/docker_compose/install.sh:122:COMPOSE_FILE_ARGS=()
deployment/docker_compose/install.sh:139:DOWNLOADER=""
deployment/docker_compose/install.sh:167:LATEST_RELEASE_TAG=""
deployment/docker_compose/install.sh:197:COMPOSE_CMD=""
deployment/docker_compose/install.sh:292:RED='\033[0;31m'
deployment/docker_compose/install.sh:293:GREEN='\033[0;32m'
deployment/docker_compose/install.sh:294:YELLOW='\033[1;33m'
deployment/docker_compose/install.sh:295:BLUE='\033[0;34m'
deployment/docker_compose/install.sh:296:BOLD='\033[1m'
deployment/docker_compose/install.sh:297:NC='\033[0m' # No Color
deployment/docker_compose/install.sh:300:CURRENT_STEP=0
deployment/docker_compose/install.sh:301:TOTAL_STEPS=9
deployment/docker_compose/install.sh:450:IS_WSL=false
deployment/docker_compose/install.sh:459:RELEASE_REF="main"
deployment/docker_compose/install.sh:460:DEFAULT_IMAGE_TAG="edge"
deployment/docker_compose/install.sh:461:RELEASE_LOOKUP_FAILED=false
deployment/docker_compose/install.sh:596:GITHUB_RAW_URL="https://raw.githubusercontent.com/onyx-dot-app/onyx/${RELEASE_REF}/deployment/docker_compose"
deployment/docker_compose/install.sh:607:DOCKER_VERSION=$(docker --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
deployment/docker_compose/install.sh:748:RESOURCE_WARNING=false
deployment/docker_compose/install.sh:749:EXPECTED_RAM_MB=$((EXPECTED_DOCKER_RAM_GB * 1024))
deployment/docker_compose/install.sh:785:NGINX_BASE_URL="https://raw.githubusercontent.com/onyx-dot-app/onyx/${RELEASE_REF}/deployment/data/nginx"
deployment/docker_compose/install.sh:900:ENV_FILE="${INSTALL_ROOT}/deployment/.env"
deployment/docker_compose/install.sh:901:ENV_TEMPLATE="${INSTALL_ROOT}/deployment/env.template"
deployment/docker_compose/install.sh:1163:PORT_CHECK_AVAILABLE=false
deployment/docker_compose/install.sh:1175:AVAILABLE_PORT=$(find_available_port 3000)
deployment/docker_compose/install.sh:1189:CURRENT_IMAGE_TAG=$(grep "^IMAGE_TAG=" "$ENV_FILE" | head -1 | cut -d'=' -f2 | tr -d ' "'"'"'')
deployment/docker_compose/install.sh:1250:UP_WAIT_ARGS=()
deployment/docker_compose/install.sh:1262:UP_EXIT=0
deployment/docker_compose/env.prod.template:7:WEB_DOMAIN=http://localhost:3000
deployment/docker_compose/env.prod.template:15:AUTH_TYPE=google_oauth
deployment/docker_compose/env.prod.template:18:GOOGLE_OAUTH_CLIENT_ID=
deployment/docker_compose/env.prod.template:19:GOOGLE_OAUTH_CLIENT_SECRET=
deployment/docker_compose/env.prod.template:20:SECRET=
deployment/docker_compose/env.prod.template:43:SESSION_EXPIRE_TIME_SECONDS=604800
deployment/docker_compose/env.prod.template:58:POSTGRES_USER=postgres
deployment/docker_compose/env.prod.template:59:POSTGRES_PASSWORD=password
deployment/docker_compose/env.prod.template:64:DB_READONLY_USER=db_readonly_user
deployment/docker_compose/env.prod.template:65:DB_READONLY_PASSWORD=password
deployment/docker_compose/env.prod.template:73:SHOW_EXTRA_CONNECTORS=False
deployment/docker_compose/env.template:13:IMAGE_TAG=latest
deployment/docker_compose/env.template:61:AUTH_TYPE=basic
deployment/docker_compose/env.template:66:USER_AUTH_SECRET=""
deployment/docker_compose/env.template:88:ENABLE_PAID_ENTERPRISE_EDITION_FEATURES=false
deployment/docker_compose/env.template:95:POSTGRES_USER=postgres
deployment/docker_compose/env.template:96:POSTGRES_PASSWORD=password
deployment/docker_compose/env.template:116:COMPOSE_PROFILES=s3-filestore
deployment/docker_compose/env.template:117:FILE_STORE_BACKEND=s3
deployment/docker_compose/env.template:120:S3_ENDPOINT_URL=http://minio:9000
deployment/docker_compose/env.template:121:S3_AWS_ACCESS_KEY_ID=minioadmin
deployment/docker_compose/env.template:122:S3_AWS_SECRET_ACCESS_KEY=minioadmin
deployment/docker_compose/env.template:123:S3_FILE_STORE_BUCKET_NAME=onyx-file-store-bucket
deployment/docker_compose/env.template:124:MINIO_ROOT_USER=minioadmin
deployment/docker_compose/env.template:125:MINIO_ROOT_PASSWORD=minioadmin
deployment/docker_compose/env.template:174:USE_IAM_AUTH=false
deployment/docker_compose/env.template:188:LOG_LEVEL=info
deployment/docker_compose/env.template:189:LOG_ONYX_MODEL_INTERACTIONS=False
deployment/docker_compose/env.template:303:POSTGRES_HOST=relational_db
deployment/docker_compose/env.template:304:REDIS_HOST=cache
deployment/docker_compose/env.template:305:MODEL_SERVER_HOST=inference_model_server
deployment/docker_compose/env.template:306:INDEXING_MODEL_SERVER_HOST=indexing_model_server
deployment/docker_compose/env.template:307:INTERNAL_URL=http://api_server:8080
deployment/aws_ecs_fargate/cloudformation/deploy.sh:9:TEMPLATE_DIR="$(pwd)"
deployment/aws_ecs_fargate/cloudformation/deploy.sh:10:SERVICE_DIR="$TEMPLATE_DIR/services"
deployment/aws_ecs_fargate/cloudformation/deploy.sh:13:CONFIG_FILE="onyx_config.jsonl"
deployment/aws_ecs_fargate/cloudformation/deploy.sh:16:AWS_REGION_FROM_CONFIG=$(remove_comments "$CONFIG_FILE" | jq -r '.AWSRegion // empty')
deployment/aws_ecs_fargate/cloudformation/deploy.sh:24:ENVIRONMENT=$(remove_comments "$CONFIG_FILE" | jq -r '.Environment')
deployment/aws_ecs_fargate/cloudformation/deploy.sh:31:S3_BUCKET_FROM_CONFIG=$(remove_comments "$CONFIG_FILE" | jq -r '.S3Bucket // empty')
deployment/aws_ecs_fargate/cloudformation/deploy.sh:38:INFRA_ORDER=(
deployment/aws_ecs_fargate/cloudformation/deploy.sh:45:SERVICE_ORDER=(
deployment/aws_ecs_fargate/cloudformation/uninstall.sh:3:AWS_REGION="${AWS_REGION:-us-west-1}"
deployment/aws_ecs_fargate/cloudformation/uninstall.sh:6:CONFIG_FILE="onyx_config.json"
deployment/aws_ecs_fargate/cloudformation/uninstall.sh:9:ENVIRONMENT=$(jq -r '.Environment' "$CONFIG_FILE")
deployment/aws_ecs_fargate/cloudformation/uninstall.sh:16:S3_BUCKET_FROM_CONFIG=$(jq -r '.S3Bucket // empty' "$CONFIG_FILE")
deployment/aws_ecs_fargate/cloudformation/uninstall.sh:23:STACK_NAMES=(
.devcontainer/init-firewall.sh:29:GITHUB_IPS=$(curl -s https://api.github.com/meta | jq -r '.api[]' 2>/dev/null | grep -v ':' || echo "")
.devcontainer/init-firewall.sh:37:ALLOWED_DOMAINS=(
.devcontainer/init-firewall.sh:73:DOCKER_GATEWAY=$(ip -4 route show default | awk '{print $3}')
.devcontainer/init-firewall.sh:114:BLOCKED_SITES=("example.com" "google.com" "facebook.com")
.devcontainer/init-dev-user.sh:16:WORKSPACE=/workspace
.devcontainer/init-dev-user.sh:17:TARGET_USER=dev
.devcontainer/init-dev-user.sh:18:REMOTE_USER="${SUDO_USER:-$TARGET_USER}"
.devcontainer/init-dev-user.sh:20:WS_UID=$(stat -c '%u' "$WORKSPACE")
.devcontainer/init-dev-user.sh:21:WS_GID=$(stat -c '%g' "$WORKSPACE")
.devcontainer/init-dev-user.sh:22:DEV_UID=$(id -u "$TARGET_USER")
.devcontainer/init-dev-user.sh:23:DEV_GID=$(id -g "$TARGET_USER")
.devcontainer/init-dev-user.sh:28:MOUNT_HOME=/home/"$TARGET_USER"

```

## Required environment variable status

| Variable / source | Status | Notes |
|---|---|---|
| Root `.env.example` | MISSING | The requested search found only widget examples. |
| `deployment/docker_compose/env.template` | PRESENT | Template file exists for Docker Compose setup; values are placeholders/defaults. |
| `deployment/docker_compose/env.prod.template` | PRESENT | Production template exists; values are placeholders/defaults and must be replaced for real deployment. |
| Runtime `.env` values | UNKNOWN | Real `.env` values were intentionally not printed. |
| Additional app secrets for local lite start | UNKNOWN | Startup could not begin because Docker is missing, so runtime missing-secret behavior was not reached. |

## Claim boundaries

This Step 47X evidence does not claim live cloud/VPS staging validation, production readiness, enterprise production readiness, external validation, compliance certification, full Onyx-wide enforcement, customer deployment, CI pass, or local Docker staging success.

## Readiness status after Step 47X

- Production-style portfolio readiness: historical readiness snapshot.
- Enterprise production-candidate readiness: NO-GO.
- Local Docker staging evidence: BLOCKED.
- Live staging/cloud validation: PENDING.
- CI Actions evidence: BLOCKED.
- External validation: PENDING.
- Compliance certification: NOT CLAIMED.

