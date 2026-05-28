from __future__ import annotations

import re

_SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9]{8,}"),
    re.compile(r"(?i)api[_-]?key\s*[:=]"),
    re.compile(r"(?i)token\s*[:=]"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)password\s*[:=]"),
)

_POLICY_PATTERNS: dict[str, re.Pattern[str]] = {
    "unauthorized_document_text": re.compile(r"(?i)raw_document_text|unauthorized_document_text"),
    "unauthorized_chunk_text": re.compile(r"(?i)raw_chunk_text|unauthorized_chunk_text"),
    "cross_tenant_marker": re.compile(r"(?i)cross_tenant|tenant_boundary_bypass"),
    "sensitive_data_marker": re.compile(r"(?i)sensitive_data|ssn|dob|credit_card"),
    "prompt_injection_marker": re.compile(r"(?i)prompt_injection|ignore_previous_instructions|jailbreak"),
    "poisoning_marker": re.compile(r"(?i)poisoning|data_poisoning|policy_bypass"),
    "dangerous_command_marker": re.compile(r"(?i)\brm\s+-rf\b|\bcurl\s+.+\|\s*sh\b|\bwget\s+.+\|\s*bash\b"),
    "path_traversal_marker": re.compile(r"\.\./|\.\.\\"),
    "unsafe_url_marker": re.compile(r"(?i)https?://[^\s]*(?:token=|api[_-]?key=|password=|secret=)"),
}


def scan_artifact_malware_markers(content: str) -> bool:
    # Placeholder isolated scanner: malware status is tracked externally in metadata.
    return "eicar" not in content.lower()


def scan_artifact_secret_markers(content: str) -> bool:
    return not any(pattern.search(content) for pattern in _SECRET_PATTERNS)


def scan_artifact_policy_markers(content: str) -> tuple[bool, list[str]]:
    flags = [name for name, pattern in _POLICY_PATTERNS.items() if pattern.search(content)]
    return len(flags) == 0, flags


def validate_artifact_size(size_bytes: int, max_size_bytes: int = 10 * 1024 * 1024) -> bool:
    return 0 <= size_bytes <= max_size_bytes


def summarize_scan(flags: list[str]) -> dict[str, str | bool | int]:
    return {
        "scan_safe": len(flags) == 0,
        "flag_count": len(flags),
        "flags_csv": ",".join(sorted(flags)),
    }
