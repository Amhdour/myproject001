# OPA Retrieval ACL Reproduction Commands

Run from the repository root. These commands validate only the Retrieval ACL OPA policy and its Rego tests; they do not claim production readiness or full runtime enforcement.

## Install OPA CLI locally

Install the OPA CLI before running Rego validation commands. The CI workflow pins OPA to `v1.17.0`; use the same version locally when reproducing CI behavior.

### Linux x86_64

```bash
curl -L -o opa https://openpolicyagent.org/downloads/v1.17.0/opa_linux_amd64_static
chmod +x opa
sudo mv opa /usr/local/bin/opa
opa version
```

### macOS Apple Silicon

```bash
curl -L -o opa https://openpolicyagent.org/downloads/v1.17.0/opa_darwin_arm64_static
chmod +x opa
sudo mv opa /usr/local/bin/opa
opa version
```

### macOS Intel

```bash
curl -L -o opa https://openpolicyagent.org/downloads/v1.17.0/opa_darwin_amd64_static
chmod +x opa
sudo mv opa /usr/local/bin/opa
opa version
```

If these downloads are blocked by a local network policy, install the same OPA version through an approved internal mirror or package-management path and then confirm `opa version` before running validation.

## Expected OPA validation commands

```bash
opa fmt --check backend/onyx/security_layer/policy/opa/
opa check backend/onyx/security_layer/policy/opa/
opa test backend/onyx/security_layer/policy/opa/
```

The GitHub Actions workflow `.github/workflows/opa-policy-checks.yml` runs the same three validation commands after installing the pinned OPA CLI.

## Adjacent local checks

These Python checks are adjacent evidence commands only. They are not substitutes for the OPA CLI commands above.

```bash
pytest backend/onyx/security_layer -q
python scripts/security/demo_attacks/opa/retrieval_acl_policy_bypass_demo.py
```

If Python dependencies are missing, retry Python commands with the project virtual environment activated:

```bash
source .venv/bin/activate
pytest backend/onyx/security_layer -q
```
