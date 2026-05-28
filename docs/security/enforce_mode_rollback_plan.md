# Enforce-Mode Rollback Plan

## Rollback triggers
Rollback triggers include deny-rate breach, false-positive breach, error-rate breach, latency breach, leakage, missing telemetry, incident response request, owner request, compliance request, or any unapproved behavior.

## Rollback owner
Security engineering owner coordinates rollback with service owners and incident response.

## Rollback decision record
Record trigger, time, owner, affected simulated control family, evidence links, and validation outcome.

## Kill-switch behavior
The emergency kill switch must force no blocking/no filtering and leave live behavior unchanged.

## Feature-flag disable behavior
Global and family flags must disable any future blocking path and return the system to no-op behavior.

## Telemetry preservation
Telemetry, audit events, findings, metrics, test output, and decision records must be preserved during and after rollback.

## User-impact review
Review valid user requests, false positives, denial text, affected cohorts, and support impact.

## Incident-response handoff
Escalate if leakage, broad impact, or user-visible disruption is suspected.

## Post-rollback validation
Confirm flags disabled, kill switch applied, no live blocking, no live filtering, evidence retained, and tests passing.

## Known limitations
Rollback is planned for future enforce mode and is not connected to live enforcement in this bundle.
