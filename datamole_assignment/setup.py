from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    port: int = 8080
    log_level: str = "debug"
    log_config: str = "dev_logger.yml"
    github_url: str = "https://api.github.com"

config = Settings()
