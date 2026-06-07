# ECHO Mod Stack







Ashfall is the modpack. ECHO is the first-party ecosystem that powers it. `ECHO: Ashfall Protocol` is the main campaign addon, built from `addons/echoashfallprotocol` as the `echoashfallprotocol` artifact.







The ECHO stack is a post-Gridfall survival saga for Minecraft 26.1.2 on NeoForge. The simplified public stack can be described as Core, Terminal, Ashfall Protocol, Blockworks, Orbital, Agriculture, Stationfall, Nexus, Industrial, and Blackbox. The build-truth Gradle `all` stack also includes NetCore, RuntimeGuard, ThemeCore, PlayerCore, MissionCore, DataCore, WorldCore, SignalOS, SignalOS Example, RenderCore, Logistics Network, Convoy Protocol, HoloMap, Index, Armory, and Lens.





Compatibility history token: `1.0.0`.





ECHO Ecosystem `1.0.0` current Gradle truth: `echoashfallprotocol` `1.0.0`, `echocore` `1.0.0`, `echonetcore` `1.0.0`, `echocommunitybridge` `1.0.0`, `echopresencelink` `1.0.0`, `echoterminal` `1.0.0`, `echomissioncore` `1.0.0`, `echoscriptcore` `1.0.0`, `echocreatorcore` `1.0.0`, `echodatacore` `1.0.0`, `echoplatformcore` `1.0.0`, `echoadaptercore` `1.0.0`, `echoschemacore` `1.0.0`, `echovalidationcore` `1.0.0`, `echopackcore` `1.0.0`, `echometadatacore` `1.0.0`, `echomodulegraph` `1.0.0`, `echohealthcore` `1.0.0`, `echoagentcore` `1.0.0`, `echobridgecore` `1.0.0`, `echocontentcore` `1.0.0`, `echoassetcore` `1.0.0`, `echoreportcore` `1.0.0`, `echopowercore` `1.0.0`, `echomachinecore` `1.0.0`, `echologisticscore` `1.0.0`, `echovehiclecore` `1.0.0`, `echobiomecore` `1.0.0`, `echoatmospherecore` `1.0.0`, `echocinematiccore` `1.0.0`, `echocameracore` `1.0.0`, `echoinputcore` `1.0.0`, `echorecipecore` `1.0.0`, `echoprogressioncore` `1.0.0`, `echosocialcore` `1.0.0`, `echoeconomycore` `1.0.0`, `echolootcore` `1.0.0`, `echostructurecore` `1.0.0`, `echostatuscore` `1.0.0`, `echocombatcore` `1.0.0`, `echocreaturecore` `1.0.0`, `echospawncore` `1.0.0`, `echoeventcore` `1.0.0`, `echoencountercore` `1.0.0`, `echodifficultycore` `1.0.0`, `echoquestdirector` `1.0.0`, `echohudcore` `1.0.0`, `echonotificationcore` `1.0.0`, `echoguidecore` `1.0.0`, `echocodexcore` `1.0.0`, `echolorecore` `1.0.0`, `echomultiblockcore` `1.0.0`, `echoruntimeguard` `1.0.0`, `signalos` `1.0.0`, `signalosexample` `1.0.0`, `echorendercore` `1.0.0`, `echothemecore` `1.3.0`, `echoscreencore` `1.0.0`, `echowiki` `1.0.0`, `echotextureforge` `1.0.0`, `echoholomap` `1.0.0`, `echoindex` `1.0.0`, `echolens` `1.0.0`, `echoarcanacore` `1.0.0`, `echoarcaneindex` `1.0.0`, `echogrimoire` `1.0.0`, `echoorbitalremnants` `1.0.0`, `echonexusprotocol` `1.0.0`, `echoagriculturereclamation` `1.0.0`, `echoworldcore` `1.0.0`, `echoblockworks` `1.0.0`, `echoplayercore` `1.0.0`, `echopowergrid` `1.0.0`, `echosoundcore` `1.0.0`, `echotutorialcore` `1.0.0`, `echorelictech` `1.0.0`, `echoritualcore` `1.0.0`, `echospellcore` `1.0.0`, `echocursecore` `1.0.0`, `echoaetherworks` `1.0.0`, `echoriftworlds` `1.0.0`, `echofamiliarcore` `1.0.0`, `echoweathercore` `1.0.0`, `echorecovery` `1.3.0`, `echonpcore` `1.0.0`, `echobasegrid` `1.0.0`, `echoprimecore` `1.0.0`, `echoarmory` `1.0.0`, `echoblackboxprotocol` `1.0.0`, `echoconvoyprotocol` `1.0.0`, `echoindustrialnexus` `1.0.0`, `echologisticsnetwork` `1.0.0`, `echostationfall` `1.0.0`. This line is generated from `settings.gradle` plus each active module `gradle.properties` and is the validation source for module IDs and versions.

