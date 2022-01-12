from types import ModuleType
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from pydantic import BaseModel, BaseSettings

if TYPE_CHECKING:
    from tortoise.router import ConnectionRouter


class Connection(BaseModel):
    engine: str
    credentials: Dict[str, Any]


class App(BaseModel):
    models: List[Union[str, ModuleType]]
    default_connection: str

    class Config:
        arbitrary_types_allowed = True


class TortoiseORM(BaseModel):
    connections: Dict[str, Union[Connection, str]]
    apps: Dict[str, App]
    routers: Optional[List[Union[str, "ConnectionRouter"]]]
    use_tz: bool = False
    timezone: str = "UTC"

    class Config:
        arbitrary_types_allowed = True


class Config(BaseSettings):
    debug: bool = False
    template_path: Optional[str] = None
    tortoise_orm: Optional[TortoiseORM] = None
    generate_schemas: bool = False
