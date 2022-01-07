from pydantic import BaseSettings


class Config(BaseSettings):
    DEBUG: bool = False
