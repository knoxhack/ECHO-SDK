package dev.echo.samples.hello;

import dev.echo.api.addon.EchoAddon;
import dev.echo.api.addon.EchoAddonDescriptor;
import dev.echo.api.addon.EchoAddonId;
import dev.echo.api.addon.EchoAddonKind;
import dev.echo.api.addon.EchoAddonRole;
import dev.echo.api.addon.EchoAddonRuntimeTarget;
import dev.echo.api.addon.EchoAddonVersion;
import dev.echo.api.block.EchoBlockDescriptor;
import dev.echo.api.block.EchoBlockId;
import dev.echo.api.block.EchoBlockSettings;
import dev.echo.api.context.EchoRegistryContext;
import dev.echo.api.item.EchoItemDescriptor;
import dev.echo.api.item.EchoItemId;
import dev.echo.api.item.EchoItemSettings;
import dev.echo.api.recipe.EchoIngredient;
import dev.echo.api.recipe.EchoRecipeDescriptor;
import dev.echo.api.recipe.EchoRecipeId;
import dev.echo.api.recipe.EchoRecipeOutput;
import dev.echo.api.recipe.EchoRecipeType;
import dev.echo.api.registry.EchoRegistryEntry;
import dev.echo.api.registry.EchoRegistryKey;
import java.util.List;
import java.util.Set;

public final class HelloContentAddon implements EchoAddon {
    private static final EchoAddonDescriptor DESCRIPTOR = new EchoAddonDescriptor(
            new EchoAddonId("hello_content_addon"),
            new EchoAddonVersion("0.1.0"),
            "Hello Content Add-on",
            EchoAddonKind.CONTENT,
            EchoAddonRole.SAMPLE,
            Set.of(
                    EchoAddonRuntimeTarget.ECHO_NATIVE,
                    EchoAddonRuntimeTarget.NEOFORGE,
                    EchoAddonRuntimeTarget.ECHO_RUNTIME_STANDALONE
            )
    );

    @Override
    public EchoAddonDescriptor descriptor() {
        return DESCRIPTOR;
    }

    @Override
    public void register(EchoRegistryContext context) {
        context.registrar().register("items", new EchoRegistryEntry<>(
                new EchoRegistryKey<>("hello_content_addon:echo_shard"),
                new EchoItemDescriptor(
                        new EchoItemId("hello_content_addon:echo_shard"),
                        EchoItemSettings.defaults(),
                        "item.hello_content_addon.echo_shard"
                )
        ));
        context.registrar().register("blocks", new EchoRegistryEntry<>(
                new EchoRegistryKey<>("hello_content_addon:echo_block"),
                new EchoBlockDescriptor(
                        new EchoBlockId("hello_content_addon:echo_block"),
                        EchoBlockSettings.defaults(),
                        "block.hello_content_addon.echo_block"
                )
        ));
        context.registrar().register("recipes", new EchoRegistryEntry<>(
                new EchoRegistryKey<>("hello_content_addon:echo_block"),
                new EchoRecipeDescriptor(
                        new EchoRecipeId("hello_content_addon:echo_block"),
                        EchoRecipeType.CRAFTING_SHAPELESS,
                        List.of(new EchoIngredient(Set.of("hello_content_addon:echo_shard"), 4)),
                        new EchoRecipeOutput("hello_content_addon:echo_block", 1)
                )
        ));
    }
}
