# [Claude Code](https://claude.com/product/claude-code)

## Overview

Prerequisites:

- Node.js >= 18
- A Claude.ai (recommended) or Claude Console account

Installation:

```bash
# Install Claude Code
npm install -g @anthropic-ai/claude-code

# Navigate to your project
cd your-awesome-project

# Start coding with Claude
claude
# You'll be prompted to log in on first use

/login
# Follow the prompts to log in with your account
```

Claude Code offers a variety of settings to configure its behavior to meet your needs. You can configure Claude Code by running the `/config` command when using the interactive REPL, which opens a tabbed Settings interface where you can view status information and modify configuration options. 

The settings.json file is our official mechanism for configuring Claude Code through hierarchical settings:
- User settings are defined in `~/.claude/settings.json` and apply to all projects.
- Project settings are defined in `.claude/settings.json` for settings that are checked into source control and shared with your team.

Example:

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test:*)",
      "Read(~/.zshrc)"
    ],
    "deny": [
      "Bash(curl:*)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ]
  },
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp"
  }
}
```

More details: [Settings](https://docs.claude.com/en/docs/claude-code/settings#tools-available-to-claude)

Features:

- Autonomously explores your codebase
- Reads and writes code
- Runs Terminal commands with your permission.
- New, friendlier interface
- Integrated with the editor
- Powerful agentic features like subagents, custom slash commands, and MCP are supported.

Usages:

- **Build features from descriptions:** Tell Claude what you want to build in plain English. It will make a plan, write the code, and ensure it works.
- **Debug and fix issues:** Describe a bug or paste an error message. Claude Code will analyze your codebase, identify the problem, and implement a fix.
- **Navigate any codebase:** Ask anything about your team’s codebase, and get a thoughtful answer back. Claude Code maintains awareness of your entire project structure, can find up-to-date information from the web, and with MCP can pull from external datasources like Google Drive, Figma, and Slack.
- **Automate tedious tasks:** Fix fiddly lint issues, resolve merge conflicts, and write release notes. Do all this in a single command from your developer machines, or automatically in CI.

Why developers love Claude Code:
- **Works in your terminal:** Not another chat window. Not another IDE. Claude Code meets you where you already work, with the tools you already love.
- **Takes action:** Claude Code can directly edit files, run commands, and create commits. Need more? MCP lets Claude read your design docs in Google Drive, update your tickets in Jira, or use your custom developer tooling.
- **Unix philosophy:** Claude Code is composable and scriptable. tail -f app.log | claude -p "Slack me if you see any anomalies appear in this log stream" works. Your CI can run claude -p "If there are new text strings, translate them into French and raise a PR for @lang-fr-team to review".
- **Enterprise-ready:** Use the Claude API, or host on AWS or GCP. Enterprise-grade security, privacy, and compliance is built-in.

Inside `.claude/`:
  - commands/ - Slash commands
  - agents/ - Custom agents
  - skills/ - Reusable skills
  - hooks/ - Hook scripts
  - settings.json - (permissions and hooks config)

Inside `.claude-plugin/` (for plugins):
  - plugin.json - Plugin metadata

**Use Claude in interactive mode**

```bash
claude
```

**Use Claude as a unix-style utility (Headless mode)**

- Add Claude to your Makefile
```makefile
.PHONY: hello

hello:
	claude -p "Hello!"
```

- Pipe in, pipe out

```bash
cat build-error.txt | claude -p 'concisely explain the root cause of this build error' > output.txt


# This outputs a JSON array of messages with metadata including cost and duration.
cat code.py | claude -p 'analyze this code for bugs' --output-format json > analysis.json

# Use streaming JSON format
cat log.txt | claude -p 'parse this log file for errors' --output-format stream-json
```

**Create custom slash commands**

```bash
# Create a commands directory in your project
mkdir -p .claude/commands

# Create a Markdown file for each command
echo "Analyze the performance of this code and suggest three specific optimizations:" > .claude/commands/optimize.md

claude

# Use your custom command in Claude Code
optimize
```

Add command arguments with `$ARGUMENTS`:

```bash
echo 'Find and fix issue #$ARGUMENTS. Follow these steps: 1.
Understand the issue described in the ticket 2. Locate the relevant code in
our codebase 3. Implement a solution that addresses the root cause 4. Add
appropriate tests 5. Prepare a concise PR description' >
.claude/commands/fix-issue.md

claude

