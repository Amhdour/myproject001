# Redaction Note

- Do not commit raw reviewer email if confidential.
- Do not commit private contact details without permission.
- Do not commit secrets, tokens, keys, cookies, env dumps, SSH keys, OCI secrets, or public IP if redaction desired.
- Store sanitized summaries in repo.
- Keep raw confidential responses outside the public repo unless permission is explicit.

If a real secret or private reviewer detail is found in a candidate artifact, stop, redact it, and keep the status at NO-GO until the exposure is resolved.
