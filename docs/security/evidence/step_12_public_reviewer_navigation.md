# Step 12 Public Reviewer Navigation

## Metadata

| Field | Value |
| --- | --- |
| UTC timestamp | 2026-06-04T14:22:00Z |
| Branch name | `step-12-public-reviewer-navigation-v2` |
| Base branch | `step-63x-runtime-retrieval-acl-proof` |
| Starting commit SHA | `592a546d46aadf79abeb06df1c37927f6937c9d5` |

## Objective

Step 12 adds public reviewer navigation from the repository README to the Step 11 reviewer CI proof chain.

This step improves reviewer discoverability only. It does not add runtime behavior, security controls, deployment validation, production readiness, or enterprise readiness.

## Files updated

```text
README.md
```

## Evidence file added

```text
docs/security/evidence/step_12_public_reviewer_navigation.md
```

## Navigation target added

```text
docs/security/evidence/reviewer_ci_proof_chain.md
```

## README changes

The README now includes:

- a `Reviewer CI Proof Chain` section near the top-level reviewer entry points;
- a link to `docs/security/evidence/reviewer_ci_proof_chain.md` in the `How To Review This Project` document list;
- an updated recommended reviewer path that asks reviewers to inspect the CI proof chain.

## Preservation check

This clean Step 12 branch preserves the existing README sections for:

- how to review the project;
- how to run local security-layer tests;
- deployment / staging status;
- safe claims;
- forbidden claims;
- next accelerated steps;
- upstream Onyx references.

## Safe claims

- Step 12 improves public reviewer navigation.
- The repository README now links to the reviewer CI proof chain.
- This is documentation and navigation only.
- Production readiness remains `NO-GO`.
- Enterprise readiness remains `NO-GO`.

## Forbidden claims

- Do not claim production readiness.
- Do not claim enterprise readiness.
- Do not claim live enforcement.
- Do not claim live blocking.
- Do not claim live filtering.
- Do not claim full Onyx staging.
- Do not claim external validation.
- Do not claim compliance certification.

## Acceptance criteria

- README contains a visible `Reviewer CI Proof Chain` section.
- README links to `docs/security/evidence/reviewer_ci_proof_chain.md`.
- README keeps the existing review instructions.
- README keeps safe and forbidden claim sections.
- README keeps production readiness as `NO-GO`.
- README keeps enterprise readiness as `NO-GO`.
- Claim-boundary checks pass.

## Next step

Step 13 should add a release-candidate package navigation update so reviewers can reach the proof chain from `portfolio/release_candidate/README.md` as well as the repository root README.
