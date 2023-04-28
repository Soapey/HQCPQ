import datetime


def can_be_float(value: str) -> bool:
    """
    Determines whether the given value can be parsed as a float.

    Args:
        value (str): The input string to be checked.

    Returns:
        bool: True if the input value can be parsed as a float, False otherwise.
    """
    try:
        float(value)
        return True
    except ValueError:
        return False


def can_be_date(value: str, formats: list = None) -> bool:
    """
    Determines whether the given value can be parsed as a date using the specified date formats.

    Args:
        value (str): The input string to be checked.
        formats (list, optional): A list of date formats to try. Defaults to ['%d/%m/%Y', '%d/%m/%y'].

    Returns:
        bool: True if the input value can be parsed as a date using any of the specified date formats, False otherwise.
    """
    if not formats:
        formats = ['%d/%m/%Y', '%d/%m/%y']
    
    for date_format in formats:
        try:
            datetime.datetime.strptime(value, date_format)
            return True
        except ValueError:
            pass
    return False
