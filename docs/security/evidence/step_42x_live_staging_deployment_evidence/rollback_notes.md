# Step 42X Rollback Notes

## Rollback Status
- Deployment started: no.
- Rollback actually tested: partially. Health and deployment stop/remove commands could not be tested because Docker is unavailable and no app started.
- Rollback need: no running Step 42X deployment existed to stop.

## Stop Deployment
If the local Docker Compose staging deployment starts in a future environment, stop it with:

```bash
docker compose -f deployment/docker_compose/docker-compose.yml \
  -f deployment/docker_compose/docker-compose.onyx-lite.yml \
  -f deployment/docker_compose/docker-compose.dev.yml down
```

## Remove Containers and Volumes
If the future staging attempt created throwaway local volumes and they are safe to remove, use:

```bash
docker compose -f deployment/docker_compose/docker-compose.yml \
  -f deployment/docker_compose/docker-compose.onyx-lite.yml \
  -f deployment/docker_compose/docker-compose.dev.yml down --volumes --remove-orphans
```

## Revert Runtime Security Mode
The Step 42X environment had `STEP_39X_RUNTIME_ENFORCEMENT_MODE` missing, so effective mode was already `disabled`. To revert a future shell session to the safe default:

```bash
unset STEP_39X_RUNTIME_ENFORCEMENT_MODE
```

or explicitly set monitor-only in a controlled staging-only context:

```bash
export STEP_39X_RUNTIME_ENFORCEMENT_MODE=monitor_only
```

## Revert Branch or Commit
To leave the Step 42X branch without losing work:

```bash
git switch work
```

To revert the Step 42X commit after it exists, use a normal reviewed revert rather than deleting history:

```bash
git revert <step-42x-commit-sha>
```

## Exact Rollback Command Output in This Environment
No `docker compose down` command was run because `docker` is not installed and `docker compose ... up` never created containers. The deployment-attempt evidence already records `docker: command not found` for all Docker Compose commands.
