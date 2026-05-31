# Redaction Note

The Step 63X retry bundle is designed to capture operational evidence without committing secrets.

- Do not commit raw `.env` files, shell history, tokens, passwords, API keys, MinIO root credentials, cookies, or authorization headers.
- Cookie values from host-proxy curl output must remain redacted as `<REDACTED>`.
- If additional HTTP headers are captured, redact `Authorization`, `Cookie`, `Set-Cookie`, and provider-specific key headers before storing evidence.
- Container names, image tags, health status, and non-secret HTTP status lines may be retained.
