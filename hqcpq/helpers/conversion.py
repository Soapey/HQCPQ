from hqcpq.helpers.comparison import isfloat


def string_to_int(value: str) -> int:
    return int(value) if value.isnumeric() else None


def string_to_float(value: str) -> float:
    return float(value) if isfloat(value) else None