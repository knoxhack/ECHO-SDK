package com.example.myaddon;

import dev.echo.nativeplatform.testkit.EchoNativeTestLoader;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class MyAddonTest {
    @Test
    public void testBootstrap() {
        EchoNativeTestLoader loader = new EchoNativeTestLoader();
        loader.loadAddon("myaddon");
        assertTrue(loader.isAddonLoaded("myaddon"));
    }
}
