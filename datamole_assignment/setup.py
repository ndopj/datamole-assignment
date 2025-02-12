import logging

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 8080
    log_level: str = "INFO"
    log_config: str = "dev_logger.yml"
    hot_reload: bool = False
    github_url: str = "https://api.github.com"
    github_api_version: str = "2022-11-28"
    github_page_size: int = 100


config = Settings()

services = {}

logging.basicConfig(level=config.log_level.upper())
log = logging.getLogger("uvicorn.error")
