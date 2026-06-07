package com.example.configexample;

import dev.echo.nativeplatform.testkit.EchoNativeTestLoader;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ConfigExampleTest {
    @Test
    public void testConfigServiceRegistered() {
        EchoNativeTestLoader loader = new EchoNativeTestLoader();
        loader.loadAddon("configexample");
        assertTrue(loader.isServiceRegistered("configexample:config_service"));
    }
}
