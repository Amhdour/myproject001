# Oracle VPS Staging Foundation - VPS Inventory

## Evidence Metadata

- Evidence ID: EVID-ORACLE-VPS-INVENTORY
- Step: Oracle VPS staging foundation
- Status: draft
- Environment: Oracle VPS staging
- Commit SHA: TBD
- Timestamp: TBD
- Redaction status: required before publication

## VPS Inventory

| Field | Value |
|---|---|
| Cloud provider | Oracle Cloud Infrastructure |
| Region | TBD |
| Availability domain | TBD |
| Shape | TBD |
| CPU / memory | TBD |
| Boot volume size | TBD |
| OS image | TBD |
| Public IP | REDACTED/TBD |
| Private IP | REDACTED/TBD |
| SSH port | 22 or custom/TBD |
| Deployment user | TBD |
| Domain/subdomain | TBD |
| Firewall/security-list rules | TBD |
| Backup target | TBD |
| Monitoring target | TBD |
| Logging target | TBD |

## Redaction Rules

Do not publish:

- private SSH keys
- access tokens
- raw `.env` files
- database passwords
- live public IPs unless intentionally approved
- raw database dumps
- customer/user data

## Notes

This inventory is required before deployment evidence can be trusted. It does not claim production readiness.
