Step 19C model validation:
- No raw document/chunk text fields in vector model dataclasses.
- No secret/api key/token/credential fields in model dataclasses.
- Explicit tenant/workspace/document/chunk/provenance field coverage verified via `VectorSecurityContext` and metadata contract fields.
- Explicit deleted/stale flags, prompt_injection_flag, poisoning_flag, and metadata_schema_version coverage verified by tests.
