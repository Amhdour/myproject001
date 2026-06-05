# Step 04 Retrieval ACL Enforcement Summary

## Result

Step 04 adds a minimal Retrieval ACL Enforcement v1 hook behind `ONYX_SECURITY_RETRIEVAL_ACL_MODE=enforce`.

## What changed

- Off mode remains unchanged and returns all chunks.
- Shadow mode remains unchanged and returns all chunks while recording decisions.
- Enforce mode filters unauthorized chunks.
- Missing ACL metadata fails closed.
- Decision records redact document references and avoid chunk content.

## Safe claim boundary

This is a portfolio technical-proof slice only.

Do not describe it as production ready.
Do not describe it as enterprise ready.
Do not describe it as compliance certified.
