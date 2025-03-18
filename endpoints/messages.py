import uuid
import json
from typing import Mapping
from werkzeug import Request, Response
from flask import stream_with_context
from queue import Queue
from dify_plugin import Endpoint


class MessageEndpoint(Endpoint):
    def _invoke(self, r: Request, values: Mapping, settings: Mapping) -> Response:
        """
        Invokes the endpoint with the given request.
        """
        app_map = {
            "chat": self.session.app.chat,
            "workflow": self.session.app.workflow,
            "completion": self.session.app.completion,
        }
        app_id = settings.get("app").get("app_id")
        app_type = app_map.get(settings.get("app-type"))
        try:
            tool = json.loads(settings.get("app-input-schema"))
        except JSONDecodeError:
            raise ValueError("Invalid app-input-schema")

        session_id = r.args.get('session_id')
        data = r.json
        response = None

        if data.get("method") == "initialize":
            response = {
                "jsonrpc": "2.0",
                "id": data.get("id"),
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "experimental": {},
                        "prompts": {"listChanged": False},
                        "resources": {
                            "subscribe": False,
                            "listChanged": False
                        },
                        "tools": {"listChanged": False}
                    },
                    "serverInfo": {
                        "name": "Dify",
                        "version": "1.3.0"
                    }
                }
            }
        
        elif data.get("method") == "notifications/initialized":
            return Response("",
                status=202,
                content_type="application/json")

        elif data.get("method") == "tools/list":
            response = {
                "jsonrpc": "2.0",
                "id": data.get("id"),
                "result": {
                    "tools": [
                        tool
                    ]
                }
            }

        elif data.get("method") == "tools/call":
            tool_name = data.get("params", {}).get("name")
            arguments = data.get("params", {}).get("arguments", {})
            
            try:
                if tool_name == tool.get("name"):
                    result = app_type.invoke(app_id=app_id, inputs=arguments, response_mode="blocking")
                else:
                    raise ValueError(f"Unknown tool: {tool_name}")

                response = {
                    "jsonrpc": "2.0",
                    "id": data.get("id"),
                    "result": {
                        "content": [{"type": "text", "text": result}],
                        "isError": False
                    }
                }
            except Exception as e:
                response = {
                    "jsonrpc": "2.0",
                    "id": data.get("id"),
                    "error": {
                        "code": -32000,
                        "message": str(e)
                    }
                }

        if response:
            self.session.storage.set(session_id, json.dumps(response).encode())
            return Response("",
                status=202,
                content_type="application/json")
        
        return Response(json.dumps({"error": "Unknown method"}),
                status=400,
                content_type="application/json")
