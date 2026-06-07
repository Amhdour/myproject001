# Retrieval/Context Hook Test Result

| Field | Value |
|---|---|
| Date | 2026-06-07 |
| Command run | `PYTHONPATH=. pytest backend/security_layer/tests/test_retrieved_content_prompt_injection.py backend/security_layer/tests/test_demo_attack_runner.py -q` |
| Exit code | `0` |
| Result | PASS: focused retrieved-content hook tests and synthetic demo-runner tests passed locally. |
| Limitation | The hook-wiring proof checks source-level placement in the real search runner and direct helper execution; it is not a live deployed request-path or staging proof. |
| Safe claim supported | A bounded retrieval/context hook is wired into the real search runner and the helper executes in tests; live enforcement is not claimed. |

## Output

```text
/root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191: PytestConfigWarning: Failed to import filter module 'cryptography': ignore::cryptography.utils.CryptographyDeprecationWarning
  warnings.warn(
..............                                                           [100%]
=============================== warnings summary ===============================
../../root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191: 5 warnings
security_layer/tests/test_retrieved_content_prompt_injection.py: 5 warnings
security_layer/tests/test_demo_attack_runner.py: 9 warnings
  /root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191: PytestConfigWarning: Failed to import filter module 'cryptography': ignore::cryptography.utils.CryptographyDeprecationWarning
    warnings.warn(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== warnings summary (final) ===========================
../../root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191
  /root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191: PytestConfigWarning: Failed to import filter module 'cryptography': ignore::cryptography.utils.CryptographyDeprecationWarning
    warnings.warn(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
14 passed, 20 warnings in 0.09s
```
