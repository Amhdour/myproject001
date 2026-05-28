# MCP Egress Policy (Planned)

- outbound egress trust boundary: MCP runtime may only reach policy-approved external destinations.
- allowed domain model: explicit allowlist keyed by egress_policy_id and risk tier.
- denied domain model: explicit denylist for known abuse/exfiltration destinations.
- internal network block model: block RFC1918, loopback, link-local, and cluster-internal hosts by default.
- metadata service block model: block cloud metadata endpoints (e.g., 169.254.169.254).
- credential exfiltration endpoint block model: block known pastebin/filedrop/webhook exfil paths unless explicitly approved.
- MCP-specific egress policy ID: each server/tool binding references egress_policy_id in registry.
- audit/finding/metric requirements: emit all three for denied/flagged egress attempts.
- monitor-only / future enforce behavior: monitor-only now; enforce behavior planned and blocked until explicit approval.
- known limitations: no live egress enforcement integrated into request paths.
