# Coolify Staging Smoke Test Plan

## Purpose
Validate a real Coolify staging deployment after it is deployed by an approved
operator. This plan is not executed by this repository change.

## Test Cases
1. Confirm the staging application loads through the frontend route.
2. Confirm unauthenticated access follows expected staging authentication flow.
3. Confirm a test login uses approved staging-only credentials stored outside the
   repository.
4. Confirm a basic health or landing page request succeeds.
5. Confirm security-layer evidence helpers remain isolated and do not alter live
   request handling.
6. Confirm enforce mode is disabled.
7. Confirm shadow-deny runtime mode is disabled.
8. Confirm no live blocking or live filtering is active.
9. Confirm logs contain no secrets and no raw sensitive prompt/document content.
10. Confirm rollback instructions are available before any staging change window.

## Evidence to Capture
- Sanitized execution timestamp and operator initials.
- Sanitized staging app identifier.
- Smoke test command summaries and pass/fail status.
- Confirmation that no production traffic was routed.

## Current Status
Pending. No real Coolify deployment was executed in this change.
