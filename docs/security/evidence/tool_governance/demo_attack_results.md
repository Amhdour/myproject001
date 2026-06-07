# Demo Attack Results

The demo attack attempts to execute the high-risk side-effecting `send_email` tool with a raw payload containing an email address and a demo secret-like value.

Expected result:

- The governance decision is `approval_required`.
- The risk level is `high`.
- An approval ID is issued for a separate approver path.
- A receipt hash is generated.
- Safe evidence contains only allowlisted metadata.
- Raw payload content is not exported.

This is not a production readiness claim. The demo validates only the local governance foundation behavior.
