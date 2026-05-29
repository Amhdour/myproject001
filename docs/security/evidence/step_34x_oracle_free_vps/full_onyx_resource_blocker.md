# Step 34X Full Onyx Resource Blocker

## Attempt summary

Full Onyx deployment was attempted through Coolify on the Oracle Free Tier VPS.

| Field | Value |
|---|---|
| Coolify project | `rag-agent-security-minimal-staging` |
| Resource | `myproject001:main-lu8fgylyjp4so3adpxep8ixb` |
| Commit imported | `a4012826cf06a2ecb859b932a9a14d2b7c44bbf1` |
| Deployment status | **FAILED** |
| Failure classification | **RESOURCE-BLOCKED** |

## Heavy services pulled

The failed deployment still pulled the full Onyx stack instead of a minimal demo. Heavy services observed during the failed attempt included:

- `indexing_model_server`
- `inference_model_server`
- `nginx`
- `code-interpreter`
- `relational_db`
- `api_server`
- `web_server`
- `opensearch`
- `background`
- `cache`

## Large image layers observed

Large image layers observed during the failed deployment included approximately:

- 775 MB
- 867 MB
- 506 MB
- 226 MB

## Decision

Full Onyx live staging is **RESOURCE-BLOCKED** on an Oracle Free Tier 1 OCPU / 6 GB RAM class VPS.

## Required next production path

Use a bigger VPS or Kubernetes/staging cluster before claiming full stack readiness.

## Explicit non-claims

- Do not claim production readiness from this failed full-stack attempt.
- Do not claim enterprise readiness from this failed full-stack attempt.
- Do not claim external validation from this failed full-stack attempt.
- Do not claim compliance certification from this failed full-stack attempt.
