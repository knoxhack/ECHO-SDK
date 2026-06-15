# Native AdapterCore Guide

AdapterCore bridges module contracts across native, NeoForge, and standalone runtimes.

Use descriptor runtime targets to keep behavior explicit and avoid loading runtime-specific code in the wrong environment.

## Receipt-Backed Gameplay Mutations

Gameplay mutations must return typed evidence. A `MUTATED` AdapterCore result is release-proof only when it includes a `NativeMutationReceipt` with before/after host state, save-write evidence, HUD/event evidence, or packet/event evidence.

Use `EchoAdapterCoreGameplayMutationService` when a Native backend is available. It accepts `EchoNativeServiceMutation` requests for inventory, player state, world blocks, structures, block entities, capabilities, save data, HUD, packets, and events, and returns `EchoNativeMutationReceipt` records. Reflection fallbacks are allowed during beta compatibility only when they can produce an equivalent typed receipt; otherwise they should report `UNSUPPORTED`.

Queued handoffs and diagnostic-only reports are useful telemetry, but they do not count as release proof. Ashfall first-join and machine flows are the reference implementation for this model.
