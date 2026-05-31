# Case Study: RAG Agent Security Readiness Portfolio

## Overview

This case study describes a production-style AI Trust & Security Readiness portfolio built around an Onyx-based RAG and autonomous-agent system. The work focuses on making runtime-security posture reviewable through evidence, claim boundaries, safe demo flows, and clearly documented limitations.

## Problem

RAG and autonomous-agent systems combine retrieval, prompt construction, model reasoning, tool execution, MCP integrations, generated artifacts, and user-facing responses. Security review is difficult when evidence is scattered or when demos blur the line between controlled proof points and production enforcement.

This portfolio addresses that problem by consolidating public-safe evidence into a reviewer-ready package.

## Approach

The Phase 4 consolidation organizes Step 3 runtime-security evidence into:

- an evidence index;
- a runtime-security evidence report;
- a runtime-security claim-boundary document;
- a case study;
- a demo walkthrough;
- a final go/no-go decision.

The package emphasizes conservative claims, explicit limitations, and a clear path from portfolio evidence to future production validation.

## Security Themes

The portfolio highlights these security themes:

- prompt injection and instruction-conflict risk;
- retrieval access control and tenant-boundary risk;
- sensitive-data exposure risk;
- safe-denial behavior;
- auditability and evidence capture;
- tool authorization and argument-safety risk;
- MCP confused-deputy and server-scope risk;
- staging deployment evidence and route polish;
- external validation readiness.

## Result

The Step 3 runtime-security evidence result is:

`PASS_WITH_LIMITATIONS`

The Phase 4 portfolio consolidation supports:

`~99% production-style portfolio coverage`

This means the portfolio is highly complete as a review artifact. It does not mean enterprise production readiness.

## What the Portfolio Demonstrates

The portfolio demonstrates:

- security-readiness thinking for RAG and agent systems;
- evidence-room organization;
- a clear difference between proof points and production claims;
- a public-safe reporting format;
- conservative reviewer-facing language;
- a remaining-work roadmap.

## What the Portfolio Does Not Demonstrate

The portfolio does not demonstrate:

- enterprise production readiness;
- external validation;
- full authenticated RBAC;
- full real-user tenant isolation;
- full real tool execution blocking;
- full real MCP server blocking;
- backup/restore readiness;
- incident-drill maturity.

## Remaining Work

The next work items are:

- host/reverse-proxy route polish;
- authenticated RBAC tests;
- seeded real-document retrieval tests;
- real configured tool execution tests;
- real MCP server execution tests;
- external validation;
- backup/restore and incident drills.
