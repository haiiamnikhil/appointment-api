from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class ConfigValues(BaseSettings):
    database_url: str = ""

    model_config = SettingsConfigDict(env_file='.env')


@lru_cache
def load_config_values():
    return ConfigValues()
