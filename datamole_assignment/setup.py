import logging

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    port: int = 8080
    log_level: str = "INFO"
    log_config: str = "dev_logger.yml"
    hot_reload: bool = False
    github_url: str = "https://api.github.com"


config = Settings()

services = {}

logging.basicConfig(level=config.log_level.upper())
log = logging.getLogger("uvicorn.error")
