from typing import Dict, Optional

from pydantic import BaseSettings


class Config(BaseSettings):
    debug: bool = False
    template_path: Optional[str] = None
    tortoise_orm: Optional[Dict] = None
    generate_schemas: bool = False
