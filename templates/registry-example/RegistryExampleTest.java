package com.example.registryexample;

import dev.echo.nativeplatform.testkit.EchoNativeTestLoader;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class RegistryExampleTest {
    @Test
    public void testBlockRegistered() {
        EchoNativeTestLoader loader = new EchoNativeTestLoader();
        loader.loadAddon("registryexample");
        assertTrue(loader.isServiceRegistered("registryexample:block_registry"));
    }
}
