package {{package_name}}.examples;

public final class {{class_name}}Surface {
    public static final String HUD_SURFACE = "{{module_id}}.hud.main";
    public static final String SCREEN_SURFACE = "{{module_id}}.screen.main";

    private {{class_name}}Surface() {
    }

    public static String renderReceipt(String surfaceId) {
        return "{{module_id}}:render/" + surfaceId;
    }
}
