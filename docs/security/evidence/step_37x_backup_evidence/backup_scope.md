# Step 37X Backup Scope

## Backup Targets

The backup scope for the minimal Oracle VPS + Coolify staging environment includes the following targets.

### Coolify Persistent Data

- Path: `/data/coolify/`
- Purpose: persistent Coolify data and deployment state for the minimal staging environment.
- Status: target identified for future backup evidence capture.

### Coolify Environment File Path Reference

- Path reference only: `/data/coolify/source/.env`
- Values are not recorded in this repository.
- The file may contain secrets and must never be committed to git.
- Any backup copy of this file must be stored securely outside the repository, such as in a password manager or secret manager.

### Coolify Application Configuration

- Coolify application configuration for `step34x-health` should be captured as sanitized evidence.
- Environment variable names may be recorded if needed.
- Environment variable values must not be recorded in this repository.

### Docker Compose Deployment Config in Git

- Deployment configuration stored in git is part of the recoverable configuration set.
- The known minimal app uses `nginx:alpine` and binding `0.0.0.0:8088->80/tcp`.
- Git-tracked deployment files are backup inputs, but generated archives must not be committed.

### Evidence Files in Git

- Existing Step 34X, Step 35X, Step 36X, and Step 37X evidence files are part of the audit trail.
- Evidence files should contain only sanitized facts and command outputs.
- Evidence files must not include secrets, tokens, private keys, or Coolify `.env` values.

### Oracle Boot Volume Backup

- Oracle boot volume backup is in scope as a manual Oracle Cloud Console action.
- Required proof must be sanitized before it is recorded in git.
- Boot volume OCIDs must be redacted or partially redacted.

### SSH Key Backup Outside Repo

- SSH private keys are backup targets only outside the repository.
- SSH private keys must never be committed to git.
- Secure storage should use a password manager, secret manager, or other approved secure storage path.

### DNS/Domain Configuration

- DNS/domain configuration is in scope if a domain is added later.
- Current Step 37X scope does not validate external DNS/domain recovery.
- Future evidence should document provider, domain, records, timestamps, and sanitized screenshots or exports without secrets.

### Secret Manager or Password Manager Storage

- Secrets required for recovery must be stored outside the server and outside git.
- Acceptable examples include a password manager or secret manager.
- Repository evidence may document secret names, secret purpose, and recovery owner, but not secret values.
