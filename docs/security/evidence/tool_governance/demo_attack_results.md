# Demo Attack Results

The demo attack now exercises the tool execution seam in `backend/onyx/tools/tool_runner.py` with `SECURITY_TOOL_GOVERNANCE_ENFORCEMENT=true`.

Attack scenario:

- A near-real `send_email` tool call is selected for execution.
- The tool arguments attempt to send external/private data to an outside address.
- The existing tool authorization gate is allowed in the demo so the governance seam is the blocking control under test.

Expected result:

- The governance request is built before tool execution with user, tenant, selected tool name, action, risk level, side-effect status, and correlation ID.
- The governance decision is `approval_required` for the high-risk side-effecting `send_email` action.
- The tool start packet is not emitted and the tool `run` method is not called automatically.
- A `tool_governance_decision` receipt/evidence event is written with the receipt hash and correlation ID.
- Safe evidence contains only allowlisted metadata.
- Raw tool payload content, external recipient, private data text, and demo secret-like values are not exported.

This is not a production readiness claim. The demo validates only the local env-gated governance foundation at the first tool execution seam.
