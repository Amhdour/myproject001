# Bundle D Tool Authorization Runtime Proof

## Metadata

| Field | Value |
| --- | --- |
| UTC timestamp | 2026-06-04T17:32:00Z |
| Branch name | `bundle-d-tool-authorization-runtime-proof` |
| Base branch | `main` |
| Starting commit SHA | `a8c072a08bb81708afe8f591b5a6f3d91e60f13c` |

## Objective

Bundle D adds an isolated tool authorization runtime helper, denial tests, audit evidence, and focused CI gate for agent/tool-call authorization decisions.

This bundle remains isolated. It does not wire into live Onyx agent/tool runtime paths.

## Accelerated scope

Bundle D combines:

- Step 33 — Tool authorization runtime helper;
- Step 34 — Tool authorization denial tests;
- Step 35 — Tool authorization CI gate.

## Files added

```text
backend/security_layer/tool_authorization/models.py
backend/security_layer/tool_authorization/enforcer.py
backend/security_layer/tool_authorization/audit.py
backend/security_layer/tests/test_tool_authorization_runtime.py
.github/workflows/tool-authorization-runtime-tests.yml
docs/security/evidence/bundle_d_tool_authorization_runtime_proof.md
```

## Runtime helper behavior

The isolated tool authorization helper:

- authorizes known tools by tenant, subject, role, action, and optional approval requirement;
- denies missing requester context;
- denies malformed requester context;
- denies unknown tools;
- denies cross-tenant tool calls;
- denies unauthorized subjects/roles;
- denies disallowed actions;
- denies approval-required tool calls without matching approval evidence;
- emits reviewer-safe audit events for denied tool calls.

## Test command

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_tool_authorization_runtime.py -q
```

## Focused tests

The Bundle D tests cover:

- allowed tool call passes;
- unknown tool is denied and audited;
- cross-tenant tool call is denied;
- disallowed action is denied;
- required approval is denied when missing;
- required approval is allowed when present;
- missing context is denied;
- malformed context is denied.

## CI artifact

Workflow:

```text
.github/workflows/tool-authorization-runtime-tests.yml
```

Artifact name:

```text
tool-authorization-runtime-test-evidence
```

Artifact contents:

```text
tool-authorization-runtime-artifacts/environment_metadata.txt
tool-authorization-runtime-artifacts/test.log
```

## Safe classification after CI passes

```text
TOOL_AUTHORIZATION_RUNTIME_HELPER_PROVEN_BY_CI
```

## What this proves

This proves an isolated runtime authorization shape for agent/tool calls before execution.

It proves deny-by-default behavior for malformed, missing, cross-tenant, unauthorized, disallowed-action, and missing-approval cases.

## What this does not prove

This does **not** prove:

- live Onyx agent/tool runtime enforcement;
- production tool-call security;
- enterprise readiness;
- live blocking;
- live filtering;
- full agent authorization;
- full MCP authorization;
- full backend test success;
- staging validation;
- external validation;
- compliance certification.

## Safe claims

- Bundle D provides isolated tool authorization runtime proof.
- Tool calls can be allowed or denied based on tenant, subject, role, action, and approval status.
- Denied tool calls produce reviewer-safe audit evidence.
- Production readiness remains `NO-GO`.
- Enterprise readiness remains `NO-GO`.

## Forbidden claims

- Do not claim live Onyx agent/tool runtime enforcement.
- Do not claim production tool-call security.
- Do not claim enterprise readiness.
- Do not claim live blocking.
- Do not claim live filtering.
- Do not claim full agent authorization.
- Do not claim full MCP authorization.

## Recommended next bundle

Bundle E should add a human approval workflow helper and CI evidence gate for approve/deny decisions around high-risk agent actions.
