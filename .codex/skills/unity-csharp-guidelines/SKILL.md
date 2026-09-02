---
name: unity-csharp-guidelines
description: Apply Unity-specific C# naming, diagnostic logging, and editor/runtime separation conventions when creating or modifying Unity C# code or assembly definitions. Do not use for non-Unity C# work.
---

# Unity C# guidelines

Apply these conventions while preserving the surrounding project's established style when it is more specific.

## Naming

- Use PascalCase for classes, structs, enums, methods, and public fields.
- Use camelCase for local variables and method parameters.
- Use `_camelCase` for private and protected fields.
- Use UPPER_CASE for constants and static readonly fields.

## Runtime logging

- Add `Debug.Log` at important logic branches where runtime traceability materially helps debugging.
- Prefix messages with `[ModuleName-ClassName]`.
- Pass `this` as the context object when the containing instance is a `UnityEngine.Object`.
- Keep logs focused; do not add noisy per-frame logging unless the task explicitly requires it.

## Editor/runtime separation

- Keep editor-only scripts and assemblies separate from runtime code. Prefer an editor-only assembly definition whose `includePlatforms` contains only `Editor`.
- If the containing assembly is not Editor-only, wrap all editor-only code, including every `UnityEditor` reference, with `#if UNITY_EDITOR` and `#endif`.
- Runtime assemblies must not depend on editor-only assemblies or expose unguarded editor-only APIs.
