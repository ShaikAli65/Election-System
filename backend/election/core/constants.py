# this module is not allowed to have any other project based imports

import dataclasses
import re
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
    gmail_path: Path

    def __str__(self):
        return ", ".join(str(k) for k in self.__dict__.items())


@dataclasses.dataclass(slots=True)
class GoogleOAuthCreds:
    client_id: str
    auth_uri: str
    token_uri: str
    auth_provider_x509_cert_url: str
    client_secret: str
    redirect_uris: list[str]
    javascript_origins: list[str]


@dataclasses.dataclass(slots=True)
class DBConfigurations:
    username: str = None
    password: str = None
    ip: str = None
    port: int = None
    database_name: str = None
    url: str = None
    engine_args: dict = None
    inmemory_dict_path: str = None

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


@dataclasses.dataclass(slots=True)
class JWTConfigurations:
    secret_key: str
    algorithm: str
    expire_time_min: int


CONFIG_FILE_PATH = Path("C:\\Users\\7862s\\Desktop\\Election-System\\backend\\config.ini")

CONFIG: Configurations | None = None
DB_CONFIG: DBConfigurations | None = None
GOOGLE_AUTH_CREDS: GoogleOAuthCreds | None = None
JWT_CONFIG: JWTConfigurations | None = None


def get_config() -> Configurations:
    global CONFIG
    return CONFIG


def get_dbconfig() -> DBConfigurations:
    return DB_CONFIG


def get_google_oauth_creds() -> GoogleOAuthCreds:
    return GOOGLE_AUTH_CREDS


def get_jwt_config() -> JWTConfigurations:
    return JWT_CONFIG
