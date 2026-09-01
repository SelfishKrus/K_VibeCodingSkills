---
name: skip-approval-gate
description: Skip the custom AGENTS.md y/n execution approval gate for the current user request when explicitly invoked as $skip-approval-gate. Do not treat it as authorization for broader, destructive, privileged, or externally visible actions.
---

# Skip Approval Gate

Treat the user's explicit invocation as task-scoped authorization to skip only the custom `Execution Approval Gate` y/n pause for the request containing the invocation.

- Provide the usual concise pre-execution summary as a non-blocking update, then begin the requested in-scope work without asking for or waiting on `y` or `n`.
- Apply the bypass only to the current user request. A later user request requires a fresh explicit invocation.
- Do not broaden the requested scope or infer permission for additional actions.
- Do not bypass mandatory sandbox or tool approvals, safety checks, secrets or permission boundaries, or separate confirmation required for destructive, irreversible, privileged, or externally visible actions.
- If the scope changes materially, obtain the authorization required by the ordinary rules before proceeding.
- Continue following every other applicable `AGENTS.md` instruction, including validation, changed-files reporting, and local Git commit requirements.
