# {{mod_name}} Client Isolation Notes

This UI surface template is common-safe by default. The generated module declares UI contracts and resource placeholders without importing `net.minecraft.client`, rendering classes, or screen classes from common code.

Client-only implementation should be added later under an explicit client package and reviewed against the module's `verifyCommonServerSafe` task before registration.

