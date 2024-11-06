import configparser
import json
from pathlib import Path

from election.core import constants
from election.core.constants import Configurations, DBConfigurations, GoogleOAuthCreds, \
    JWTConfigurations, get_config


def make_default_config(config_fd: "A file descriptor"):
    parser = configparser.ConfigParser()
    parser.read_file(config_fd)
    basic_configs = parser['BASIC']
    paths = parser['PATHS']

    constants.CONFIG = Configurations(
        version=basic_configs.getfloat('VERSION'),
        app_name=basic_configs['APP_NAME'],
        download_path=Path(paths['DOWNLOAD_PATH']),
        portfolios_path=Path(paths['PORTFOLIOS_PATH']),
        na_portfolio_path=Path(paths['PORTFOLIOS_PATH']) / Path(paths['NA_PORTFOLIO']),
        secrets_path=Path(paths['SECRETS_PATH']),
        google_oauth_secrets_path=Path(paths['GOOGLE_OAUTH_SECRETS_PATH']),
    )

    with open(get_config().secrets_path / Path("google_oauth.json")) as f:
        g_creds = json.load(fp=f)

    gcreds = g_creds['web']

    constants.GOOGLE_AUTH_CREDS = GoogleOAuthCreds(
        client_id=gcreds['client_id'],
        auth_uri=gcreds['auth_uri'],
        token_uri=gcreds['token_uri'],
        auth_provider_x509_cert_url=gcreds['auth_provider_x509_cert_url'],
        client_secret=gcreds['client_secret'],
        redirect_uris=gcreds['redirect_uris'],
        javascript_origins=gcreds['javascript_origins'],
    )

    with open(get_config().secrets_path / Path("jwtcreds.ini")) as f:
        config = configparser.ConfigParser()
        config.read_file(f)
        constants.JWT_CONFIG = JWTConfigurations(
            secret_key=config['JWT']['SECRET_KEY'],
            algorithm=config['JWT']['ALGORITHM'],
            expire_time_min=config['JWT'].getint('EXPIRE_TIME_MIN'),
        )


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
        inmemory_dict_path=dbconfig['INMEMORY_DICT_PATH'],
    )
    dbconfigs.make_url(dbconfig['URL'])
    dbconfigs.engine_args = {
        'connect_args': {"server_settings": {"jit": dbconfig['JIT']}},
    }
    constants.DB_CONFIG = dbconfigs


def make_db_configurations(url_frame, url):
    dbconfig = DBConfigurations()
    dbconfig.make_attributes(url, url_frame)
    constants.DB_CONFIG = dbconfig
