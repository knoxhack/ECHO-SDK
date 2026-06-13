# Example Addon Walkthrough: EchoExampleMod

This walkthrough builds a minimal ECHO Native addon from scratch. It declares a content registration through the typed Native registry host, packages a `.echo-addon`, and remains independent from NeoForge and Native Loader internals.

## 1. Create the Project

Use the new-addon template:

```bash
./gradlew createEchoNativeAddon \
  --id echoexample \
  --name "Echo Example Mod" \
  --package com.example.echoexample \
  --policy NATIVE
```

## 2. Descriptor

`src/main/resources/META-INF/echo.mod.json`

```json
{
  "schema": "echo.mod.v1",
  "id": "echoexample",
  "name": "Echo Example Mod",
  "version": "1.0.0-RC1",
  "entrypoint": "com.example.echoexample.EchoExampleAddon",
  "side": "common",
  "provides": ["echoexample.content"],
  "access": {
    "nativeClasspath": ["addon.jar"]
  },
  "apiStability": "beta"
}
```

## 3. Main Class

`src/main/java/com/example/echoexample/EchoExampleAddon.java`

```java
package com.example.echoexample;

import dev.echo.nativeplatform.contracts.*;

public class EchoExampleAddon implements EchoNativeModuleEntrypoint {
    @Override
    public void registerServices(EchoNativeModuleLoadContext context) {
        context.registerService("echoexample:content_registry", new ExampleContentService(), "registry");
    }

    @Override
    public void registerContent(EchoNativeModuleLoadContext context) {
        EchoNativeServiceMutation mutation = EchoNativeServiceMutation.of(
                "echoexample", "registry", "declare_content", "echoexample:example_item", EchoNativeRuntimeSide.COMMON);
        context.serviceRegistry()
                .service("echo.native.registry", EchoNativeRegistryService.class)
                .map(registry -> registry.register(mutation))
                .ifPresent(context::recordMutation);
    }
}
```

## 4. Block and Item

```java
public class ExampleBlock extends Block {
    public ExampleBlock() {
        super(Properties.of().strength(2.0f).requiresCorrectToolForDrops());
    }
}

public class ExampleItem extends Item {
    public ExampleItem() {
        super(new Properties().stacksTo(64));
    }
}
```

## 5. Datapack Recipe

`src/main/resources/data/echoexample/recipe/example_smelt.json`

```json
{
  "type": "minecraft:smelting",
  "ingredient": { "item": "echoexample:example_block" },
  "result": { "id": "echoexample:example_item" },
  "experience": 0.5,
  "cookingtime": 200
}
```

## 6. Test Fixture

`src/test/java/com/example/echoexample/EchoExampleAddonTest.java`

```java
import dev.echo.nativeplatform.testkit.*;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class EchoExampleAddonTest {
    @Test
    public void testBootstrap() {
        EchoNativeSdkTestkit.Environment env = EchoNativeSdkTestkit.common("echoexample");
        EchoNativeModuleLoadContext context = env.loadEntrypoint(new EchoExampleAddon());
        assertTrue(context.serviceRegistry().hasService("echoexample:content_registry"));
        env.goldenParity().requireMutatedServices("echo.native.registry");
        env.goldenParity().requireOnlyTypedReceipts();
    }
}
```

## 7. Build and Package

```bash
./gradlew build
./gradlew packageEchoNativeAddon
```

Output:
- `build/echo-native/addons/echoexample-1.0.0-RC1.echo-addon`
- `build/reports/echoexample-parity.json`

## 8. Install and Verify

Install the `.echo-addon` through the launcher-managed addon store or a release-mode product profile. Do not install the development jar from `build/classes` or an IDE classpath.

Launch and run:

```
/give @p echoexample:example_item
```

If Index is installed, check `/index` for the new documentation page.

## Key Takeaways

- The descriptor drives loader behavior; code only runs after validation passes.
- Optional integrations keep the addon standalone-safe.
- Datapacks are first-class; prefer JSON over hardcoded recipes.
- Tests use `echo-native-testkit` for fast, headless validation.
