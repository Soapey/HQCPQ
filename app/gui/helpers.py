from PyQt5.QtWidgets import QTableWidget, QPushButton
from app.gui.view_enum import ViewPage


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


def toggle_buttons(
    new_btn: QPushButton,
    show_new: bool,
    edit_btn: QPushButton,
    show_edit: bool,
    delete_btn: QPushButton,
    show_delete: bool,
):
    new_btn.setVisible(show_new)
    edit_btn.setVisible(show_edit)
    delete_btn.setVisible(show_delete)


def isfloat(value: str):
    try:
        f = float(value)
        return True
    except:
        return False


def int_conv(value: str):
    return int(value) if value.isnumeric() else None


def float_conv(value: str):
    return float(value) if isfloat(value) else None
