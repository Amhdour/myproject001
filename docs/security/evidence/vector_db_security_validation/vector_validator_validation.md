Step 19C validator validation:
- Missing tenant/subject safely denied via context validation + controls tests.
- Namespace mismatch denied.
- Invalid metadata, missing/stale ACL snapshot, and missing provenance denied.
- Deleted/stale candidates filtered and flagged.
- Prompt-injection and poisoning markers flagged.
- Decision reason redaction prevents raw text leakage.
