from PyQt5.QtWidgets import QTableWidget, QPushButton
from app.gui.view_enum import ViewPage
from datetime import datetime


def change_view(stacked_widget, page: ViewPage):
    stacked_widget.setCurrentIndex(page.value)


def selected_row_id(tbl: QTableWidget):

    indexes = tbl.selectedIndexes()

    if len(indexes) == 0:
        return None

    selected_row = indexes[0].row()
    id_column = 0
    id = int(tbl.item(selected_row, id_column).text())

    return id


def toggle_buttons(button_show_tuple_list: list[tuple]):

    for t in button_show_tuple_list:
        button: QPushButton = t[0]
        show_hide: bool = t[1]
        button.setVisible(show_hide)


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
