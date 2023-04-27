import configparser
import os

CONFIG_PATH = "hqcpq\\config.ini"

def resource_path(relative_path):

    base_path = os.path.abspath(".")

    full_path = os.path.join(base_path, relative_path)

    return full_path


def read_config(confile_file_path: str = None):

    if not confile_file_path:
        confile_file_path = resource_path(CONFIG_PATH)

    config = configparser.ConfigParser()
    config.read(confile_file_path)
    return config


def update_config(config: configparser.ConfigParser, config_file_path: str = None):

    if not config_file_path:
        config_file_path = resource_path(CONFIG_PATH)

    with open(config_file_path, "w+") as configFile:
        config.write(configFile)