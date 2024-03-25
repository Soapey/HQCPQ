from PyQt5.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)

from hqcpq.classes.SpecialCondition import SpecialCondition
from hqcpq.gui.components.main_window import Ui_MainWindow
from hqcpq.gui.classes.InfoMessageBox import InfoMessageBox
from hqcpq.gui.classes.ErrorMessageBox import ErrorMessageBox
from hqcpq.gui.classes.AskYesNoMessageBox import AskYesNoMessageBox
from hqcpq.gui.helpers import change_view, selected_row_id, toggle_buttons
from hqcpq.gui.view_enum import ViewPage
from hqcpq.helpers.conversion import string_to_int

special_conditions: dict[int, SpecialCondition] = dict()
matches: dict[int, SpecialCondition] = dict()


def navigate_to_listing_view(main_window: Ui_MainWindow):

    global special_conditions, matches
    special_conditions = SpecialCondition.get_all()
    matches = special_conditions

    refresh_table(main_window)

    change_view(main_window.swPages, ViewPage.SPECIAL_CONDITIONS)


def search(main_window: Ui_MainWindow, search_text: str):

    global special_conditions, matches
    matches = (
        special_conditions
        if not search_text
        else {
            sc.id: sc
            for sc in special_conditions.values()
            if search_text in sc.name.lower()
        }
    )

    refresh_table(main_window)


def on_row_select(main_window: Ui_MainWindow):

    selected_id: int = selected_row_id(main_window.tblSpecialConditions)

    toggle_buttons(
        [
            (main_window.btnNewSpecialCondition, True),
            (main_window.btnEditSpecialCondition, selected_id is not None),
            (main_window.btnDeleteSpecialCondition, selected_id is not None),
        ]
    )


def refresh_table(main_window: Ui_MainWindow):

    global matches

    tbl_headers = ["ID", "Name", "Message", "Is Default"]

    tbl: QTableWidget = main_window.tblSpecialConditions
    tbl.clear()
    tbl.setRowCount(len(matches.values()))
    tbl.setColumnCount(len(tbl_headers))
    tbl.setHorizontalHeaderLabels(tbl_headers)

    for index, special_condition in enumerate(matches.values()):
        tbl.setItem(index, 0, QTableWidgetItem(str(special_condition.id)))
        tbl.setItem(index, 1, QTableWidgetItem(special_condition.name))
        tbl.setItem(index, 2, QTableWidgetItem(special_condition.message))
        tbl.setItem(index, 3, QTableWidgetItem(str(special_condition.is_default)))

    header: QHeaderView = tbl.horizontalHeader()
    for i in range(len(tbl_headers)):
        header.setSectionResizeMode(
            i,
            QHeaderView.ResizeMode.ResizeToContents
            if i < len(tbl_headers) - 1
            else QHeaderView.ResizeMode.Stretch,
        )

    toggle_buttons(
        [
            (main_window.btnNewSpecialCondition, True),
            (main_window.btnEditSpecialCondition, False),
            (main_window.btnDeleteSpecialCondition, False),
        ]
    )


def clear_entry_fields(main_window: Ui_MainWindow):

    main_window.lblSpecialConditionId.clear()
    main_window.txtSpecialCondition_Name.clear()
    main_window.txtSpecialCondition_Message.clear()
    main_window.chkSpecialCondition_IsDefault.setChecked(False)


def new(main_window: Ui_MainWindow):

    clear_entry_fields(main_window)

    change_view(main_window.swPages, ViewPage.SPECIAL_CONDITION_ENTRY)


def edit(main_window: Ui_MainWindow):

    selected_id = selected_row_id(main_window.tblSpecialConditions)

    global special_conditions
    special_condition: SpecialCondition = special_conditions[selected_id]

    clear_entry_fields(main_window)

    main_window.lblSpecialConditionId.setText(str(special_condition.id))
    main_window.txtSpecialCondition_Name.setText(special_condition.name)
    main_window.txtSpecialCondition_Message.setPlainText(special_condition.message)
    main_window.chkSpecialCondition_IsDefault.setChecked(bool(special_condition.is_default))

    change_view(main_window.swPages, ViewPage.SPECIAL_CONDITION_ENTRY)


def delete(main_window: Ui_MainWindow):

    selected_id = selected_row_id(main_window.tblSpecialConditions)

    global special_conditions
    special_condition: SpecialCondition = special_conditions[selected_id]

    delete_confirmed: bool = AskYesNoMessageBox(f"Are you sure that you would like to delete {special_condition.name}?")

    if not delete_confirmed:
        return

    SpecialCondition.delete(special_condition.id)

    del special_conditions[special_condition.id]

    refresh_table(main_window)

    InfoMessageBox(f"Successfully deleted {special_condition.name}.")


def save(main_window: Ui_MainWindow):

    if form_is_valid(main_window) is False:
        return

    special_condition_id: int = string_to_int(main_window.lblSpecialConditionId.text())
    special_condition_name: str = main_window.txtSpecialCondition_Name.text()
    special_condition_message: str = main_window.txtSpecialCondition_Message.toPlainText()
    special_condition_is_default: bool = main_window.chkSpecialCondition_IsDefault.isChecked()

    special_condition = SpecialCondition(
        special_condition_id,
        special_condition_name,
        special_condition_message,
        int(special_condition_is_default),
    )

    special_condition.update() if special_condition_id else special_condition.insert()

    navigate_to_listing_view(main_window)

    clear_entry_fields(main_window)

    InfoMessageBox(f"Successfully saved {special_condition.name}.")


def form_is_valid(main_window: Ui_MainWindow):

    error_string = str()

    special_condition_name: str = main_window.txtSpecialCondition_Name.text()
    special_condition_message: str = main_window.txtSpecialCondition_Message.toPlainText()

    if len(special_condition_name) == 0:
        error_string += "\n- Name field cannot be blank."

    if len(special_condition_message) == 0:
        error_string += "\n- Message field cannot be blank."

    if len(error_string) > 0:
        ErrorMessageBox(error_string)

    return len(error_string) == 0


def connect(main_window: Ui_MainWindow):

    main_window.actionSpecial_Conditions.triggered.connect(
        lambda: navigate_to_listing_view(main_window)
    )
    main_window.tblSpecialConditions.selectionModel().selectionChanged.connect(
        lambda: on_row_select(main_window)
    )
    main_window.btnNewSpecialCondition.clicked.connect(lambda: new(main_window))
    main_window.btnEditSpecialCondition.clicked.connect(lambda: edit(main_window))
    main_window.btnDeleteSpecialCondition.clicked.connect(lambda: delete(main_window))
    main_window.btnSaveSpecialCondition.clicked.connect(lambda: save(main_window))
    main_window.txtSpecialConditionsSearch.textChanged.connect(
        lambda: search(
            main_window, main_window.txtSpecialConditionsSearch.text().lower()
        )
    )

