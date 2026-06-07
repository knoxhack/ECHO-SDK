package com.example.eventexample;

import dev.echo.nativeplatform.contracts.EchoNativeAddon;
import dev.echo.nativeplatform.contracts.EchoNativeAddonRuntime;
import dev.echo.api.event.EchoEventBus;
import dev.echo.api.event.EchoEventType;

public class EventExampleAddon implements EchoNativeAddon {
    @Override
    public void onInitialize(EchoNativeAddonRuntime runtime) {
        EchoEventBus bus = EchoEventBus.create("eventexample");
        bus.subscribe(EchoEventType.PLAYER_JOIN, event -> {
            // Handle player join
        });
        runtime.registerService("eventexample:event_bus", bus);
    }
}
