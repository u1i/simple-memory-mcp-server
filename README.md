# Simple Memory MCP Server

**An educational project demonstrating Model Context Protocol (MCP) fundamentals**

This project shows how to build a basic memory system for LLMs using MCP. It's designed as a **learning example** to demonstrate:
- How MCP servers work
- Tool integration with LLMs
- Effective prompting strategies
- Simple, reliable tool design

*Note: This is an educational setup focused on demonstrating MCP concepts, not a production-ready solution.*

## What You'll Learn

This project demonstrates:
- **MCP Server Basics**: How to create tools that LLMs can call
- **Tool Design**: Why simple tools work better than complex ones
- **LLM Integration**: How to connect MCP servers to AI clients
- **Prompting Strategy**: How to guide LLMs to use tools effectively
- **Database Integration**: Basic SQLite usage in MCP context

The memory system stores simple facts about users and retrieves them - perfect for understanding MCP fundamentals without complexity.

## Project Files

* `my-fmcp-server.py`: The main MCP server with two memory tools
* `user_memory.db`: SQLite database storing user facts (created automatically)
* `requirements.txt`: Python dependencies
* `sample-agent-prompt.md`: Example prompt for AI agents using this memory system
* `mcp_config.json`: Ready-to-use MCP configuration for Claude Desktop

## Educational Features

* **Two Simple Tools**: Perfect for learning MCP tool design
* **Clear Examples**: Shows good vs bad tool usage patterns
* **Ready-to-Use Config**: Demonstrates MCP client setup
* **Prompting Guide**: Shows how to instruct LLMs to use tools
* **SQLite Integration**: Basic database operations in MCP context
* **Multi-User Demo**: Simple user separation example

## Available Memory Tools

The server exposes just **2 simple tools** that LLMs can reliably use:

### 1. `store_user_info(fact)`
Store a single piece of information about the user as a one-line fact.

**Examples:**
- `store_user_info("The user lives in Singapore")`
- `store_user_info("The user has a cat called Wendy")`
- `store_user_info("The user prefers Python over JavaScript")`
- `store_user_info("The user works as a software engineer")`

### 2. `get_user_info()`
Retrieve ALL stored information about the user in a simple numbered list.

**Returns something like:**
```
Here's what I know about the user:

1. The user lives in Singapore
2. The user has a cat called Wendy
3. The user prefers Python over JavaScript
4. The user works as a software engineer
```

## Setup Instructions

Follow these steps to get your Long-Term Memory MCP server running.

### 1. Install Dependencies

```bash
# Install required packages
pip install fastmcp
# Note: sqlite3 is included with Python by default
```

### 2. Run the Memory Server

The server code is already implemented in `my-fmcp-server.py`. Simply run:

```bash
python my-fmcp-server.py
```

You should see output like:

```
Starting Long-Term Memory MCP server...
Database location: /path/to/your/project/user_memory.db
[INFO]: Database initialized successfully
[INFO]: Starting MCP server 'LongTermMemoryMCP' with transport 'streamable-http' on http://0.0.0.0:8000/mcp
INFO:     Started server process [PROCESS_ID]
INFO:     Waiting for application startup.
[INFO]: StreamableHTTP session manager started
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

The SQLite database (`user_memory.db`) will be created automatically in your project directory.

### 3. Configure Your LLM Client

#### For Claude Desktop

Edit the Claude configuration file:
- **macOS:** `~/Library/Application Support/Claude/config.json`  
- **Windows:** `%APPDATA%\Claude\config.json`

You can copy the configuration from the included `mcp_config.json` file:

```json
{
  "mcpServers": {
    "memory1": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://localhost:8000/mcp"
      ]
    }
  }
}
```

**Note:** You'll need to install `mcp-remote` first:
```bash
npm install -g mcp-remote
```

#### For Other LLM Clients

Any MCP-compatible client can connect to `http://localhost:8000/mcp` using the HTTP transport.

### 4. Configure Your AI Agent

For best results, use the provided agent prompt from `sample-agent-prompt.md`:

```markdown
You are a helpful assistant.
You must remember the essence of the conversation, so each time you learn something about the user, make a tool use to store the condensed info.
```

This ensures the AI will:
- Store important facts as it learns them
- Keep information condensed and relevant
- Build a useful memory over time

### 5. Using the Memory System

Once connected, the AI can automatically use the memory tools:

#### Storing Information
When you tell the AI something, it might store:
```
store_user_info("The user lives in Singapore")
```

#### Retrieving Context
Before responding, the AI will call:
```
get_user_info()
```

And get back all your information in one simple list. No complex filtering, no missed results - just everything it knows about you.
## Quick Start (Learning Path)

1. **Install dependencies:** `pip install fastmcp`
2. **Run the server:** `python my-fmcp-server.py`
3. **Install mcp-remote:** `npm install -g mcp-remote`
4. **Copy config:** Use the `mcp_config.json` configuration in your LLM client
5. **Add the prompt:** Use `sample-agent-prompt.md` to configure your AI agent
6. **Experiment:** Try different prompts and see how the AI uses the tools
7. **Modify:** Change the tools and see how it affects LLM behavior

