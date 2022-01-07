import typing

from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.routing import Route, BaseRoute

from ergo.http import Method
from ergo.view import View


class Router:
    def __init__(self, response_cls: typing.Type[Response] = JSONResponse):
        self._routes: typing.List[BaseRoute] = []
        self._response_cls = response_cls

    def add_route(self, path: str, func: typing.Callable, methods: typing.List[Method] = None):
        async def wrapped(request: Request) -> Response:
            return self._response_cls(await func(request))

        self._routes.append(Route(path, wrapped, methods=[method.value for method in methods or []]))

    def route(self, path: str, methods: typing.List[Method] = None):
        def wrapper(func: typing.Union[typing.Callable, typing.Type[View]]):
            return self.add_route(path, func, methods)

        return wrapper

    def add_view(self, path: str, view: View):
        for method in Method:
            self.add_route(path, getattr(view, method.lower()), methods=[Method(method)])

    def get(self, path: str):
        return self.route(path, methods=[Method.GET])

    def post(self, path: str):
        return self.route(path, methods=[Method.POST])

    def delete(self, path: str):
        return self.route(path, methods=[Method.DELETE])

    def put(self, path: str):
        return self.route(path, methods=[Method.PUT])

    def patch(self, path: str):
        return self.route(path, methods=[Method.PATCH])

    def option(self, path: str):
        return self.route(path, methods=[Method.OPTION])

    def head(self, path: str):
        return self.route(path, methods=[Method.HEAD])

    def trace(self, path: str):
        return self.route(path, methods=[Method.TRACE])
