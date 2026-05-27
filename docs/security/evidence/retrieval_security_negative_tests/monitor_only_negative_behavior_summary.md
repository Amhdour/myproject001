# Monitor-Only Negative Behavior Summary

All monitor-only negative-case tests assert:
- no candidate blocking
- no candidate filtering/removal
- no denial toggles set on candidate metadata
- audit/findings/metrics are still emitted

No enforce mode or shadow-deny mode is enabled in these tests.
