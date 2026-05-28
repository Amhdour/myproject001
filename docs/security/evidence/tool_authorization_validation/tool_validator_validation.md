Validated validators.py:
- Denies missing tenant/subject/workspace.
- Denies unknown tool.
- Denies permission/group/role gaps.
- Denies out-of-scope service accounts.
- Denies missing/expired/wrong-tenant delegated credentials.
- High-risk approval-required tools return approval_required until approved.
- Unsafe/secret-leakage result metadata flagged.
- Decisions use safe reason/category fields without raw secret payloads.
