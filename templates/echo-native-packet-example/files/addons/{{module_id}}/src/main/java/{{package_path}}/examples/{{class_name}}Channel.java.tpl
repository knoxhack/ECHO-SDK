package {{package_name}}.examples;

public final class {{class_name}}Channel {
    public static final String CHANNEL = "{{module_id}}:main";
    public static final int PROTOCOL_VERSION = 1;

    private {{class_name}}Channel() {
    }

    public static String packetReceipt(String packetId) {
        return "{{module_id}}:network/" + CHANNEL + "/" + packetId;
    }
}
