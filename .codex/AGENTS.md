# Global working agreements

## Writing assistance

- Before answering or acting on each user request, first briefly improve the user's wording for clarity, grammar, and concision while preserving their intent and language. Present it as `[header] : [optimized sentences]`, using a short, descriptive header, then proceed with the requested task.

## Implementation

- Make the smallest safe, localized change that fully satisfies the request. Preserve existing behavior, architecture, public APIs, data formats, workflows, and visual design unless the request requires otherwise.
- Reuse existing patterns before adding abstractions, dependencies, files, or configuration. Avoid unrelated refactoring, cleanup, renaming, formatting, optimization, and speculative extensibility.
- Inspect the affected behavior and nearby conventions before editing. Review the task diff and run focused validation afterward. Explain broad or high-impact tradeoffs before proceeding.
- For work that produces outputs in multiple stages, establish checkpoints at meaningful stage boundaries. Make each intermediate output easy to inspect and reproduce, define its expected behavior or acceptance criteria, and validate it with focused unit tests where appropriate or lightweight checks otherwise, so developers can review results and isolate failures. Reuse existing testing and debugging tools, and document how to inspect or rerun each checkpoint.

## Houdini node layout

- Whenever creating or modifying a Houdini node network, lay out the affected nodes in dependency/cook order from top to bottom: sources and inputs above their consumers, with final outputs at the bottom. Derive placement from actual connections and dependencies, not creation order or node names; keep intentional feedback loops clearly separated and labeled.
- Keep sequential chains vertically aligned and parallel branches in separate, consistently spaced columns, converging above their merge or consuming node. Keep logical stages together and leave clear gaps between stages.
- Prevent overlaps between nodes, labels, network boxes, and sticky notes. Minimize wire crossings and wires passing through unrelated nodes; use reroute dots where helpful.
- Perform the final layout after all nodes and connections are in place, including inside affected subnets. Automatic layout is only a starting point: inspect and correct its result. Preserve unrelated user layouts and do not change wiring, parameters, or behavior solely to improve appearance.
- Before saving and reporting completion, visually inspect each affected network in the Network Editor or a screenshot and correct overlaps, unreadable spacing, and dependency-order violations. If visual inspection is unavailable, check node positions and connections programmatically and report that limitation.

## Local Git commits

- After an approved task changes files or software state in a Git repository, inspect status and diffs, stage only task-specific files or separable hunks, and create a local commit before the final response.
- Use a concise subject in the form `[prefix] summary`, with an appropriate prefix such as `feat`, `fix`, `asset`, `config`, `refactor`, `test`, `chore` or `docs`. Never push, publish, or open a pull request without separate approval.
- If a changed file cannot be separated safely from unrelated or user-authored edits, exclude it and report the commit as incomplete or skipped. Apply the `houdini-workflow` skill's binary exception when it governs the task.
- Do not create empty commits. Report when no task-specific changes exist or Git or hooks prevent the commit.

## Final reporting

- After completing each task, explain the causes of the issue or the reason for the work, and describe how you resolved it or completed the task.
- End every completed task with a `Changed files` section listing each added, modified, renamed, or deleted path and its purpose. Write `Changed files: none` when applicable.
- When files changed, finish with `Local Git commit: <short-hash> — <result>; files: <paths>` and, on the final line, `Commit message: [prefix] summary`.
