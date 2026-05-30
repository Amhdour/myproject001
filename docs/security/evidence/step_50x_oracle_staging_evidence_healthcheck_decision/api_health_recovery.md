# API Health Recovery

## Before MinIO fix

The API was failing/restarting because it could not connect to the expected MinIO endpoint for the configured S3-compatible file-store bucket.

Observed blocker:

```text
botocore.exceptions.EndpointConnectionError: Could not connect to the endpoint URL: "http://minio:9000/onyx-file-store-bucket"
```

## After MinIO fix

After adding MinIO to the Onyx Docker network with alias `minio`, creating the `onyx-file-store-bucket` bucket, and restarting services, `api_server` became healthy.

## Claim boundary

API health is GO for this Oracle staging diagnostic state. Full app GO is not claimed because `web_server` remains Docker-unhealthy due to the documented healthcheck mismatch.
