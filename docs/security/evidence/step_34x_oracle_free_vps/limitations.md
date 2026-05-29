# Step 34X Limitations

- The attempted Coolify staging deployment was **BLOCKED** before container startup.
- The blocked run used `deployment/docker_compose/docker-compose.yml`, whose `build:` contexts resolve incorrectly when Coolify uses the repository root as the project directory.
- No live redeploy was executed by Codex after adding `deployment/docker_compose/docker-compose.coolify-staging.yml`.
- No live smoke tests were executed by Codex.
- No production-readiness, enterprise-readiness, external-validation, or compliance-certification claims are made.
- No secrets were committed to the repository.
- Future evidence must come from an approved operator redeploying with the Coolify-specific compose file and capturing sanitized logs/results.
