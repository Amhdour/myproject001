# Gateway Governance Demo Attack Results

## External secret route block

The demo attempts to route a request containing a secret to an external model provider.

Expected result summary:

- `decision`: `deny`
- `route_target`: `blocked`
- raw prompt and secret values: absent from evidence

## Restricted tenant external route

The demo attempts to route restricted tenant data to an external model provider with restricted external mode set to `route_private`.

Expected result summary:

- `decision`: `route_private`
- `route_target`: `private`
- raw retrieved context: absent from evidence
