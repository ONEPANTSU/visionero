from dotenv import load_dotenv
from loguru import logger
from yaml import safe_load

from src.config.app import AppConfig
from src.config.database import DataBaseConfig


class Config:
    config_file: str
    configs: dict
    app: AppConfig
    database: DataBaseConfig
    origins: list[str]

    def __init__(self):
        self.is_loaded = False

    def load(self, config_file: str = "config.yml"):
        self.config_file = config_file
        self._set_configs()
        self.is_loaded = True
        return self

    def _set_configs(self):
        with open(f"{self.config_file}", "r") as config_file:
            configs = safe_load(config_file)
        self.configs = configs
        load_dotenv(self.configs["env_file"])
        self.set_app()
        self.set_database()
        self.set_logger()
        self.set_origins()

    def set_app(self):
        app_configs = self.configs["app"]
        self.app = AppConfig(
            host=app_configs["host"],
            port=app_configs["port"],
        )

    def set_database(self):
        db_configs = self.configs["database"]
        self.database = DataBaseConfig(db_configs)

    def set_logger(self):
        logger_configs = self.configs["logger"]
        logger.remove()
        logger.add(
            sink=logger_configs["sink"],
            format=logger_configs["format"],
            level=logger_configs["level"],
            rotation=logger_configs["rotation"],
            compression=logger_configs["compression"],
        )

    def set_origins(self):
        self.origins = self.configs["origins"]


config = Config().load()
