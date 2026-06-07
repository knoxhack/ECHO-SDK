package com.example.packetexample;

import dev.echo.nativeplatform.testkit.EchoNativeTestLoader;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PacketExampleTest {
    @Test
    public void testPacketServiceRegistered() {
        EchoNativeTestLoader loader = new EchoNativeTestLoader();
        loader.loadAddon("packetexample");
        assertTrue(loader.isServiceRegistered("packetexample:packet_service"));
    }
}
