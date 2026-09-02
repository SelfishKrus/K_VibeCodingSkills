---
name: notion-task-creator
description: Create structured task pages from a user's natural-language description by using the configured Notion template page and Tasks database. Use when the user asks to add, draft, or create a task for a named project in their Notion project-management system; do not use for executing the task or merely reporting task status.
---

# Notion Task Creator

Create a complete, executable task record while preserving the user's meaning and the existing Projects-to-Tasks relationship.

## Configured Notion System

- Projects data source: `collection://6b63f55d-d124-48e5-a34f-2f6afd787139`
- Tasks data source: `collection://3730eb25-780c-465a-b1b2-47026764e868`
- Template source page: `3cfb674e-a72b-80c9-93d9-ff1ff4ca3666` (`Task document template`)
- Match projects with the `Project Name` title property. `Project Key` is optional and must not be required for task creation.
- Create tasks in the Tasks data source and populate its `Project` relation with the matched project page URL or ID.

Fetch both data sources and the template source page on every invocation. The live schemas govern valid Notion properties; the current template page governs task defaults, body structure, and drafting rules. Never use a cached or local copy of the template.

## Creation Workflow

1. Fetch the template source page. Stop and identify the problem if it is missing, inaccessible, empty, or no longer clearly describes a task template.
2. Extract the requested task title, Project Name, objective, scope, context, acceptance criteria, constraints, dependencies, resources, validation, priority, and status. Preserve explicit wording where it affects requirements.
3. Require a usable task objective and Project Name. Ask one concise question when either cannot be determined safely from the request.
4. Resolve the project with a parameterized, case-insensitive exact-name query against the Projects data source. Select its `url`, `Project Name`, `Working Directory`, `Default Branch`, and `Codex Instructions` when available. If there is no exact match or more than one valid match, ask the user instead of guessing or creating a project.
5. Check the Tasks data source for an existing non-Done task with the same project and substantially identical title. If one exists, show its link and ask whether to create a duplicate.
6. Draft one task unless the user explicitly requests multiple tasks. Apply the template page as follows:
   - Use `Task properties` to determine database-property defaults and rules.
   - Render the sections from `Objective` through `Execution Log` as the created task's page body, preserving their current order and hierarchy.
   - Use `Generation rules` while drafting, but do not copy that section, the source-of-truth callout, `Task properties`, or template dividers into the created task.
   - Replace instructional text with task-specific content. Preserve template prompts that are explicitly meant for the future executor.
7. Honor valid property values supplied by the user over template defaults. Follow the template's readiness rule before assigning `Ready`.
8. Before the state-changing create call, show a compact preview containing title, Project Name, status, priority, and any meaningful inference. Obtain any approval required by the active instructions. Skill invocation alone is not blanket permission for external changes.
9. Immediately before creation, fetch the live Tasks schema and the Notion enhanced Markdown specification. Create the page under the Tasks data source with:
   - `Task`: the concise action-oriented title
   - `Project`: an array containing the matched project page URL or ID
   - `Status` and `Priority`: the resolved values
   - `Depends On`: only verified task URLs or IDs explicitly requested by the user
   - page content rendered from the task template
10. Do not set `Task ID`, `Created`, `Last Edited`, empty completion fields, `Result`, `Artifact URL`, `Blocks`, or `Completed At` during creation. These are generated, reverse-related, or completion-time fields.
11. Fetch the created page and verify its title, Project relation, status, priority, and body. Return the page link and a short summary. Follow any one-time connector follow-up requirement emitted by the Notion tools.

## Failure Boundaries

- If the Notion connector is unavailable or lacks write access, stop after the draft and tell the user what must be connected or enabled.
- If the template page cannot be fetched or interpreted safely, stop instead of using a stale fallback.
- If a schema field was renamed or removed, adapt only when the replacement is unambiguous. Otherwise stop and identify the mismatch.
- Never create a missing project, update another task, or start executing the new task unless the user separately requests it.
