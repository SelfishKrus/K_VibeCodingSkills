---
name: houdini-workflow
description: Use for Houdini scene, HDA, VEX, baking, or node-network work, including Git handling for .hip, .hiplc, .hipnc, .hda, .hdalc, and .hdanc files. Do not use for unrelated Unity-only or generic 3D tasks.
---

# Houdini workflow

Follow the active global and project approval boundaries before changing files or Houdini state.

## Implementation choices

- Prefer VEX for Houdini code. Use Python only when the workflow requires it or it provides a clear, justified performance advantage.
- Limit baking to the required frames, geometry, attributes, channels, and resolution. Cache reusable upstream results, avoid recooking unchanged nodes, batch safe operations, and profile before optimizing.

## Binary Git checkpoint

- Before modifying a `.hip`, `.hiplc`, or `.hipnc` scene, inspect its Git status.
- If the target scene is already modified, disclose in the pre-execution approval summary that its existing binary state will be captured in a local baseline commit.
- After approval and before editing the scene, stage only the affected pre-existing Houdini scene files and commit them with `[chore] checkpoint pre-existing Houdini scene changes`.
- If task changes are already mixed into a previously modified Houdini binary and separation is impossible, commit the entire affected binary in the task commit and clearly disclose the mixed content. Do not skip it solely because it contains pre-existing binary changes.
- Never include unrelated files. A checkpoint or mixed-binary commit never authorizes pushing or publishing.

## Saving and committing

- Save the active Houdini scene after every modification made through Houdini or an MCP server, and save it again immediately before committing.
- Save every modified digital asset definition back to its `.hda`, `.hdalc`, or `.hdanc` library.
- Include all task-specific Houdini scene and asset-library changes in the same task commit.

## Node graph quality

- Route each stage's result to a Null node named `OUT_XXXX`, replacing `XXXX` with a descriptive stage name.
- Group each logical module into a clearly named subnet unless doing so would break behavior, interfaces, or references. Use named network boxes (frames) to organize related nodes and wiring. Update and verify affected paths after subnetting.
- When it improves wiring clarity, pass inputs through a subnet unchanged; do not modify the data solely to tidy connections.
- Add concise comments or sticky notes for non-obvious scripts and networks, documenting purpose, important inputs and outputs, and assumptions.
- Keep graphs consistently oriented, spaced, aligned, and descriptively named. Minimize wire crossings and use reroute dots when they improve readability.
