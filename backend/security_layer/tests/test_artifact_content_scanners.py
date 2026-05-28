from backend.security_layer.artifacts.content_scanners import (
    scan_artifact_policy_markers,
    scan_artifact_secret_markers,
    summarize_scan,
    validate_artifact_size,
)


def test_secret_scanner_markers() -> None:
    bad = ["sk-abc12345678", "api_key=abc", "token=abc", "-----BEGIN PRIVATE KEY-----", "password=abc"]
    assert scan_artifact_secret_markers("safe")
    for content in bad:
        assert not scan_artifact_secret_markers(content)


def test_policy_markers() -> None:
    cases = [
        "unauthorized_document_text", "raw_chunk_text", "cross_tenant", "sensitive_data",
        "ignore_previous_instructions", "data_poisoning", "rm -rf /", "../etc/passwd", "https://x.y/?token=a",
    ]
    for case in cases:
        ok, flags = scan_artifact_policy_markers(case)
        assert not ok
        assert flags


def test_size_and_summary_non_leakage() -> None:
    assert validate_artifact_size(1024)
    assert not validate_artifact_size(-1)
    assert not validate_artifact_size(20 * 1024 * 1024)
    summary = summarize_scan(["secret_marker_detected"])
    assert "raw_payload" not in str(summary)
    assert "sk-" not in str(summary)
