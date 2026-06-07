# Employer / Technical Reviewer Readme

## Role target

**AI Trust & Security Readiness Engineer specializing in RAG and Autonomous Agents.**

## What skills this repo demonstrates

This repository is intended to demonstrate:

- threat modeling for RAG and autonomous-agent systems;
- evidence discipline and reviewer-facing packaging;
- policy and control design;
- isolated Python security helpers;
- pytest-based validation;
- CI gates for security-layer and portfolio checks;
- claim-boundary governance;
- demo attack design, including retrieved-content prompt-injection coverage;
- launch-gate thinking;
- deployment limitation honesty.

## What to ask me in an interview

Good interview prompts include:

- Walk through the threat model for prompt injection, retrieval leakage, tool misuse, and MCP confused-deputy risk.
- Explain which controls are isolated helpers versus live runtime behavior.
- Explain why production readiness remains NO-GO.
- Explain how the claim-boundary scripts reduce portfolio overclaiming.
- Show how the retrieved-content prompt-injection detector is tested, how the demo attack runner is structured, and what PASS does not prove.
- Describe what evidence would be required before claiming live enforcement or full staging.
- Explain how you would turn this into a client-ready assessment plan.

## What I should be able to explain live

I should be able to explain:

- the difference between portfolio readiness and production readiness;
- the purpose of the `/portfolio` package;
- the final evidence package contents;
- why synthetic attacks are useful but limited;
- how pytest and CI gates support evidence discipline;
- which claims are safe, forbidden, or pending, including why full prompt-injection defense is not claimed;
- what work remains before stronger deployment claims could be considered.

## What the repo does not prove

This repo does not prove production readiness, enterprise readiness, external validation, compliance certification, full Onyx live staging, live enforce-mode behavior, live blocking, or live filtering. It proves a strong portfolio-style security-readiness approach and evidence discipline.
