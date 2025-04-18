from typing import Mapping

from werkzeug import Request, Response
from dify_plugin import Endpoint


class HTTPGetEndpoint(Endpoint):
    def _invoke(self, r: Request, values: Mapping, settings: Mapping) -> Response:
        """
        Streamable HTTP in dify is a lightweight design, it only support POST and don't support SSE.
        """
        response = {
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32000, "message": "Method not allowed"},
        }

        return Response(response, status=405, content_type="application/json")
