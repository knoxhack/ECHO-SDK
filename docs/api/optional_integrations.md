# Optional Integrations

Optional integrations must be safe when the target module or runtime is absent.

## Rules

- Declare optional module IDs in `optional`.
- Feature-detect services before calling them.
- Treat missing optional integrations as no-op behavior.
- Do not require optional integrations for install, update, or repair.
