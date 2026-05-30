# Manual Screenshot Checklist

Do not add screenshots until captured manually. Do not fabricate screenshots. Do not include secrets, IPs, tokens, emails, private URLs, SSH keys, or credentials.

Each screenshot is optional reviewer-support material. Screenshots can improve review speed, but they do not replace repository evidence, tests, CI runs, or the claim boundary.

## Screenshot Items

### 1. Root README top section

- [ ] Capture manually after verifying the repository state.
- **Purpose:** Show the main project positioning and reviewer entry point.
- **What it proves:** The repository presents itself as a security-readiness portfolio with visible boundaries.
- **What it does NOT prove:** It does not prove production readiness, enterprise readiness, live enforcement, live blocking, live filtering, external validation, or compliance certification.
- **Sanitization warning:** Crop browser/account chrome and remove any private repository URLs, usernames, emails, tokens, or branch protection details.

### 2. Portfolio README

- [ ] Capture manually after verifying the portfolio package links.
- **Purpose:** Show the reviewer-facing portfolio route.
- **What it proves:** The portfolio README exists and gives reviewers a structured path.
- **What it does NOT prove:** It does not prove runtime deployment, live staging, external validation, or certification.
- **Sanitization warning:** Ensure no private account metadata, browser profile details, or private URLs appear.

### 3. Portfolio architecture page

- [ ] Capture manually after opening `portfolio/architecture.md`.
- **Purpose:** Show the architecture explanation reviewers should inspect.
- **What it proves:** The portfolio includes architecture documentation for review.
- **What it does NOT prove:** It does not prove full live Onyx staging, production monitoring, or enterprise operations.
- **Sanitization warning:** Do not include real infrastructure hostnames, private network details, or service credentials.

### 4. Claim boundary page

- [ ] Capture manually after opening the claim-boundary documentation.
- **Purpose:** Show the explicit safe-claim and forbidden-claim boundary.
- **What it proves:** The repository documents what must not be claimed.
- **What it does NOT prove:** It does not remediate NO-GO, PENDING, or NOT CLAIMED items.
- **Sanitization warning:** Confirm the screenshot does not reveal private tabs, tokens, emails, or account names.

### 5. Evidence index

- [ ] Capture manually after opening `portfolio/evidence_index.md`.
- **Purpose:** Show the evidence-room navigation and interpretation rules.
- **What it proves:** Evidence links are organized for reviewer inspection.
- **What it does NOT prove:** It does not prove the linked items are production, enterprise, external-audit, or compliance evidence.
- **Sanitization warning:** Do not expose private repository controls, account menu information, or private URLs.

### 6. GitHub Actions passing security-layer tests

- [ ] Capture manually only from a real passing GitHub Actions run.
- **Purpose:** Show CI execution for the security-layer test gate.
- **What it proves:** The specific CI run shown passed the security-layer tests at that commit.
- **What it does NOT prove:** It does not prove production protection, live blocking, live filtering, or broad runtime integration.
- **Sanitization warning:** Hide private runner names, internal URLs, secrets, environment variables, account emails, and any infrastructure identifiers.

### 7. GitHub Actions passing claim-boundary checks

- [ ] Capture manually only from a real passing GitHub Actions run.
- **Purpose:** Show automated claim-boundary validation.
- **What it proves:** The specific CI run shown found no unsafe positive readiness claims under the scanner's scope.
- **What it does NOT prove:** It does not prove legal review, external validation, compliance certification, or complete absence of every possible unsafe phrase.
- **Sanitization warning:** Hide account details, workflow secrets, private repository URLs, and runner metadata.

### 8. GitHub Actions passing evidence-integrity checks

- [ ] Capture manually only from a real passing GitHub Actions run.
- **Purpose:** Show evidence-link or evidence-presence validation in CI.
- **What it proves:** The specific CI run shown passed the configured evidence-integrity checks.
- **What it does NOT prove:** It does not prove all evidence is production-grade, externally validated, or independently audited.
- **Sanitization warning:** Remove private metadata, tokens, environment values, internal URLs, and account identifiers.

### 9. Demo attack runner terminal output

- [ ] Capture manually after running `python demo_attacks/run_demo_attacks.py`.
- **Purpose:** Show deterministic synthetic demo attack execution.
- **What it proves:** The demo runner produced the expected local synthetic outcomes in that environment.
- **What it does NOT prove:** It does not prove live application blocking, live filtering, live enforcement, production protection, or external validation.
- **Sanitization warning:** Ensure terminal prompt, path, shell history, usernames, and environment variables do not reveal secrets or private infrastructure.

### 10. Pytest terminal output

- [ ] Capture manually after running `python -m pytest backend/security_layer/tests -q`.
- **Purpose:** Show local isolated security-layer test execution.
- **What it proves:** The isolated security-layer tests passed in the captured local environment.
- **What it does NOT prove:** It does not prove end-to-end production behavior, full Onyx live staging, enterprise readiness, or compliance certification.
- **Sanitization warning:** Remove terminal prompts, local usernames, private paths, environment variables, tokens, and private machine details.

### 11. Oracle/Coolify minimal staging evidence only if real evidence exists

- [ ] Capture manually only if real repository-backed evidence exists and is safe to share.
- **Purpose:** Show the narrow minimal staging evidence path when it is actually supported by real artifacts.
- **What it proves:** Only the specific minimal staging fact shown by the real evidence.
- **What it does NOT prove:** It does not prove full Onyx live staging, production readiness, enterprise readiness, production traffic handling, live enforcement, or live filtering.
- **Sanitization warning:** Do not include IP addresses, domains, private URLs, tokens, SSH keys, credentials, cloud account details, or customer data.

### 12. Known limitations / NO-GO page

- [ ] Capture manually after opening the known limitations or release GO/NO-GO page.
- **Purpose:** Show that unresolved limitations and NO-GO boundaries are visible.
- **What it proves:** The portfolio keeps limitations and claim boundaries visible to reviewers.
- **What it does NOT prove:** It does not prove the limitations have been remediated.
- **Sanitization warning:** Remove private browser/account metadata and any infrastructure details that are not already safe public documentation.
