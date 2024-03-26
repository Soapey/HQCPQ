import traceback
import re
import os
from hqcpq.helpers.io import read_config
from PyQt5.QtWidgets import QFileDialog


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
    kilometre_cap: int = int(config['kilometre_cap'])

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


def is_valid_email(email: str) -> bool:
    regex = r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(regex, email))


def select_directory():
    current_dir = os.getcwd()
    return QFileDialog.getExistingDirectory(None, "Select Directory", current_dir)


def insert_newline_at_max_length(string, max_length):
    lines = []
    current_line = ''

    for char in string:
        if char == '\n':
            lines.append(current_line.strip())  # Add the current line to the list of lines
            current_line = ''  # Start a new line
        elif len(current_line) < max_length:  # If the current line length is less than the max length
            current_line += char  # Add the character to the current line
        else:
            lines.append(current_line.strip())  # Add the current line to the list of lines
            current_line = char  # Start a new line with the current character

    if current_line:
        lines.append(current_line.strip())  # Add the last line if there's any remaining text

    return lines