Arcana Division beta modules: `echoarcanacore` `1.0.0`, `echoarcaneindex` `1.0.0`, `echogrimoire` `1.0.0`, `echoritualcore` `1.0.0`, `echospellcore` `1.0.0`, `echocursecore` `1.0.0`, `echoaetherworks` `1.0.0`, `echoriftworlds` `1.0.0`, and `echofamiliarcore` `1.0.0`.





ECHO: Ashfall Protocol starts in a compact armored drop pod with ECHO-7, a damaged emergency operator that is useful before it is comforting. The opening is now a `16x9x16` Blockworks-heavy drop pod with a clear spawn bay, emergency bunk, ECHO control core, Echo crates/cache, ramp, struts, side windows, roof beacons, and discoverable first-night supplies.






The world is not just hostile. It reacts. Radiation mutates after sustained severe exposure, dirty water is an emergency fallback, toxic air drains filters only in hazard pockets, machines need FE power and maintenance, factions remember what you do, and the Nexus route data covers Restore, Destroy, and Control outcomes while final Minecraft-host parity evidence is still pending.







## Current Stack







| Module | Version | Role |



|---|---:|---|



| `echocore` | `1.0.0` | Shared ECHO service registry, profile ledger, diagnostics, hazards, route records, factions, rewards, terminal placement, and Nexus campaign mirrors. |



| `echonetcore` | `1.0.0` | Shared packet registration, sync, action validation, and debug network contracts. |

| `echopresencelink` | `1.0.0` | Client privacy-safe Discord Rich Presence for ECHO and Ashfall activity. |



| `echoruntimeguard` | `1.0.0` | Shared TPS/FPS pressure monitoring, runtime budgets, smart tick hints, and performance diagnostics. |


| `echothemecore` | `1.3.0` | Shared visual/theme/UI skin service for ECHO modules and vanilla surfaces. |


| `echoplayercore` | `1.0.0` | Player utility commands, homes, back, spawn, random teleport, and travel QoL. |

| `echonpcore` | `1.0.0` | Data-driven NPC profiles, dialogue, trades, services, and villager replacement runtime. |


| `echorecovery` | `1.3.0` | Standalone-first graves, death caches, recovery compass, grave keys, and Field Recovery integrations. |

| `echobasegrid` | `1.0.0` | ScreenCore-powered chunk claiming, member permissions, and base protection. |


| `echomissioncore` | `1.0.0` | Shared mission, objective, progression, reward, and Terminal feed engine. |


| `echodatacore` | `1.0.0` | Shared persistent player, world, and team progression data. |



| `echoworldcore` | `1.0.0` | Shared world regions, markers, hazards, discoveries, and world event contracts. |



| `echoterminal` | `1.0.0` | Common terminal shell with Command Deck, What Now, Mission Graph, Route Records, Faction Atlas, Vitals, Reward Inbox, Archives, Baseline, and Addons surfaces. |



| `signalos` | `1.0.0` | Reusable terminal/content framework for chapters, missions, archives, rewards, diagnostics, JSON content, and the soft KubeJS bridge. |



| `signalosexample` | `1.0.0` | Example-only SignalOS addon for Java, JSON, diagnostics, rewards, archives, and KubeJS-friendly integration patterns. |



| `echorendercore` | `1.0.0` | Shared V12 visual-state, animation-profile, particle-profile, preview, composition, screen chrome, QA, and renderer helper layer for polished ECHO/Ashfall assets. |


