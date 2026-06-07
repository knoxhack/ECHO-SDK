package {{package_name}};

import com.mojang.logging.LogUtils;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.ModContainer;
import net.neoforged.fml.common.Mod;
import org.slf4j.Logger;

@Mod({{class_name}}.MOD_ID)
public final class {{class_name}} {
    public static final String MOD_ID = "{{module_id}}";
    private static final Logger LOGGER = LogUtils.getLogger();

    public {{class_name}}(IEventBus ignoredModEventBus, ModContainer ignoredModContainer) {
        LOGGER.info("{} loaded from the ECHO SDK template.", MOD_ID);
    }
}
