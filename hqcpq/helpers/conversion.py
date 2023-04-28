from datetime import datetime
from hqcpq.helpers.comparison import can_be_float


def string_to_int(value: str) -> int:
    return int(value) if value.isnumeric() else None


def string_to_float(value: str) -> float:
    return float(value) if can_be_float(value) else None


def string_to_date(date_str, formats: list = None):

    if not formats:
        formats = ['%d/%m/%Y', '%d/%m/%y']

    for fmt in formats:
        try:
            date = datetime.strptime(date_str, fmt).date()
            return date
        except ValueError:
            pass
    return None
