# Example Addon Walkthrough: EchoExampleMod

This walkthrough builds a minimal ECHO Native addon from scratch. It registers a block, an item, a datapack-driven recipe, and an optional Index integration.

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
        context.recordMutation(EchoNativeMutationReceipt.mutated("echoexample:content_registry", mutation, 1));
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
        EchoNativeTestLoader loader = new EchoNativeTestLoader();
        loader.loadAddon("echoexample");
        assertTrue(loader.isServiceRegistered("echoexample:content_registry"));
        assertEquals(2, loader.registeredContentCount());
    }
}
```

## 7. Build and Package

```bash
./gradlew build
./gradlew validateAddon
./gradlew packageEchoNativeAddon
```

Output:
- `build/echo-native/addons/echoexample-1.0.0-RC1.echo-addon`
- `build/reports/echoexample-parity.json`

## 8. Install and Verify

Drop the jar into `mods/`. Launch and run:

```
/give @p echoexample:example_item
```

If Index is installed, check `/index` for the new documentation page.

## Key Takeaways

- The descriptor drives loader behavior; code only runs after validation passes.
- Optional integrations keep the addon standalone-safe.
- Datapacks are first-class; prefer JSON over hardcoded recipes.
- Tests use `EchoNativeTestLoader` for fast, headless validation.
