# Drowned Sanctuary — Stone Titan Level

A reference-inspired Blender environment: a colossal fractured limestone head rises from a dark flooded basin, with scattered ruins, stepping ledges, low mist and a lone explorer carrying a lantern.

## Open and explore

Open `Stone_Titan_Level.blend` in Blender 5.2. The main scene is **STONE TITAN • The Drowned Sanctuary**. Press **Numpad 0** for the composed camera. The numbered Outliner collections separate the statue, ruins, water, explorer, atmosphere and lighting. The hidden source collection retains the modified head mesh.

The scene contains 19 individually editable solid head fragments, procedural stone and water materials, eroded boulders, carved eye sockets, mist, a camera and a lighting rig. This is an artistic environment with a suggested traversal route; game-engine collision, navigation and gameplay are not implemented.

`Stone_Titan_Preview.png` is the rendered camera view. The scene uses Cycles with denoising at 1000 × 1250; it is configured for the local NVIDIA GPU. It has no external texture dependencies.

## Rebuild

Run `build_level.py` in Blender's Python environment or through the MCP `execute_blender_code` tool. The script uses the project path `C:\Users\WIN10\Desktop\BlenderMCP`; update `ROOT` if moving the folder. It rebuilds its named scene, saves the blend file, and leaves rendering as a separate step. The generated scene is editable, but rebuilding replaces manual edits in that scene.

## Asset attribution

**Infinite, 3D Head Scan** by **Lee Perry-Smith / Infinite Realities**, based on work at **www.triplegangers.com**. Licensed under [Creative Commons Attribution 3.0 Unported](https://creativecommons.org/licenses/by/3.0/).

Source: [three.js example asset](https://github.com/mrdoob/three.js/tree/dev/examples/models/gltf/LeePerrySmith). Original license: `assets/LeePerrySmith_License.txt`. Original mesh: `assets/LeePerrySmith.glb`.

Changes to the scan: neck and shoulders trimmed, eye sockets carved, surface eroded, mesh split into capped fracture fragments, selected fragments recessed, stone materials applied, and pose and scale changed. The surrounding environment and procedural scene builder were created for this project. The user's image supplied the visual reference; it is not used as a texture or background plane.
