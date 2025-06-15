# MCP Server Demo

A demonstration server implementing the Model Control Protocol (MCP) for AI model interactions.

## Overview

This project showcases a modular MCP server implementation that allows AI models to:
- Execute tools (calculate user statistics and update user status)
- Access resources (user data and system information)
- Use predefined prompts for common interactions

We are providing some basic static resources, tools, and prompts to illustrate how an MCP server can be structured. The server is designed to be compatible with the Claude desktop client.

## Packages

- `mcp[cli]` package version 1.9.4 or higher

## Installation

1. Create and activate virtual environment:

```bash
uv venv
source .venv/bin/activate  # On Unix/MacOS
# or
.\.venv\Scripts\activate   # On Windows
```
2. Install the required packages:

```bash
uv sync 
```

## Usage

Add the server to your MCP client configuration:
To use this MCP server with the Claude desktop client, you need to modify the client configuration file to include the server details.
You can find the configuration file in the following locations depending on your operating system:

MacOS/Linux 
```code ~/Library/Application\ Support/Claude/claude_desktop_config.json```
Windows
```code %APPDATA%\Claude\claude_desktop_config.json```

And add the following configuration:

```json
{
  "mcpServers": {
    "demo": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/PARENT/FOLDER/demo",
        "run",
        "demo.py"
      ]
    }
  }
}
```

### Resources

The server provides two in-memory resources:
- `memory://users`: A collection of user records with basic information
- `memory://system-info`: System metadata about the server

### Tools

Two tools are implemented:
1. `calculate_user_stats`: Analyzes user data and returns statistics
2. `update_user_status`: Modifies a user's active status

### Prompts

Pre-defined interaction templates:
- `analyze-user-data`: For analyzing patterns in user data
- `generate-report`: For creating formatted reports based on available data

## Project Structure

The project follows a modular organization:

```
mcp-server-demo/
├── demo.py                    # Main entry point
├── pyproject.toml             # Project configuration
├── README.md                  # This documentation
├── uv.lock                    # Dependencies lock file
└── src/                       # Main package
    ├── __init__.py            # Package initialization
    ├── server.py              # Server creation and configuration
    ├── resources/             # Resource-related modules
    │   ├── __init__.py
    │   └── handlers.py        # Resource handlers implementation
    ├── tools/                 # Tool-related modules
    │   ├── __init__.py
    │   └── handlers.py        # Tool handlers implementation
    └── prompts/               # Prompt-related modules
        ├── __init__.py
        └── handlers.py        # Prompt handlers implementation
```

## Protocol Details

The Model Control Protocol (MCP) defines a standardized way for AI models to interact with applications. It provides:

- **Resources**: Application-controlled sources of contextual data
- **Tools**: Model-controlled functions that perform actions
- **Prompts**: User-controlled templates for LLM interactions
