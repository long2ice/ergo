import typing

import uvicorn
from starlette.applications import Starlette
from starlette.responses import Response
from starlette.types import Scope, Receive, Send
from tortoise.contrib.starlette import register_tortoise

from ergo.config import Config
from ergo.group import Group
from ergo.http import Method
from ergo.route import Router


class Ergo(Router):

    def __init__(self, config: Config, response_cls: typing.Type[Response] = None):
        if response_cls:
            super().__init__(response_cls)
        else:
            super(Ergo, self).__init__()
        self._groups: typing.List[Group] = []
        self._config = config
        self._app: typing.Optional[Starlette] = None

    @property
    def config(self):
        return self.config

    async def _init_app(self):
        if self._app:
            return
        routes = self._routes + [g.mount for g in self._groups]
        self._app = Starlette(routes=routes, debug=self._config.DEBUG)
        if self._config.TORTOISE_ORM:
            register_tortoise(self._app, config=self._config.TORTOISE_ORM)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        await self._init_app()
        scope["app"] = self._app
        if self._app:
            await self._app.middleware_stack(scope, receive, send)

    def run(self, **kwargs: typing.Any):
        uvicorn.run(self, **kwargs)  # type:ignore

    def group(self, path: str, name: str = None, response_cls: typing.Type[Response] = None):
        g = Group(path, name=name, response_cls=response_cls or self._response_cls)
        self._groups.append(g)
        return g
