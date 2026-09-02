# Global working agreements

## Execution approval

- Read-only inspection, explanation, diagnosis, research, and status reporting do not require the custom approval gate.
- Before modifying code or project files, or performing a state-changing MCP or external action, give a concise in-chat summary of the approach and material side effects. Do not create a separate planning artifact for this step.
- Unless the current request explicitly includes `$skip-approval-gate`, end that summary by asking for exactly `y` to proceed or `n` to stop, then wait. Only `y` approves; after any other response, do not modify state and ask again.
- `$skip-approval-gate` bypasses only this custom pause for the current request. Still provide the summary, and do not treat the bypass as broader scope or as an override of safety, sandbox, permission, secret, destructive-action, or external-visibility checks.
- After approval, implement directly. Request another `y` or `n` only for a material scope change or a separately confirmable destructive, irreversible, privileged, or externally visible action.

## Implementation

- Make the smallest safe, localized change that fully satisfies the request. Preserve existing behavior, architecture, public APIs, data formats, workflows, and visual design unless the request requires otherwise.
- Reuse existing patterns before adding abstractions, dependencies, files, or configuration. Avoid unrelated refactoring, cleanup, renaming, formatting, optimization, and speculative extensibility.
- Inspect the affected behavior and nearby conventions before editing. Review the task diff and run focused validation afterward. Explain broad or high-impact tradeoffs before proceeding.

## Local Git commits

- After an approved task changes files or software state in a Git repository, inspect status and diffs, stage only task-specific files or separable hunks, and create a local commit before the final response.
- Use a concise subject in the form `[prefix] summary`, with an appropriate prefix such as `feat`, `fix`, `asset`, `config`, `refactor`, `test`, or `docs`. Never push, publish, or open a pull request without separate approval.
- If a changed file cannot be separated safely from unrelated or user-authored edits, exclude it and report the commit as incomplete or skipped. Apply the `houdini-workflow` skill's binary exception when it governs the task.
- Do not create empty commits. Report when no task-specific changes exist or Git or hooks prevent the commit.

## Final reporting

- End every completed task with a `Changed files` section listing each added, modified, renamed, or deleted path and its purpose. Write `Changed files: none` when applicable.
- When files changed, finish with `Local Git commit: <short-hash> — <result>; files: <paths>` and, on the final line, `Commit message: [prefix] summary`.
