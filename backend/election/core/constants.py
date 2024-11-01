# this module is not allowed to have any other project based imports

import contextvars
import dataclasses
import re
from dataclasses import Field
from pathlib import Path


@dataclasses.dataclass
class Configurations:
    version: float
    app_name: str
    download_path: Path
    portfolios_path: Path
    na_portfolio_path: Path
    secrets_path: Path
    google_oauth_secrets_path: Path
    google_oauth_creds: dict = None

    def __str__(self):
        for k, v in self.__dict__.items():
            print(k, v)
        return ""


@dataclasses.dataclass
class DBConfigurations:
    username: str = None
    password: str = None
    ip: str = None
    port: int = None
    database_name: str = None
    url: str = None
    engine_args: dict = None

    def make_url(self, url_frame):
        self.url = url_frame.format(
            username=self.username,
            password=self.password,
            ip=self.ip,
            port=self.port,
            database_name=self.database_name
        )

    def make_attributes(self, url_frame, url_string):
        pattern = re.sub(r"{(\w+)}", r"(?P<\1>[^:/@]+)", url_frame)
        match = re.match(pattern, url_string)
        self.url = url_string
        if match:
            extracted_values = match.groupdict()
            for key, value in extracted_values.items():
                setattr(self, key, value)
        else:
            raise ValueError("database url matching failed")

    def __str__(self):
        for k, v in self.__dict__.items():
            print(k, v)
        return ""


CONFIG_FILE_PATH = Path("C:\\Users\\7862s\\Desktop\\Election-System\\backend\\config.ini")

CONFIG = contextvars.ContextVar[Configurations]('config')
DB_CONFIG = contextvars.ContextVar[DBConfigurations]('dbconfig')


def get_config() -> Configurations:
    return CONFIG.get()


def get_dbconfig() -> DBConfigurations:
    return DB_CONFIG.get()
