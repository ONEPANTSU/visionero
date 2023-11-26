import os


class DataBaseConfig:
    driver: str
    host: str
    port: int
    name: str
    user: str
    password: str

    def __init__(self, db_configs):
        self.driver = db_configs["driver"]
        self.name = db_configs["name"]
        self.__set_protected_params()

    def __set_protected_params(self) -> None:
        self.user = os.environ.get("DB_USER")
        self.password = os.environ.get("DB_PASSWORD")
        self.host = os.environ.get("DB_HOST")
        self.port = os.environ.get("DB_PORT")

    def get_url(self) -> str:
        return self.get_default_url() + f"/{self.name}"

    def get_default_url(self) -> str:
        return f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}"
