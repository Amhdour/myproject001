Non-leakage validation summary:
- Registry forbidden-field/content checks reject secret-like patterns.
- Argument sanitization redacts secret-like values.
- Validator decision assertions verify status/category semantics only,
  with no raw credential/secret/policy/tenant internals included.
