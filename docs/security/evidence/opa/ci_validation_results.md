# OPA CI Validation Results

This page records observed validation evidence for the Retrieval ACL OPA policy validation workflow. It does not claim production readiness and it does not claim that OPA validation proves live RAG runtime enforcement.

## GitHub Actions run previously observed

- Workflow name: `OPA Policy Checks`
- Job name: `Validate Retrieval ACL OPA policy`
- Trigger: pull request
- Branch name: `codex/add-opa-policy-validation-workflow`
- Commit SHA: `1cd5be64d9fd7b01d6b962f470517983fdcaf637`
- Run reference: <https://github.com/Amhdour/myproject001/actions/runs/27087442196>
- Pull request reference: <https://github.com/Amhdour/myproject001/pull/185>
- Observed run time: June 7, 2026 08:31, as displayed by the public GitHub Actions run page
- Observed job duration: 5 seconds
- Result: failed

## New local validation attempt after formatting patch

- Observation date: June 7, 2026
- Branch scope: current working branch for this change
- Local OPA CLI version: not observed because `opa` is not installed in this agent environment
- Local result: not runnable in this environment; this is **not** evidence of pass or fail for the policy
- Environment blocker: `/bin/bash: line 1: opa: command not found`
- Follow-up install attempt: public OPA release downloads were blocked locally with `curl: (56) CONNECT tunnel failed, response 403`

## OPA CLI version expected in CI

The workflow pins `OPA_VERSION` to `v1.17.0` and installs the Linux static OPA binary before validation. The public GitHub Actions page requires sign-in to view full logs, so the prior failed-run evidence records the pinned CLI version from the workflow definition rather than claiming a verbatim `opa version` log line.

## Validation commands

The workflow defines and should run these OPA validation commands:

```bash
opa fmt --check backend/onyx/security_layer/policy/opa/
opa check backend/onyx/security_layer/policy/opa/
opa test backend/onyx/security_layer/policy/opa/
```

Observed execution for the previously referenced failed run:

| Command | Observed status |
| --- | --- |
| `opa fmt --check backend/onyx/security_layer/policy/opa/` | Executed as the `Check Rego formatting` step and failed with exit code 1. |
| `opa check backend/onyx/security_layer/policy/opa/` | Defined in the workflow, but not observed as executed because the preceding formatting step failed. |
| `opa test backend/onyx/security_layer/policy/opa/` | Defined in the workflow, but not observed as executed because the preceding formatting step failed. |

Observed local execution after this patch:

| Command | Observed status |
| --- | --- |
| `opa fmt --check backend/onyx/security_layer/policy/opa/` | Not runnable locally because `opa` is not installed. |
| `opa check backend/onyx/security_layer/policy/opa/` | Not runnable locally because `opa` is not installed. |
| `opa test backend/onyx/security_layer/policy/opa/` | Not runnable locally because `opa` is not installed. |

## Failure reason for the prior CI run

The previously referenced GitHub Actions run failed in the `Check Rego formatting` step. The public run page shows `Process completed with exit code 1` for that step. Full step logs were not available without signing in, so this document does not claim a more specific formatter diff or file-level failure reason.

## Limitations

- CI OPA validation does not prove live RAG runtime enforcement.
- CI OPA validation does not prove production readiness.
- The previous failed run is evidence for the referenced GitHub Actions run only; it is not evidence that future runs pass or fail.
- Because the previous run failed at formatting, that run is not evidence that `opa check` or `opa test` completed successfully.
- The local agent environment could not run OPA validation after the formatting patch because OPA was not installed and public downloads were blocked.
