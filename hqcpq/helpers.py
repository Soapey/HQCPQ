import os
import configparser
import traceback
from datetime import datetime

CONFIG_PATH = "hqcpq\\config.ini"


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


def isfloat(value: str):
    try:
        f = float(value)
        return True
    except:
        return False


def isdate(value: str):

    try:
        datetime.strptime(value, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def int_conv(value: str):
    return int(value) if value.isnumeric() else None


def float_conv(value: str):
    return float(value) if isfloat(value) else None


def get_transport_rate_ex_gst(kilometres: int, charge_type: str):

    if kilometres == 0:
        return 0

    config = read_config()['TransportSettings']

    bracket_size = int(config['bracket_size'])

    if charge_type.lower() == 'rigid':
        flagfall = float(config['flagfall_rigid'])
        starting_increment = float(config['starting_increment_rigid'])
        starting_jump = float(config['starting_jump_rigid'])
        jump_per_bracket = float(config['jump_per_bracket_rigid'])
    else:
        flagfall = float(config['flagfall_td'])
        starting_increment = float(config['starting_increment_td'])
        starting_jump = float(config['starting_jump_td'])
        jump_per_bracket = float(config['jump_per_bracket_td'])

    result: float = flagfall
    bracket_increment: float

    for i in range(1, kilometres + 1):
        bracket = ((i - 1) // bracket_size) + 1
        bracket_increment = starting_increment
        for j in range(1, bracket + 1):
            bracket_increment += starting_jump + (jump_per_bracket * (j - 1))
        print('kilometre:', i, 'increment:', bracket_increment)
        result += bracket_increment

    return round(result, 2)


def resource_path(relative_path):

    base_path = os.path.abspath(".")

    full_path = os.path.join(base_path, relative_path)

    return full_path


def log_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            with open('crash_log.txt', 'a') as f:
                traceback.print_exc(file=f)
            raise e
    return wrapper