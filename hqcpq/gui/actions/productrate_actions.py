from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QComboBox

from hqcpq.classes.Product import Product
from hqcpq.classes.ProductRate import ProductRate
from hqcpq.classes.RateType import RateType
from hqcpq.db.SQLiteUtil import SQLiteConnection
from hqcpq.gui.components.main_window import Ui_MainWindow
from hqcpq.gui.classes.InfoMessageBox import InfoMessageBox
from hqcpq.gui.classes.ErrorMessageBox import ErrorMessageBox
from hqcpq.gui.classes.AskYesNoMessageBox import AskYesNoMessageBox
from hqcpq.gui.helpers import selected_row_id, change_view, toggle_buttons
from hqcpq.gui.view_enum import ViewPage
from hqcpq.helpers.conversion import string_to_float
from hqcpq.helpers.conversion import string_to_int

products: dict[int, Product] = dict()
product_rates: dict[int, ProductRate] = dict()
rate_types: dict[int, RateType] = dict()
product_rates_for_product: dict[int, ProductRate] = dict()


def fetch_global_entities():
    global products, product_rates, rate_types
    products = Product.get_all()
    product_rates = ProductRate.get_all()


def fetch_product_rates_for_product(main_window: Ui_MainWindow):
    product_id: int = string_to_int(main_window.lblProductId.text())

    if not product_id:
        return

    global product_rates_for_product
    product_rates_for_product = ProductRate.get_by_product_id(product_id)


def on_row_select(main_window: Ui_MainWindow):

    selected_id: int = selected_row_id(main_window.tblProductRates)

    toggle_buttons(
        [
            (main_window.btnNewProductRate, True),
            (main_window.btnEditProductRate, selected_id is not None),
            (main_window.btnDeleteProductRate, selected_id is not None),
        ]
    )


def refresh_table(main_window: Ui_MainWindow):

    tbl: QTableWidget = main_window.tblProductRates

    fetch_product_rates_for_product(main_window)
    global product_rates_for_product

    tbl_headers: list[str] = ["ID", "Name", "Rate", "Weighbridge ID"]
    tbl.clear()
    tbl.setRowCount(len(product_rates_for_product))
    tbl.setColumnCount(len(tbl_headers))
    tbl.setHorizontalHeaderLabels(tbl_headers)

    index = 0
    for obj_id, record in product_rates_for_product.items():
        tbl.setItem(index, 0, QTableWidgetItem(str(record.id)))
        tbl.setItem(index, 1, QTableWidgetItem(record.name))
        tbl.setItem(index, 2, QTableWidgetItem(str(record.rate)))
        tbl.setItem(index, 3, QTableWidgetItem(str(record.weighbridge_product_rate_id)))
        index += 1

    toggle_buttons(
        [
            (main_window.btnNewProductRate, True),
            (main_window.btnEditProductRate, False),
            (main_window.btnDeleteProductRate, False),
        ]
    )


def clear_entry_fields(main_window: Ui_MainWindow):
    fetch_product_rates_for_product(main_window)
    fetch_global_entities()

    global rate_types, product_rates_for_product

    main_window.lblProductRate_Id.clear()
    main_window.txtProductRate_WeighbridgeId.clear()
    main_window.txtProductRate_Name.clear()
    main_window.txtProductRate_Rate.clear()


def new(main_window: Ui_MainWindow):
    clear_entry_fields(main_window)
    change_view(main_window.swPages, ViewPage.PRODUCT_RATE_ENTRY)


def edit(main_window: Ui_MainWindow):
    selected_id: int = selected_row_id(main_window.tblProductRates)

    clear_entry_fields(main_window)

    global product_rates_for_product
    record = product_rates_for_product[selected_id]

    if not record:
        return

    main_window.lblProductRate_Id.setText(str(record.id))
    main_window.txtProductRate_WeighbridgeId.setText(str(record.weighbridge_product_rate_id))
    main_window.txtProductRate_Name.setText(record.name)
    main_window.txtProductRate_Rate.setText(str(record.rate))

    change_view(main_window.swPages, ViewPage.PRODUCT_RATE_ENTRY)


def delete(main_window: Ui_MainWindow):
    selected_id: int = selected_row_id(main_window.tblProductRates)

    global product_rates
    product_rate: ProductRate = product_rates[selected_id]

    delete_confirmed: bool = AskYesNoMessageBox(f"Are you sure that you would like to delete Product Rate with id: {product_rate.id}?")

    if not delete_confirmed:
        return

    ProductRate.delete(product_rate.id)

    del product_rates[product_rate.id]

    refresh_table(main_window)

    InfoMessageBox(f"Product Rate id: {product_rate.id}, successfully deleted.")


def save(main_window: Ui_MainWindow):

    if form_is_valid(main_window) is False:
        return

    product_id: int = string_to_int(main_window.lblProductId.text())
    product_rate_id: int = string_to_int(main_window.lblProductRate_Id.text())
    product_rate_weighbridge_id: int = string_to_int(main_window.txtProductRate_WeighbridgeId.text())
    product_rate_name: str = main_window.txtProductRate_Name.text()
    product_rate_rate: float = string_to_float(main_window.txtProductRate_Rate.text())

    product_rate = ProductRate(product_rate_id, product_rate_weighbridge_id, product_rate_name, product_rate_rate, product_id)

    product_rate.update() if product_rate_id else product_rate.insert()

    refresh_table(main_window)

    change_view(main_window.swPages, ViewPage.PRODUCT_ENTRY)

    clear_entry_fields(main_window)

    InfoMessageBox(f"Successfully saved Product Rate id: {product_rate.id}.")


def form_is_valid(main_window: Ui_MainWindow):

    error_string = str()

    product_rate_id: int = string_to_int(main_window.lblProductRate_Id.text())
    product_rate_weighbridge_id: int = string_to_int(main_window.txtProductRate_WeighbridgeId.text())
    product_rate_name: str = main_window.txtProductRate_Name.text()
    product_rate_rate: float = string_to_float(main_window.txtProductRate_Rate.text())

    if product_rate_weighbridge_id is None:
        error_string += "\n- Weighbridge ID field cannot be blank."

    if len(product_rate_name) == 0:
        error_string += "\n- Name field cannot be blank."
    else:
        product_id: int = string_to_int(main_window.lblProductId.text())
        global product_rates
        if len([pr for pr in product_rates.values() if pr.product_id == product_id and pr.name.lower() == product_rate_name.lower() and pr.id != product_rate_id]) > 0:
            error_string += "\n- A Product Rate with this name already exists for this Product."

    if product_rate_rate is None:
        error_string += "\n- Rate field cannot be blank."

    if len(error_string) > 0:
        ErrorMessageBox(error_string)

    return len(error_string) == 0


def connect(main_window: Ui_MainWindow):
    main_window.tblProductRates.selectionModel().selectionChanged.connect(
        lambda: on_row_select(main_window)
    )
    main_window.btnNewProductRate.clicked.connect(lambda: new(main_window))
    main_window.btnEditProductRate.clicked.connect(lambda: edit(main_window))
    main_window.btnDeleteProductRate.clicked.connect(lambda: delete(main_window))
    main_window.btnSaveProductRate.clicked.connect(lambda: save(main_window))

    only_numeric_validator = QDoubleValidator()
    only_numeric_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
    only_numeric_validator.setRange(0.00, 9999.00, 2)
    main_window.txtProductRate_Rate.setValidator(only_numeric_validator)
