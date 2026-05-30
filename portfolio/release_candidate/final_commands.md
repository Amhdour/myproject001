# Final Release-Candidate Commands

Run all commands from the repository root.

## `python demo_attacks/run_demo_attacks.py`

- **Purpose:** Execute synthetic reviewer-safe demo attack scenarios.
- **Expected PASS:** The runner completes and reports expected synthetic outcomes.
- **What PASS proves:** Demo fixtures and scenario logic are executable locally.
- **What PASS does not prove:** Live production blocking, filtering, enforcement, or full Onyx staging.

## `python scripts/portfolio/check_claim_boundary.py`

- **Purpose:** Check required claim-boundary language and portfolio status markers.
- **Expected PASS:** Required claim-boundary files and phrases are present.
- **What PASS proves:** Claim-boundary documentation exists in expected locations.
- **What PASS does not prove:** Third-party validation or complete absence of risky wording everywhere.

## `python scripts/portfolio/check_no_fake_claims.py`

- **Purpose:** Scan configured portfolio files for unsupported fake-claim wording.
- **Expected PASS:** No configured forbidden fake-claim patterns are found.
- **What PASS proves:** The scripted fake-claim guard did not find known disallowed phrases.
- **What PASS does not prove:** Exhaustive legal, compliance, or marketing review.

## `python scripts/portfolio/check_evidence_links.py`

- **Purpose:** Confirm required reviewer evidence files are present.
- **Expected PASS:** Required evidence and reviewer files exist.
- **What PASS proves:** Core evidence map dependencies are available locally.
- **What PASS does not prove:** The evidence is complete, externally validated, or production sufficient.

## `python scripts/portfolio/check_public_sharing_readiness.py`

- **Purpose:** Confirm public-sharing readiness files and CI references are present.
- **Expected PASS:** Required public-sharing files, claim-boundary files, and CI files exist.
- **What PASS proves:** Public-sharing audit materials are present.
- **What PASS does not prove:** Public sharing is safe without manual sanitization.

## `python scripts/portfolio/check_release_candidate.py`

- **Purpose:** Confirm required release-candidate files and prerequisite portfolio packages are present.
- **Expected PASS:** All required release-candidate and prerequisite files exist.
- **What PASS proves:** The release-candidate package is structurally complete.
- **What PASS does not prove:** Production readiness, enterprise readiness, live staging, or external validation.

## `python -m pytest backend/security_layer/tests -q`

- **Purpose:** Run isolated security-layer helper tests.
- **Expected PASS:** Tests in `backend/security_layer/tests` pass.
- **What PASS proves:** Isolated helper behavior covered by those tests is working in this environment.
- **What PASS does not prove:** End-to-end live application security, live enforcement, compliance certification, or production readiness.
