from typing import Dict, Optional

from pydantic import BaseSettings


class Config(BaseSettings):
    DEBUG: bool = False
    TORTOISE_ORM: Optional[Dict] = None
    TEMPLATE: Optional[str] = None
