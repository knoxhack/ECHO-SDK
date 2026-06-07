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

`src/main/resources/META-INF/echo-native-addon.descriptor.json`

```json
{
  "schema": "echo.native.descriptor.v1",
  "id": "echoexample",
  "name": "Echo Example Mod",
  "version": "1.0.0",
  "nativePolicy": "NATIVE",
  "entryPoints": {
    "native": "com.example.echoexample.EchoExampleAddon"
  },
  "services": ["echoexample:content_registry"],
  "optionalIntegrations": ["echoindex"],
  "side": "BOTH"
}
```

## 3. Main Class

`src/main/java/com/example/echoexample/EchoExampleAddon.java`

```java
package com.example.echoexample;

import dev.echo.nativeplatform.contracts.*;
import dev.echo.core.services.*;

public class EchoExampleAddon implements EchoNativeAddon {
    @Override
    public void onInitialize(EchoNativeAddonRuntime runtime) {
        // Register block and item
        EchoCoreServices.contentRegistry().registerBlock("echoexample:example_block", new ExampleBlock());
        EchoCoreServices.contentRegistry().registerItem("echoexample:example_item", new ExampleItem());

        // Register optional Index provider
        EchoOptionalServices.index().ifPresent(index -> {
            index.registerProvider(new ExampleIndexProvider());
        });

        runtime.registerService("echoexample:content_registry", new ExampleContentService());
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
./gradlew packageAddon
```

Output:
- `build/libs/echoexample-1.0.0-echo-native.jar`
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
