# Retrieval Security Test Fixtures (Step 18A)

Status: planned/design-only.

| fixture ID | purpose | safe fake fields | forbidden real data | mapped test groups | planned tests | implementation status |
|---|---|---|---|---|---|---|
| tenant_a | primary tenant scope | tenant_id=t_a, name=Tenant A | real tenant UUIDs/names | RST-G01,G11 | RST-T001,T011,T016 | planned |
| tenant_b | cross-tenant scope | tenant_id=t_b, name=Tenant B | real tenant identifiers | RST-G01 | RST-T002,T004 | planned |
| user_allowed | authorized subject | user_id=u_allow, email=fake_allow@example.test | real emails/user IDs | RST-G02,G16 | RST-T001,T017 | planned |
| user_denied | unauthorized subject | user_id=u_deny | real identities | RST-G02 | RST-T004,T026 | planned |
| group_allowed | allowed group binding | group_id=g_allow | prod group names | RST-G03 | RST-T001 | planned |
| group_denied | denied group binding | group_id=g_deny | prod group names | RST-G03 | RST-T005 | planned |
| role_allowed | allowed role binding | role=reader_allow | prod RBAC role labels | RST-G03 | RST-T001 | planned |
| role_denied | denied role binding | role=reader_deny | prod RBAC roles | RST-G03 | RST-T006 | planned |
| document_allowed | authorized document | doc_id=d_allow, source=fake_repo | real doc IDs/sources | RST-G04 | RST-T001 | planned |
| document_cross_tenant | unauthorized tenant doc | doc_id=d_cross | real cross-tenant docs | RST-G01,G04,G20 | RST-T002,T004 | planned |
| document_deleted | tombstoned doc | doc_id=d_deleted, deleted=true | real deleted docs | RST-G09 | RST-T008 | planned |
| chunk_allowed | authorized chunk | chunk_id=c_allow | real chunk text/IDs | RST-G05 | RST-T001 | planned |
| chunk_cross_tenant | unauthorized chunk tenant | chunk_id=c_cross | real chunks | RST-G05,G20 | RST-T003,T004 | planned |
| chunk_denied_group | group-denied chunk | chunk_id=c_grp_deny | real ACL labels | RST-G05,G14,G15 | RST-T005,T014,T015 | planned |
| chunk_denied_role | role-denied chunk | chunk_id=c_role_deny | real ACL labels | RST-G05,G14,G15 | RST-T006,T014,T015 | planned |
| stale_acl_snapshot | stale ACL state | acl_version=v1_old, ts=old | real ACL snapshots | RST-G08,G10 | RST-T007 | planned |
| fresh_acl_snapshot | current ACL state | acl_version=v2_new | real ACL snapshots | RST-G08,G10 | RST-T001 | planned |
| vector_namespace_allowed | matching namespace | namespace=ns_a | real namespaces | RST-G06 | RST-T001 | planned |
| vector_namespace_denied | mismatched namespace | namespace=ns_b | real namespaces | RST-G06 | RST-T009 | planned |
| vector_metadata_allowed | metadata match | tenant_tag=t_a, acl_hash=h1 | real metadata values | RST-G07 | RST-T001 | planned |
| vector_metadata_denied | metadata mismatch | tenant_tag=t_b, acl_hash=bad | real metadata | RST-G07 | RST-T010 | planned |
| cache_entry_allowed | valid cached retrieval | cache_key=ck_allow | real cache keys/payload | RST-G11 | RST-T011 | planned |
| cache_entry_cross_tenant | invalid cached retrieval | cache_key=ck_cross | real cached content | RST-G11 | RST-T011 | planned |
| citation_allowed | authorized citation | source_id=s_allow | real source refs | RST-G13 | RST-T013 | planned |
| citation_denied | unauthorized citation | source_id=s_deny | real source refs | RST-G13,G15 | RST-T013,T015 | planned |
| rerank_candidate_allowed | authorized rerank item | cand_id=r_allow | real rerank payload | RST-G12 | RST-T012 | planned |
| rerank_candidate_denied | unauthorized rerank item | cand_id=r_deny | real rerank payload | RST-G12 | RST-T012 | planned |

## Step 18B Fixture Implementation Status (2026-05-27)
- Status: implemented (synthetic fixtures only).
- File: `backend/security_layer/tests/retrieval_security_fixtures.py`.
- Validation tests: `backend/security_layer/tests/test_retrieval_security_fixtures.py`.

## Step 18B-A Fixture Evidence Update (2026-05-27)
- Fixture skeleton coverage executed successfully in direct suite rerun.
- Evidence: `docs/security/evidence/retrieval_security_test_skeletons/fixture_implementation_summary.md`.
