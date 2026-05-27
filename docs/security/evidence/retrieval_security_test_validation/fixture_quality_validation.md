# Step 18C Fixture Quality Validation

- Fixtures are synthetic-only (`fake_`, `synthetic_`, `.invalid` email domains).
- Cross-tenant fixtures are explicitly marked (`synthetic_cross_tenant: true`).
- Denied fixtures are explicitly marked (`unauthorized: true`).
- Deterministic fixture IDs validated across repeated construction.
