# MCP Server

[![Version](https://img.shields.io/badge/version-0.0.1-blue.svg)](https://github.com/hjlarry/dify-plugin-mcp_server)
[![Repo](https://img.shields.io/badge/repo&issue-github-green.svg)](https://github.com/hjlarry/dify-plugin-mcp_server)

A Dify endpoint plugin that change a dify app to a mcp server.

**To keep your data secure, use this plugin exclusively within your private network.**

## Get Started

### 1. create a simple workflow app in dify.
![1](./_assets/1.png)

### 2. add a endpoint and select this app.
![2](./_assets/2.png)

The app's input schema must define its input parameters. For a chat dify app, ensure to include a `query` field in the input schema, formatted as follows:
```json
{
    "name": "get_weather",
    "description": "Get weather status for a place.",
    "inputSchema": {
        "properties": {
            "place": {"title": "Place", "type": "string"}
        },
        "required": ["place"],
        "title": "get_weatherArguments",
        "type": "object"
    }
}
```

### 3. copy the endpoint url to your mcp client, like `Cherry Studio`
![3](./_assets/3.png)
![4](./_assets/4.png)

### 4. enjoy it!
![5](./_assets/5.png)
