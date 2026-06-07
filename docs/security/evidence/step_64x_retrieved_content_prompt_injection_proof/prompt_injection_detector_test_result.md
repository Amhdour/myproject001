# Prompt-Injection Detector Test Result

| Field | Value |
|---|---|
| Date | 2026-06-07 |
| Command run | `PYTHONPATH=. pytest backend/security_layer/tests/test_retrieved_content_prompt_injection.py -q` |
| Exit code | `0` |
| Result | PASS: focused detector, mode behavior, negative, and real-path source-wiring tests passed locally. |
| Limitation | Local execution used available system pytest; full project dependency sync was not performed in this evidence step. |
| Safe claim supported | Retrieved-content prompt-injection detection is implemented and covered by focused local tests; full prompt-injection defense is not claimed. |

## Output

```text
/root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191: PytestConfigWarning: Failed to import filter module 'cryptography': ignore::cryptography.utils.CryptographyDeprecationWarning
  warnings.warn(
.....                                                                    [100%]
=============================== warnings summary ===============================
../../root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191: 5 warnings
security_layer/tests/test_retrieved_content_prompt_injection.py: 5 warnings
  /root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191: PytestConfigWarning: Failed to import filter module 'cryptography': ignore::cryptography.utils.CryptographyDeprecationWarning
    warnings.warn(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== warnings summary (final) ===========================
../../root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191
  /root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191: PytestConfigWarning: Failed to import filter module 'cryptography': ignore::cryptography.utils.CryptographyDeprecationWarning
    warnings.warn(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
5 passed, 11 warnings in 0.05s
```