fix-issue 123
```

## Features

### [Subagents](https://docs.claude.com/en/docs/claude-code/sub-agents)

Subagents are pre-configured AI personalities that Claude Code can delegate tasks to. Subagents are stored as Markdown files with YAML frontmatter in two possible locations:

- Project subagents	`.claude/agents/`	Available in current project	with Highest priority
- User subagents	`~/.claude/agents/`	Available across all projects	Lower priority

You can also manage subagents by working directly with their files:

```bash
# Create a project subagent
mkdir -p .claude/agents
echo '---
name: test-runner
description: Use proactively to run tests and fix failures
---

You are a test automation expert. When you see code changes, proactively run the appropriate tests. If tests fail, analyze the failures and fix them while preserving the original test intent.' > .claude/agents/test-runner.md

# Create a user subagent
mkdir -p ~/.claude/agents
# ... create subagent file
```

**How to activate:**
- Use subagents automatically: `review my recent code changes for security issues`
- Explicitly request specific subagents: `> use the code-reviewer subagent to check the auth module`

**Key benefits:**
- Context preservation: Each subagent operates in its own context, preventing pollution of the main conversation and keeping it focused on high-level objectives.
- Specialized expertise: Subagents can be fine-tuned with detailed instructions for specific domains, leading to higher success rates on designated tasks.
- Reusability: Once created, subagents can be used across different projects and shared with your team for consistent workflows.
- Flexible permissions: Each subagent can have different tool access levels, allowing you to limit powerful tools to specific subagent types.

**File format**

Each subagent is defined in a Markdown file with this structure:

```yaml
---
name: your-sub-agent-name
description: Description of when this subagent should be invoked
tools: tool1, tool2, tool3  # Optional - inherits all tools if omitted
model: sonnet  # Optional - specify model alias or 'inherit'
---

Your subagent's system prompt goes here. This can be multiple paragraphs
and should clearly define the subagent's role, capabilities, and approach
to solving problems.

Include specific instructions, best practices, and any constraints
the subagent should follow.
```

|Field	|Required	|Description|
|---	|---	|---|
|name	|Yes	|Unique identifier using lowercase letters and hyphens|
|description	|Yes	|Natural language description of the subagent’s purpose|
|tools	|No	|Comma-separated list of specific tools. If omitted, inherits all tools from the main thread|
|model	|No	|Model to use for this subagent. Can be a model alias (sonnet, opus, haiku) or 'inherit' to use the main conversation’s model. If omitted, defaults to the configured subagent model|

**Tools available to Claude:**

| Tool | Description | Permission Required |
|------|-------------|---------------------|
| Bash | Executes shell commands in your environment | Yes |
| Edit | Makes targeted edits to specific files | Yes |
| Glob | Finds files based on pattern matching | No |
| Grep | Searches for patterns in file contents | No |
| NotebookEdit | Modifies Jupyter notebook cells | Yes |
| NotebookRead | Reads and displays Jupyter notebook contents | No |
| Read | Reads the contents of files | No |
| SlashCommand | Runs a custom slash command | Yes |
| Task | Runs a sub-agent to handle complex, multi-step tasks | No |
| TodoWrite | Creates and manages structured task lists | No |
| WebFetch | Fetches content from a specified URL | Yes |
| WebSearch | Performs web searches with domain filtering | Yes |
| Write | Creates or overwrites files | Yes |

**Usage:**
- Automatic delegation: `review my recent code changes for security issues`
- Explicit delegation: `> use the code-reviewer subagent to check the auth module`
- Chaining subagents: `> First use the code-analyzer subagent to find performance issues, then use the optimizer subagent to fix them`
- Dynamic subagent selection

### [Agent skills](https://docs.claude.com/en/docs/claude-code/skills)

Skills are modular capabilities that extend Claude’s functionality through organized folders containing instructions, scripts, and resources. Each Skill consists of a `SKILL.md` file with instructions that Claude reads when relevant, plus optional supporting files like scripts and templates. Skills are **model-invoked**—Claude autonomously decides when to use them based on your request and the Skill’s description. This is different from slash commands, which are **user-invoked** (you explicitly type `/`command to trigger them).

**Benefits:**
- Extend Claude’s capabilities for your specific workflows
- Share expertise across your team via git
- Reduce repetitive prompting
- Compose multiple Skills for complex tasks

Personal Skills are available across all your projects. Store them in `~/.claude/skills/`: `mkdir -p ~/.claude/skills/my-skill-name`. Use personal Skills for: Your individual workflows and preferences, Experimental Skills you’re developing, Personal productivity tools.

Project Skills are shared with your team. Store them in `.claude/skills/` within your project: `mkdir -p .claude/skills/my-skill-name`. Use project Skills for: Team workflows and conventions, Project-specific expertise, Shared utilities and scripts.

Create a `SKILL.md` file with YAML frontmatter and Markdown content:

```markdown
---
name: your-skill-name
description: Brief description of what this Skill does and when to use it
---