| `echoashfallprotocol` | `1.0.0` | Main Earth survival campaign: drop pod start, wasteland systems, factions/NPCs, guardians, Prime Relays, Nexus warfront, and finale. |



| `echoorbitalremnants` | `1.0.0` | Post-Nexus orbital continuation: launch chain, route worlds, ECHO-0, orbital factions, route records, diagnostics, and support caches. |



| `echoagriculturereclamation` | 1.0.0 | Complete field-recovery integration chapter for recovered seed capsules, machine menus, persisted processing, contaminated soils, hydroponics, greenhouse zones, pollinator drones, gene stabilization, and chunk-local restoration. |


| `echostationfall` | `1.0.0` | Station ECHO horror chapter with station power, panic pressure, crew logs, station route state, and terminal handoff. |



| `echonexusprotocol` | `1.0.0` | Nexus corruption chapter for charge control, smarter field-map risk planning, stabilized fields, memory recovery, matter rewriting, and Core-state escalation. |



| `echoindustrialnexus` | `1.0.0` | Industrial automation chapter for Thermal Flux, named-fluid recipes, rusted machines, automated filters, salvage processing, MultiblockCore factory ops, upgradeable factories, and factory command. |


| `echologisticsnetwork` | `1.0.0` | Supply crates, labels, loadouts, drone delivery docks, remote requests, faction depots, external endpoints, courier persistence, and operations dashboards. |



| `echoconvoyprotocol` | `1.0.0` | Ruined-Earth vehicles, multiblock depots, cargo/fuel logistics, deterministic Field Ops, HoloMap routes, recovery signals, and convoy operations. |



| `echoholomap` | `1.0.0` | Terminal-integrated command map for regions, routes, hazards, scans, missions, and addon markers. |



| `echoindex` | `1.0.0` | Shared item, recipe, usage, and archive index for Terminal-facing reference surfaces. |



| `echoarcanacore` | `1.0.0` | Shared Aether Signal, spell, ritual, curse, relic, and Arcana provider contracts. |



| `echoarcaneindex` | `1.0.0` | Official magic knowledge browser for Arcana Division pages, discovery states, and Veilbound bridge records. |



| `echogrimoire` | `1.0.0` | Terminal archive shell for Arcana lore, progression, and forbidden knowledge. |



| `echoritualcore` | `1.0.0` | Shared ritual circuits, altar diagnostics, RelicTech stabilization, and relic curse cleansing. |
| `echospellcore` | `1.0.0` | Signal Focus casting, starter spells, Aether Signal costs, cooldowns, and HUD diagnostics. |
| `echocursecore` | `1.0.0` | Persistent curses, symptoms, cleansing hooks, and explicit consequence records. |
| `echoaetherworks` | `1.0.0` | Arcana Division aether machine provider scaffold for condensers, cells, conduits, reactors, fabricators, chargers, engravers, automators, monitors, and purification matrices. |
| `echoriftworlds` | `1.0.0` | Arcana Division rift marker/provider scaffold for cracks, pocket rifts, anchored rifts, void temples, ancient libraries, caches, and fractured ruins. |
| `echofamiliarcore` | `1.0.0` | Arcana Division familiar provider scaffold for wisps, spirit drones, ash hounds, crystal sprites, soul moths, storm ravens, and cursed familiars. |



| `echoarmory` | `1.0.0` | Modular weapons, armor, modules, energy recharge, faction locks, Terminal hooks, and Logistics hooks. |



| `echolens` | `1.0.0` | Smart scanner HUD with local inspection, server-assisted Deep Scan, inventory privacy, and addon context. |



| `echomultiblockcore` | `1.0.0` | Shared data-driven multiblock validation, runtime, robotics, workcell, and scanner/map/terminal contracts. |



| `echoblockworks` | `1.0.0` | First-party decorative, structural, themed block families, palette kits, and rare showcase ruin palettes for ECHO builds. |



| `echoblackboxprotocol` | `1.0.0` | Late-game Blackbox finale with memory fragments, archive dungeons, hostile recordings, boss proofs, and final outcome directives. |







## Core Features







- **Expedition survival:** slow hydration loss, emergency dirty water, zone-based toxic air, radiation, mutations, filter cartridges, RadAway, gas masks, scrubbers, and field medicine.



