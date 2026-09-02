# Task Template

Read this file whenever creating a task. Render the task body in Notion-flavored Markdown and do not repeat the task title as a heading.

## Property Mapping

| Property | Rule |
| --- | --- |
| `Task` | Short, action-oriented title derived from the requested outcome. |
| `Project` | One verified project page URL or ID found by exact `Project Name`. |
| `Status` | `Backlog` by default; valid values are `Backlog`, `Ready`, `In Progress`, `Blocked`, `Review`, and `Done`. New tasks should normally be `Backlog` or `Ready`. |
| `Priority` | `P2` by default; valid values are `P0`, `P1`, `P2`, and `P3`. |
| `Depends On` | Verified prerequisite task URLs or IDs only. Omit when none were specified. |

Do not set blank properties merely to make them appear. Do not use `Project Key` for task lookup or task creation.

## Page Body

Use every top-level section below. Replace guidance with task-specific content; do not leave braces, bracketed placeholders, or drafting instructions in the created page.

```markdown
<callout icon="📋" color="blue_bg">
	**Execution summary:** {{One sentence stating the required outcome and why it matters.}}
</callout>

## Objective

{{Describe the observable outcome.}}

## Scope

### Included

- {{Required change or deliverable}}

### Excluded

- {{Explicit non-goal, or "No exclusions specified."}}

## Context

{{Summarize relevant user-provided context. Include project-level working directory, branch, or Codex instructions only when they help execute this task.}}

## Acceptance Criteria

- [ ] {{Observable, testable requirement}}
- [ ] {{Required validation succeeds}}
- [ ] No unrelated changes are introduced.

## Implementation Constraints

- {{User-provided or project-level constraint, or "No additional constraints specified."}}

## Dependencies

- {{Verified prerequisite task link, or "None specified."}}

## Resources

- {{Verified specification, design, repository path, or related page, or "None specified."}}

## Validation

- {{Exact command when supplied or safely known; otherwise a concrete manual verification.}}

## Execution Log

### Progress

To be completed by the executor.

### Validation Results

To be completed by the executor.

### Completion

Record the outcome, commit or artifact, and remaining notes here. Then populate `Result`, `Artifact URL` when applicable, `Completed At`, and the final `Status`.
```

## Drafting Rules

- Convert the user's description into measurable acceptance criteria without adding new product scope.
- Prefer a specific manual validation over an invented command.
- Preserve uncertainty explicitly with `Not specified` for non-critical details. Ask the user about uncertainty that changes the intended outcome, project match, or readiness.
- Keep the execution log empty except for its executor prompts; it records future work, not task creation.
