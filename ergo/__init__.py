import typing

import uvicorn
from starlette.applications import Starlette
from starlette.responses import Response
from starlette.types import Scope, Receive, Send

from ergo.config import Config
from ergo.group import Group
from ergo.http import Method
from ergo.route import Router
from ergo.view import View


class Ergo(Router):

    def __init__(self, config: Config, response_cls: typing.Type[Response] = None):
        if response_cls:
            super().__init__(response_cls)
        else:
            super(Ergo, self).__init__()
        self._groups: typing.List[Group] = []
        self._config = config

    @property
    def config(self):
        return self.config

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        routes = self._routes + [g.mount for g in self._groups]
        app = Starlette(routes=routes, debug=self._config.DEBUG)
        scope["app"] = app
        await app.middleware_stack(scope, receive, send)

    def run(self, **kwargs: typing.Any):
        uvicorn.run(self, **kwargs)  # type:ignore

    def group(self, path: str, name: str = None, response_cls: typing.Type[Response] = None):
        g = Group(path, name=name, response_cls=response_cls or self._response_cls)
        self._groups.append(g)
        return g
