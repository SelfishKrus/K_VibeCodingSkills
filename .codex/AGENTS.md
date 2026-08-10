- C# Naming Conventions 
    - PascalCase: Classes, Structs, Enums, Methods, and Public/Protected fields.
    - camelCase: Local variables and method parameters.
    - _camelCase (with underscore): Private and protected fields.
    - UPPER_CASE: Constants (const) and static read-only variables.

- Unity C# Log Debugging 
    - For key logic branches, include Debug.Log using the prefix [{ModuleName}-{ClassName}] and pass this as the context object so I can track the runtime behavior in the Unity Console."

- Execution Approval Gate
  - Before modifying code or project files, or performing any state-changing MCP or external action, provide a concise, refined in-chat summary of the proposed approach, the core idea, and the potential side effects.
  - Do not create a separate planning, design, or specification document as part of this pre-execution step. The concise in-chat summary is the complete plan unless a higher-priority instruction explicitly requires another artifact.
  - End the summary by asking the user to reply with exactly `y` to proceed or `n` to stop, then wait for that reply before taking the proposed action.
  - Treat only `y` as approval. If the user replies `n`, stop without making the proposed changes. If the reply is neither `y` nor `n`, ask again and do not proceed.
  - After `y`, begin implementation directly in code or through the applicable MCP tools. Do not write an additional planning document.
  - Request a new `y` or `n` decision only if the approved scope changes materially or a separate destructive, irreversible, privileged, or externally visible action requires confirmation.
  - This gate does not apply to read-only inspection, explanation, diagnosis, research, or status reporting, and it does not replace mandatory safety checks, sandbox approvals, or higher-priority instructions.

- Local Git Commit After Changes
  - After every approved task that modifies code, project files, or software state directly or through MCP tools, inspect the repository status and diff, stage only the files or separable hunks changed for the current task, and create a local Git commit before the final response. Never include pre-existing, unrelated, or user-authored changes.
  - If task changes cannot be separated safely from unrelated changes in the same file, exclude that file and report the commit as incomplete or skipped rather than committing someone else's work.
  - Use a concise subject in the format `[prefix] summary`, choosing an appropriate prefix such as `feat`, `fix`, `asset`, `config`, `refactor`, `test`, or `docs`, and describe only the current task.
  - Keep commits local: never push, publish, or open a pull request without separate user approval. Do not create empty commits; report when no task-specific changes exist, the directory is not a Git repository, hooks reject the commit, or Git otherwise fails.
  - End the final response with `Local Git commit: <short-hash> — <result>; files: <paths>` or `Local Git commit: not created — <reason>`, followed on its own final line by `Commit message: [prefix] summary`. Omit both lines only when no files were modified.
