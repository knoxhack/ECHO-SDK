package com.example.screenhudexample;

import dev.echo.nativeplatform.testkit.EchoNativeTestLoader;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ScreenHudExampleTest {
    @Test
    public void testHudServiceRegistered() {
        EchoNativeTestLoader loader = new EchoNativeTestLoader();
        loader.loadAddon("screenhudexample");
        assertTrue(loader.isServiceRegistered("screenhudexample:hud_service"));
    }
}
