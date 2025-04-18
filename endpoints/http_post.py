import uuid
import json
from typing import Mapping

from werkzeug import Request, Response
from dify_plugin import Endpoint


class HTTPPostEndpoint(Endpoint):
    def _invoke(self, r: Request, values: Mapping, settings: Mapping) -> Response:
        """
        the simplest Streamable HTTP mcp protocol implementation.

        1. not valid session id
        2. not support SSE
        3. not support streaming
        4. only basic logic
        """
        app_id = settings.get("app").get("app_id")
        try:
            tool = json.loads(settings.get("app-input-schema"))
        except json.JSONDecodeError:
            raise ValueError("Invalid app-input-schema")

        session_id = r.args.get("session_id")
        data = r.json

        if data.get("method") == "initialize":
            session_id = str(uuid.uuid4()).replace("-", "")
            response = {
                "jsonrpc": "2.0",
                "id": data.get("id"),
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {},
                    },
                    "serverInfo": {"name": "Dify", "version": "0.0.1"},
                },
            }
            headers = {"mcp-session-id": session_id}
            return Response(
                json.dumps(response),
                status=200,
                content_type="application/json",
                headers=headers,
            )

        elif data.get("method") == "notifications/initialized":
            return Response("", status=202, content_type="application/json")

        elif data.get("method") == "tools/list":
            response = {
                "jsonrpc": "2.0",
                "id": data.get("id"),
                "result": {"tools": [tool]},
            }

        elif data.get("method") == "tools/call":
            tool_name = data.get("params", {}).get("name")
            arguments = data.get("params", {}).get("arguments", {})

            try:
                if tool_name == tool.get("name"):
                    if settings.get("app-type") == "chat":
                        result = self.session.app.chat.invoke(
                            app_id=app_id,
                            query=arguments.get("query", "empty query"),
                            inputs=arguments,
                            response_mode="blocking",
                        )
                    else:
                        result = self.session.app.workflow.invoke(
                            app_id=app_id, inputs=arguments, response_mode="blocking"
                        )
                else:
                    raise ValueError(f"Unknown tool: {tool_name}")

                if settings.get("app-type") == "chat":
                    final_result = {"type": "text", "text": result.get("answer")}
                else:
                    r = [
                        v
                        for v in result.get("data").get("outputs", {}).values()
                        if isinstance(v, str)
                    ]
                    final_result = {"type": "text", "text": "\n".join(r)}

                response = {
                    "jsonrpc": "2.0",
                    "id": data.get("id"),
                    "result": {"content": [final_result], "isError": False},
                }
            except Exception as e:
                response = {
                    "jsonrpc": "2.0",
                    "id": data.get("id"),
                    "error": {"code": -32000, "message": str(e)},
                }
        else:
            response = {
                "jsonrpc": "2.0",
                "id": data.get("id"),
                "error": {"code": -32001, "message": "unsupported method"},
            }

        return Response(
            json.dumps(response), status=200, content_type="application/json"
        )
