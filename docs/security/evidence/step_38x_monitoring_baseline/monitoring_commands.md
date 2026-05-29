# Step 38X Monitoring Commands

## Planned Commands

Run these commands on the Oracle VPS hosting the Coolify minimal staging environment and capture sanitized output.

```bash
uptime
```

```bash
free -h
```

```bash
df -h
```

```bash
sudo docker ps
```

```bash
sudo docker stats --no-stream
```

```bash
curl -I http://localhost:8088
```

```bash
sudo docker logs --tail=100 $(sudo docker ps --filter "name=step34x-health" -q)
```

## Optional Public Endpoint Check

Run this only if the public endpoint is reachable from the operator's network and the Oracle firewall/security list permits the traffic.

```bash
curl -I http://84.8.223.251:8088
```

## Capture Notes

- Remove secrets, tokens, private keys, session cookies, and unrelated environment values before committing evidence.
- Preserve timestamps where possible.
- Do not convert failed or partial command output into a readiness claim.
