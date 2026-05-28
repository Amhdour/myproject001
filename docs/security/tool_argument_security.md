# Tool Argument Security Rules (Planned)

## Allowed argument types
- string, integer, float, boolean, arrays/objects constrained by schema.

## Forbidden argument names
- `password`, `secret`, `api_key`, `access_token`, `private_key` as raw freeform inputs unless explicitly designated as secure references.

## Forbidden raw secret values
- Inline credential/token/key material in plaintext.

## File path validation
- Normalize path, enforce allowed roots, reject `..`, null-byte patterns, and mixed-encoding bypasses.

## URL validation
- Require absolute URL for URL fields, allowed schemes only, canonical host parsing.

## Domain allowlist/denylist model
- Per-tool allowlist primary; explicit denylist for metadata/loopback/internal ranges.

## Command argument handling
- No shell concatenation model; arguments must be structured tokens validated against schema.

## SQL-like input handling
- Detect suspicious SQL control sequences in non-SQL fields and flag/deny by policy tier.

## Prompt-derived argument handling
- Mark argument provenance (user/prompt/system); higher scrutiny for prompt-derived values.

## Detection Controls
- Path traversal detection: `../`, encoded traversal, absolute-path escape.
- SSRF detection: loopback/private IPs, cloud metadata addresses, unsupported schemes.
- Command injection detection: shell metacharacters and chained command patterns.
- Credential/token/API-key detection: regex + entropy-assisted heuristics.

## Size and structure checks
- Max length per field and total payload size.
- Structured schema validation must pass before content checks are evaluated as complete.

## Redaction expectations
- Sensitive substrings redacted in audit/findings evidence.

## Evidence expectations
- Record matched rule id, normalized argument path, and safe-denial category.

## Known limitations
- Design-only; not integrated into live call path; no enforce-mode blocking.

- Step 21B: isolated argument validators implemented in `backend/security_layer/tools/argument_validators.py`.

## Step 21C Argument Validation Status (2026-05-28)
- Path traversal, SSRF URL, command injection, secret-value, and prompt-injection markers validated.
- Sanitization redaction and no-live-side-effect assumptions validated via isolated tests.
