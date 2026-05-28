from backend.security_layer.cache.key_contract import REQUIRED_CACHE_KEY_FIELDS, build_safe_cache_key, validate_cache_key, validate_no_forbidden_cache_key_content


def _base():
    return {k: "x" for k in REQUIRED_CACHE_KEY_FIELDS}


def test_safe_cache_key_creation_and_required_fields() -> None:
    key = build_safe_cache_key(**_base())
    for field in REQUIRED_CACHE_KEY_FIELDS:
        assert field in key
    assert validate_cache_key(key)


def test_forbidden_and_patterns_rejected() -> None:
    key = _base()
    key["raw_query_text"] = "hello"
    assert not validate_no_forbidden_cache_key_content(key)
    assert not validate_no_forbidden_cache_key_content({"a": "api_key=abc"})
    assert not validate_no_forbidden_cache_key_content({"a": "a@example.com"})
    assert not validate_no_forbidden_cache_key_content({"a": "https://u:pw@host"})
