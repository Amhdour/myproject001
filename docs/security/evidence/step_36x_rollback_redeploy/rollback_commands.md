# Step 36X Planned Rollback/Redeploy Commands

These commands are planned for operator execution on the VPS. They are not evidence of execution unless paired with captured command output and Coolify logs/screenshots.

## Before rollback

```bash
sudo docker ps
curl -I http://localhost:8088
```

## After stopping resource

```bash
sudo docker ps -a | grep step34x-health || true
```

## After redeploy

```bash
sudo docker ps
curl -I http://localhost:8088
```

## Optional public check

```bash
curl -I http://84.8.223.251:8088
```
