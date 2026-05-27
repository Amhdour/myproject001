from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SecurityFinding:
    action: str
    reason_code: str
    request_id: str


_FINDINGS: list[SecurityFinding] = []


def record_finding(finding: SecurityFinding) -> None:
    _FINDINGS.append(finding)


def get_findings() -> list[SecurityFinding]:
    return list(_FINDINGS)


def clear_findings() -> None:
    _FINDINGS.clear()