- **Scrap economy:** debris salvage, substrate harvesting, hand recycling, thermal burning, ore grinding, isotope refining, and machine chains.



- **Recovered biome goods:** ruined worlds still provide paper, dyes, clay, flowers, mushrooms, cactus, sugar cane, bamboo, ocean salvage, ice, animal goods, and new Agriculture Reclamation crops through recipes, POI caches, seed vaults, hydroponics, and faction imports.



- **Power restoration:** micro generators, battery banks, power nodes, thermal arrays, deep-core mining, and the Nexus grid.



- **Mission progression:** ECHO-7 keeps the required route practical through podfall survival, biological adaptation, geological extraction, buried guardian nodes, Prime Relay warfront prep, grid restoration, and the irreversible Nexus choice.



- **Signal Leads:** optional recon records explain crash telemetry, region identity, factions, drone memory, guardians, Nexus context, and ECHO-0 quarantine without blocking the main route or spoiling final outcomes.



- **Factions and intel:** Radwarden Compact, Crashbreak Salvage, and Sporebound Sanctum are the three Echo Core Ashfall factions for reputation, contacts, contracts, POI affinity, patrol pressure, services, dossiers, and drone reconnaissance.



- **World exploration:** scanner-led POI routes across wasteland biomes, toxic swamps, ruined cities, radiation zones, crash scars, cryogenic ruins, Nexus scars, faction hubs, procedural landmarks, and underground guardian arenas with visible surface entrances.



- **ECHO terminal:** Command Deck, What Now, Mission Graph, Protocol Roadmap, Signal Leads, Route Map, POI Atlas, Route Records, Recipe Index, Field Archive, Survival Index, Faction Atlas, Baseline, Vitals, Companion Link, Reward Inbox, Nexus Core, and ORBITAL channels collect lore, objectives, telemetry, recipes, faction reports, route state, and optional expansion status.







## Addon Chapter Chain







The public beta stack documents and stages the full chapter chain, but Agent 1 has not cleared full playable native parity yet. ECHO: Ashfall Protocol remains the entry campaign; ECHO: Orbital Remnants opens after any Ashfall Nexus choice; Agriculture Reclamation can run alongside beta field recovery; Stationfall, Nexus Protocol, Industrial Nexus, and Blackbox Protocol extend the shared ECHO state through their own route, machine, archive, and terminal surfaces.







Addons communicate through `echocore` and `echoterminal` instead of reaching into another chapter's save data. The shared terminal navigation profile API is public addon-facing surface: `TerminalNavigationProfile`, `TerminalNavigationProfiles`, and `TerminalNavigationSection`; the shell organizes pages into Command, Progress, Intel, and System. Recipe-aware addons can also publish process data through the Terminal recipe provider API.







## Quick Start







1. Start a fresh world and secure the compact drop pod. Spawn is at template `(8, 3, 10)` with a clear bay, and the emergency bunk is at `(4, 3, 7)` / `(4, 3, 8)`.



2. Open visible Echo crates/cache for the scanner, water, filters, rations, meds, bottles, torches, basic weapon support, campfire support, and salvage.



3. Craft an early weapon, use the ramp/door to scout safely, shelter before night, and follow ECHO-7 mission prompts.



4. Build the Hand Recycler, Micro Generator, Filter Workbench, Water Purifier, and Battery Bank.



5. Use the Portable Signal Scanner to find a POI, read its route/hazard/prep report, then open Route Map -> POI Atlas to compare that scanner profile against the concrete template signals it can represent.



6. Clear the eight active biome guardians by scanning surface entrances and descending into their buried Gridfall nodes; each guardian reports back into Radwarden, Crashbreak, or Sporebound faction memory.



7. Wake the Nexus campaign, scan six Prime Relays, resolve three relays, survive the Core countermeasure siege, then restore enough grid infrastructure to reach the Nexus Core and choose Restore, Destroy, or Control.



8. Use FIELD > Reclamation to recover seeds and stabilize a small food route, then use ORBITAL / Orbital Command to begin the post-Nexus quarantine expansion and surface the Stationfall, Nexus, Industrial, and Blackbox chapter entries from the shared terminal.







## Requirements







