# Claude Agent Skills

Personal collection of Claude Code agents and skills for enhancing development workflows.

## Overview

This repository contains custom agents and skills designed to work with Claude Code (formerly GitHub Copilot Workspace). Agents are specialized AI assistants with specific expertise, while skills are task-oriented workflows that leverage these agents.

## Repository Structure

```
.github/
├── agents/          # Agent definitions
│   ├── python-expert.md
│   ├── documentation-expert.md
│   └── ...
└── skills/          # Skill definitions
    ├── python-code-review.md
    ├── generate-documentation.md
    └── ...
```

## Agents

Agents are specialized AI assistants with focused expertise in specific domains. Each agent is defined in a Markdown file that describes:

- Capabilities and strengths
- Guidelines and best practices
- Available tools
- Example tasks

### Available Agents

- **[python-expert](/.github/agents/python-expert.md)** - Python programming expert with deep knowledge of best practices, design patterns, and the Python ecosystem
- **[documentation-expert](/.github/agents/documentation-expert.md)** - Technical documentation specialist for creating clear, comprehensive documentation

## Skills

Skills are task-oriented workflows that leverage agents to accomplish specific goals. Each skill defines:

- Description and purpose
- Which agent(s) it uses
- Usage instructions
- Expected process and output

### Available Skills

- **[python-code-review](/.github/skills/python-code-review.md)** - Performs comprehensive code reviews of Python code using the Python Expert agent
- **[generate-documentation](/.github/skills/generate-documentation.md)** - Creates professional project documentation using the Documentation Expert agent

## Installation

To install this package and make the agents and skills available to your projects:

```bash
# Clone this repository
git clone https://github.com/ericbusboom/claude-agent-skills.git
cd claude-agent-skills

# Install with pipx in editable mode
pipx install -e .
```

The editable installation allows you to modify agents and skills in the cloned repository, and the changes will be immediately available when you link them to other projects.

## Linking to Your Projects

Once installed, you can link the agents and skills to any project:

```bash
# Navigate to your project directory
cd /path/to/your/project

# Link the agents and skills
link-claude-agents
```

This will:
- Create symlinks from your project's `.github/agents` and `.github/skills` directories to this repository
- If those directories already exist in your project, it will link individual files instead
- Preserve any existing custom agents or skills in your project

## Usage

To use an agent or skill in Claude Code:

1. Reference the agent in your prompt: "Use the python-expert agent to help me refactor this code"
2. Invoke a skill directly: "Use the python-code-review skill on src/utils.py"
3. Let Claude choose automatically based on context

## Creating New Agents

To create a new agent:

1. Create a new Markdown file in `.github/agents/`
2. Define the agent's expertise and capabilities
3. List guidelines and best practices
4. Provide examples of tasks the agent can handle

**Template:**
```markdown
# [Agent Name]

[Brief description of the agent's expertise]

## Capabilities
- [List key capabilities]

## Guidelines
- [List important guidelines]

## Tools Available
- [List available tools]

## Example Tasks
- [List example use cases]
```

## Creating New Skills

To create a new skill:

1. Create a new Markdown file in `.github/skills/`
2. Describe what the skill does
3. Specify which agent(s) it uses
4. Define the process and expected output

**Template:**
```markdown
# [Skill Name]

[Brief description]

## Description
[Detailed description of what the skill does]

## Agent Used
**[agent-name]** - [Why this agent is used]

## Usage
[How to invoke this skill]

## Process
1. [Step 1]
2. [Step 2]
...

## Output
[What the skill produces]

## Benefits
- [Key benefits]
```

## Contributing

Feel free to contribute new agents and skills! Please ensure they:

- Have clear, descriptive names
- Include comprehensive documentation
- Follow the established templates
- Provide practical value

## License

This is a personal collection. Feel free to use and adapt for your own purposes.
