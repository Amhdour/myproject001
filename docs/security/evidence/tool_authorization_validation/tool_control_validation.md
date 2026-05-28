Validated controls.py:
- 20 isolated stage control functions covered by tests.
- Audit/finding/metric helpers are runtime in-memory helper calls.
- No live tool execution calls, no MCP calls.
- No network/filesystem/shell execution.
- No production DB/cache/vector writes.
- No live app integration wiring.
