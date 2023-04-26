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

    start: float = 0
    rate_per_km: float = 0
    jump_per_50: float = 0

    match charge_type:
        case "Truck & Trailer":
            start = 3.43
            rate_per_km = 0.11
            jump_per_50 = 0.03
        case "Rigid":
            start = 8.92
            rate_per_km = 0.12
            jump_per_50 = 0.04

    result: float = start
    section: float = 0
    for i in range(1, kilometres + 1):
        section = int(i / 50) + 1
        result = result + (rate_per_km + (jump_per_50 * section))

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