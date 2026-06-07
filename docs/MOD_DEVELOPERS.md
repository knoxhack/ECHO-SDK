# Mod Developers



Depend on ECHO Core for shared service contracts and use optional lookups for every cross-addon connection.



## Gradle



Use ECHO Core as an implementation dependency. Optional addon integrations should be `compileOnly` with runtime guarded by `EchoIntegrations` or `EchoOptionalServices`.



```groovy

dependencies {

    implementation project(':echocore')

    compileOnly project(':echoterminal')

    compileOnly project(':echoindex')

}

```



## Services



Prefer:



```java

EchoOptionalServices.terminalOrNoOp().registerDashboardCard(cardId);

EchoOptionalServices.index().ifPresent(index -> index.refresh());

```



Avoid direct `ModList` checks outside setup code unless the integration is too small to need a service.



## Provider Rules



- Providers must be duplicate-safe and id-stable.

- Provider failures should log and no-op, never crash the addon.

- Do not read or write another addon's saved data directly.

- Use ECHO Core registries, datapack schemas, service contracts, and optional bridges.



## Ashfall



Ashfall is a flagship content pack. Generic addons should expose generic APIs and fallback content; Ashfall modules register Ashfall missions, themes, map layers, scans, sound rules, route records, and lore into those APIs.



## 1.3.4 Public API Labels



Use [API_STABILITY.md](API_STABILITY.md) as the source of truth for Stable/Beta/Experimental/Internal API surfaces. Use [OPTIONAL_INTEGRATIONS.md](OPTIONAL_INTEGRATIONS.md) for safe no-op integration patterns.



Minimal optional provider example:



```java

public void registerEchoIntegrations() {

    EchoCoreServices.indexService().registerProvider(myProvider);

    EchoCoreServices.holoMapService().registerMarkerProvider(myMarkers);

}

```



The call must remain safe if Index or HoloMap is not installed because Core supplies no-op services for absent optional integrations.