- Minecraft 26.1.2



- NeoForge 26.1.2.29-beta or newer



- Java 25+







Build-truth Gradle `all` stack:







- `echocore` `1.0.0` - required shared API and service mod.



- `echonetcore` `1.0.0` - shared packet bridge and network diagnostics.



- `echoruntimeguard` `1.0.0` - shared runtime budgets, lag diagnostics, and smart tick hints.


- `echothemecore` `1.3.0` - shared visual/theme/UI skin service.


- `echoplayercore` `1.0.0` - player utility commands, homes, back, spawn, random teleport, and travel QoL.

- `echonpcore` `1.0.0` - data-driven NPC profiles, dialogue, trades, services, and villager replacement runtime.


- `echorecovery` `1.3.0` - graves, death caches, recovery compass, grave keys, and Field Recovery integrations.

- `echobasegrid` `1.0.0` - ScreenCore-powered chunk claiming, member permissions, and base protection.


- `echomissioncore` `1.0.0` - shared mission service and objective registry.


- `echodatacore` `1.0.0` - shared persistent player/world/team data service.



- `echoworldcore` `1.0.0` - shared world region, hazard, and marker service.



- `echoterminal` `1.0.0` - shared ECHO Terminal addon.



- `signalos` `1.0.0` - reusable terminal/content framework.



- `signalosexample` `1.0.0` - example-only SignalOS addon.



- `echorendercore` `1.0.0` - shared V12 visual-state, preview, composition, cyberglass chrome, creator QA, and renderer profile support.


- `echoashfallprotocol` `1.0.0` - main campaign addon for the Ashfall modpack.



- `echoorbitalremnants` `1.0.0` - post-Nexus orbital expansion.



- `echoagriculturereclamation` `1.0.0` - field agriculture, persisted machine processing, pollinator drone, and ecology recovery chapter.


- `echostationfall` `1.0.0` - Station ECHO horror chapter.



- `echonexusprotocol` `1.0.0` - Nexus corruption chapter.



- `echoindustrialnexus` `1.0.0` - industrial automation chapter with stack-integrated factory, recipe, mission, Lens, and Logistics-safe surfaces.


- `echologisticsnetwork` `1.0.0` - logistics, storage, loadouts, external endpoints, delivery, and operations dashboard chapter.



- `echoconvoyprotocol` `1.0.0` - ruined-Earth vehicles, multiblock depots, cargo/fuel logistics, Field Ops lifecycles, and HoloMap convoy routes chapter.



- `echoholomap` `1.0.0` - Terminal-integrated command map and marker registry.



- `echoindex` `1.0.0` - shared item, recipe, usage, and archive index.



- `echoarcanacore` `1.0.0` - shared Arcana Core APIs and Aether Signal contracts.



- `echoarcaneindex` `1.0.0` - official Arcana Division knowledge pages built on ECHO: Index.



- `echogrimoire` `1.0.0` - Terminal archive shell for Arcana lore and forbidden pages.



- `echoritualcore` `1.0.0` - Basic Altar ritual slice for RelicTech stabilization and relic curse cleansing.
- `echospellcore` `1.0.0` - Signal Focus starter casting slice for Signal, Aether, and Ash spells.
- `echocursecore` `1.0.0` - Live Echo Rot/Glass Veins curse persistence and RitualCore cleansing bridge.
- `echoaetherworks` `1.0.0` - Arcana Division aether machine provider scaffold for future machine blocks and network rules.
- `echoriftworlds` `1.0.0` - Arcana Division rift marker provider scaffold for future rift world content.
- `echofamiliarcore` `1.0.0` - Arcana Division familiar provider scaffold for future bonded companion content.



- `echoarmory` `1.0.0` - combat, gear, modules, and loadout support chapter.



- `echolens` `1.0.0` - smart scanner HUD with server-assisted Deep Scan and addon-context inspection layer.



- `echomultiblockcore` `1.0.0` - shared multiblock validation, runtime, and robotics framework.



- `echoblockworks` `1.0.0` - themed block family, decoration catalog, palette kit, and rare showcase site palette module.



- `echoblackboxprotocol` `1.0.0` - late-game Blackbox finale.







Build all release jars from the workspace root:







