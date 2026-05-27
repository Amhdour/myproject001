Behavior preservation assertions:
- No enforce mode activation in live path.
- No candidate filtering or request blocking in new hook.
- Return value remains original `guard_result.allowed_chunks` list.
- No prompt/ranking/citation/cache logic changes.
