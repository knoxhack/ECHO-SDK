package com.example.configexample;

import dev.echo.nativeplatform.contracts.EchoNativeAddon;
import dev.echo.nativeplatform.contracts.EchoNativeAddonRuntime;

public class ConfigExampleAddon implements EchoNativeAddon {
    @Override
    public void onInitialize(EchoNativeAddonRuntime runtime) {
        AddonConfig config = AddonConfig.load("configexample");
        runtime.registerService("configexample:config_service", config);
    }
}
