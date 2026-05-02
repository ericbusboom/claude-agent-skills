# clasr

`clasr` is a cross-platform agent-config renderer that installs an `asr/`
(agent-source-root) directory into Claude Code, Codex, and GitHub Copilot platform
layouts. It supports multiple independent providers in the same target directory via
per-provider named marker blocks and JSON-manifests, enabling clean coexistence and
independent uninstall. Run `clasr --instructions` for usage guidance.
