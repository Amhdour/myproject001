from __future__ import annotations

from backend.security_layer.tests.retrieval_security_fixtures import build_retrieval_security_fixtures


EXPECTED_KEYS = {
    "tenant_a", "tenant_b", "user_allowed", "user_denied", "group_allowed", "group_denied",
    "role_allowed", "role_denied", "document_allowed", "document_cross_tenant", "document_deleted",
    "chunk_allowed", "chunk_cross_tenant", "chunk_denied_group", "chunk_denied_role", "stale_acl_snapshot",
    "fresh_acl_snapshot", "vector_namespace_allowed", "vector_namespace_denied", "vector_metadata_allowed",
    "vector_metadata_denied", "cache_entry_allowed", "cache_entry_cross_tenant", "citation_allowed",
    "citation_denied", "rerank_candidate_allowed", "rerank_candidate_denied",
}


def _iter_leaf_strings(value: object):
    if isinstance(value, dict):
        for v in value.values():
            yield from _iter_leaf_strings(v)
    elif isinstance(value, (list, tuple, set)):
        for v in value:
            yield from _iter_leaf_strings(v)
    elif isinstance(value, str):
        yield value


def test_all_planned_fixtures_constructible() -> None:
    fixtures = build_retrieval_security_fixtures()
    assert EXPECTED_KEYS.issubset(fixtures.keys())


def test_fixture_ids_are_synthetic() -> None:
    fixtures = build_retrieval_security_fixtures()
    for key in EXPECTED_KEYS:
        assert str(fixtures[key]["id"]).startswith("fake_")


def test_no_real_looking_email_addresses() -> None:
    fixtures = build_retrieval_security_fixtures()
    assert fixtures["user_allowed"]["email"].endswith("@fake.invalid")
    assert fixtures["user_denied"]["email"].endswith("@fake.invalid")


def test_no_raw_text_or_secrets_present() -> None:
    fixtures = build_retrieval_security_fixtures()
    banned = ("api_key", "token", "secret=", "BEGIN PRIVATE KEY", "real customer", "lorem ipsum")
    banned_raw = ("document text", "chunk text", "raw text")
    all_strings = list(_iter_leaf_strings(fixtures))
    assert not any(any(b in s.lower() for b in banned) for s in all_strings)
    assert not any(any(b in s.lower() for b in banned_raw) for s in all_strings)


def test_cross_tenant_deleted_acl_and_denied_markers() -> None:
    fixtures = build_retrieval_security_fixtures()
    assert fixtures["document_cross_tenant"]["synthetic_cross_tenant"] is True
    assert fixtures["chunk_cross_tenant"]["synthetic_cross_tenant"] is True
    assert fixtures["cache_entry_cross_tenant"]["synthetic_cross_tenant"] is True
    assert fixtures["document_deleted"]["deleted"] is True
    assert fixtures["stale_acl_snapshot"]["stale"] is True
    assert fixtures["fresh_acl_snapshot"]["fresh"] is True
    assert fixtures["vector_namespace_allowed"]["namespace"] != fixtures["vector_namespace_denied"]["namespace"]
    assert fixtures["vector_metadata_allowed"]["security_scope"] != fixtures["vector_metadata_denied"]["security_scope"]
    assert fixtures["citation_denied"]["unauthorized"] is True
    assert fixtures["rerank_candidate_denied"]["unauthorized"] is True
