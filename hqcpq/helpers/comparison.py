from datetime import datetime


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