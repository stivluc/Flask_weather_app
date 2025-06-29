# Weather MCP Server MVP

A minimal Model Context Protocol (MCP) server that provides weather information for major cities.

## What is MCP?

MCP (Model Context Protocol) allows AI assistants to securely connect to external data sources and tools. This server demonstrates the basic concepts by providing weather data through two simple tools.

## Features

- `get_weather`: Get weather information for a specific city
- `list_cities`: List all available cities

## Setup

1. Install dependencies:
```bash
npm install
```

2. Run the server:
```bash
npm start
```

## Usage with Claude Desktop

Add this to your Claude Desktop MCP configuration:

```json
{
  "mcpServers": {
    "weather": {
      "command": "node",
      "args": ["/path/to/this/project/index.js"]
    }
  }
}
```

## Available Cities

- New York
- London  
- Tokyo
- Paris
- Sydney

## Example

Ask Claude: "What's the weather like in Tokyo?" and it will use this MCP server to provide the weather information.