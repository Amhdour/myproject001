# Redaction Helper Limitations

- This helper is not a production-readiness claim and does not provide a complete data-loss-prevention program.
- Presidio is optional. If it is not installed, fallback redaction uses regexes and cannot detect every possible PII or secret format.
- Regex fallback intentionally targets common evidence-export risks: email addresses, phone-like values, bearer tokens, API-key-like values, and obvious secret-key assignments.
- Redaction can produce false positives, especially for phone-like numeric strings and token-like identifiers.
- Redaction can produce false negatives for uncommon secret formats, obfuscated PII, multi-field secrets, or data that only becomes sensitive in context.
- `safe_metadata` preserves explicitly allowlisted fields (`correlation_id`, `decision`, `policy_package`, `fallback_used`, and `enforcement_enabled`) by design. Do not place raw prompts, chunk text, or secrets in those fields.
- The helper does not change OPA enforcement behavior.
- The helper does not change OpenTelemetry behavior. Langfuse evidence payload preparation uses it only as defense-in-depth after deny-by-default field selection.
- The helper does not add LlamaFirewall, AgentShield, PyRIT, garak, promptfoo, or Ragas.
