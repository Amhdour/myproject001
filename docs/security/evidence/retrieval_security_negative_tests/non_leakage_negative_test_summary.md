# Non-Leakage Negative Test Summary

`test_negative_decisions_do_not_include_raw_text_or_secrets` validates that negative decision metadata does not include:
- raw document/chunk text fields
- secret-like fields (`api_key`, `token`, `password`, etc.)
- token-style values (e.g. `sk-...`)

All fixtures are synthetic (`fake_*`, `synthetic_*`, `@fake.invalid`) and contain no real customer/user/document data.
