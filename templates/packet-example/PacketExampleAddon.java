package com.example.packetexample;

import dev.echo.nativeplatform.contracts.EchoNativeAddon;
import dev.echo.nativeplatform.contracts.EchoNativeAddonRuntime;
import dev.echo.api.event.EchoEventBus;
import dev.echo.api.event.EchoEventType;

public class PacketExampleAddon implements EchoNativeAddon {
    @Override
    public void onInitialize(EchoNativeAddonRuntime runtime) {
        EchoEventBus bus = EchoEventBus.create("packetexample");
        bus.subscribe(EchoEventType.CUSTOM_PACKET, event -> {
            MyPacket payload = event.getPayload(MyPacket.class);
            // process payload
        });
        runtime.registerService("packetexample:packet_service", bus);
    }

    public static record MyPacket(String message, int value) {}
}
