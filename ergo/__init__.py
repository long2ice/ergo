import typing

import uvicorn
from starlette.applications import Starlette
from starlette.background import BackgroundTask
from starlette.responses import Response
from starlette.status import HTTP_200_OK
from starlette.templating import Jinja2Templates
from starlette.types import Receive, Scope, Send
from tortoise.contrib.starlette import register_tortoise

from ergo.config import Config
from ergo.errors import ConfigurationError
from ergo.group import Group
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
        self._template: typing.Optional[Jinja2Templates] = None

    @property
    def config(self):
        return self._config

    def _init_app(self):
        if self._app:
            return
        routes = self._routes + [g.mount for g in self._groups]
        self._app = Starlette(routes=routes, debug=self._config.debug)
        if self._config.tortoise_orm:
            register_tortoise(
                self._app,
                config=self._config.tortoise_orm.dict(),
                generate_schemas=self._config.generate_schemas,
            )
        if self._config.template_path:
            self._template = Jinja2Templates(directory=self._config.template_path)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        self._init_app()
        scope["app"] = self
        if self._app:
            await self._app.middleware_stack(scope, receive, send)

    def run(self, **kwargs: typing.Any):
        uvicorn.run(self, **kwargs)  # type:ignore

    def group(self, path: str, name: str = None, response_cls: typing.Type[Response] = None):
        g = Group(path, name=name, response_cls=response_cls or self._response_cls)
        self._groups.append(g)
        return g

    def render(
        self,
        name: str,
        context: dict,
        status_code: int = HTTP_200_OK,
        headers: dict = None,
        media_type: str = None,
        background: BackgroundTask = None,
    ):
        if not self._template:
            raise ConfigurationError("You need set TEMPLATE_PATH config first")
        return self._template.TemplateResponse(
            name, context, status_code, headers, media_type, background
        )