# Your Skill Name

## Instructions
Provide clear, step-by-step guidance for Claude.

## Examples
Show concrete examples of using this Skill.
```

Add supporting files:

```
my-skill/
├── SKILL.md (required)
├── reference.md (optional documentation)
├── examples.md (optional examples)
├── scripts/
│   └── helper.py (optional utility)
└── templates/
    └── template.txt (optional template)
```

Reference these files from SKILL.md:

```markdown
For advanced usage, see [reference.md](reference.md).

Run the helper script:`python scripts/helper.py input.txt`
```

Use the allowed-tools frontmatter field to limit which tools Claude can use when a Skill is active:


```markdown
---
name: safe-file-reader
description: Read files without making changes. Use when you need read-only file access.
allowed-tools: Read, Grep, Glob
---

# Safe File Reader

This Skill provides read-only file access.

## Instructions
1. Use Read to view file contents
2. Use Grep to search within files
3. Use Glob to find files by pattern
```

For more details, see [quickstart](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/quickstart), [best practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)

### [Hooks](https://docs.claude.com/en/docs/claude-code/hooks-guide)

### [MCP](https://docs.claude.com/en/docs/claude-code/mcp)

### [Output Styles](https://docs.claude.com/en/docs/claude-code/output-styles)

### [Plugins](https://docs.claude.com/en/docs/claude-code/plugins)

Plugins let you extend Claude Code with custom functionality that can be shared across projects and teams. Install plugins from [marketplaces](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces) to add pre-built commands, agents, hooks, Skills, and MCP servers, or create your own to automate your workflows.

Create your first plugin:

```bash
# Create the marketplace structure
mkdir test-marketplace
cd test-marketplace

# Create the plugin directory
mkdir my-first-plugin
cd my-first-plugin

# Create the plugin manifest
mkdir .claude-plugin
cat > .claude-plugin/plugin.json << 'EOF'
{
"name": "my-first-plugin",
"description": "A simple greeting plugin to learn the basics",
"version": "1.0.0",
"author": {
"name": "locch"
}
}
EOF

# Add a custom command
mkdir commands
cat > commands/hello.md << 'EOF'
---
description: Greet the user with a personalized message
---

# Hello Command

Greet the user warmly and ask how you can help them today. Make the greeting personal and encouraging.
EOF

# Create the marketplace manifest
cd ..
mkdir .claude-plugin
cat > .claude-plugin/marketplace.json << 'EOF'
{
"name": "test-marketplace",
"owner": {
"name": "Test User"
},
"plugins": [
{
  "name": "my-first-plugin",
  "source": "./my-first-plugin",
  "description": "My first test plugin"
}
]
}
EOF

# Start Claude Code from parent directory
cd ..
claude

# Add the test marketplace
/plugin marketplace add ./test-marketplace

# Try your new command
/hello
```

Your plugin follows this basic structure:

```
my-first-plugin/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata
├── commands/                 # Custom slash commands (optional)
│   └── hello.md
├── agents/                   # Custom agents (optional)
│   └── helper.md
├── skills/                   # Agent Skills (optional)
│   └── my-skill/
│       └── SKILL.md
└── hooks/                    # Event handlers (optional)
    └── hooks.json
