package com.example.registryexample;

import dev.echo.nativeplatform.contracts.EchoNativeAddon;
import dev.echo.nativeplatform.contracts.EchoNativeAddonRuntime;
import dev.echo.api.registry.EchoRegistry;
import dev.echo.api.registry.EchoRegistryKey;
import dev.echo.api.block.EchoBlockDescriptor;

public class RegistryExampleAddon implements EchoNativeAddon {
    @Override
    public void onInitialize(EchoNativeAddonRuntime runtime) {
        EchoRegistry<EchoBlockDescriptor> blocks = EchoRegistry.create("registryexample:blocks");
        blocks.register(EchoRegistryKey.of("registryexample:example_block"),
            new EchoBlockDescriptor("registryexample:example_block"));
        runtime.registerService("registryexample:block_registry", blocks);
    }
}
