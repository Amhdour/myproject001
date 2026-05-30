# Rollback Notes

## Purpose

These notes describe how to remove the manual staging diagnostic MinIO container, optionally remove its volume, and restart Onyx services to return toward the previous staging state.

## Non-destructive container removal

```bash
docker stop minio-lu8fgylyjp4so3adpxep8ixb || true
docker rm minio-lu8fgylyjp4so3adpxep8ixb || true
```

## Destructive optional volume removal

Destructive warning: `docker volume rm onyx-minio-data` deletes uploaded/file-store test data stored in that volume. Do not run this command automatically unless intentionally testing rollback or intentionally deleting the staging diagnostic file-store data.

```bash
docker volume rm onyx-minio-data || true
```

## Restart Onyx services

```bash
docker restart api_server-lu8fgylyjp4so3adpxep8ixb-122758538471
docker restart background-lu8fgylyjp4so3adpxep8ixb-122758678866
docker restart web_server-lu8fgylyjp4so3adpxep8ixb-122758961321
```

## Revert-to-previous-state guidance

1. Stop and remove the diagnostic MinIO container.
2. Only if intentional, remove the `onyx-minio-data` volume.
3. Restart the API, background, and web services.
4. Re-check API logs and Docker health states.
5. Expect the original MinIO file-store blocker to return if the API still expects `http://minio:9000` and no durable MinIO service is present.
