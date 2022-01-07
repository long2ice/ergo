from abc import ABC

from starlette.requests import Request


class View(ABC):
    async def get(self, request: Request):
        pass

    async def post(self, request: Request):
        pass

    async def delete(self, request: Request):
        pass

    async def put(self, request: Request):
        pass

    async def head(self, request: Request):
        pass

    async def option(self, request: Request):
        pass

    async def patch(self, request: Request):
        pass

    async def trace(self, request: Request):
        pass
