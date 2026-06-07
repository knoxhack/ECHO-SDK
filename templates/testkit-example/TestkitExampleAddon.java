package com.example.testkitexample;

import dev.echo.nativeplatform.contracts.EchoNativeAddon;
import dev.echo.nativeplatform.contracts.EchoNativeAddonRuntime;

public class TestkitExampleAddon implements EchoNativeAddon {
    @Override
    public void onInitialize(EchoNativeAddonRuntime runtime) {
        CounterService service = new CounterService();
        runtime.registerService("testkitexample:counter_service", service);
    }
}
