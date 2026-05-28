Validated argument_validators.py:
- Path traversal detection present.
- SSRF/localhost URL detection present.
- Command injection detection present.
- Secret/token/api-key/private-key/password detection present.
- Prompt injection marker detection present.
- Sanitization redacts secret-like argument values.
- No filesystem/network/shell side-effects in validator functions.
