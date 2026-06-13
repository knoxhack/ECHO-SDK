# Openlands Test Checklist

## First-Hour Acceptance

- Spawn near wood, loose stone, fiber, food, water, and one exploration hook.
- Discovery prompts fire for first stick, first stone, first fiber, first tool, first campfire, and first shelter score.
- Player can craft fiber binding, crude axe, crude pick, crude spade, flint knife, torch bundle, campfire, workbench, and bedroll.
- Shelter score reaches the sleep milestone with partial roof, partial enclosure, light/fire, and bedroll.
- Sleep sets a return point.
- Recoverable death pack is enabled in Standard.
- Save/load preserves inventory, hotbar, placed blocks, chest contents, bedroll spawn, campfire lit state, shelter score, HoloMap discovery, and waystone state.
- `playtests/mvp_first_hour_acceptance.json` covers the same route steps, save/load fields, HoloMap fields, waystone states, and release evidence.
- `systems/playable_runtime_contract.json` maps starter spawn, shelter scoring, waystone transitions, Standard rules, first-hour route order, and adapter readiness to shared `OpenlandsFirstHourRuntime` hooks.

## Cross-Runtime Parity

- `node addons/echoopenlandsprotocol/scripts/validate-openlands-contract.mjs --module-root addons/echoopenlandsprotocol` passes from `ECHO-Modules`.
- `node addons/echoopenlandsprotocol/scripts/validate-openlands-runtime-core.mjs --module-root addons/echoopenlandsprotocol` passes from `ECHO-Modules`.
- `node addons/echoopenlandsprotocol/scripts/validate-openlands-editions.mjs --module-root addons/echoopenlandsprotocol --workspace-root C:/Development/Github` passes from `ECHO-Modules`.
- Native loads the same block, item, recipe, biome, creature, waystone, and HoloMap IDs.
- Standalone loads the same block, item, recipe, biome, creature, waystone, and HoloMap IDs.
- NeoForge loads generated assets/data from Echo IDs without making Minecraft-owned content the source.
- Runtime-specific limitations are documented in the edition repo before release.
- Every edition release manifest template requires the adapter phases and Public Alpha evidence from `runtime_adapter_load_plan.json`.
- Every edition `evidence/runtime-evidence.template.json` matches all runtime evidence IDs, runtime-core report paths, first-hour scenarios, save/load checkpoints, and the public-alpha waystone scenario.
- `systems/legal_content_audit.json` rejects prohibited public terms and keeps placeholder assets warning-only until final original assets exist.
- `systems/launcher_flow_acceptance.json` proves install, update, repair, rollback, hash checks, and world/config preservation for all editions.

## Release Gates

- `echoopenlandsprotocol-0.1.0.echo-addon` exists with checksum.
- `echoopenlandsprotocol-0.1.0-standalone.jar` exists with checksum.
- `echoopenlandsprotocol-0.1.0-neoforge.jar` exists with checksum.
- Launcher install succeeds for all three edition repos.
- Launcher update applies changed module artifacts only.
- Launcher repair restores missing/corrupt files.
- Rollback returns to the previous manifest.
- Release Index validation passes.
- Website/card data marks Openlands as preview until artifacts are real.
