from tkinter import messagebox
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QComboBox,
    QHeaderView,
)
from hqcpq.classes.Toast import Toast
from hqcpq.classes.VehicleCombination import VehicleCombination
from hqcpq.gui.components.main_window import Ui_MainWindow
from hqcpq.gui.view_enum import ViewPage
from hqcpq.helpers.conversion import string_to_float
from hqcpq.gui.helpers import change_view, selected_row_id, toggle_buttons
from hqcpq.helpers.conversion import string_to_int


vehicle_combinations: dict[int, VehicleCombination] = dict()
matches: dict[int, VehicleCombination] = dict()


def navigate_to_listing_view(main_window: Ui_MainWindow):

    global vehicle_combinations, matches
    vehicle_combinations = VehicleCombination.get()
    matches = vehicle_combinations

    refresh_table(main_window)

    change_view(main_window.swPages, ViewPage.VEHICLE_COMBINATIONS)


def search(main_window: Ui_MainWindow, search_text: str):

    global vehicle_combinations, matches
    matches = (
        vehicle_combinations
        if not search_text
        else {
            vc.id: vc
            for vc in vehicle_combinations.values()
            if search_text in vc.name.lower()
        }
    )

    refresh_table(main_window)


def on_row_select(main_window: Ui_MainWindow):

    selected_id: int = selected_row_id(main_window.tblVehicleCombinations)

    toggle_buttons(
        [
            (main_window.btnNewVehicleCombination, True),
            (main_window.btnEditVehicleCombination, selected_id is not None),
            (main_window.btnDeleteVehicleCombination, selected_id is not None),
        ]
    )


def refresh_table(main_window: Ui_MainWindow):

    global matches

    tbl_headers = ["ID", "Name", "Average Net", "Charge Type"]

    tbl: QTableWidget = main_window.tblVehicleCombinations
    tbl.clear()
    tbl.setRowCount(len(matches.values()))
    tbl.setColumnCount(len(tbl_headers))
    tbl.setHorizontalHeaderLabels(tbl_headers)

    for index, vehicle_combination in enumerate(matches.values()):
        tbl.setItem(index, 0, QTableWidgetItem(str(vehicle_combination.id)))
        tbl.setItem(index, 1, QTableWidgetItem(vehicle_combination.name))
        tbl.setItem(index, 2, QTableWidgetItem(str(vehicle_combination.net)))
        tbl.setItem(index, 3, QTableWidgetItem(vehicle_combination.charge_type))

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
            (main_window.btnNewVehicleCombination, True),
            (main_window.btnEditVehicleCombination, False),
            (main_window.btnDeleteVehicleCombination, False),
        ]
    )


def clear_entry_fields(main_window: Ui_MainWindow):

    main_window.lblVehicleCombinationId.clear()
    main_window.txtVehicleCombination_Name.clear()
    main_window.txtVehicleCombination_Net.clear()

    cmb: QComboBox = main_window.cmbVehicleCombination_ChargeType
    cmb.clear()
    cmb.addItem("Truck & Trailer")
    cmb.addItem("Rigid")
    cmb.setCurrentIndex(0)


def new(main_window: Ui_MainWindow):

    clear_entry_fields(main_window)

    change_view(main_window.swPages, ViewPage.VEHICLE_COMBINATION_ENTRY)


def edit(main_window: Ui_MainWindow):

    selected_id = selected_row_id(main_window.tblVehicleCombinations)

    global vehicle_combinations
    vehicle_combination: VehicleCombination = vehicle_combinations[selected_id]

    clear_entry_fields(main_window)

    main_window.lblVehicleCombinationId.setText(str(vehicle_combination.id))
    main_window.txtVehicleCombination_Name.setText(vehicle_combination.name)
    main_window.txtVehicleCombination_Net.setText(str(vehicle_combination.net))

    change_view(main_window.swPages, ViewPage.VEHICLE_COMBINATION_ENTRY)


def delete(main_window: Ui_MainWindow):

    selected_id = selected_row_id(main_window.tblVehicleCombinations)

    global vehicle_combinations
    vehicle_combination: VehicleCombination = vehicle_combinations[selected_id]

    delete_confirmed: bool = messagebox.askyesno(
        title="Confirm Delete",
        message=f"Are you sure that you would like to delete {vehicle_combination.name}?",
    )

    if not delete_confirmed:
        return

    vehicle_combination.delete()

    del vehicle_combinations[vehicle_combination.id]

    refresh_table(main_window)

    Toast("Delete Success", f"Successfully deleted {vehicle_combination.name}.").show()


def save(main_window: Ui_MainWindow):

    if form_is_valid(main_window) is False:
        return

    vehicle_combination_name: str = main_window.txtVehicleCombination_Name.text()
    vehicle_combination_id: int = string_to_int(main_window.lblVehicleCombinationId.text())
    vehicle_combination_net: float = string_to_float(
        main_window.txtVehicleCombination_Net.text()
    )
    vehicle_combination_charge_type: str = (
        main_window.cmbVehicleCombination_ChargeType.currentText()
    )

    vehicle_combination = VehicleCombination(
        vehicle_combination_id,
        vehicle_combination_name,
        vehicle_combination_net,
        vehicle_combination_charge_type,
    )

    vehicle_combination.update() if vehicle_combination_id else vehicle_combination.insert()

    navigate_to_listing_view(main_window)

    clear_entry_fields(main_window)

    Toast("Save Success", f"Successfully saved {vehicle_combination.name}.").show()


def form_is_valid(main_window: Ui_MainWindow):

    result = True
    error_string = str()

    vehicle_combination_id: int = string_to_int(main_window.lblVehicleCombinationId.text())
    vehicle_combination_name: str = main_window.txtVehicleCombination_Name.text()

    if not vehicle_combination_name:
        result = False
        error_string += "\n- Name field cannot be blank."

    else:

        global vehicle_combinations
        entities_with_same_name = [
            vc
            for vc in vehicle_combinations.values()
            if vc.name == vehicle_combination_name and vc.id != vehicle_combination_id
        ]

        if len(entities_with_same_name) > 0:
            result = False
            error_string += f"\n- {vehicle_combination_name} already exists."

    if result == False:
        messagebox.showerror("Save Error", error_string)

    return result


def connect(main_window: Ui_MainWindow):

    main_window.actionVehicle_Combinations.triggered.connect(
        lambda: navigate_to_listing_view(main_window)
    )
    main_window.tblVehicleCombinations.selectionModel().selectionChanged.connect(
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
