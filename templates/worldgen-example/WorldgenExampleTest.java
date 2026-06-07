package com.example.worldgenexample;

import dev.echo.nativeplatform.testkit.EchoNativeTestLoader;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class WorldgenExampleTest {
    @Test
    public void testWorldgenServiceRegistered() {
        EchoNativeTestLoader loader = new EchoNativeTestLoader();
        loader.loadAddon("worldgenexample");
        assertTrue(loader.isServiceRegistered("worldgenexample:worldgen_service"));
    }
}
