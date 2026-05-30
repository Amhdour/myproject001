# Sanitization Checklist

Use this checklist before publishing the repository, screenshots, logs, terminal recordings, videos, release notes, or reviewer packets.

## Secret Scan Checklist

- [ ] Run repository secret scanning with the available project-approved tool before public sharing.
- [ ] Confirm no API keys, tokens, passwords, private keys, SSH keys, cookies, session IDs, or OAuth credentials are committed.
- [ ] Confirm `.env` files and local credential files are not included.
- [ ] Confirm example values are clearly fake placeholders.
- [ ] Confirm no real customer identifiers or private organization names are present.

## Screenshot Sanitization Checklist

- [ ] Capture screenshots manually; do not fabricate screenshots.
- [ ] Remove browser profile names, account emails, avatars, tabs, bookmarks, and private URLs.
- [ ] Redact private repository URLs if the repository is not already public.
- [ ] Redact terminal prompts that reveal usernames, hostnames, local paths, or infrastructure names.
- [ ] Redact IP addresses, domains, tokens, API keys, SSH key material, and cloud resource identifiers.
- [ ] Confirm screenshots do not imply live enforcement, live blocking, live filtering, production readiness, enterprise readiness, external validation, or certification.

## Deployment Evidence Sanitization Checklist

- [ ] Include deployment evidence only if it is real, manually captured, and repository-supported.
- [ ] Remove public IPs, private IPs, hostnames, dashboard URLs, provider account IDs, project IDs, SSH key references, and credentials.
- [ ] Avoid exposing infrastructure topology beyond what is already safe public documentation.
- [ ] Label minimal staging evidence as scoped evidence only.
- [ ] Do not present minimal staging evidence as proof of full Onyx live staging, production readiness, enterprise readiness, live enforcement, live blocking, or live filtering.

## Log Sanitization Checklist

- [ ] Remove secrets, tokens, cookies, authorization headers, credentials, keys, and signed URLs.
- [ ] Remove real emails, user IDs, customer data, organization names, and private document contents.
- [ ] Remove private IPs, public IPs, hostnames, domains, container registry paths, and internal service URLs unless already safe public examples.
- [ ] Preserve only enough log context to support the evidence claim.
- [ ] Mark sanitized logs as sanitized excerpts when excerpts are used.

## Public Sharing Checklist

- [ ] Confirm claim boundary pages are linked from the root README and portfolio README.
- [ ] Confirm NO-GO / PENDING / NOT CLAIMED language remains visible.
- [ ] Confirm optional screenshots and videos, if present, are sanitized.
- [ ] Confirm release notes do not add unsupported claims.
- [ ] Confirm no fake deployment evidence or fabricated review evidence has been added.
- [ ] Confirm reviewer instructions tell reviewers to run local commands and inspect real CI results.
