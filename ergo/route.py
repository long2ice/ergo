import typing

from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import BaseRoute, Route

from ergo.http import Method


class Router:
    def __init__(self, response_cls: typing.Type[Response] = JSONResponse):
        self._routes: typing.List[BaseRoute] = []
        self._response_cls = response_cls

    async def _wrapped(
        self, request: Request, func: typing.Callable, response_cls: typing.Type[Response] = None
    ) -> Response:
        response = await func(request)
        if not isinstance(response, Response):
            if response_cls:
                return response_cls(response)
            return self._response_cls(response)
        return response

    def add_route(
        self,
        path: str,
        func: typing.Callable,
        methods: typing.List[Method] = None,
        response_cls: typing.Type[Response] = None,
    ):
        async def _(request: Request):
            return await self._wrapped(request, func, response_cls)

        self._routes.append(Route(path, _, methods=[method.value for method in methods or []]))

    def route(
        self,
        path: str,
        methods: typing.List[Method] = None,
        response_cls: typing.Type[Response] = None,
    ):
        def wrapper(func: typing.Callable):
            return self.add_route(path, func, methods, response_cls)

        return wrapper

    def add_view(self, path: str, view):
        for method in Method:
            route = method.lower()
            if hasattr(view, route):
                self.add_route(path, getattr(view, route), methods=[Method(method)])

    def get(self, path: str, response_cls: typing.Type[Response] = None):
        return self.route(path, methods=[Method.GET], response_cls=response_cls)

    def post(self, path: str, response_cls: typing.Type[Response] = None):
        return self.route(path, methods=[Method.POST], response_cls=response_cls)

    def delete(self, path: str, response_cls: typing.Type[Response] = None):
        return self.route(path, methods=[Method.DELETE], response_cls=response_cls)

    def put(self, path: str, response_cls: typing.Type[Response] = None):
        return self.route(path, methods=[Method.PUT], response_cls=response_cls)

    def patch(self, path: str, response_cls: typing.Type[Response] = None):
        return self.route(path, methods=[Method.PATCH], response_cls=response_cls)

    def option(self, path: str, response_cls: typing.Type[Response] = None):
        return self.route(path, methods=[Method.OPTION], response_cls=response_cls)

    def head(self, path: str, response_cls: typing.Type[Response] = None):
        return self.route(path, methods=[Method.HEAD], response_cls=response_cls)

    def trace(self, path: str, response_cls: typing.Type[Response] = None):
        return self.route(path, methods=[Method.TRACE], response_cls=response_cls)
