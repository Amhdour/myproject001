# Log Summary

## Relevant log evidence

- API before fix: MinIO endpoint connection error for `http://minio:9000/onyx-file-store-bucket`.
- Web: Next.js ready log was observed.
- API after fix: `api_server` became healthy after MinIO was added, the bucket was created, and services were restarted.

## Redaction boundary

- No secrets are included in this summary.
- Raw environment output contained default credentials and must be redacted before any public evidence publication.
- Do not publish raw environment dumps.
