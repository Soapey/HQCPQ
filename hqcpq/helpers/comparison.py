from datetime import datetime


def can_be_float(value: str):
    try:
        f = float(value)
        return True
    except:
        return False


def can_be_date(value: str, formats: list = None):

    if not formats:
        formats = ['%d/%m/%Y', '%d/%m/%y']
        
    for format in formats:
        try:
            datetime.strptime(value, format)
            return True
        except ValueError:
            pass
    return False