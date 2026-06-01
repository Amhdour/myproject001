# Validation Decision Rules

## Purpose

These rules define how to classify future reviewer feedback without overstating it.

## Classification options

### `SAMPLE_ONLY_NOT_EXTERNALLY_VALIDATED`

Use when the package contains only templates, example responses, or AI-generated drafts.

External validation remains `PENDING / NOT CLAIMED`.

### `REVIEW_REQUEST_SENT`

Use when a real request has been sent to a reviewer but no response has been received.

External validation remains `PENDING`.

### `REVIEW_RESPONSE_RECEIVED_PRIVATE`

Use when a real reviewer responded but did not grant permission to publish details.

Record only metadata allowed by the reviewer.

### `REVIEW_RESPONSE_RECEIVED_ANONYMIZED`

Use when a real reviewer responded and allowed anonymized recording.

Do not include identifying details.

### `REVIEW_RESPONSE_RECEIVED_PUBLIC`

Use when a real reviewer responded and explicitly allowed their feedback to be recorded publicly.

### `EXTERNAL_PORTFOLIO_REVIEW_COMPLETE`

Use only when:

1. a real reviewer identity or anonymized identity is recorded according to permission;
2. review date is recorded;
3. scope reviewed is recorded;
4. reviewer findings are recorded;
5. limitations are recorded;
6. follow-up actions are recorded.

## Disallowed classifications

Do not use:

- production approved;
- enterprise approved;
- certified;
- audited;
- red-team completed;
- compliance validated;
- customer-ready;
- externally validated by example response.

## Claim boundary

External reviewer feedback can improve portfolio credibility. It does not automatically prove production readiness, enterprise readiness, compliance certification, full-system security, or customer deployment readiness.
