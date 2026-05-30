# Redaction Note

Do not publish raw env dumps.

Redact passwords, tokens, keys, cookies, SSH keys, and public IP addresses when appropriate for public sharing.

Required redaction targets include:

- `OPENSEARCH_ADMIN_PASSWORD`
- `S3_AWS_SECRET_ACCESS_KEY`
- `POSTGRES_PASSWORD`
- `MINIO_ROOT_PASSWORD`
- `Set-Cookie` values
- SSH private key
- OCI secrets
- any `.env` content
