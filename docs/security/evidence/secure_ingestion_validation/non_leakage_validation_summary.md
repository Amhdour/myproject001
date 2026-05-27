# Non-Leakage Validation Summary (Step 15C)

Date: 2026-05-27

Validated through isolated tests:
- Decision reasons do not include raw prompt-injection marker phrases.
- Decision reasons do not include raw poisoning marker phrases.
- Decision reasons do not include source secret-like values (e.g., `sk-secret`).
- Denial responses use safe denial categories (`TENANT_CONTEXT_MISSING`, `SUBJECT_CONTEXT_MISSING`, `VALIDATION_FAILED`) rather than raw source details.

Note: these are isolated control tests only and do not represent active production enforcement.
