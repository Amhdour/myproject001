# Safe Metadata Validation
- `context_builder` metadata safety gate blocks sensitive keys:
  `document_text`, `chunk_text`, `source_secret`, `secret`, `raw_text`, `content`.
- Parametrized test asserts each blocked key raises `ValueError`.
- Adapter metadata usage validated as identifier-only and non-content fields.
