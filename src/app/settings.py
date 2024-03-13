from enum import StrEnum, auto

from pydantic_settings import BaseSettings, SettingsConfigDict


class Enviroments(StrEnum):
    local = auto()
    server = auto()


class Settings(BaseSettings):
    enviroment: Enviroments = Enviroments.local

    pg_dsn: str = "postgresql+asyncpg://postgres:postgres@db/postgres"

    kot: str = "<br>\
┈┈┈╭┳┳╮<br>\
┈┈┈┣╭╮┫┈┏╮┈╭┓<br>\
┈┈┈┣╰╰╯━┫╋┳╋┃<br>\
┈┈┈╰┫┈╮┈┣▇━▇┫<br>\
┈┈┈┈┃┈┻╮╰╰┻╯╯┳╮<br>\
┈┈▔▔▔▔▔▔▔▔▔▔▔▔▔"

    model_config = SettingsConfigDict()


settings = Settings()
