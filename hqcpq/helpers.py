import os
import sys
import configparser
from datetime import datetime


def read_config():
    config = configparser.ConfigParser()
    config.read(resource_path("hqcpq\\config.ini"))
    return config


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
    for i in range(1, kilometres + 1):
        section = int(i / 50) + 1
        result = result + (rate_per_km + (jump_per_50 * section))

    return round(result, 2)


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""

    base_path = os.path.abspath(".")

    full_path = os.path.join(base_path, relative_path)

    print("Base Path:", base_path)
    print("Relative Path:", relative_path)
    print("Full Path:", full_path)

    return full_path
