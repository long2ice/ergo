from starlette.requests import Request

from ergo.shortcuts import render
from examples.factory import create_app
from examples.models import User
from examples.responses import ModelResponse

app = create_app()


class Index:
    async def get(self, request: Request):
        return {"msg": "view"}


app.add_view("/view", Index())


@app.get("/")
async def index(request: Request):
    return {"msg": "index"}


@app.get("/template")
async def template(request: Request):
    return render(request, "index.html", {"msg": "template"})


@app.post("/user", response_cls=ModelResponse)
async def create_user(request: Request):
    return await User.create(name="name")


group = app.group("/group")


@group.get("/sub")
async def sub(request: Request):
    return {"msg": "sub"}


if __name__ == "__main__":
    app.run()
