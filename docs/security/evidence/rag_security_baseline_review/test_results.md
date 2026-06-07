# Test Results

## Purpose
Record exact test/check commands, outcomes, warnings, and environment limitations for the RAG Security Baseline Review.

## Commands or search methods used
Exact commands are listed below as individual sections.

## Files found
Relevant test files are inventoried in `test_inventory.md` and `demo_attack_inventory.md`.

## Relevant code paths found
The executed tests exercise isolated retrieval ACL runtime behavior, retrieval negative cases, selected security demo attacks, and security evidence validation.

## Findings
System-Python pytest runs passed for selected isolated retrieval/security tests. Initial venv pytest attempts failed because pytest was missing in `.venv`. Attempts to use `/usr/local/bin/python` failed because that path did not exist.

## Gaps
Full integration, external-dependency, Playwright, live service, CI, staging, and production tests were not executed.

## Claim boundary
Only the exact local command outcomes listed below may be claimed. Passing isolated tests do not prove production readiness.

## python -m pytest backend/security_layer/tests/test_retrieval_acl_runtime.py -q

/workspace/myproject001/.venv/bin/python: No module named pytest
exit_code=1

## python -m pytest backend/security_layer/tests/test_retrieval_security_negative_cases.py -q

/workspace/myproject001/.venv/bin/python: No module named pytest
exit_code=1

## python -m pytest --confcutdir=backend/tests/security backend/tests/security/demo_attacks/test_cross_tenant_retrieval_attack.py -q

/workspace/myproject001/.venv/bin/python: No module named pytest
exit_code=1

## python -m pytest --confcutdir=backend/tests/security backend/tests/security/demo_attacks/test_prompt_injection_retrieval_attack.py -q

/workspace/myproject001/.venv/bin/python: No module named pytest
exit_code=1

## python scripts/security/validate_security_evidence.py

Security evidence validation passed for 12 required paths.
exit_code=0

Note: the initial four pytest invocations were run after `source .venv/bin/activate`; `.venv/bin/python` reported `No module named pytest`. The evidence validation command passed.

## /usr/local/bin/python -m pytest backend/security_layer/tests/test_retrieval_acl_runtime.py -q

environment: line 6: /usr/local/bin/python: No such file or directory
exit_code=127

## /usr/local/bin/python -m pytest backend/security_layer/tests/test_retrieval_security_negative_cases.py -q

environment: line 6: /usr/local/bin/python: No such file or directory
exit_code=127

## /usr/local/bin/python -m pytest --confcutdir=backend/tests/security backend/tests/security/demo_attacks/test_cross_tenant_retrieval_attack.py -q

environment: line 6: /usr/local/bin/python: No such file or directory
exit_code=127

## /usr/local/bin/python -m pytest --confcutdir=backend/tests/security backend/tests/security/demo_attacks/test_prompt_injection_retrieval_attack.py -q

environment: line 6: /usr/local/bin/python: No such file or directory
exit_code=127

## /usr/local/bin/python scripts/security/validate_security_evidence.py

environment: line 6: /usr/local/bin/python: No such file or directory
exit_code=127

## python -m pytest backend/security_layer/tests/test_retrieval_acl_runtime.py -q

/root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191: PytestConfigWarning: Failed to import filter module 'cryptography': ignore::cryptography.utils.CryptographyDeprecationWarning
  warnings.warn(
.......                                                                  [100%]
=============================== warnings summary ===============================
../../root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191: 5 warnings
security_layer/tests/test_retrieval_acl_runtime.py: 7 warnings
  /root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191: PytestConfigWarning: Failed to import filter module 'cryptography': ignore::cryptography.utils.CryptographyDeprecationWarning
    warnings.warn(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== warnings summary (final) ===========================
../../root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191
  /root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191: PytestConfigWarning: Failed to import filter module 'cryptography': ignore::cryptography.utils.CryptographyDeprecationWarning
    warnings.warn(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
7 passed, 13 warnings in 0.09s
exit_code=0

## python -m pytest backend/security_layer/tests/test_retrieval_security_negative_cases.py -q

/root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191: PytestConfigWarning: Failed to import filter module 'cryptography': ignore::cryptography.utils.CryptographyDeprecationWarning
  warnings.warn(
.............                                                            [100%]
=============================== warnings summary ===============================
../../root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191: 5 warnings
security_layer/tests/test_retrieval_security_negative_cases.py: 13 warnings
  /root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191: PytestConfigWarning: Failed to import filter module 'cryptography': ignore::cryptography.utils.CryptographyDeprecationWarning
    warnings.warn(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== warnings summary (final) ===========================
../../root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191
  /root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191: PytestConfigWarning: Failed to import filter module 'cryptography': ignore::cryptography.utils.CryptographyDeprecationWarning
    warnings.warn(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
13 passed, 19 warnings in 0.18s
exit_code=0

## python -m pytest --confcutdir=backend/tests/security backend/tests/security/demo_attacks/test_cross_tenant_retrieval_attack.py -q

/root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191: PytestConfigWarning: Failed to import filter module 'cryptography': ignore::cryptography.utils.CryptographyDeprecationWarning
  warnings.warn(
.                                                                        [100%]
=============================== warnings summary ===============================
../../root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191
../../root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191
../../root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191
../../root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191
tests/security/demo_attacks/test_cross_tenant_retrieval_attack.py::test_cross_tenant_retrieval_attack_blocked
../../root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191
  /root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191: PytestConfigWarning: Failed to import filter module 'cryptography': ignore::cryptography.utils.CryptographyDeprecationWarning
    warnings.warn(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== warnings summary (final) ===========================
../../root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191
  /root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191: PytestConfigWarning: Failed to import filter module 'cryptography': ignore::cryptography.utils.CryptographyDeprecationWarning
    warnings.warn(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
1 passed, 7 warnings in 0.02s
exit_code=0

## python -m pytest --confcutdir=backend/tests/security backend/tests/security/demo_attacks/test_prompt_injection_retrieval_attack.py -q

/root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191: PytestConfigWarning: Failed to import filter module 'cryptography': ignore::cryptography.utils.CryptographyDeprecationWarning
  warnings.warn(
.                                                                        [100%]
=============================== warnings summary ===============================
../../root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191
../../root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191
../../root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191
../../root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191
tests/security/demo_attacks/test_prompt_injection_retrieval_attack.py::test_prompt_injection_in_retrieved_content_not_scanned_limitation_recorded
../../root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191
  /root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191: PytestConfigWarning: Failed to import filter module 'cryptography': ignore::cryptography.utils.CryptographyDeprecationWarning
    warnings.warn(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== warnings summary (final) ===========================
../../root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191
  /root/.pyenv/versions/3.14.4/lib/python3.14/site-packages/_pytest/config/__init__.py:2191: PytestConfigWarning: Failed to import filter module 'cryptography': ignore::cryptography.utils.CryptographyDeprecationWarning
    warnings.warn(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
1 passed, 7 warnings in 0.02s
exit_code=0

## python scripts/security/validate_security_evidence.py

Security evidence validation passed for 12 required paths.
exit_code=0

## python scripts/security/validate_security_evidence.py

Security evidence validation passed for 12 required paths.
exit_code=0
