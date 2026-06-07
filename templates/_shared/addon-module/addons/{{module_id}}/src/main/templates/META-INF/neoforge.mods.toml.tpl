modLoader="javafml"
loaderVersion="[1,)"
license="${mod_license}"
issueTrackerURL="https://github.com/knoxhack/Echo/issues"

[[mods]]
modId="${mod_id}"
version="${mod_version}"
displayName="${mod_name}"
displayURL="https://github.com/knoxhack/Echo"
authors="KnoxHack"
credits="Generated from the ECHO SDK template system."
description='''
{{mod_name}} is an ECHO SDK generated addon template. It is safe to scan,
review, and adapt before being wired into official addon sets.
'''

[[dependencies.${mod_id}]]
modId="neoforge"
type="required"
versionRange="[${neo_version},)"
ordering="NONE"
side="BOTH"

[[dependencies.${mod_id}]]
modId="minecraft"
type="required"
versionRange="${minecraft_version_range}"
ordering="NONE"
side="BOTH"

[[dependencies.${mod_id}]]
modId="echocore"
type="required"
reason="Generated SDK modules depend only on the stable ECHO core baseline until reviewed."
versionRange="[1.0.0,)"
ordering="AFTER"
side="BOTH"
