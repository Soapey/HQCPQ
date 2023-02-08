from tkinter import messagebox
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QComboBox
from hqcpq.gui.components.main_window import Ui_MainWindow
from hqcpq.gui.view_enum import ViewPage
from hqcpq.classes.Toast import Toast
from hqcpq.classes.Product import Product
from hqcpq.classes.ProductRate import ProductRate
from hqcpq.classes.RateType import RateType
from hqcpq.db.db import get_cursor_type
from hqcpq.gui.helpers import selected_row_id, change_view, toggle_buttons
from hqcpq.helpers import int_conv, float_conv


# Global entities
products: dict[int, Product] = dict()
product_rates: dict[int, ProductRate] = dict()
rate_types: dict[int, RateType] = dict()
records: list[tuple] = dict()


def fetch_global_entities():

    global products, product_rates, rate_types
    products = Product.get()
    product_rates = ProductRate.get()
    rate_types = RateType.get()


def fetch_records(main_window: Ui_MainWindow):

    product_id: int = int_conv(main_window.lblProductId.text())

    with get_cursor_type() as cur:

        if cur and product_id:
            global records
            records = cur.execute(
                """
                SELECT pr.id, rt.name, pr.rate
                FROM product_rate pr
                LEFT JOIN rate_type rt ON pr.rate_type_id = rt.id
                WHERE pr.product_id = ?;
                """,
                (product_id,),
            ).fetchall()


def on_row_select(main_window: Ui_MainWindow):

    selected_id: int = selected_row_id(main_window.tblProductRates)

    toggle_buttons(
        [
            (main_window.btnNewProductRate, True),
            (main_window.btnEditProductRate, selected_id is not None),
            (main_window.btnDeleteProductRate, selected_id is not None),
        ]
    )


def refresh_table(main_window: Ui_MainWindow, selected_id: int = None):

    tbl: QTableWidget = main_window.tblProductRates

    fetch_records(main_window)
    global records

    tbl_headers: list[str] = ["ID", "Type", "Rate"]
    tbl.clear()
    tbl.setRowCount(len(records))
    tbl.setColumnCount(len(tbl_headers))
    tbl.setHorizontalHeaderLabels(tbl_headers)

    for index, record in enumerate(records):
        tbl.setItem(index, 0, QTableWidgetItem(str(record[0])))
        tbl.setItem(index, 1, QTableWidgetItem(record[1]))
        tbl.setItem(index, 2, QTableWidgetItem(str(record[2])))

    toggle_buttons(
        [
            (main_window.btnNewProductRate, True),
            (main_window.btnEditProductRate, False),
            (main_window.btnDeleteProductRate, False),
        ]
    )


def clear_entry_fields(main_window: Ui_MainWindow):

    # Fetch all RateTypes from SQLite database.
    fetch_records(main_window)
    fetch_global_entities()
    global rate_types, records

    main_window.lblProductRateId.clear()

    # Create list of RateType name options for the gui combobox.
    existing_ratetype_names: list[str] = [r[1] for r in records]
    selectable_rate_type_names = [
        rt.name for rt in rate_types.values() if rt.name not in existing_ratetype_names
    ]

    # Clear the gui combobox and fill with RateType name options.
    productrate_ratetype_combobox: QComboBox = main_window.cmbProductRate_RateType
    productrate_ratetype_combobox.clear()
    productrate_ratetype_combobox.addItems(selectable_rate_type_names)

    # Clear the Rate field textbox.
    main_window.txtProductRate_Rate.clear()


def new(main_window: Ui_MainWindow):

    clear_entry_fields(main_window)

    change_view(main_window.swPages, ViewPage.PRODUCT_RATE_ENTRY)


def edit(main_window: Ui_MainWindow):

    selected_id: int = selected_row_id(main_window.tblProductRates)

    clear_entry_fields(main_window)

    global records
    record_list: list[tuple] = [r for r in records if r[0] == selected_id]

    record = record_list[0] if record_list else None

    if not record:
        return

    main_window.lblProductRateId.setText(str(record[0]))
    main_window.cmbProductRate_RateType.addItem(record[1])
    main_window.cmbProductRate_RateType.setCurrentText(record[1])
    main_window.txtProductRate_Rate.setText(str(record[2]))

    change_view(main_window.swPages, ViewPage.PRODUCT_RATE_ENTRY)


