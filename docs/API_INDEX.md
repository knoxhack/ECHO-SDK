# ECHO API Index

| API Surface | Stability | Purpose | Notes |
|---|---:|---|---|
| EchoCore services / optional services | Stable | Safe service discovery and no-op fallbacks | Use before direct addon calls. |
| Terminal page providers | Beta | Add dashboard/pages when Terminal is installed | Must no-op without Terminal. |
| Index content providers | Beta | Add docs, entries, relations, recipes | Datapack examples preferred. |
| HoloMap marker/layer providers | Beta | Add map markers and layers | Avoid client-only server loads. |
| Lens scan providers | Beta | Add scan results | Keep privacy-safe. |
| MissionCore objectives/rewards | Beta | Track and reward player actions | Use data-driven examples when possible. |
| ThemeCore tokens | Beta | Theme UI surfaces | Default dark fallback required. |
| SoundCore rules | Beta | Add subtle sound cues | Missing sounds must fallback safely. |
| DataCore persistence | Beta | Store player/world/team state | Avoid direct save access. |
| RuntimeGuard budgets | Stable | Register heavy-system budgets | Useful for low-end/server packs. |
| WorldCore hazards/regions | Beta | Data-driven world context | Ashfall content belongs in Ashfall namespace. |
| PowerGrid energy hooks | Beta | Connect machines/power consumers | Keep optional. |
