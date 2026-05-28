from backend.security_layer.artifacts.content_scanners import scan_artifact_malware_markers, scan_artifact_policy_markers, scan_artifact_secret_markers


def test_malware_scanner() -> None:
    assert scan_artifact_malware_markers("normal")
    assert not scan_artifact_malware_markers("contains eicar string")


def test_secret_scanner() -> None:
    assert scan_artifact_secret_markers("hello")
    assert not scan_artifact_secret_markers("api_key=abc")


def test_policy_scanner() -> None:
    ok, flags = scan_artifact_policy_markers("this has prompt_injection")
    assert not ok
    assert "prompt_injection" in flags
