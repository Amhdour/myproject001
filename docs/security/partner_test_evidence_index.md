# Partner Test Evidence Index

## Step 30X focused tests

Command:

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_evidence_room_models.py backend/security_layer/tests/test_evidence_room_index.py -q
```

Status: **passed**.

## Full security-layer tests

Command:

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests -q
```

Status: **passed**.

## Evidence files

- `docs/security/evidence/partner_evidence_room_bundle/test_output.txt`
- `docs/security/evidence/partner_evidence_room_bundle/test_exitcode.txt`
- `docs/security/evidence/partner_evidence_room_bundle/evidence_room_helper_coverage.md`
