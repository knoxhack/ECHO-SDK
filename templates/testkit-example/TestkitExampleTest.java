package com.example.testkitexample;

import dev.echo.nativeplatform.testkit.EchoNativeTestLoader;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestkitExampleTest {
    @Test
    public void testCounterService() {
        EchoNativeTestLoader loader = new EchoNativeTestLoader();
        loader.loadAddon("testkitexample");
        assertTrue(loader.isServiceRegistered("testkitexample:counter_service"));

        CounterService svc = loader.getService("testkitexample:counter_service", CounterService.class);
        svc.increment();
        assertEquals(1, svc.getCount());
    }
}
