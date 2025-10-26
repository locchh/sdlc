## [Claude Code](https://claude.com/product/claude-code)

Install `npm install -g @anthropic-ai/claude-code` (Prequesite: Node.js >= 18)

Features:

- Autonomously explores your codebase
- Reads and writes code
- Runs Terminal commands with your permission.
- New, friendlier interface
- Integrated with the editor
- Powerful agentic features like subagents, custom slash commands, and MCP are supported.

### CLI

Usage: `claude [options] [command] [prompt]`

**Key Options:**

- Debug and verbose modes
- Print mode for piping and automation (with text, JSON, or stream-json output formats)
- Permission controls (skip, allow, or restrict permissions)
- Tool filtering (allow/disallow specific tools)
- MCP configuration options
- Session management (continue, resume, fork sessions)
- Model selection and fallback options
- Custom system prompts
- IDE integration
- Plugin and settings configuration

**Commands:**
- mcp - Configure and manage MCP servers
- plugin - Manage Claude Code plugins
- migrate-installer - Migration from npm installation
- setup-token - Authentication token setup
- doctor - Health check for auto-updater
- update - Check and install updates
- install - Install native builds
