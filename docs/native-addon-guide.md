# Native Addon Guide

Native addons are packaged as `.echo-addon` files.

## Required Metadata

- `META-INF/echo.mod.json`
- `echo-addon-package.json`
- Runtime payload files referenced by package metadata

## Update Behavior

Native Edition manifests declare `moduleArtifactFamily: "echo-addon"`. The launcher resolves each `moduleRequirements` entry to `<module>-<version>.echo-addon` unless overridden.
