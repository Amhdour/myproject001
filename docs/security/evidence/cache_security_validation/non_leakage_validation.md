# Non-leakage validation
- Key contract tests reject raw text/secret patterns.
- Decision reason checks verify no raw query/prompt/document/chunk leak through decision reason text.
- Isolated-scope tests only; no production payload paths modified.
