from tkinter import messagebox
from app.classes.VehicleCombination import VehicleCombination
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton, QComboBox
from app.gui.view_enum import ViewPage
from app.gui.helpers import change_view, selected_row_id, int_conv, float_conv


entities: list[VehicleCombination] = list()


def change_to_vehiclecombinations_view(main_window):

    global entities
    entities = VehicleCombination.get()

    refresh_table(main_window, entities)

    change_view(main_window.swPages, ViewPage.VEHICLE_COMBINATIONS)


def search(main_window, search_text):

    global entities
    matching_products = list(filter(lambda e: search_text in e.name.lower(), entities))

    refresh_table(main_window, matching_products)


def on_row_select(main_window):

    tbl: QTableWidget = main_window.tblVehicleCombinations

    selected_id = selected_row_id(tbl)

    edit_button: QPushButton = main_window.btnEditVehicleCombination
    delete_button: QPushButton = main_window.btnDeleteVehicleCombination

    if selected_id:
        edit_button.setVisible(True)
        delete_button.setVisible(True)
    else:
        edit_button.setVisible(False)
        delete_button.setVisible(False)


def refresh_table(main_window, fetched_entities: list[VehicleCombination] = None):

    fetched_entities = fetched_entities or entities

    tbl: QTableWidget = main_window.tblVehicleCombinations

    headers = ["ID", "Name", "Average Net"]

    tbl.setRowCount(len(fetched_entities))
    tbl.setColumnCount(len(headers))
    tbl.setHorizontalHeaderLabels(headers)

    for index, entity in enumerate(fetched_entities):
        tbl.setItem(index, 0, QTableWidgetItem(str(entity.id)))
        tbl.setItem(index, 1, QTableWidgetItem(entity.name))
        tbl.setItem(index, 2, QTableWidgetItem(str(entity.net)))

    on_row_select(main_window)


def clear_entry_fields(main_window):

    main_window.lblVehicleCombinationId.clear()
    main_window.txtVehicleCombination_Name.clear()
    main_window.txtVehicleCombination_Net.clear()
    main_window.tblProductRates.setRowCount(0)

    cmb: QComboBox = main_window.cmbVehicleCombination_ChargeType
    cmb.clear()
    cmb.addItem("Truck & Trailer")
    cmb.addItem("Rigid")
    cmb.setCurrentIndex(0)


def new(main_window):

    clear_entry_fields(main_window)

    change_view(main_window.swPages, ViewPage.VEHICLE_COMBINATION_ENTRY)


def edit(main_window):

    selected_id = selected_row_id(main_window.tblVehicleCombinations)

    entity = list(filter(lambda e: e.id == selected_id, entities))[0]

    clear_entry_fields(main_window)

    main_window.lblVehicleCombinationId.setText(str(entity.id))
    main_window.txtVehicleCombination_Name.setText(entity.name)
    main_window.txtVehicleCombination_Net.setText(entity.net)

    change_view(main_window.swPages, ViewPage.VEHICLE_COMBINATION_ENTRY)


def delete(main_window):

    selected_id = selected_row_id(main_window.tblVehicleCombinations)

    entity = list(filter(lambda e: e.id == selected_id, entities))[0]
    entity.delete()
    entities.remove(entity)

    refresh_table(main_window)


def save(main_window):

    if form_is_valid(main_window):

        id: int = int_conv(main_window.lblVehicleCombinationId.text())
        name: str = main_window.txtVehicleCombination_Name.text()
        net: float = float_conv(main_window.txtVehicleCombination_Net.text())
        charge_type: str = main_window.cmbVehicleCombination_ChargeType.text()

        vc = VehicleCombination(id, name, net, charge_type)

        vc.update() if id else vc.insert()

        change_to_vehiclecombinations_view(main_window)

        clear_entry_fields(main_window)


def form_is_valid(main_window):

    result = True
    error_string = str()

    id: int = int_conv(main_window.lblVehicleCombinationId.text())
    name: str = main_window.txtVehicleCombination_Name.text()

    if not name:
        result = False
        error_string += "\n- Name field cannot be blank."

    else:
        entities_with_same_name = list(
            filter(lambda e: e.name == name and e.id != id, entities)
        )

        if len(entities_with_same_name) > 0:
            result = False
            error_string += f"\n- {name} already exists."

    if result == False:
        messagebox.showerror("Save Error", error_string)

    return result


def connect(main_window):

    main_window.actionVehicle_Combinations.triggered.connect(
        lambda: change_to_vehiclecombinations_view(main_window)
    )
    main_window.tblProducts.selectionModel().selectionChanged.connect(
        lambda: on_row_select(main_window)
    )
    main_window.btnNewVehicleCombination.clicked.connect(lambda: new(main_window))
    main_window.btnEditVehicleCombination.clicked.connect(lambda: edit(main_window))
    main_window.btnDeleteVehicleCombination.clicked.connect(lambda: delete(main_window))
    main_window.btnSaveVehicleCombination.clicked.connect(lambda: save(main_window))
    main_window.txtVehicleCombinationSearch.textChanged.connect(
        lambda: search(
            main_window, main_window.txtVehicleCombinationSearch.text().lower()
        )
    )

    # Set numeric only validator on Net textbox.
    onlyNumeric = QDoubleValidator()
    onlyNumeric.setNotation(QDoubleValidator.Notation.StandardNotation)
    onlyNumeric.setRange(0.0, 9999.0, 2)
    main_window.txtVehicleCombination_Net.setValidator(onlyNumeric)
