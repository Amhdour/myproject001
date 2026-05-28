Step 19C metadata contract validation:
- 21 required metadata fields validated.
- Forbidden metadata keys rejected.
- Forbidden value patterns rejected (raw text markers, api key/token/credential, secret URL, email-like content).
- Metadata schema version validated against VECTOR_METADATA_SCHEMA_VERSION.
- Sanitization helper verified to avoid raw-content key leakage.
