package com.example.mynativemodule;

import dev.echo.nativeplatform.contracts.EchoNativeAddon;
import dev.echo.nativeplatform.contracts.EchoNativeAddonRuntime;
import dev.echo.api.registry.EchoRegistry;
import dev.echo.api.registry.EchoRegistryRegistrar;

public class NativeModule implements EchoNativeAddon {
    @Override
    public void onInitialize(EchoNativeAddonRuntime runtime) {
        EchoRegistryRegistrar registrar = EchoRegistryRegistrar.create("mynativemodule");
        runtime.registerService("mynativemodule:native_service", new NativeService(registrar));
    }
}
