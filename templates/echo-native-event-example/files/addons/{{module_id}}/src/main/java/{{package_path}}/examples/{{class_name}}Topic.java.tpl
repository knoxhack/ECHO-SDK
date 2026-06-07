package {{package_name}}.examples;

public final class {{class_name}}Topic {
    public static final String MODULE_ID = "{{module_id}}";
    public static final String TOPIC = "{{module_id}}.events.lifecycle";

    private {{class_name}}Topic() {
    }

    public static String subscriptionReceipt() {
        return MODULE_ID + ":event/" + TOPIC;
    }
}
