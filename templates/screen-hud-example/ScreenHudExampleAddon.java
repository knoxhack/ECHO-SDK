package com.example.screenhudexample;

import dev.echo.nativeplatform.contracts.EchoNativeAddon;
import dev.echo.nativeplatform.contracts.EchoNativeAddonRuntime;

public class ScreenHudExampleAddon implements EchoNativeAddon {
    @Override
    public void onInitialize(EchoNativeAddonRuntime runtime) {
        HudOverlay overlay = new HudOverlay();
        runtime.registerService("screenhudexample:hud_service", overlay);
    }
}
