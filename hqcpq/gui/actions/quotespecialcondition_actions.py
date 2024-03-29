from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView, QCheckBox

from hqcpq.classes.Quote import Quote
from hqcpq.classes.SpecialCondition import SpecialCondition
from hqcpq.classes.QuoteSpecialCondition import QuoteSpecialCondition
from hqcpq.gui.components.main_window import Ui_MainWindow
from hqcpq.gui.helpers import selected_row_id

special_conditions: dict[int, SpecialCondition] = dict()


def fetch_global_entities():
    global special_conditions
    special_conditions = SpecialCondition.get_all()


def on_checkbox_state_changed(state, table_widget, row):
    checkbox_widget = table_widget.cellWidget(row, 3)  # Get the checkbox widget in the specified cell
    if isinstance(checkbox_widget, QCheckBox):  # Ensure it's a checkbox widget
        if state == Qt.Checked:
            checkbox_widget.setCheckState(Qt.Checked)  # Set the checkbox state to checked
        else:
            checkbox_widget.setCheckState(Qt.Unchecked)  # Set the checkbox state to unchecked


def get_checkbox_state(table_widget, row):
    checkbox_widget = table_widget.cellWidget(row, 3)  # Get the checkbox widget in the specified cell
    if isinstance(checkbox_widget, QCheckBox):  # Ensure it's a checkbox widget
        return checkbox_widget.isChecked()  # Return whether the checkbox is checked or not


def refresh_table(main_window: Ui_MainWindow, quote_id=None):
    fetch_global_entities()

    selected_quote_id = quote_id or selected_row_id(main_window.tblQuotes)

    quote = Quote.get(selected_quote_id)

    tbl_headers = [
        "ID",
        "Name",
        "Message",
        "Is Added"
    ]

    tbl = main_window.tblQuoteSpecialConditions
    tbl.clear()
    tbl.setRowCount(len(special_conditions.values()))
    tbl.setColumnCount(len(tbl_headers))
    tbl.setHorizontalHeaderLabels(tbl_headers)

    header = tbl.horizontalHeader()
    for i in range(len(tbl_headers)):
        header.setSectionResizeMode(
            i,
            QHeaderView.ResizeToContents
            if i < len(tbl_headers) - 1
            else QHeaderView.Stretch,
        )

    for index, special_condition in enumerate(special_conditions.values()):
        tbl.setItem(index, 0, QTableWidgetItem(str(special_condition.id)))
        tbl.setItem(index, 1, QTableWidgetItem(special_condition.name))
        tbl.setItem(index, 2, QTableWidgetItem(special_condition.message))

        if quote:
            quote_special_condition = QuoteSpecialCondition.get_by_quote_and_special_condition(quote.id, special_condition.id)
            if quote_special_condition is None:
                quote_special_condition = QuoteSpecialCondition(0, quote.id, special_condition.id, special_condition.is_default)
            checkbox_item_ischecked = quote_special_condition.is_checked
        else:
            checkbox_item_ischecked = special_condition.is_default

        # Create checkbox
        checkbox = QCheckBox()
        checkbox.setChecked(checkbox_item_ischecked)  # Set initial checked state
        checkbox.stateChanged.connect(lambda state, tw=tbl, r=index: on_checkbox_state_changed(state, tw, r))

        tbl.setCellWidget(index, 3, checkbox)
