from backend.security_layer.cache.key_contract import (
    CACHE_KEY_SCHEMA_VERSION,
    FORBIDDEN_CACHE_KEY_FIELDS,
    REQUIRED_CACHE_KEY_FIELDS,
    build_safe_cache_key,
    sanitize_cache_key,
    validate_cache_key,
    validate_cache_key_schema_version,
    validate_no_forbidden_cache_key_content,
)


def _base_key() -> dict[str, object]:
    return {k: "safe-value" for k in REQUIRED_CACHE_KEY_FIELDS}


def test_required_cache_key_fields_count_and_coverage() -> None:
    assert len(REQUIRED_CACHE_KEY_FIELDS) == 21
    key = build_safe_cache_key(**_base_key())
    assert set(REQUIRED_CACHE_KEY_FIELDS).issubset(key.keys())


def test_cache_key_schema_version_validated() -> None:
    key = _base_key()
    key["cache_key_schema_version"] = CACHE_KEY_SCHEMA_VERSION
    assert validate_cache_key_schema_version(key)
    key["cache_key_schema_version"] = "v999"
    assert not validate_cache_key_schema_version(key)


def test_forbidden_cache_key_fields_are_rejected() -> None:
    for forbidden in FORBIDDEN_CACHE_KEY_FIELDS:
        key = _base_key()
        key[forbidden] = "forbidden"
        assert not validate_no_forbidden_cache_key_content(key)


def test_forbidden_patterns_are_rejected() -> None:
    assert not validate_no_forbidden_cache_key_content({"x": "raw query text should not be here"})
    assert not validate_no_forbidden_cache_key_content({"x": "raw prompt text should not be here"})
    assert not validate_no_forbidden_cache_key_content({"x": "raw document text should not be here"})
    assert not validate_no_forbidden_cache_key_content({"x": "raw chunk text should not be here"})
    assert not validate_no_forbidden_cache_key_content({"x": "source_secret=abc"})
    assert not validate_no_forbidden_cache_key_content({"x": "api_key=abc"})
    assert not validate_no_forbidden_cache_key_content({"x": "token=abc"})
    assert not validate_no_forbidden_cache_key_content({"x": "credential=abc"})
    assert not validate_no_forbidden_cache_key_content({"x": "https://user:password@connector.example"})
    assert not validate_no_forbidden_cache_key_content({"x": "a@example.com"})
    assert not validate_no_forbidden_cache_key_content({"x": "raw_policy_internal_blob"})
    assert not validate_no_forbidden_cache_key_content({"x": "raw_cache_backend_internal_blob"})


def test_sanitize_does_not_leak_forbidden_fields() -> None:
    key = _base_key()
    key["raw_query_text"] = "hello"
    key["token"] = "secret"
    key["subject_id_hash_or_safe_id"] = "  safe-subject  "
    sanitized = sanitize_cache_key(key)
    assert "raw_query_text" not in sanitized
    assert "token" not in sanitized
    assert sanitized["subject_id_hash_or_safe_id"] == "safe-subject"


def test_validate_cache_key_rejects_missing_required_fields() -> None:
    key = _base_key()
    key["cache_key_schema_version"] = CACHE_KEY_SCHEMA_VERSION
    del key[REQUIRED_CACHE_KEY_FIELDS[-1]]
    assert not validate_cache_key(key)


def test_validate_cache_key_happy_path() -> None:
    key = build_safe_cache_key(**_base_key())
    assert validate_cache_key(key)
