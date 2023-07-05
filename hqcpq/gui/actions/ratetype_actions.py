from tkinter.messagebox import showinfo, showerror, askyesno

from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

from hqcpq.classes.RateType import RateType
from hqcpq.gui.components.main_window import Ui_MainWindow
from hqcpq.gui.helpers import change_view, selected_row_id, toggle_buttons
from hqcpq.gui.view_enum import ViewPage
from hqcpq.helpers.conversion import string_to_int

rate_types: dict[int, RateType] = dict()
matches: dict[int, RateType] = dict()


def navigate_to_listing_view(main_window: Ui_MainWindow):

    global rate_types, matches
    rate_types = RateType.get_all()
    matches = rate_types

    refresh_table(main_window)

    change_view(main_window.swPages, ViewPage.RATE_TYPES)


def search(main_window: Ui_MainWindow, search_text: str):

    global rate_types, matches
    matches = (
        rate_types
        if not search_text
        else {rt.id: rt for rt in rate_types.values() if search_text in rt.name.lower()}
    )

    refresh_table(main_window)


def on_row_select(main_window: Ui_MainWindow):

    selected_id = selected_row_id(main_window.tblRateTypes)

    toggle_buttons(
        [
            (main_window.btnNewRateType, True),
            (main_window.btnEditRateType, selected_id is not None),
            (main_window.btnDeleteRateType, selected_id is not None),
        ]
    )


def refresh_table(main_window: Ui_MainWindow):

    global matches
    headers = ["ID", "Name"]

    tbl: QTableWidget = main_window.tblRateTypes
    tbl.clear()
    tbl.setRowCount(len(matches.values()))
    tbl.setColumnCount(len(headers))
    tbl.setHorizontalHeaderLabels(headers)

    for index, rate_type in enumerate(matches.values()):
        tbl.setItem(index, 0, QTableWidgetItem(str(rate_type.id)))
        tbl.setItem(index, 1, QTableWidgetItem(rate_type.name))

    toggle_buttons(
        [
            (main_window.btnNewRateType, True),
            (main_window.btnEditRateType, False),
            (main_window.btnDeleteRateType, False),
        ]
    )


def clear_entry_fields(main_window: Ui_MainWindow):

    main_window.lblRateTypeId.clear()
    main_window.txtRateType_Name.clear()


def new(main_window: Ui_MainWindow):

    clear_entry_fields(main_window)

    change_view(main_window.swPages, ViewPage.RATE_TYPE_ENTRY)


def edit(main_window: Ui_MainWindow):

    rate_type: RateType = rate_types[selected_row_id(main_window.tblRateTypes)]

    main_window.lblRateTypeId.setText(str(rate_type.id))
    main_window.txtRateType_Name.setText(rate_type.name)

    change_view(main_window.swPages, ViewPage.RATE_TYPE_ENTRY)


def delete(main_window: Ui_MainWindow):

    global rate_types
    rate_type: RateType = rate_types[selected_row_id(main_window.tblRateTypes)]

    delete_confirmed: bool = askyesno(
        title="Confirm Delete",
        message=f"Are you sure that you would like to delete {rate_type.name}?"
    )

    if not delete_confirmed:
        return

    RateType.delete(rate_type.id)

    del rate_types[rate_type.id]

    refresh_table(main_window)

    showinfo(title="Delete Success", message=f"{rate_type.name} successfully deleted.")


def save(main_window: Ui_MainWindow):

    if form_is_valid(main_window) is False:
        return

    rate_type_id: int = string_to_int(main_window.lblRateTypeId.text())
    rate_type_name: str = main_window.txtRateType_Name.text()

    rate_type: RateType = RateType(rate_type_id, rate_type_name)

    rate_type.update() if rate_type_id else rate_type.insert()

    navigate_to_listing_view(main_window)

    clear_entry_fields(main_window)

    showinfo(title="Save Success", message=f"Successfully saved {rate_type.name}.")


def form_is_valid(main_window: Ui_MainWindow):

    result = True
    error_string = str()

    entity_id: int = string_to_int(main_window.lblRateTypeId.text())
    entity_name: str = main_window.txtRateType_Name.text()

    if len(entity_name) == 0:
        result = False
        error_string += "\n- Name field cannot be blank."
    else:

        global rate_types
        ratetypes_with_same_name = [
            rt
            for rt in rate_types.values()
            if rt.name == entity_name and rt.id != entity_id
        ]

        if len(ratetypes_with_same_name) > 0:
            result = False
            error_string += f"\n- {entity_name} already exists."

    if result is False:
        showerror(title="Save Error", message=error_string)

    return result


def connect(main_window: Ui_MainWindow):

    main_window.actionRate_Types.triggered.connect(
        lambda: navigate_to_listing_view(main_window)
    )
    main_window.tblRateTypes.selectionModel().selectionChanged.connect(
        lambda: on_row_select(main_window)
    )
    main_window.btnNewRateType.clicked.connect(lambda: new(main_window))
    main_window.btnEditRateType.clicked.connect(lambda: edit(main_window))
    main_window.btnDeleteRateType.clicked.connect(lambda: delete(main_window))
    main_window.btnSaveRateType.clicked.connect(lambda: save(main_window))
    main_window.txtRateTypeSearch.textChanged.connect(
        lambda: search(main_window, main_window.txtRateTypeSearch.text().lower())
    )
