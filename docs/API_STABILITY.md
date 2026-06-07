# ECHO 1.3.5 API Stability

| Label | Meaning | Public guidance |
|---|---|---|
| Stable | Safe for external mods across patch updates | Prefer these APIs for public integrations. |
| Beta | Usable in public packs but may change with wrappers | Use when needed and watch changelogs. |
| Experimental | Creator/dev tooling or early API | Avoid hard dependencies in public packs. |
| Internal Only | Not for external mods | Do not integrate directly. |
| Deprecated/Obsolete | Replaced or retained as marker | Do not use for new work. |

## Current API Families

- EchoCore service lookup and optional/no-op services: Stable.
- RuntimeGuard budgets: Stable.
- Terminal, Index, HoloMap, Lens, MissionCore, ThemeCore, SoundCore, DataCore, WorldCore, PowerGrid, Logistics, Armory, RelicTech, and MultiblockCore public hooks: Beta unless module metadata marks them otherwise.
- TextureForge and SignalOS Example surfaces: Experimental/Internal according to metadata.

Reusable integrations must not require Ashfall unless the module metadata explicitly says Ashfall is required.
