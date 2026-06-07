package com.example.mynativemodule;

import dev.echo.nativeplatform.testkit.EchoNativeTestLoader;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class NativeModuleTest {
    @Test
    public void testServiceRegistered() {
        EchoNativeTestLoader loader = new EchoNativeTestLoader();
        loader.loadAddon("mynativemodule");
        assertTrue(loader.isServiceRegistered("mynativemodule:native_service"));
    }
}
