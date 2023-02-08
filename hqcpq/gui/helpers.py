from PyQt5.QtWidgets import QTableWidget, QPushButton
from hqcpq.gui.view_enum import ViewPage


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
