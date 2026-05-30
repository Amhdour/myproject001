# Custom Backend Image Strategy

## Strategy

The Oracle staging compose path uses `ONYX_BACKEND_IMAGE` to select the backend image for both `api_server` and `background`.

## Required Consistency

`api_server` and `background` must use the same backend image so runtime enforcement code, migrations, task workers, and shared backend modules stay aligned.

## Oracle Staging Example Tag

```bash
ONYX_BACKEND_IMAGE=rag-agent-security-onyx-backend:step53x-b77bee6
```

This tag is an Oracle staging example from the prior custom image work. It is not claimed as the latest stable production image.

## Verification Boundary

Build and deploy verification must happen on the Oracle VPS before claiming the durable deployment is active. Step 62X only prepares the repeatable configuration and retest plan.
