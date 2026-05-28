from __future__ import annotations

import re

_MALWARE_MARKERS = ("eicar", "x5o!p%@ap")
_SECRET_PATTERNS = (re.compile(r"sk-[A-Za-z0-9]{8,}"), re.compile(r"(?i)api[_-]?key"))
_POLICY_MARKERS = ("prompt_injection", "jailbreak", "policy_bypass")


def scan_artifact_malware_markers(content: str) -> bool:
    lowered = content.lower()
    return not any(marker in lowered for marker in _MALWARE_MARKERS)


def scan_artifact_secret_markers(content: str) -> bool:
    return not any(pattern.search(content) for pattern in _SECRET_PATTERNS)


def scan_artifact_policy_markers(content: str) -> tuple[bool, list[str]]:
    lowered = content.lower()
    flags = [marker for marker in _POLICY_MARKERS if marker in lowered]
    return len(flags) == 0, flags
