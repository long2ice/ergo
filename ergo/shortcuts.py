from starlette.requests import Request

from ergo import Ergo


def render(request: Request, template: str, context: dict = None, **kwargs):
    app = request.app  # type:Ergo
    context = context or {}
    context.update(request=request)
    return app.render(template, context, **kwargs)