```powershell



.\gradlew.bat build -PechoAddonSet=all



```







Run the full release verification gate:







```powershell



.\gradlew.bat verifyEchoRelease --warning-mode all



```







Copy the verified jars into a local CurseForge or launcher profile only when doing local modpack QA:





```powershell


.\gradlew.bat -PechoModpackModsDir="C:/path/to/Ashfall/mods" copyEchoJarsToModpack verifyEchoModpackProfile


```





`verifyEchoRelease` is the pure repo gate and does not require a local modpack profile. `copyEchoJarsToModpack`, `checkEchoModJarSet`, and `verifyEchoModpackProfile` require `-PechoModpackModsDir="C:/path/to/Ashfall/mods"`; no historical default path is treated as the Ashfall target.






Release artifacts:







- `build/libs/echoashfallprotocol-1.0.0.jar`



- `core/echocore/build/libs/echocore-1.0.0.jar`



- `addons/echonetcore/build/libs/echonetcore-1.0.0.jar`


- `addons/echoruntimeguard/build/libs/echoruntimeguard-1.0.0.jar`


- `addons/echorecovery/build/libs/echorecovery-1.3.0.jar`


- `addons/echomissioncore/build/libs/echomissioncore-1.0.0.jar`


- `addons/echodatacore/build/libs/echodatacore-1.0.0.jar`



- `addons/echoworldcore/build/libs/echoworldcore-1.0.0.jar`



- `addons/echoterminal/build/libs/echoterminal-1.0.0.jar`



- `addons/echosignalos/build/libs/signalos-1.0.0.jar`



- `addons/signalosexample/build/libs/signalosexample-1.0.0.jar`



- `addons/echorendercore/build/libs/echorendercore-1.0.0.jar`


- `addons/echoorbitalremnants/build/libs/echoorbitalremnants-1.0.0.jar`



- `addons/echoagriculturereclamation/build/libs/echoagriculturereclamation.jar`


- `addons/echostationfall/build/libs/echostationfall-1.0.0.jar`



- `addons/echonexusprotocol/build/libs/echonexusprotocol-1.0.0.jar`



- `addons/echoindustrialnexus/build/libs/echoindustrialnexus-1.0.0.jar`


- `addons/echologisticsnetwork/build/libs/echologisticsnetwork-1.0.0.jar`



- `addons/echoconvoyprotocol/build/libs/echoconvoyprotocol-1.0.0.jar`



- `addons/echoholomap/build/libs/echoholomap-1.0.0.jar`



- `addons/echoindex/build/libs/echoindex-1.0.0.jar`



- `addons/echoarcanacore/build/libs/echoarcanacore-1.0.0.jar`



- `addons/echoarcaneindex/build/libs/echoarcaneindex-1.0.0.jar`



- `addons/echogrimoire/build/libs/echogrimoire-1.0.0.jar`



- `addons/echoritualcore/build/libs/echoritualcore-1.0.0.jar`
- `addons/echospellcore/build/libs/echospellcore-1.0.0.jar`
- `addons/echocursecore/build/libs/echocursecore-1.0.0.jar`
- `addons/echoaetherworks/build/libs/echoaetherworks-1.0.0.jar`
- `addons/echoriftworlds/build/libs/echoriftworlds-1.0.0.jar`
- `addons/echofamiliarcore/build/libs/echofamiliarcore-1.0.0.jar`



- `addons/echoarmory/build/libs/echoarmory-1.0.0.jar`



- `addons/echolens/build/libs/echolens-1.0.0.jar`



- `addons/echomultiblockcore/build/libs/echomultiblockcore-1.0.0.jar`



- `addons/echoblockworks/build/libs/echoblockworks-1.0.0.jar`



- `addons/echoblackboxprotocol/build/libs/echoblackboxprotocol-1.0.0.jar`







Verification commands:







```powershell



python -m pip install -r tools\requirements.txt



python tools\validate_resources.py --addon-set all



python tools\validate_gameplay_data.py



.\gradlew.bat build -PechoAddonSet=all



```







