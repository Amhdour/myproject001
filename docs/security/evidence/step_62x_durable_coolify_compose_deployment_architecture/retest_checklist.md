# Retest Checklist

- [ ] `docker compose config` passes for the selected compose/override path.
- [ ] `api_server` uses `rag-agent-security-onyx-backend:step53x-b77bee6` or the explicitly selected custom backend image.
- [ ] `background` uses the same custom backend image as `api_server`.
- [ ] MinIO service exists in Compose/Coolify, not as an unmanaged diagnostic container.
- [ ] `onyx-file-store-bucket` exists in MinIO.
- [ ] API is healthy.
- [ ] Web Docker health is healthy or any remaining health behavior is documented with exact evidence.
- [ ] Host/proxy checks pass or are documented with exact limitations.
- [ ] Step 39X runtime hook exists in the deployed API container.
- [ ] Step 55X runtime smoke test still passes after redeploy.
- [ ] no secrets exposed in committed evidence or logs.
