# Live Hook Inspection
- File inspected: `backend/onyx/context/search/retrieval/search_runner.py`.
- Monitor-only hook executes after `apply_retrieval_acl_guard` and before final return.
- Return value remains `chunks` unchanged in all code paths.
- Hook exceptions are caught (`except Exception`) and retrieval response is preserved (fail-open).
- No retrieval filtering/blocking/denial added in the hook path.
- Live path invokes monitor-only adapter only when `is_monitor_only(config)` is true.
