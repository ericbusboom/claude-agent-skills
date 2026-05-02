---
status: draft
sprint: "014"
---
<!-- CLASI: Before changing code or making plans, review the SE process in CLAUDE.md -->

# Sprint 014 Use Cases

## SUC-001: Install clasr CLI via pip

- **Actor**: Developer
- **Preconditions**: `clasi` package is installed or being installed; `pyproject.toml` has
  the `clasr = clasr.cli:main` console_scripts entry
- **Main Flow**:
  1. Developer runs `pip install -e .` (or `pip install clasi`)
  2. Both `clasi` and `clasr` CLI entry points are installed
  3. Developer runs `clasr --help` and sees the install/uninstall subcommands
- **Postconditions**: Both CLIs are available on PATH from the same pip install
- **Acceptance Criteria**:
  - [ ] `clasr --help` works after `pip install -e .`
  - [ ] `clasr --version` or similar returns a version string
  - [ ] `clasi --help` continues to work unchanged

## SUC-002: Print bundled instructions

- **Actor**: Developer or agent
- **Preconditions**: `clasr` is installed
- **Main Flow**:
  1. Developer/agent runs `clasr --instructions`
  2. clasr loads `instructions.md` from the package via `importlib.resources`
  3. The Markdown content is printed to stdout
- **Postconditions**: Instructions are available without opening source files
- **Acceptance Criteria**:
  - [ ] `clasr --instructions` prints non-empty Markdown content to stdout
  - [ ] The content explains the `asr/` directory layout and frontmatter schema
  - [ ] Content is loaded from `clasr/instructions.md` package data, not hardcoded

## SUC-003: Install a single platform from an asr/ source directory

- **Actor**: Developer or agent running `clasr install`
- **Preconditions**: A valid `asr/` source directory exists with at least one skill,
  agent, or rule; target project directory is writable
- **Main Flow**:
  1. Developer runs `clasr install --source ./asr --provider myprovider --claude`
  2. clasr reads `asr/` content
  3. Skills are symlinked (or copied if `--copy`) under `.claude/skills/`
  4. Agents and rules are rendered with Claude-projected frontmatter under `.claude/agents/`
     and `.claude/rules/`
  5. `asr/AGENTS.md` content is written as a named marker block into `AGENTS.md` and
     `CLAUDE.md`
  6. `asr/claude/` contents are tree-copied into `.claude/`
  7. Manifest is written to `.claude/.clasr-manifest/myprovider.json`
- **Postconditions**: Platform directory populated; manifest records all installed entries
- **Acceptance Criteria**:
  - [ ] Symlinks resolve to correct `asr/` source files
  - [ ] Agent `.md` files have platform-projected frontmatter (Claude fields only)
  - [ ] Named marker blocks use the `<!-- BEGIN clasr:myprovider -->` format
  - [ ] Manifest is valid JSON with correct `kind` values for each entry
  - [ ] `asr/` source directory is byte-identical before and after install

## SUC-004: Install all three platforms in one command

- **Actor**: Developer or agent
- **Preconditions**: Valid `asr/` source directory; writable target
- **Main Flow**:
  1. Developer runs `clasr install --source ./asr --provider myprovider --claude --codex --copilot`
  2. clasr installs Claude, Codex, and Copilot platforms in sequence
  3. Each platform gets its own manifest
  4. AGENTS.md gets one named marker block (same content, shared across platforms)
- **Postconditions**: All three platform directories populated; three manifests written
- **Acceptance Criteria**:
  - [ ] `.claude/.clasr-manifest/myprovider.json` exists and is valid
  - [ ] `.codex/.clasr-manifest/myprovider.json` exists and is valid
  - [ ] `.github/.clasr-manifest/myprovider.json` exists and is valid
  - [ ] All platform-specific files are present and correct

## SUC-005: Uninstall a single platform

- **Actor**: Developer or agent running `clasr uninstall`
- **Preconditions**: Platform was previously installed by clasr for the given provider
- **Main Flow**:
  1. Developer runs `clasr uninstall --provider myprovider --claude`
  2. clasr reads `.claude/.clasr-manifest/myprovider.json`
  3. Each manifest entry is reversed: symlinks removed, rendered files deleted, marker
     blocks stripped from AGENTS.md and CLAUDE.md
  4. Manifest file is deleted
  5. If AGENTS.md or CLAUDE.md become empty after stripping, they are deleted
- **Postconditions**: All provider-specific entries removed from `.claude/`; other
  providers' entries untouched
- **Acceptance Criteria**:
  - [ ] All symlinks and rendered files from the provider are removed
  - [ ] Named marker block is stripped from AGENTS.md and CLAUDE.md
  - [ ] Other providers' marker blocks in AGENTS.md are preserved
  - [ ] Manifest file is removed after successful uninstall