Expected verification result: every required build and GameTest task reports clean completion across Core, NetCore, MissionCore, DataCore, WorldCore, Terminal, SignalOS, SignalOS Example, ECHO: Ashfall Protocol, Orbital, Agriculture Reclamation, Stationfall, Nexus, Industrial, Logistics, Convoy, HoloMap, Armory, and Blackbox. Run `verifyEchoModpackProfile` only after the local modpack destination is configured for Ashfall.


`validate_resources.py` also runs the release-polish checks for mojibake, stale terminal/drone references, plural structure resource paths, placeholder markers, and uppercase real resource namespaces.







## ECHO Core Integration Contract







Addons should communicate through `echocore` instead of reaching directly into another chapter's save data. Current shared services cover pack mode/profile state, progress ledgers, diagnostics, hazard telemetry, route records, faction definitions/profiles/standing/contracts/actions, POI affinity, NPC dialogue roles, recovery hooks, terminal placement, terminal reward storage, intel mirroring, and Nexus path/campaign status. Providers are expected to be tolerant: duplicate IDs are ignored, failed providers are logged, and the owning mod remains responsible for validating actions and rewards server-side.







Terminal addons should register navigation through the public `echoterminal` profile types rather than special-casing the screen. Explicit `TerminalNavigationProfile` registration is the chapter ownership contract; older chrome group fallbacks exist only as compatibility. Recipe-aware addons should register `TerminalRecipeProvider` implementations with `TerminalRecipeRegistry`, using `TerminalRecipeCategory`, `TerminalRecipeEntry`, `TerminalRecipeSlot`, `TerminalRecipeNote`, and `TerminalRecipeSnapshot` so the shared Recipe Index can search outputs, uses, machine slots, catalysts, info notes, and locked schematic hints. A chapter owns its actions, rewards, recipe authority, and persistence; Terminal owns presentation and routing.







## Release Operations







`tools/echo-release-terminal` is a private local release-ops dashboard. It is useful for QA state and release drafting, but it is not part of the published mod artifact set. Keep it buildable with `npm.cmd run build` before public release.







## Documentation







- `MODPACK_OVERVIEW.md` - full systems, mechanics, factions, progression, and lore overview.



- `LORE_BIBLE.md` - shared tactical-eerie canon and writing rules for missions, archives, docs, and addon chapters.


- `GETTING_STARTED.md` - player-facing walkthrough from drop pod to Nexus choice.


- `PROCEDURAL_STRUCTURES.md` - POI and structure generation reference.


- `docs/release_process.md` - release checklist, version contract, and CI release artifact expectations.


- `CHANGELOG_1.0.0.md` - current public beta changelog for the active ECHO ecosystem.


- `docs/RELEASE_NOTES_1.0.0.md` - current public beta release notes.


- `docs/KNOWN_ISSUES_1.0.0.md` - current public beta known issues.


- `docs/official_packs/ashfall/CHANGELOG_1.0.0.md` - Ashfall Official Pack #1 public beta changelog.


- `docs/arcana_division/overview.md` - current Arcana Division beta overview for Arcana Core, Arcane Index, Grimoire, RitualCore, SpellCore, CurseCore, AetherWorks, RiftWorlds, FamiliarCore, and RelicTech bridges.


- `docs/releases/ashfall_1.0.0_smoke_test.md` - Ashfall first-world release smoke checklist and gate log.







## Version Contract







Releases follow an explicit version contract so tags, module versions, and release names stay aligned:







- Git tags must use `v<major>.<minor>.<patch>` with optional prerelease suffixes (for example `v1.0.1-beta.1`).



- The numeric part of the tag must match each module's release version for that cut.



- GitHub release names should reuse the exact tag value for traceability.







See `docs/release_process.md` for the full release workflow and manifest checks.







## 1.0.0 Full Stack Smoke Checklist







Start a fresh world, keep the default ECHO: Ashfall Protocol worldgen, and test the first night without using vanilla forests as your main route. The intended opening is debris, ruined vegetation, dead/charred trees, pod salvage, and ECHO-7 mission guidance.







What to test first:







- First 10 minutes: compact pod spawn, visible lockers, sticks/fiber, ruined planks, first weapon, shelter, clean water, emergency dirty water, and ECHO terminal guidance.



- First machine loop: Hand Recycler, Micro Generator, Filter Workbench, Water Purifier, and Battery Bank.



