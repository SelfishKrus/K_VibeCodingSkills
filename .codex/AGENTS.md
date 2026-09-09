# Global working agreements

## Writing assistance

- Before answering or acting on each user request, first briefly improve the user's wording for clarity, grammar, and concision while preserving their intent and language. Present it as `[header] : [optimized sentences]`, using a short, descriptive header, then proceed with the requested task.

## Implementation

- Make the smallest safe, localized change that fully satisfies the request. Preserve existing behavior, architecture, public APIs, data formats, workflows, and visual design unless the request requires otherwise.
- Reuse existing patterns before adding abstractions, dependencies, files, or configuration. Avoid unrelated refactoring, cleanup, renaming, formatting, optimization, and speculative extensibility.
- Inspect the affected behavior and nearby conventions before editing. Review the task diff and run focused validation afterward. Explain broad or high-impact tradeoffs before proceeding.

## Local Git commits

- After an approved task changes files or software state in a Git repository, inspect status and diffs, stage only task-specific files or separable hunks, and create a local commit before the final response.
- Use a concise subject in the form `[prefix] summary`, with an appropriate prefix such as `feat`, `fix`, `asset`, `config`, `refactor`, `test`, `chore` or `docs`. Never push, publish, or open a pull request without separate approval.
- If a changed file cannot be separated safely from unrelated or user-authored edits, exclude it and report the commit as incomplete or skipped. Apply the `houdini-workflow` skill's binary exception when it governs the task.
- Do not create empty commits. Report when no task-specific changes exist or Git or hooks prevent the commit.

## Final reporting

- End every completed task with a `Changed files` section listing each added, modified, renamed, or deleted path and its purpose. Write `Changed files: none` when applicable.
- When files changed, finish with `Local Git commit: <short-hash> — <result>; files: <paths>` and, on the final line, `Commit message: [prefix] summary`.
