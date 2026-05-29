# Step 37X Planned Backup Commands

## Status

These commands are a planned safe command set for future backup evidence capture. This file documents commands to run; it does not claim that they were executed for this Step 37X repository update.

## Planned Safe Discovery Commands

```bash
sudo du -sh /data/coolify || true
sudo ls -la /data/coolify || true
sudo docker ps
df -h
free -h
```

## Planned Safe Archive Command

The following archive plan intentionally excludes the Coolify `.env` path to avoid recording or packaging secret values in a general evidence artifact:

```bash
sudo tar --exclude='/data/coolify/source/.env' -czf /tmp/coolify-config-backup-step37x.tar.gz /data/coolify
```

## Handling Requirements

- Do not run or document secret values.
- Do not print `/data/coolify/source/.env` contents.
- Do not commit generated backup archives to git.
- Store any generated archive outside the repository.
- Copy any generated archive off the VPS only through an approved secure channel.
- Store Coolify `.env` securely outside the server and outside git, such as in a password manager or secret manager.

## Evidence Required After Future Execution

Future execution evidence should include sanitized outputs for:

- `/data/coolify` size and listing.
- `sudo docker ps` running state.
- `df -h` disk state.
- `free -h` RAM/swap state.
- Archive creation timestamp and checksum, without committing the archive itself.
- Off-server storage location description, without secrets or credentials.
