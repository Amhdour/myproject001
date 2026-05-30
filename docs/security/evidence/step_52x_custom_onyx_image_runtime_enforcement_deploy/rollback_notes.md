# Rollback Notes

## Rollback Status

No rollback was executed because no custom image was deployed.

## Rollback Path If Future Deployment Is Attempted

1. Capture pre-change container inventory and image tags.
2. Preserve database, Redis, OpenSearch/Vespa, MinIO, volumes, and network `lu8fgylyjp4so3adpxep8ixb`.
3. If the custom backend image breaks the app, restore both `api_server` and `background` to the previously deployed backend image, currently expected from Step 51X to be `onyxdotapp/onyx-backend:latest` unless newer VPS evidence shows otherwise.
4. Restart only the backend services needed for rollback.
5. Re-run API, web/proxy, MinIO, and container inventory checks.
6. Record logs and classify `ORACLE_CUSTOM_IMAGE_DEPLOYED_APP_NO_GO` if the custom image caused material breakage.

## Evidence Path

This file is the Step 52X rollback evidence placeholder. It must be supplemented with real VPS rollback commands/output if a future deployment is executed.
