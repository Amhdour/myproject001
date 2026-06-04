# Step 10 Demo Attack Execution Gate

## Metadata

| Field | Value |
| --- | --- |
| UTC timestamp | 2026-06-04T14:05:00Z |
| Branch name | `step-10-demo-attack-execution-gate` |
| Base branch | `step-63x-runtime-retrieval-acl-proof` |
| Starting commit SHA | `e5b860b9fc0a233bd75cd1785311ba3ca942aa89` |

## Objective

Step 10 adds a CI-backed reviewer-safe demo attack execution gate using the existing deterministic demo attack runner.

This step does not add new security controls. It proves that the synthetic demo attack runner executes in CI and produces artifact evidence.

## Existing runner used

```text
demo_attacks/run_demo_attacks.py
```

## Runner scope

The runner is deterministic and synthetic-data-only. It uses only Python standard library behavior and does not call networks, tools, MCP servers, secret stores, or live application runtime paths.

## Demo attack scenarios covered by the existing runner

- prompt injection;
- retrieval cross-tenant leakage;
- unsafe tool call;
- MCP confused-deputy risk;
- sensitive data exposure.

## Workflow added

```text
.github/workflows/demo-attack-runner.yml
```

## Command executed

```bash
python demo_attacks/run_demo_attacks.py
```

## Artifact paths

Demo attack runner log:

```text
.artifacts/demo-attack-runner/demo-attack-runner.log
```

Environment metadata:

```text
.artifacts/demo-attack-runner/environment.txt
```

Uploaded artifact name:

```text
demo-attack-runner-evidence
```

## Expected CI classifications

If the workflow passes and uploads the artifact:

```text
DEMO_ATTACK_RUNNER_PROVEN_BY_CI
```

If the workflow reaches the runner and fails:

```text
DEMO_ATTACK_RUNNER_FAILED_IN_CI
```

If the workflow fails before the runner executes:

```text
DEMO_ATTACK_WORKFLOW_SETUP_FAILED
```

## Safe claims

- Step 10 adds a CI-backed synthetic demo attack execution gate.
- The demo runner executes deterministic synthetic cases only.
- Passing this workflow proves the demo runner executed and classified the synthetic cases as expected.
- Production readiness remains `NO-GO`.
- Enterprise readiness remains `NO-GO`.

## Forbidden claims

- Do not claim production protection.
- Do not claim live blocking.
- Do not claim live filtering.
- Do not claim live enforcement.
- Do not claim full Onyx request-path protection.
- Do not claim external validation.
- Do not claim compliance certification.
- Do not claim enterprise readiness.

## Acceptance criteria

- `Demo Attack Runner` workflow runs in GitHub Actions.
- `python demo_attacks/run_demo_attacks.py` executes.
- Artifact `demo-attack-runner-evidence` is uploaded.
- The artifact includes `demo-attack-runner.log` and `environment.txt`.
- Claim boundaries remain visible.

## Next step

After Step 10 passes, proceed to Step 11: add a claim-boundary/evidence index update that links the Step 07, Step 08, Step 09, and Step 10 CI artifacts into a reviewer-readable proof chain.
