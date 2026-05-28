# MCP Signing and Replay Coverage

`backend/security_layer/mcp/signing_replay.py` includes concrete checks for:
- signature required/present/freshness metadata
- replay protection required/present/freshness metadata
- replay decision builder

This verifies request signing and replay metadata control points are implemented.