def delete(main_window: Ui_MainWindow):

    global product_rates
    product_rate: ProductRate = product_rates[
        selected_row_id(main_window.tblProductRates)
    ]

    delete_confirmed: bool = messagebox.askyesno(
        title="Confirm Delete",
        message=f"Are you sure that you would like to delete Product Rate with id: {product_rate.id}?",
    )

    if not delete_confirmed:
        return

    product_rate.delete()

    del product_rates[product_rate.id]

    refresh_table(main_window, product_rate.product_id)

    Toast(
        "Delete Success", f"Product Rate id: {product_rate.id}, successfully deleted."
    ).show()


def save(main_window: Ui_MainWindow):

    if form_is_valid(main_window) is False:
        return

    selected_rate_type_name: str = main_window.cmbProductRate_RateType.currentText()

    product_rate_id: int = int_conv(main_window.lblProductRateId.text())
    product_id: int = int_conv(main_window.lblProductId.text())

    global rate_types
    rate_type_list: list[RateType] = [
        rt for rt in rate_types.values() if rt.name == selected_rate_type_name
    ]

    rate_type: RateType = rate_type_list[0] if rate_type_list else None
    rate: float = float_conv(main_window.txtProductRate_Rate.text())

    product_rate = ProductRate(product_rate_id, product_id, rate_type.id, rate)

    product_rate.update() if product_rate_id else product_rate.insert()

    refresh_table(main_window, product_id)

    change_view(main_window.swPages, ViewPage.PRODUCT_ENTRY)

    clear_entry_fields(main_window)

    Toast(
        "Save Success", f"Successfully saved Product Rate id: {product_rate.id}."
    ).show()


def form_is_valid(main_window: Ui_MainWindow):

    result: bool = True
    error_string: str = str()

    product_rate_id: int = int_conv(main_window.lblProductRateId.text())
    selected_rate_type_name: str = main_window.cmbProductRate_RateType.currentText()
    product_rate_rate: float = float_conv(main_window.txtProductRate_Rate.text())

    if not selected_rate_type_name:
        result = False
        error_string += "\n- Rate Type field cannot be blank."

    if not product_rate_rate:
        result = False
        error_string += "\n- Rate field cannot be blank."

    elif selected_rate_type_name and product_rate_rate:

        global rate_types, product_rates

        product_id: int = int(main_window.lblProductId.text())

        rate_type_list: list[RateType] = [
            rt for rt in rate_types.values() if rt.name == selected_rate_type_name
        ]

        rate_type: RateType = rate_type_list[0] if rate_type_list else None

        existing_product_rates = [
            pr
            for pr in product_rates.values()
            if pr.product_id == product_id
            and pr.rate_type_id == rate_type.id
            and pr.id != product_rate_id
        ]

        if len(existing_product_rates) > 0:
            result = False
            error_string += f"\n- {products[product_id].name} with a {rate_types[rate_type.id].name} rate already exists."

    if result is False:
        messagebox.showerror("Save Error", error_string)

    return result


def connect(main_window: Ui_MainWindow):

    # Connect all actions to lambda functions.
    main_window.tblProductRates.selectionModel().selectionChanged.connect(
        lambda: on_row_select(main_window)
    )
    main_window.btnNewProductRate.clicked.connect(lambda: new(main_window))
    main_window.btnEditProductRate.clicked.connect(lambda: edit(main_window))
    main_window.btnDeleteProductRate.clicked.connect(lambda: delete(main_window))
    main_window.btnSaveProductRate.clicked.connect(lambda: save(main_window))

    # Set numeric only validator on Rate textbox.
    onlyNumeric = QDoubleValidator()
    onlyNumeric.setNotation(QDoubleValidator.Notation.StandardNotation)
    onlyNumeric.setRange(0.00, 9999.00, 2)
    main_window.txtProductRate_Rate.setValidator(onlyNumeric)
