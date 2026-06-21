# {{display_name}} — Player Surface Manifest

This module declares module-owned player surfaces using `echo.native.player_surface_manifest.v1`.

## Owner boundaries

- This module owns the surface manifest and the gameplay actions it dispatches.
- The runtime host (NeoForge, ECHO Native Loader, Standalone Runtime, or Standalone Engine) owns the adapter that renders the surface and routes input.
- The pack is a fixture; it does not own player-facing UI contracts.

## Validation

Run the following from the workspace root:

```text
python ..\\ECHO-SDK\\tools\\validate_echo_contracts.py --json
.\\gradlew generateEchoModuleGraph -PechoAddonSet=beta
```
