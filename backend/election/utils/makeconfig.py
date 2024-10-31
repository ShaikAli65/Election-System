import configparser
import json
from pathlib import Path

from core.constants import CONFIG, Configurations, DBConfigurations, DB_CONFIG


def make_default_config(config_fd: "A file descriptor"):
    parser = configparser.ConfigParser()
    parser.read_file(config_fd)
    basic_configs = parser['BASIC']
    paths = parser['PATHS']
    with open(paths['GOOGLE_OAUTH_SECRETS_PATH']) as f:
        g_creds = json.load(fp=f)

    CONFIG.set(Configurations(
        version=basic_configs.getfloat('VERSION'),
        app_name=basic_configs['APP_NAME'],
        download_path=Path(paths['DOWNLOAD_PATH']),
        portfolios_path=Path(paths['PORTFOLIOS_PATH']),
        na_portfolio_path=Path(paths['PORTFOLIOS_PATH']) / Path(paths['NA_PORTFOLIO']),
        secrets_path=Path(paths['SECRETS_PATH']),
        google_oauth_secrets_path=Path(paths['GOOGLE_OAUTH_SECRETS_PATH']),
        google_oauth_creds=g_creds,
    ))


def load_db_configs(config_fd: "A file descriptor"):
    parser = configparser.ConfigParser()
    parser.read_file(config_fd)

    dbconfig = parser['POSTGRES']

    dbconfigs = DBConfigurations(
        username=dbconfig['USERNAME'],
        password=dbconfig['PASSWORD'],
        ip=dbconfig['IP'],
        port=dbconfig.getint('PORT'),
        database_name=dbconfig['DATABASE_NAME'],
    )
    dbconfigs.make_url(dbconfig['URL'])
    dbconfigs.engine_args = {
        'connect_args': {
            "server_settings": {"jit": dbconfig.getboolean('JIT')}
        }
    }

    DB_CONFIG.set(dbconfigs)


def make_db_configurations(url_frame, url):
    dbconfig = DBConfigurations()
    dbconfig.make_attributes(url, url_frame)
    DB_CONFIG.set(dbconfig)
