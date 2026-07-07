---
applyTo: "**"
---

- Response Format For Code Changes
  - Before modifying code or files, present the confirmation block exactly in this style:
    `Plan: ...`
    `Side Effects: ...`
    `Proceed? y/n`
  - Put each label on its own line, and insert one blank line after the block before any following text.
  - Keep `Plan` to 1-3 concise sentences describing the intended architecture and affected files.
  - Keep `Side Effects` to 1-2 concise sentences describing behavior changes, risks, or "None expected."
  - Do not modify files until I explicitly confirm with `y`.

- C# Naming Conventions
  - PascalCase: Classes, Structs, Enums, Methods, and Public/Protected fields.
  - camelCase: Local variables and method parameters.
  - _camelCase (with underscore): Private and protected fields.
  - UPPER_CASE: Constants (const) and static read-only variables.

- Unity C# Log Debugging
  - For key logic branches, include Debug.Log using the prefix [{ModuleName}-{ClassName}] and pass this as the context object so I can track the runtime behavior in the Unity Console.

- Commit Message After Code Changes
  - After every turn where you modify code or project files, end your final response with exactly one single-sentence commit message.
  - Put it on its own final line in this format: `Commit message: [prefix] ...`
  - Choose an appropriate prefix such as `[feat]`, `[fix]`, `[asset]`, `[config]`, `[refactor]`, `[test]`, or `[docs]`.
  - The message must summarize only the changes made in that turn and must not imply that a git commit was created.
  - If no files were modified, omit the commit message.