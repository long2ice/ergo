from starlette.requests import Request

from ergo import Ergo, Config

app = Ergo(config=Config())


class Index:
    async def get(self, request: Request):
        return {'msg': 'view'}


app.add_view("/view", Index())


@app.get("/")
async def index(request: Request):
    return {'msg': 'index'}


group = app.group('/group')


@group.get('/sub')
async def sub(request: Request):
    return {'msg': 'sub'}


if __name__ == "__main__":
    app.run()
