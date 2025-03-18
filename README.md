# MCP Server

[![Version](https://img.shields.io/badge/version-0.0.1-blue.svg)](https://github.com/hjlarry/dify-plugin-mcp_server)
[![Repo](https://img.shields.io/badge/repo-github-green.svg)](https://github.com/hjlarry/dify-plugin-mcp_server)

A Dify endpoint plugin that change a dify app to a mcp server.

## Get Started

### 1. create a simple workflow app in dify.
![1](./_assets/1.png)

### 2. add a endpoint and select this app.
![2](./_assets/2.png)

the app input schema should describe the input parameters of the app, the format like this:
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

### 3. copy the endpoint url to your mcp client, like `cursor`
![3](./_assets/3.png)
![4](./_assets/4.png)
### 4. enjoy it!
![5](./_assets/5.png)
