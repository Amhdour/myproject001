"""Validate Step 43X GitHub sync evidence claim boundaries.

This checker is intentionally narrow: it verifies that the Step 43X evidence
package exists, classifies PR/CI state explicitly, and does not convert blocked
remote evidence into unsupported positive claims.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "docs/security/evidence/step_43x_github_remote_pr_ci_verification_gate"
REQUIRED_FILES = [
    "README.md",
    "remote_check.md",
    "branch_sync.md",
    "pr_verification.md",
    "ci_verification.md",
    "local_verification_results.md",
    "secret_hygiene.md",
    "go_no_go.md",
    "remaining_limitations.md",
    "blockers.md",
]
REQUIRED_PHRASES = [
    "REMOTE_SYNC_BLOCKED",
    "Step 42X branch push status: **BLOCKED_LOCAL_AUTH_OR_REMOTE**",
    "Step 42X PR number and URL: **UNVERIFIED / unavailable**",
    "CI run status: **UNAVAILABLE**",
    "Live staging/cloud validation: **PENDING**",
    "External validation: **PENDING**",
    "Compliance certification: **NOT CLAIMED**",
    "Enterprise production-candidate readiness after Step 43X: **NO-GO / 5%**",
]
UNSUPPORTED_POSITIVE_CLAIMS = [
    "REMOTE_PR_CI_GO",
    "GitHub Actions passed: **YES**",
    "CI passed: **YES**",
    "Remote sync resolved: **YES**",
    "live staging/cloud validation: **VERIFIED**",
    "external validation: **VERIFIED**",
    "compliance certification: **CERTIFIED**",
    "enterprise production-candidate readiness after Step 43X: **GO",
]


def main() -> int:
    missing = [name for name in REQUIRED_FILES if not (EVIDENCE_DIR / name).is_file()]
    if missing:
        print("FAIL: missing Step 43X evidence files:")
        for name in missing:
            print(f"  - {name}")
        return 1

    combined = "\n".join((EVIDENCE_DIR / name).read_text() for name in REQUIRED_FILES)
    missing_phrases = [phrase for phrase in REQUIRED_PHRASES if phrase not in combined]
    if missing_phrases:
        print("FAIL: missing required Step 43X classification phrases:")
        for phrase in missing_phrases:
            print(f"  - {phrase}")
        return 1

    found_unsupported = [phrase for phrase in UNSUPPORTED_POSITIVE_CLAIMS if phrase in combined]
    # The exact classification list may mention alternatives in user task text only; evidence files must not.
    if found_unsupported:
        print("FAIL: unsupported positive Step 43X claim found:")
        for phrase in found_unsupported:
            print(f"  - {phrase}")
        return 1

    print(f"PASS: Step 43X evidence package is complete in {EVIDENCE_DIR.relative_to(ROOT)}")
    print("PASS: PR/CI status is explicitly blocked or unavailable, with claim boundaries preserved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
