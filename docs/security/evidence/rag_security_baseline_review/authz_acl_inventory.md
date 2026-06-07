# Authorization and ACL Inventory

## Purpose
Inventory confirmed authorization and ACL constructs relevant to retrieval.

## Commands or search methods used
- `rg -n -i "permission|acl|authz|tenant|group|role" backend docs .github`
- Direct inspection of access, DB models, Vespa filter/indexing code, and retrieval guard code.

## Files found
- `backend/onyx/access/models.py`
- `backend/onyx/access/access.py`
- `backend/onyx/access/utils.py`
- `backend/onyx/db/models.py`
- `backend/onyx/db/enums.py`
- `backend/onyx/context/search/preprocessing/access_filters.py`
- `backend/onyx/document_index/vespa/indexing_utils.py`
- `backend/onyx/document_index/vespa/shared_utils/vespa_request_builders.py`
- `backend/onyx/security_layer/retrieval_guard/acl_verifier.py`

## Relevant code paths found
- `DocumentAccess.to_acl()` converts user email, user group, external user email, external group, and public access into ACL strings.
- `get_acl_for_user()` returns public access for anonymous users and user-email plus public access for standard users in the community implementation.
- Vespa indexing writes `ACCESS_CONTROL_LIST` from `chunk.access.to_acl()`.
- Vespa filter construction applies a weighted set filter over `access_control_list` when ACL filters are present.
- Retrieval guard code evaluates embedded metadata ACL and ACL state values.

## Findings
- Documents can carry ownership/permission fields such as `primary_owners`, `secondary_owners`, `external_user_emails`, `external_user_group_ids`, and connector access type.
- Connector credential pairs have `AccessType.PUBLIC`, `PRIVATE`, and `SYNC` values.
- ACL entries are stored in vector-index metadata and used during query filtering.

## Gaps
- This review did not prove all enterprise external-permission behavior because some EE implementations are dynamically fetched.
- DB-backed ACL verification is explicitly TODO in `backend/onyx/security_layer/retrieval_guard/acl_verifier.py`.
- Stale permission handling was found in tests/fixtures and metadata states, but not proven against a live sync service.

## Claim boundary
ACL models and enforcement paths exist in code; full authorization correctness across all connectors and deployments is not proven.
