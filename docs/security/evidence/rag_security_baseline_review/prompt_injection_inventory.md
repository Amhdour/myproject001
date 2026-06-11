# Prompt Injection Inventory

## Purpose
Inventory prompt-injection evidence and limitations for retrieved-content RAG.

## Commands or search methods used
- `rg -n -i "prompt injection|injection|malicious" backend docs demo_attacks`
- Direct inspection of search-tool context construction and prompt-injection demo attack tests.

## Files found
- `backend/tests/security/demo_attacks/test_prompt_injection_retrieval_attack.py`
- `backend/onyx/security_layer/demo_attacks/prompt_injection_tool_call.md`
- `backend/onyx/tools/tool_implementations/utils.py`
- `backend/onyx/tools/tool_implementations/search/search_tool.py`
- `backend/onyx/chat/llm_step.py`

## Relevant code paths found
- `convert_inference_sections_to_llm_string` serializes retrieved sections as JSON `results` with title, source fields, optional URL/document ID/file name, content, and metadata.
- `SearchTool.run` passes that string to the LLM as the tool-facing response.
- The prompt-injection demo attack test explicitly records a limitation: retrieved prompt-injection text is allowed by the security enforcer in that test scenario.

## Findings
- Retrieved document content can flow into the LLM-facing context string.
- A test exists that documents prompt-injection-in-retrieved-content as a limitation rather than a proven blocked condition.

## Gaps
- No repository evidence was found proving comprehensive document-level prompt-injection scanning, context sanitization, instruction-hierarchy enforcement, or output validation for retrieved content.
- Tool-call prompt injection artifacts exist, but that does not prove RAG retrieved-content prompt-injection defense.

## Claim boundary
The safe claim is that prompt-injection risk was identified and a limitation test exists. Full prompt-injection protection must not be claimed.