- Resource recovery: JEI custom machine categories, Terminal Recipe Index coverage, recovered biome goods, healthy sapling rarity, and route-specific POI cache identity.



- Agriculture Reclamation: seed capsule recovery, mature-only crop drops, soil purifier no-op safety, hydroponic persistence, gene stabilization, greenhouse zone scans, Pollinator Drone service, and ecology scanner restoration pressure.



- Scanner loop: Portable Signal Scanner reports the actual site, hazard profile, prep kit, reward track, distance, direction, and field-log status.



- Terminal loop: What Now, Mission Graph, Route Records, Faction Atlas, Vitals, Reward Inbox, Archives, and Addons should agree with the owning chapter state.



- Factions and drones: Scout Drone fallback, ECHO companion repair/modes, faction NPC dialogue, contracts, standing, trader rewards, raids, and intel reports.



- Nexus path: buried guardian nodes, Prime Relays, Core countermeasure siege, Power Nodes, final choice, path objectives, Archives arena entry/return, Warden defeat, final epilogue, Orbital unlock, and Stationfall/Nexus/Industrial/Blackbox chapter entry visibility.







Known 1.0.0 watchpoints:







- Old worlds may not contain the newest POI/resource distribution until new chunks generate, but old POI progress ids are normalized through compatibility aliases.



- Old worlds may lose legacy Ashfall-owned terminal blocks; the supported terminal block is now `echoterminal:echo_terminal`.



- The standalone drone menu path is intentionally not exposed; drone control is through the ECHO terminal and direct drone interaction.



- Some audio cues intentionally reuse vanilla sound events in this release.







Bug report format:







```text



Version / mod list:



World age and seed:



What you expected:



What happened:



Steps to reproduce:



Screenshots or crash report:



Coordinates / biome / POI:



```







## Compatibility







- **ECHO addon chapters:** Orbital Remnants, Agriculture Reclamation, Stationfall, Nexus Protocol, Industrial Nexus, Logistics Network, Convoy Protocol, Armory, and Blackbox Protocol are included in the full Gradle stack and surface through ECHO Core plus ECHO Terminal.



- **Multiplayer:** designed for solo and server packs; fresh-start, join, shutdown, UI/surface, reward, and relog smoke evidence must be collected before public copy should promise broad server readiness.



- **Recipe viewers:** JEI support is optional and includes custom ECHO categories for hardcoded Ashfall machine/process recipes. ECHO Terminal also includes a provider-backed Recipe Index with searchable ECHO items, Recipes/Uses modes, category filters, item detail panes, process notes, and locked schematic hints. Normal crafting/smelting recipes still appear through vanilla recipe data.







## Newly Active Service Addons (Audit Pass)







The explicit public stack also includes these active service addons in the current docs table: `echopowergrid` `1.0.0`, `echosoundcore` `1.0.0`, `echotutorialcore` `1.0.0`, `echorelictech` `1.0.0`, `echoritualcore` `1.0.0`, `echospellcore` `1.0.0`, `echocursecore` `1.0.0`, `echoaetherworks` `1.0.0`, `echoriftworlds` `1.0.0`, `echofamiliarcore` `1.0.0`, and `echoweathercore` `1.0.0`. They are included in `settings.gradle` and are tracked in `docs/reports/ECHO_ECOSYSTEM_AUDIT.md` with honest partial/blocked notes.



## 1.0.0 Creator Platform Quickstart



1. Install required dependencies: echocore, echonetcore.

2. Launch the game or tool and confirm the module appears in `metadata/modules/echoashfallprotocol.json`.

3. First action: open the module UI, command, keybind, or primary block/item.

4. Common issue: missing optional integrations should reduce features, not crash.

5. Ashfall behavior: this module is part of the official Ashfall profile.



Public release page: `docs/release_pages/echoashfallprotocol.md`.

## 1.0.0 Creator Tooling Active Modules

The active Gradle workspace also includes `echoscriptcore` (`1.0.0`) and `echocreatorcore` (`1.0.0`) as creator-platform tooling modules. They are not Ashfall requirements; they support JSON-first authoring, drafts, validation, and creator diagnostics for custom ECHO-powered packs.
