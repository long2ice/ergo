from ergo import Config, Ergo
from examples import models


def create_app():
    config = Config(
        debug=True,
        template_path="templates",
        generate_schemas=True,
        tortoise_orm={
            "connections": {"default": "sqlite://:memory:"},
            "apps": {
                "models": {
                    "models": [models],
                    "default_connection": "default",
                }
            },
            "use_tz": True,
        },
    )
    app = Ergo(config=config)
    return app
