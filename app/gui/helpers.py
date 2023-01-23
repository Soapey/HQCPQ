from PyQt5.QtWidgets import QTableWidget


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