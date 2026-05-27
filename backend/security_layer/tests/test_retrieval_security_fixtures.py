from __future__ import annotations

import re

from backend.security_layer.tests.retrieval_security_fixtures import build_retrieval_security_fixtures


EXPECTED_KEYS = {
    "tenant_a", "tenant_b", "user_allowed", "user_denied", "group_allowed", "group_denied",
    "role_allowed", "role_denied", "document_allowed", "document_cross_tenant", "document_deleted",
    "chunk_allowed", "chunk_cross_tenant", "chunk_denied_group", "chunk_denied_role", "stale_acl_snapshot",
    "fresh_acl_snapshot", "vector_namespace_allowed", "vector_namespace_denied", "vector_metadata_allowed",
    "vector_metadata_denied", "cache_entry_allowed", "cache_entry_cross_tenant", "citation_allowed",
    "citation_denied", "rerank_candidate_allowed", "rerank_candidate_denied",
}

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})")
SECRET_PATTERNS = (
    "api_key", "apikey", "token", "bearer ", "authorization:", "password", "passwd", "secret",
    "credential", "access_key", "private key", "-----begin",
)
TEXT_LEAK_PATTERNS = ("document text", "chunk text", "body text", "raw chunk", "source content")


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
    assert EXPECTED_KEYS == set(fixtures.keys()) & EXPECTED_KEYS


def test_fixture_ids_are_synthetic_and_deterministic() -> None:
    fixtures_a = build_retrieval_security_fixtures()
    fixtures_b = build_retrieval_security_fixtures()
    for key in EXPECTED_KEYS:
        fixture_id_a = str(fixtures_a[key]["id"])
        fixture_id_b = str(fixtures_b[key]["id"])
        assert fixture_id_a.startswith("fake_")
        assert fixture_id_a == fixture_id_b


def test_no_real_looking_email_addresses_or_domains() -> None:
    fixtures = build_retrieval_security_fixtures()
    emails = [fixtures["user_allowed"]["email"], fixtures["user_denied"]["email"]]
    assert all(str(email).endswith("@fake.invalid") for email in emails)

    for value in _iter_leaf_strings(fixtures):
        match = EMAIL_RE.search(value)
        if match:
            assert match.group(1) == "fake.invalid"


def test_no_document_or_chunk_body_text_present() -> None:
    fixtures = build_retrieval_security_fixtures()
    all_strings = [s.lower() for s in _iter_leaf_strings(fixtures)]
    assert all(not any(pattern in s for pattern in TEXT_LEAK_PATTERNS) for s in all_strings)
    assert all("placeholder" in s or "synthetic" in s or "fake_" in s or "tenant:" in s for s in all_strings)


def test_no_secrets_tokens_or_credentials_present() -> None:
    fixtures = build_retrieval_security_fixtures()
    all_strings = [s.lower() for s in _iter_leaf_strings(fixtures)]
    assert all(not any(pattern in s for pattern in SECRET_PATTERNS) for s in all_strings)


def test_cross_tenant_and_denied_markers_are_explicitly_synthetic() -> None:
    fixtures = build_retrieval_security_fixtures()
    assert fixtures["document_cross_tenant"]["synthetic_cross_tenant"] is True
    assert fixtures["chunk_cross_tenant"]["synthetic_cross_tenant"] is True
    assert fixtures["cache_entry_cross_tenant"]["synthetic_cross_tenant"] is True

    assert fixtures["chunk_denied_group"]["unauthorized"] is True
    assert fixtures["chunk_denied_role"]["unauthorized"] is True
    assert fixtures["vector_namespace_denied"]["unauthorized"] is True
    assert fixtures["vector_metadata_denied"]["unauthorized"] is True
    assert fixtures["citation_denied"]["unauthorized"] is True
    assert fixtures["rerank_candidate_denied"]["unauthorized"] is True

    assert fixtures["document_deleted"]["deleted"] is True
    assert fixtures["stale_acl_snapshot"]["stale"] is True
    assert fixtures["fresh_acl_snapshot"]["fresh"] is True