```

Additional components you can add:

- **Commands:** Create markdown files in commands/ directory
- **Agents:** Create agent definitions in agents/ directory
- **Skills:** Create SKILL.md files in skills/ directory
- **Hooks:** Create hooks/hooks.json for event handling
- **MCP servers:** Create .mcp.json for external tool integration


### [Headless mode](https://docs.claude.com/en/docs/claude-code/headless)


## Reference

### [CLI Reference](https://docs.claude.com/en/docs/claude-code/cli-reference)

Usage: `claude [options] [command] [prompt]`

Key CLI commands:
- `claude` - Start interactive session
- `claude "query"` - Single query mode
- `claude -p "query"` - Print mode (non-interactive, output to stdout)
- `cat file | claude -p "query"` - Pipe input to Claude
- `claude -c` - Continue last session
- `claude -r "<session-id>" "query"` - Resume specific session
- `claude update` - Check and install updates
- `claude mcp` - Configure MCP servers

Key CLI flags:
- `--add-dir` - Add working directories
- `--agents` - Configure subagents
- `--allowedTools` / `--disallowedTools` - Restrict tool access
- `--append-system-prompt` - Add custom instructions
- `--output-format` - text, json, or stream-json
- `--input-format` - text or stream-json
- `--verbose` - Enable verbose logging
- `--max-turns` - Limit conversation turns
- `--model` - Select Claude model (sonnet, opus)
- `--permission-mode` - plan, accept, or skip
- `--dangerously-skip-permissions` - Skip all permission checks

### [Interactive mode](https://docs.claude.com/en/docs/claude-code/interactive-mode)

Keyboard shortcuts:
General controls:
- `Ctrl+C` - Cancel current operation
- `Ctrl+D` - Exit Claude Code
- `Ctrl+L` - Clear screen
- `Ctrl+O` - Open file in editor
- `Ctrl+R` - Search command history
- `Ctrl+V` - Paste from clipboard
- `Alt+V` - Paste with formatting
- `Up/Down arrows` - Navigate history
- `Esc` - Cancel/go back
- `Tab` - Enable extended thinking
- `Shift+Tab` - Switch between `auto-accept edits`, `plan mode` and normal mode
- `Alt+M` - Toggle multiline mode

Multiline input:
- `\` - Continue line
- `Option+Enter` - New line (Mac)
- `Shift+Enter` - New line (with /terminal-setup)
- `Ctrl+J` - New line (alternative)

Quick commands:
- `#` - Comment
- `/` - Slash command
- `!` - Bash command
- `@` - Reference file/directory

### [Slash Commands](https://docs.claude.com/en/docs/claude-code/slash-commands)

Built-in slash commands:
- `/add-dir` - Add working directories
- `/agents` - Manage subagents
- `/bug` - Report bugs
- `/clear` - Clear conversation
- `/compact [instructions]` - Compact with summary
- `/config` - Open config panel
- `/cost` - Show session cost
- `/doctor` - Diagnose installation
- `/help` - Show help
- `/init` - Initialize CLAUDE.md
- `/login` / `/logout` - Authentication
- `/mcp` - Manage MCP servers
- `/memory` - Edit memory files
- `/model` - Change AI model
- `/permissions` - Manage permissions
- `/pr_comments` - Get PR comments
- `/review` - Review PR
- `/sandbox` - Configure sandbox
- `/rewind` - Restore to checkpoint
- `/status` - Show status
- `/terminal-setup` - Setup Shift+Enter
- `/usage` - Show plan usage
- `/vim` - Toggle Vim mode

Custom slash commands:
- Defined in `.claude/commands/`
- Can be plugin-provided
- Can invoke MCP prompts

### [Checkpointing](https://docs.claude.com/en/docs/claude-code/checkpointing)

How checkpoints work:
Automatic tracking:
- Every user prompt creates a checkpoint
- Checkpoints persist across sessions (30-day retention)
- Automatically cleaned up after 30 days

Rewinding changes:
- `Esc` - Show rewind menu
- `/rewind` - Access rewind interface
- Three rewind options:
  1. Conversation only - Keep code changes, revert conversation
  2. Code only - Revert file changes, keep conversation
  3. Both - Restore both to prior point

Limitations:
- Bash command changes not tracked
- External changes not tracked
- Not a replacement for version control

### [Hooks reference](https://docs.claude.com/en/docs/claude-code/hooks)

Hook events:
- `PreToolUse` - Before tool calls (can block)
- `PostToolUse` - After tool calls complete
- `UserPromptSubmit` - Before Claude processes prompt
- `Notification` - When notifications sent
- `Stop` - When Claude finishes responding
- `SubagentStop` - When subagent tasks complete
- `PreCompact` - Before compact operation
- `SessionStart` - Session starts/resumes
- `SessionEnd` - Session ends

Configuration:
- Stored in `.claude/hooks/` directory
- Configured via `/hooks` command
- Can be project-specific or plugin-provided
- Input/output via JSON or exit codes

### [Plugin reference](https://docs.claude.com/en/docs/claude-code/plugins-reference)

Plugin components:
- Commands - Custom slash commands
- Agents - Subagents
- Skills - Reusable expertise
- Hooks - Event handlers
- MCP servers - Tool integrations

Plugin structure:
- `plugin.json` - Plugin metadata (required fields, component paths)
- `commands/` - Slash command definitions
- `agents/` - Subagent configurations
- `skills/` - Skill definitions
- `hooks/` - Hook scripts
- `mcp/` - MCP server configs

Debugging:
- Use `/doctor` to diagnose issues
- Check plugin.json schema
- Verify file paths and syntax
- Test locally before sharing

Distribution:
- Version management via plugin.json
- Can be shared via marketplaces
- Team-level or user-level installation