package com.example.eventexample;

import dev.echo.nativeplatform.testkit.EchoNativeTestLoader;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class EventExampleTest {
    @Test
    public void testEventBusRegistered() {
        EchoNativeTestLoader loader = new EchoNativeTestLoader();
        loader.loadAddon("eventexample");
        assertTrue(loader.isServiceRegistered("eventexample:event_bus"));
    }
}
