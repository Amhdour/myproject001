# Step 34X Smoke Tests

## Planned commands

Run these commands on the VPS after setting the Coolify compose path to `deployment/docker_compose/docker-compose.step34x-minimal.yml` and deploying:

```bash
sudo docker ps
curl -I http://localhost:8088
curl -I http://84.8.223.251:8088
```

## Expected result

- `sudo docker ps` should show the `step34x-health` container running.
- `curl -I http://localhost:8088` should return an nginx HTTP response.
- `curl -I http://84.8.223.251:8088` should return an nginx HTTP response if host firewall, cloud firewall, and Coolify deployment routing allow public access.

## Current status

**PENDING** until the user redeploys through Coolify and captures live command output. Codex did not run these VPS smoke tests in this repository update.
