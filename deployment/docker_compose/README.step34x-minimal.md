# Step 34X Minimal Coolify Staging Target

## Purpose

This compose target provides minimal live staging validation for Step 34X.

## Why minimal

Oracle Free Tier failed the full Onyx deployment due to resource pressure. The prior Coolify attempt pulled the full stack and large image layers, so this file intentionally uses a single lightweight public image instead of any Onyx application services.

## Coolify compose path

Set the Coolify compose path to:

```text
deployment/docker_compose/docker-compose.step34x-minimal.yml
```

## Expected public URL

```text
http://84.8.223.251:8088
```

## Smoke test

```bash
curl -I http://localhost:8088
curl -I http://84.8.223.251:8088
```

## Non-claims

- This does not prove full Onyx production readiness.
- This does not prove enterprise readiness.
- This does not prove compliance certification.
