from tkinter import messagebox
from app.classes.RateType import RateType
from app.gui.view_enum import ViewPage
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton
from app.gui.helpers import change_view, selected_row_id


entities: list[RateType] = list()


def change_to_rate_type_view(main_window):

    global entities
    entities = RateType.get()

    refresh_table(main_window, entities)

    main_window.swPages.setCurrentIndex(4)


def search(main_window, search_text):

    global entities
    matching_products = list(filter(lambda e: search_text in e.name.lower(), entities))

    refresh_table(main_window, matching_products)


def on_row_select(main_window):

    tbl: QTableWidget = main_window.tblRateTypes

    selected_id = selected_row_id(tbl)

    edit_button: QPushButton = main_window.btnEditRateType
    delete_button: QPushButton = main_window.btnDeleteRateType

    if selected_id:
        edit_button.setVisible(True)
        delete_button.setVisible(True)
    else:
        edit_button.setVisible(False)
        delete_button.setVisible(False)


def refresh_table(main_window, fetched_entities: list[RateType] = None):

    tbl: QTableWidget = main_window.tblRateTypes

    headers = ["ID", "Name"]
    tbl.setRowCount(len(fetched_entities))
    tbl.setColumnCount(len(headers))
    tbl.setHorizontalHeaderLabels(headers)

    for index, entity in enumerate(fetched_entities):
        tbl.setItem(index, 0, QTableWidgetItem(str(entity.id)))
        tbl.setItem(index, 1, QTableWidgetItem(entity.name))

    on_row_select(main_window)


def clear_entry_fields(main_window):

    main_window.lblRateTypeId.clear()
    main_window.txtRateType_Name.clear()


def new(main_window):

    clear_entry_fields(main_window)

    change_view(main_window.swPages, ViewPage.RATE_TYPE_ENTRY)


def edit(main_window):

    selected_id = selected_row_id(main_window.tblRateTypes)

    entity = list(filter(lambda e: e.id == selected_id, entities))[0]

    main_window.lblRateTypeId.setText(str(entity.id))
    main_window.txtRateType_Name.setText(entity.name)

    change_view(main_window.swPages, ViewPage.RATE_TYPE_ENTRY)


def delete(main_window):

    selected_id = selected_row_id(main_window.tblRateTypes)

    entity = list(filter(lambda e: e.id == selected_id, entities))[0]
    entity.delete()

    refresh_table(main_window)


def save(main_window):

    if form_is_valid(main_window):

        id_label_text = main_window.lblRateTypeId.text()

        if len(id_label_text) > 0:
            RateType(int(id_label_text), main_window.txtRateType_Name.text()).update()
        else:
            RateType(None, main_window.txtRateType_Name.text()).insert()

        change_to_rate_type_view(main_window)

        clear_entry_fields(main_window)


def form_is_valid(main_window):

    result = True
    error_string = str()

    entity_id: int = 0
    entity_name = main_window.txtRateType_Name.text()
    id_label_text = main_window.lblRateTypeId.text()

    if len(id_label_text) > 0:
        entity_id = int(id_label_text)

    if len(entity_name) == 0:
        result = False
        error_string += "\n- Name field cannot be blank."
    else:
        ratetypes_with_same_name = list(
            filter(lambda e: e.name == entity_name and e.id != entity_id, entities)
        )

        if len(ratetypes_with_same_name) > 0:
            result = False
            error_string += f"\n- {entity_name} already exists."

    if result == False:
        messagebox.showerror("Save Error", error_string)

    return result


def connect(main_window):

    main_window.actionRate_Types.triggered.connect(
        lambda: change_to_rate_type_view(main_window)
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
