# Openlands Known Issues

Openlands is currently an implementation foundation, not a playable public beta.

## Known Gaps

- Final textures, models, audio, icons, screenshots, and pack artwork are not present yet.
- Runtime adapters still need to consume `echoopenlandsprotocol` registries and emit Native, Standalone, and NeoForge artifacts.
- Creature AI names are contract placeholders until implemented in `echocreaturecore`/runtime adapters.
- HoloMap fallback behavior is specified but not implemented here.
- Waystone multiplayer permissions are specified but need runtime persistence tests.
- Launcher install, update, repair, rollback, and parity validation are still release gates.

## Non-Negotiable Rules

- Do not mark Openlands public-ready while any Minecraft-derived asset, copied name, copied silhouette, or copied recipe identity remains.
- Do not enable stamina, hydration, food spoilage, or temperature damage in `openlands_standard`.
- Do not publish a runtime edition as approved until all three edition lanes have matching Echo IDs or documented runtime limitations.