**Learning Goals:**
- Understand how MCP tools are called
- See the difference good prompting makes
- Experience simple vs complex tool design
- Learn MCP client configuration

        "my-fastmcp-server": {
          "command": "npx",
          "args": [
            "mcp-remote",
            "http://localhost:8000/mcp"
          ]
        }
      }
    }
    ```
    * **`"my-fastmcp-server"`**: This is the arbitrary name you give your server in Claude AI Desktop. You'll use this name when interacting with Claude.
    * **`"http://localhost:8000/mcp"`**: This is the crucial URL.
        * `localhost:8000` refers to your computer's IP address and the port your server is listening on.
        * `/mcp` is the specific path where the FastMCP server exposes its protocol endpoint.

3.  **Save the `config.json` file.**

4.  **Restart Claude AI Desktop.** For the new server configuration to load, you must completely quit and restart the Claude AI Desktop application.

## How to Use with Claude AI Desktop

Once your server is running and Claude AI Desktop has been restarted, you can interact with your `add` tool.

1.  **Open Claude AI Desktop.**
2.  **Start a new conversation.**
## Tool Reference

### store_user_info(fact, user_id="default")
Store a single line of information about the user.
- **fact**: One line describing something about the user
- **user_id**: User identifier (optional, defaults to "default")

**Returns:** Simple confirmation message

### get_user_info(user_id="default")
Get all stored information about the user.
- **user_id**: User identifier (optional, defaults to "default")

**Returns:** Numbered list of all stored facts about the user

## Example Usage Scenarios

**Learning User Preferences:**
```
User: "I prefer React over Vue for frontend development"
AI stores: "The user prefers React over Vue for frontend development"
```

**Remembering Project Context:**
```
User: "I'm building an e-commerce API with FastAPI"
AI stores: "The user is building an e-commerce API with FastAPI"
```

**Personal Information:**
```
User: "I live in Singapore and have a cat called Wendy"
AI stores: "The user lives in Singapore"
AI stores: "The user has a cat called Wendy"
```

## Benefits

- **Reliable Memory**: Simple storage that actually works with LLMs
- **No Complexity**: No categories, tags, or importance levels to confuse the AI
- **Complete Context**: AI gets all your information in one call
- **Personalized Conversations**: AI remembers what you tell it
- **Multi-User Support**: Different users get separate memory spaces

## Database Schema

The SQLite database contains a simple `user_facts` table with:
- `id`: Unique identifier
- `user_id`: User identifier for multi-user support
- `fact`: The stored information as plain text
- `created_at`: Timestamp when stored

That's it! No complex schema, no confusing relationships.

## Educational Scope & Limitations

**What this project demonstrates:**
- Basic MCP server implementation
- Simple tool design principles
- LLM-tool integration patterns
- Client configuration examples

**What this project doesn't cover:**
- Production security considerations
- Scalability and performance optimization
- Advanced MCP features
- Complex data relationships
- Error handling and recovery

**For learning purposes:**
- All data stays local (SQLite database)
- No external dependencies beyond MCP
- Easy to modify and experiment with
- Clear, readable code structure

## Educational Insights

**Why we chose this simple design:**
- **Learning Focus**: Two tools are easier to understand than complex systems
- **Demonstrates Principles**: Shows core MCP concepts without distractions
- **Real-World Applicable**: Patterns you can use in your own projects
- **Debugging Friendly**: Simple enough to troubleshoot and modify

**What this teaches about LLM tool design:**
- Simple tools work better than complex ones
- Clear instructions prevent tool misuse
- Complete data retrieval avoids missed context
- Good prompting is crucial for tool adoption

## Troubleshooting

**Server won't start:**
- Check if port 8000 is available
- Ensure FastMCP is installed: `pip install fastmcp`

**Database errors:**
- Check write permissions in the project directory
- Database file will be created automatically

**Claude can't connect:**
- Verify the config.json syntax is correct
- Restart Claude AI Desktop after config changes
- Check server logs for connection attempts

**Memory not working:**
- Check that the AI is calling `get_user_info()` before responding
- Verify facts are being stored with `store_user_info()`
- Simple is better - let the AI store one fact at a time

## Understanding the MCP Protocol

This section provides educational insights into the JSON-RPC messages exchanged between MCP clients (like Claude) and your FastMCP server.

### Tool Discovery Process

When an MCP client connects to your server, it first discovers what tools are available. Here's what the JSON-RPC messages look like:

#### Request: List Available Tools

```json
{
  "jsonrpc": "2.0",
  "id": 1, // A unique integer ID
  "method": "tools/list",
  "params": {} // No parameters needed for listing all tools
}
```

#### Response: Tool Definitions

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": [
    {
      "name": "add",
      "description": "Use this to add two numbers together. You MUST use this tool when asked to perform additions",
      "parameters": {
        "type": "object",
        "properties": {
          "a": {
            "type": "integer"
          },
          "b": {
            "type": "integer"
          }
        },
        "required": ["a", "b"]
      }
    }
    // If you had other tools, they would be listed here as well
  ]
}
```

### Tool Invocation

When Claude decides to use your tool, it sends an invocation request:

#### Request: Call the Add Tool

```json
{
  "jsonrpc": "2.0",
  "id": 2, // A new unique ID
  "method": "tools/call",
  "params": {
    "name": "add",
    "arguments": {
      "a": 123,
      "b": 456
    }
  }
}
```

#### Response: Tool Result

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "value": 579
  }
}
```

Understanding these message exchanges helps you build more sophisticated tools and debug any issues that might arise when integrating with MCP clients.
