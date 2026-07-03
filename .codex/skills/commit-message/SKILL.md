---
name: commit-message
description: Generate a concise subject and per-file commit body from git diff for selected files, then ask before staging or committing locally. Use when the user asks for a commit message, selected-file commit, quick commit prompt, local-only git commit, or invokes $commit-message.
---

# Commit Message

Generate an integrated commit subject plus a compact per-module/file body from selected-file changes, then ask before making a local commit.

## Workflow

1. Determine the selected files from the user prompt.
   - If no files are specified, ask which files to include.
   - Never include unrelated modified files.
   - If a specified file does not exist or is not tracked/modified, report it and ask how to proceed.

2. Inspect only the selected files.
   - Run `git status --short -- <files>`.
   - Run `git diff -- <files>`.
   - Run `git diff --cached -- <files>` when staged changes may exist.
   - If both staged and unstaged changes exist for the same selected file, explain that `git add` will include the full selected-file working-tree content, then ask before proceeding.

3. Check for risks before proposing a commit.
   - Warn about secrets, credentials, generated junk, accidental binary changes, or unrelated edits.
   - Stop and ask the user how to proceed if any risk is found.

4. Summarize the selected changes in 1-3 bullets.

5. Generate one commit message with a subject and body.

   Subject:
   - Format: `[prefix] concise integrated summary`.
   - Keep under 72 characters when possible.
   - Capture the shared purpose of the selected changes.
   - Choose the prefix from the primary intent, not from file count.
   - Prefer specific verbs such as `Persist`, `Generate`, `Overwrite`, `Remove`, `Validate`, `Compact`, `Save`, or `Refine`.
   - Avoid vague verbs such as `Update`, `Change`, `Improve`, or `Adjust` unless no clearer verb fits.

   Body:
   - Add 1 bullet per selected module/file when multiple modules/files changed.
   - Format each bullet as `- <ModuleNameOrFileName>: <what changed and why/result>.`
   - Keep bullets compact and behavior-focused.
   - Include implementation detail only when it explains user-visible or workflow behavior.
   - If changes span multiple independent intentions, warn that separate commits may be better before proposing the message.

6. Ask exactly:

   `Commit these selected changes locally with this message? y/n`

7. Only if the user explicitly answers `y`:
   - Run `git add -- <files>`.
   - Run `git commit -m "[prefix] concise integrated summary" -m "<body bullets>"`.
   - Run `git rev-parse --short HEAD`.
   - Report the local commit hash and say that nothing was pushed.

8. If the user answers anything other than `y`, do not stage or commit.

## Safety Rules

- Commit only to the current local branch.
- Never run `git push`, `git push --force`, `gh pr create`, or any remote publishing command.
- If the user asks to push, stop and say this skill is local-commit only.
- Never commit without explicit `y` after showing the proposed message.
- Never stage files outside the selected list.
- Never run destructive git commands such as `git reset`, `git checkout --`, or branch deletion.
- Do not amend, squash, rebase, or rewrite history unless the user explicitly asks outside this skill.
- If a command fails, report the failure and stop; do not try a different commit command silently.

## Output Shape

Before confirmation, respond with:

```text
Selected files:
- <file>

Summary:
- <change>

Commit message:
[prefix] concise integrated summary

- <ModuleNameOrFileName>: <what changed and why/result>.
- <ModuleNameOrFileName>: <what changed and why/result>.

Commit these selected changes locally with this message? y/n
```

After a successful commit, respond with:

```text
Created local commit <hash>.
Nothing was pushed.
```
