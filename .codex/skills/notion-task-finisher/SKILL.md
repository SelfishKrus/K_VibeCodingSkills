---
name: notion-task-finisher
description: Execute and finish one task from the configured Notion Tasks database using a user-supplied task page ID or URL, then publish a result document and update the task record. Use when the user asks Codex to complete a specific Notion task; do not use to create tasks, choose work from a queue, or merely report status.
---

# Notion Task Finisher

Complete exactly one verified Notion task, validate the outcome, publish its result, and leave the task record consistent.

## Configured Notion System

- Tasks data source: `collection://3730eb25-780c-465a-b1b2-47026764e868`
- Projects data source: `collection://6b63f55d-d124-48e5-a34f-2f6afd787139`
- Result template page: `3cfb674e-a72b-80c6-a725-e3d3e3031f64`
- The `Result` property is currently text. Store the canonical URL of the generated result page in it.

Fetch the live data-source schemas and result template on every invocation. Treat live Notion state as authoritative. If the `Result` property type has changed, use its unambiguous native representation; otherwise stop and explain the mismatch.

## Intake and Readiness

1. Require exactly one task page ID or URL supplied by the user. If it is missing or ambiguous, ask for it. Never select a task from a queue.
2. Fetch the task and Tasks data source. Verify that the page belongs to the configured Tasks data source and has the expected task properties. Reject unrelated pages.
3. Read the entire task body, including scope, acceptance criteria, constraints, resources, validation, and execution log.
4. Resolve exactly one related `Project`, then fetch its complete page plus `Working Directory`, `Default Branch`, and `Codex Instructions`. Ask if the relation is missing or ambiguous.
5. Fetch every `Depends On` task and require each one to be `Done`. Never bypass unresolved dependencies.
6. Do not silently rerun `Done` tasks. Treat `Backlog` as not actionable unless the user explicitly asks to proceed and missing requirements can be resolved. Resume `In Progress` only when the user intends to continue it.
7. Present a concise execution preview and obtain every approval required by active instructions before changing Notion, repository files, or external state. Invoking this skill is not blanket permission.

## Execute

1. After approval, set `Status` to `In Progress`. Add a timestamped start entry under `Execution Log` with a targeted content update that preserves all existing task content.
2. Work only within the documented scope and verified project context. Use the project working directory when relevant; never invent a path. Read and obey applicable repository instructions and skills before editing.
3. Keep task progress notes concise. Record material decisions, approved deviations, blockers, changed files, commits, artifacts, and validation evidence.
4. Run every documented validation plus focused checks required by active repository instructions.
5. Do not publish success or select `Done` or `Review` until every acceptance criterion has evidence and all required validation passes.

## Publish Result

1. After the implementation outcome is known, fetch the live result template and the current Notion enhanced-Markdown specification.
2. Create one child page under the task named `Result — <Task title>` with the `📄` icon.
3. Render the result from the current template:
   - Preserve its section order, hierarchy, restrained colors, columns, and icons.
   - Replace the introductory callout and every placeholder with verified task facts.
   - Include direct task and project links, acceptance-criterion evidence, deliverables, changed files, commands or checks with outcomes, decisions, deviations, limitations, follow-ups, and a completion statement.
   - Remove `Template Instructions`, unused prompts, and every bracketed placeholder.
   - Never invent a URL, path, command, commit, artifact, or success claim.
4. Fetch the result page and verify its title, parent task, content, and absence of placeholders and template instructions.
5. If the task's `Result` already contains a different result-page URL, ask before replacing it. When retrying after a partial failure, reuse the existing result page rather than creating a duplicate.
6. When possible, make one final task-property update:
   - `Result`: canonical result-page URL
   - `Completed At`: current ISO-8601 date and time
   - `Status`: `Done`, or `Review` only when the task explicitly requires human review
   - `Artifact URL`: an actual primary-deliverable URL only; do not put the result-page URL here unless the user explicitly chooses that convention
7. Append the result link and final status to the task's `Execution Log`, then fetch both the task and result again to verify the final state.

## Blocked or Failed Work

- If work cannot continue, record the exact blocker and evidence in `Execution Log`, set `Status` to `Blocked`, and do not set `Completed At` or create a success result document.
- If `Result` is empty, it may temporarily contain `Blocked: <short reason>`. Replace that note with the result-document URL only after a later successful completion.
- If result-page creation succeeds but the task update fails, reuse that page, retry the task update safely, and report the partial state. Never create another result page.
- Do not delete prior results, rewrite unrelated task content, expand scope, push, publish, or open a pull request without separate authorization.
