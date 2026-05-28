Validated models.py in isolated scope:
- No raw credential/secret/tool-config secret fields.
- No raw prompt/document/chunk text fields.
- Explicit tool identity/version/category/risk tier fields.
- Explicit caller/tenant/workspace/subject/group/role fields.
- Explicit delegated credential scope, approval requirement, argument schema id,
  result safety policy id, and metadata schema version.
