# Security Gap Register

## Purpose
Record gaps identified during the RAG Security Baseline Review.

## Commands or search methods used
- Consolidated from all evidence inventories and executed tests.

## Files found
See `repository_file_inventory.txt` and the individual topic inventories.

## Relevant code paths found
- Retrieval filtering and guard code: `backend/onyx/context/search/*`, `backend/onyx/document_index/vespa/*`, `backend/onyx/security_layer/retrieval_guard/*`.
- Tests and workflows: `backend/security_layer/tests/*`, `backend/tests/security/*`, `.github/workflows/*`.

## Findings
| Gap ID | Area | Gap | Evidence | Risk | Recommended next step |
|---|---|---|---|---|---|
| RAG-GAP-001 | Prompt injection | Retrieved-content prompt injection is documented as allowed in a demo attack limitation test. | `backend/tests/security/demo_attacks/test_prompt_injection_retrieval_attack.py` | Malicious documents may influence answer/tool behavior. | Define invariant and add scanner/boundary/output-validation tests. |
| RAG-GAP-002 | Live enforcement proof | Isolated tests pass, but live Onyx/Vespa/Postgres retrieval was not executed. | `test_results.md` | Controls may not behave as expected in deployment. | Add integration/staging demo attack with real services. |
| RAG-GAP-003 | DB-backed ACL verification | Retrieval guard TODO says current checks only evaluate embedded chunk metadata. | `backend/onyx/security_layer/retrieval_guard/acl_verifier.py` | Stale or malformed embedded ACL metadata may be trusted. | Add DB-backed verifier or freshness proof and tests. |
| RAG-GAP-004 | Citation leakage proof | Citation mapping exists, but live unauthorized citation leakage prevention was not proven. | `citation_integrity_inventory.md` | Unauthorized source identity may leak in answer/citations. | Add negative citation leakage integration/demo tests. |
| RAG-GAP-005 | CI/staging proof | CI workflows exist, but pass status and staging validation are not available locally. | `ci_gate_inventory.md` | Audit claims cannot rely on unobserved CI/staging state. | Capture CI artifacts and staging run logs. |

## Gaps
This register is not exhaustive for all security domains; it is scoped to RAG security baseline review evidence.

## Claim boundary
Gaps identify missing proof or incomplete controls. They do not assert exploitable vulnerabilities unless supported by test/code evidence.
