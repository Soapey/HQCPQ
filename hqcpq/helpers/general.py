import traceback
from hqcpq.helpers.io import read_config


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
    kilometre_cap: float = int(config['kilometre_cap'])

    for i in range(1, kilometres + 1):
        kilometre = min(i, kilometre_cap)
        bracket = ((kilometre - 1) // bracket_size) + 1
        bracket_increment = starting_increment
        for j in range(1, bracket + 1):
            bracket_increment += starting_jump + (jump_per_bracket * (j - 1))
        result += bracket_increment

    return round(result, 2)


def log_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            with open('crash_log.txt', 'a') as f:
                traceback.print_exc(file=f)
            raise e
    return wrapper