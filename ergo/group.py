import typing

from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Mount

from ergo.route import Router

if typing.TYPE_CHECKING:
    from ergo import Method


class Group(Router):
    def __init__(self, path: str, name: str = None, response_cls: typing.Type[Response] = None):
        if response_cls:
            super().__init__(response_cls)
        else:
            super(Group, self).__init__()
        self._mount = Mount(path, name=name, routes=self._routes)
        self._path = path

    def add_route(self, path: str, func: typing.Callable, methods: typing.List['Method'] = None):
        async def wrapped(request: Request) -> Response:
            return self._response_cls(await func(request))

        self.mount.app.add_route(path, wrapped, methods=methods)

    def group(self, path: str, name: str = None, response_cls: typing.Type[Response] = None):
        g = Group(self._path + path, name=name, response_cls=response_cls or self._response_cls)
        self._routes.append(g.mount)
        return g

    @property
    def mount(self):
        return self._mount
