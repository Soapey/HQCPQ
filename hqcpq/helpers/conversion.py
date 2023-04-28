from datetime import datetime
from hqcpq.helpers.comparison import can_be_float


def string_to_int(value: str) -> int:
    """
    Converts a string to an integer if possible.

    Args:
        value (str): The string value to be converted.

    Returns:
        int: The integer representation of the string if conversion is possible, else None.
    """
    return int(value) if value.isnumeric() else None


def string_to_float(value: str) -> float:
    """
    Converts a string to a float if possible.

    Args:
        value (str): The string value to be converted.

    Returns:
        float: The float representation of the string if conversion is possible, else None.
    """
    return float(value) if can_be_float(value) else None


def string_to_date(date_str: str, formats: list[str] = None) -> datetime.date:
    """
    Converts a string to a date if possible.

    Args:
        date_str (str): The string value to be converted to date.
        formats (list[str], optional): A list of date formats to try for conversion. Defaults to None.

    Returns:
        datetime.date: The datetime.date object if the string can be converted, else None.
    """
    if not formats:
        formats = ['%d/%m/%Y', '%d/%m/%y']

    for fmt in formats:
        try:
            date = datetime.strptime(date_str, fmt).date()
            return date
        except ValueError:
            pass
    return None
