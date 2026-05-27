Implemented a minimal live monitor-only hook call path:
- search_runner now invokes `_apply_monitor_only_live_acl_hook` after existing retrieval guard.
- hook is disabled by default via `default_retrieval_integration_config`.
- when monitor-only, it builds context/candidates from safe metadata and evaluates via isolated retrieval integration hook.
- any telemetry/hook error fails open and preserves retrieval response.
