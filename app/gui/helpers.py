from PyQt5.QtWidgets import QTableWidget, QPushButton


def selected_row_id(tbl: QTableWidget):

    indexes = tbl.selectedIndexes()

    if len(indexes) == 0:
        return None

    selected_row = indexes[0].row()
    id_column = 0
    id = int(tbl.item(selected_row, id_column).text())

    return id


def change_view(stacked_widget, page_index: int):

    stacked_widget.setCurrentIndex(page_index)


def toggle_buttons(new_btn: QPushButton, show_new: bool, edit_btn: QPushButton, show_edit: bool, delete_btn: QPushButton, show_delete: bool):

    new_btn.setVisible(show_new)
    edit_btn.setVisible(show_edit)
    delete_btn.setVisible(show_delete)


def int_conv(value: str):

    if value.isnumeric():
        return int(value)

    return None


def float_conv(value: str):

    if value.isnumeric():
        return float(value)

    return None