## SUC-006: Multi-tenant install — two providers coexist

- **Actor**: Developer using two different tools (e.g. `clasi` and `curik`) that both
  use `clasr`
- **Preconditions**: First provider has already been installed into the target
- **Main Flow**:
  1. Provider A installs: `clasr install --provider a --claude`
  2. Provider B installs: `clasr install --provider b --claude`
  3. Both manifests coexist in `.claude/.clasr-manifest/`
  4. AGENTS.md contains two named marker blocks: `clasr:a` and `clasr:b`
  5. Skills from both providers coexist (different names; naming collision is consumer's
     responsibility)
- **Postconditions**: Both providers installed and independently managed
- **Acceptance Criteria**:
  - [ ] `.claude/.clasr-manifest/a.json` and `.claude/.clasr-manifest/b.json` both exist
  - [ ] AGENTS.md contains both `<!-- BEGIN clasr:a -->` and `<!-- BEGIN clasr:b -->` blocks
  - [ ] `clasr uninstall --provider a --claude` removes only provider A's entries
  - [ ] Provider B's manifest and marker block survive after provider A is uninstalled

## SUC-007: Union frontmatter projection

- **Actor**: clasr renderer (internal)
- **Preconditions**: An `asr/agents/<n>.md` or `asr/rules/<n>.md` file with union
  frontmatter (shared top-level fields + platform-specific nested keys)
- **Main Flow**:
  1. clasr parses the union frontmatter from the source file
  2. For target platform (e.g. Claude), it merges top-level shared fields with
     the `claude:` nested block
  3. Drops all other platform keys (`codex:`, `copilot:`)
  4. Writes output frontmatter + original body to the target file
- **Postconditions**: Target file has clean platform-specific frontmatter; no union bleed
- **Acceptance Criteria**:
  - [ ] Output file contains only fields valid for the target platform
  - [ ] Shared top-level fields appear in output
  - [ ] Platform-specific nested fields are promoted to top level in output
  - [ ] Absent platform key results in shared-only output frontmatter
  - [ ] Body is verbatim (no modification)

## SUC-008: Atomic manifest write

- **Actor**: clasr manifest module (internal)
- **Preconditions**: Install or update is completing; manifest needs to be written
- **Main Flow**:
  1. clasr serializes the new manifest to JSON
  2. Writes to `<manifest>.tmp` in the same directory
  3. Calls `os.replace` to atomically rename `.tmp` to final path
- **Postconditions**: Manifest file is either the complete new version or the previous
  version; no partial/corrupt intermediate state
- **Acceptance Criteria**:
  - [ ] `.tmp` file is used as intermediate; final file is written atomically
  - [ ] Manifest JSON is valid and matches the schema (version, provider, platform, entries)
  - [ ] If manifest parent dir does not exist, it is created before write

## SUC-009: Symlink fallback to copy on Windows / sandboxed CI

- **Actor**: Developer or CI system without symlink permission
- **Preconditions**: `os.symlink` raises `OSError` (Windows without Developer Mode, or
  sandboxed CI); or `--copy` flag is passed
- **Main Flow**:
  1. clasr attempts `os.symlink`
  2. `OSError` is caught; a warning is emitted
  3. `shutil.copy2` is used instead
  4. Manifest records `kind: "copy"` instead of `kind: "symlink"`
- **Postconditions**: Files are installed as copies; behavior is correct even without
  symlink privilege
- **Acceptance Criteria**:
  - [ ] `--copy` flag forces copy mode without attempting symlink
  - [ ] `OSError` from `os.symlink` triggers warning + copy fallback
  - [ ] Manifest records `"copy"` kind correctly in both cases
  - [ ] Uninstall removes copied files correctly

## SUC-010: Per-platform passthrough of asr/<platform>/ subdirs

- **Actor**: Developer maintaining platform-private files in `asr/`
- **Preconditions**: `asr/claude/` (or `codex/`, `copilot/`) contains platform-specific
  files (e.g. `settings.json`, `hooks.json`)
- **Main Flow**:
  1. clasr detects files under `asr/claude/`
  2. Tree-copies them to the corresponding platform directory (e.g. `.claude/`)
  3. Records each copied file in the manifest with `kind: "copy"`
  4. On uninstall, removes each recorded file
- **Postconditions**: Platform-private files installed into the correct directory;
  manifested for clean uninstall
- **Acceptance Criteria**:
  - [ ] `asr/claude/settings.json` → `.claude/settings.json` (no transform)
  - [ ] Nested subdirs are preserved: `asr/claude/commands/foo.md` → `.claude/commands/foo.md`
  - [ ] Each passthrough file appears in the manifest
  - [ ] Uninstall removes each passthrough file recorded in the manifest
