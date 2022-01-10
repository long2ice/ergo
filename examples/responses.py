import json

from starlette.responses import Response
from tortoise import Model


class ModelResponse(Response):
    def render(self, content: Model) -> bytes:
        return json.dumps(dict(content)).encode()
