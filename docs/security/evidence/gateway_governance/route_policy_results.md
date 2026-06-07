# Gateway Governance Route Policy Results

Configured route policy behavior:

- Low-risk clean external request: `route_external` to `external`.
- PII external request: `mask` by default, or `deny`/`monitor` when `SECURITY_GATEWAY_PII_EXTERNAL_MODE` is configured accordingly.
- Secret-bearing request: `deny` to `blocked` before model routing.
- Restricted tenant data with an external provider: `deny` by default, or `route_private`/`monitor` when `SECURITY_GATEWAY_RESTRICTED_EXTERNAL_MODE` is configured accordingly.
- High-risk request: `approval_required` by default, or `monitor` when `SECURITY_GATEWAY_HIGH_RISK_MODE=monitor`.
