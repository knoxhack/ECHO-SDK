# ECHO Artifact Ownership

GitHub stores source, release assets, and attestations. ECHO stores product policy, trust, compatibility, install UX, and the canonical Release Index.

| Repository | Owns | Release Index role |
| --- | --- | --- |
| `knoxhack/ECHO-Launcher` | Desktop launcher installers and updater metadata. | Product entry for launcher self-update and deep-link handling. |
| `knoxhack/ECHO-Modules` | First-party module source plus `.echo-addon`, `-neoforge.jar`, `-standalone.jar`, and `-sources.jar` release assets. | Module entries consumed by all Ashfall editions. |
| `knoxhack/ECHO-Ashfall-Native-Edition` | Native Ashfall pack manifest and native pack artifacts. | Modpack entry targeting `.echo-addon` module artifacts. |
| `knoxhack/ECHO-Ashfall-NeoForge-Edition` | NeoForge Ashfall pack manifest and pack artifacts. | Modpack entry targeting `-neoforge.jar` module artifacts. |
| `knoxhack/ECHO-Ashfall-Standalone-Edition` | Standalone Ashfall pack manifest and pack artifacts. | Modpack entry targeting `-standalone.jar` module artifacts. |
| `knoxhack/ECHO-Release-Index` | Canonical catalog, channels, trust tiers, blocks, compatibility, and exact artifact metadata. | Source of truth for install and update resolution. |
| `knoxhack/ECHO-SDK` | Schemas, templates, validator/build tools, docs, and examples. | Contract source used by validators and publishing tooling. |
| `knoxhack/ECHO-Addons-Studio` | Third-party authoring and release preparation app. | Product entry plus publisher workflow client. |
| `knoxhack/ECHO-Developer-Studio` | First-party developer tooling app. | Product entry for studio updates. |
| `knoxhack/ECHO-Native-Platform` | Native runtime, loader, contracts, diagnostics, and PackOS integration. | Runtime/product entries for native pack resolution. |
| `knoxhack/ECHO-Standalone-Runtime` | Standalone runtime shell and runtime modules. | Runtime/product entries for standalone pack resolution. |
| `knoxhack/ECHO-Platform-Website` | Docs, directory, downloads, and install buttons. | Reads Release Index and emits `echo://` deep links. |

Release assets are installable only when Release Index metadata names exact files, SHA-256 hashes, source repository, release tag, trust tier, validation state, and compatibility targets.
