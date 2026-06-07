package com.example.worldgenexample;

import dev.echo.nativeplatform.contracts.EchoNativeAddon;
import dev.echo.nativeplatform.contracts.EchoNativeAddonRuntime;

public class WorldgenExampleAddon implements EchoNativeAddon {
    @Override
    public void onInitialize(EchoNativeAddonRuntime runtime) {
        WorldgenFeature feature = new WorldgenFeature("worldgenexample:example_ore");
        runtime.registerService("worldgenexample:worldgen_service", feature);
    }
}
