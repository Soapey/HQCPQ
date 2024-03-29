from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QComboBox, QHeaderView

from hqcpq.classes.Product import Product
from hqcpq.classes.ProductRate import ProductRate
from hqcpq.classes.Quote import Quote
from hqcpq.classes.QuoteItem import QuoteItem
from hqcpq.classes.RateType import RateType
from hqcpq.classes.VehicleCombination import VehicleCombination
from hqcpq.gui.components.main_window import Ui_MainWindow
from hqcpq.gui.classes.InfoMessageBox import InfoMessageBox
from hqcpq.gui.classes.ErrorMessageBox import ErrorMessageBox
from hqcpq.gui.classes.AskYesNoMessageBox import AskYesNoMessageBox
from hqcpq.gui.helpers import selected_row_id, toggle_buttons, change_view
from hqcpq.gui.view_enum import ViewPage
from hqcpq.helpers.conversion import string_to_float, string_to_int
from hqcpq.helpers.general import get_transport_rate_ex_gst

vehicle_combinations: dict[int, VehicleCombination] = dict()
products: dict[int, Product] = dict()
product_rates: dict[int, ProductRate] = dict()
quotes: dict[int, Quote] = dict()
quote_items: dict[int, QuoteItem] = dict()


def fetch_global_entities():

    global vehicle_combinations, products, product_rates, quotes, quote_items

    vehicle_combinations = VehicleCombination.get_all()
    products = Product.get_all()
    product_rates = ProductRate.get_all()
    quotes = Quote.get_all()
    quote_items = QuoteItem.get_all()


def refresh_table(main_window: Ui_MainWindow, quote_id: int = None):

    fetch_global_entities()

    selected_quote_id: int = quote_id or selected_row_id(main_window.tblQuotes)

    quote = Quote.get(selected_quote_id)

    tbl_headers: list[str] = [
        "ID",
        "Vehicle Combination",
        "Net",
        "Product",
        "Transport Rate ex. GST",
        "Product Rate ex. GST",
        "Total inc. GST",
    ]

    tbl: QTableWidget = main_window.tblQuoteItems
    tbl.clear()
    tbl.setRowCount(0)
    tbl.setColumnCount(len(tbl_headers))
    tbl.setHorizontalHeaderLabels(tbl_headers)

    header = tbl.horizontalHeader()
    for i in range(len(tbl_headers)):
        header.setSectionResizeMode(
            i,
            QHeaderView.ResizeMode.ResizeToContents
            if i < len(tbl_headers) - 1
            else QHeaderView.ResizeMode.Stretch,
        )

    if not quote:
        return

    global quote_items
    items: dict[int, QuoteItem] = quote.items()
    tbl.setRowCount(len(items))

    for index, quote_item in enumerate(items.values()):
        tbl.setItem(index, 0, QTableWidgetItem(str(quote_item.id)))
        tbl.setItem(index, 1, QTableWidgetItem(quote_item.vehicle_combination_name))
        tbl.setItem(index, 2, QTableWidgetItem(str(quote_item.vehicle_combination_net)))
        tbl.setItem(index, 3, QTableWidgetItem(quote_item.product_name))
        tbl.setItem(
            index,
            4,
            QTableWidgetItem("${:,.2f}".format(quote_item.transport_rate_ex_gst)),
        )
        tbl.setItem(
            index,
            5,
            QTableWidgetItem("${:,.2f}".format(quote_item.product_rate_ex_gst)),
        )
        tbl.setItem(
            index,
            6,
            QTableWidgetItem("${:,.2f}".format(quote_item.total_inc_gst())),
        )


def calculate_quote_item_totals(main_window: Ui_MainWindow, quote_id: int = None):

    selected_id: int = quote_id or selected_row_id(main_window.tblQuotes)
    quote = Quote.get(selected_id)

    if not quote:
        return

    transport_total_ex_gst: float = 0
    product_total_ex_gst: float = 0

    items = quote.items()

    for quote_item in items.values():
        transport_total_ex_gst += (
            quote_item.transport_rate_ex_gst * quote_item.vehicle_combination_net
        )
        product_total_ex_gst += (
            quote_item.product_rate_ex_gst * quote_item.vehicle_combination_net
        )

    main_window.lblQuote_ProductTotalExGST.setText(
        "${:,.2f}".format(product_total_ex_gst)
    )
    main_window.lblQuote_TransportTotalExGST.setText(
        "${:,.2f}".format(transport_total_ex_gst)
    )
    main_window.lblQuote_TotalExGST.setText(
        "${:,.2f}".format(product_total_ex_gst + transport_total_ex_gst)
    )
    main_window.lblQuote_TotalIncGST.setText(
        "${:,.2f}".format(1.1 * (product_total_ex_gst + transport_total_ex_gst))
    )


def update_product_rate(main_window: Ui_MainWindow):

    product_name = main_window.cmbQuoteItem_Product.currentText()
    product_rate_name = main_window.cmbQuoteItem_ProductRate.currentText()

    global product_rates

    product_rates_list = [
        pr
        for pr in product_rates.values()
        if products[pr.product_id].name == product_name
        and pr.name == product_rate_name
    ]

    product_rate: ProductRate = product_rates_list[0] if product_rates_list else None

    if not product_rate:
        return

    main_window.txtQuoteItem_ProductRate.setText(str(product_rate.rate))


def on_product_select(main_window: Ui_MainWindow):

    cmb_product_rates: QComboBox = main_window.cmbQuoteItem_ProductRate

    show_hide = len(main_window.cmbQuoteItem_Product.currentText()) > 0
    main_window.lblQuoteItem_ProductRate.setVisible(show_hide)
    cmb_product_rates.setVisible(show_hide)

    if show_hide is False:
        return

    selected_product_name: str = main_window.cmbQuoteItem_Product.currentText()

    global products
    products_list = [p for p in products.values() if p.name == selected_product_name]

    product: Product = products_list[0] if products_list else None

    product_rate_names = [pr.name for pr in product_rates.values() if pr.product_id == product.id]

    cmb_product_rates.clear()
    cmb_product_rates.addItems(product_rate_names)

    update_product_rate(main_window)


def update_transport_rate(main_window: Ui_MainWindow):
    selected_vehicle_combination_name: str = (
        main_window.cmbQuoteItem_VehicleCombination.currentText()
    )

    global vehicle_combinations
    vehicle_combinations_list = [
        vc
        for vc in vehicle_combinations.values()
        if vc.name == selected_vehicle_combination_name
    ]

    vehicle_combination: VehicleCombination = (
        vehicle_combinations_list[0] if vehicle_combinations_list else None
    )

    if vehicle_combination:
        main_window.txtQuoteItem_Tonnes.setText(str(vehicle_combination.net))

        quote_id: int = string_to_int(main_window.lblQuoteItem_QuoteId.text())

        if quote_id:
            kilometres = quotes[quote_id].kilometres

            main_window.txtQuoteItem_TransportRate.setText(
                str(
                    get_transport_rate_ex_gst(
                        kilometres,
                        vehicle_combination.charge_type,
                    )
                )
            )


def on_vehicle_combination_select(main_window: Ui_MainWindow):
    update_transport_rate(main_window)


def clear_entry_fields(main_window: Ui_MainWindow):

    main_window.lblQuoteItemId.clear()
    main_window.lblQuoteItem_QuoteId.clear()
    main_window.txtQuoteItem_Tonnes.clear()
    main_window.txtQuoteItem_ProductRate.clear()
    main_window.txtQuoteItem_TransportRate.clear()

    global vehicle_combinations
    cmb_vehicle_combinations: QComboBox = main_window.cmbQuoteItem_VehicleCombination
    cmb_vehicle_combinations.clear()
    cmb_vehicle_combinations.addItems([vc.name for vc in vehicle_combinations.values()])

    global products
    cmb_products: QComboBox = main_window.cmbQuoteItem_Product
    cmb_products.clear()
    cmb_products.addItems([p.name for p in products.values()])

    on_product_select(main_window)


def form_is_valid(main_window: Ui_MainWindow):

    result: bool = True
    error_string: str = str()

    if len(main_window.lblQuoteItem_QuoteId.text()) == 0:
        result = False
        error_string += "\n- Quote Id field cannot be blank."

    if len(main_window.cmbQuoteItem_VehicleCombination.currentText()) == 0:
        result = False
        error_string += "\n- Vehicle Combination field cannot be blank."

    if len(main_window.cmbQuoteItem_Product.currentText()) == 0:
        result = False
        error_string += "\n- Product field cannot be blank."

    if len(main_window.cmbQuoteItem_ProductRate.currentText()) == 0:
        result = False
        error_string += "\n- Rate Type field cannot be blank."

    if len(main_window.txtQuoteItem_Tonnes.text()) == 0:
        result = False
        error_string += "\n- Tonnes field cannot be blank."

    if len(main_window.txtQuoteItem_ProductRate.text()) == 0:
        result = False
        error_string += "\n- Product Rate field cannot be blank."

    if result is False:
        ErrorMessageBox(error_string)

    return result


def new(main_window: Ui_MainWindow):

    fetch_global_entities()

    clear_entry_fields(main_window)

    main_window.lblQuoteItem_QuoteId.setText(main_window.lblQuoteId.text())

    change_view(main_window.swPages, ViewPage.QUOTE_ITEM_ENTRY)

    update_transport_rate(main_window)


def edit(main_window: Ui_MainWindow):

    fetch_global_entities()

    quote_item: QuoteItem = quote_items[selected_row_id(main_window.tblQuoteItems)]

    clear_entry_fields(main_window)

    main_window.lblQuoteItemId.setText(str(quote_item.id))
    main_window.lblQuoteItem_QuoteId.setText(str(quote_item.quote_id))
    main_window.cmbQuoteItem_VehicleCombination.setCurrentText(
        quote_item.vehicle_combination_name
    )
    main_window.cmbQuoteItem_Product.setCurrentText(quote_item.product_name)
    main_window.cmbQuoteItem_ProductRate.setCurrentText(quote_item.charge_type_name)
    main_window.txtQuoteItem_Tonnes.setText(str(quote_item.vehicle_combination_net))
    main_window.txtQuoteItem_ProductRate.setText(str(quote_item.product_rate_ex_gst))
    main_window.txtQuoteItem_TransportRate.setText(
        str(quote_item.transport_rate_ex_gst)
    )

    change_view(main_window.swPages, ViewPage.QUOTE_ITEM_ENTRY)


def delete(main_window: Ui_MainWindow):

    global quote_items
    quote_item: QuoteItem = quote_items[selected_row_id(main_window.tblQuoteItems)]

    delete_confirmed: bool = AskYesNoMessageBox(
            f"Are you sure that you would like to delete "
            f"{quote_item.vehicle_combination_net} tonnes of {quote_item.product_name} via "
            f"{quote_item.vehicle_combination_name}?"
    )

    if not delete_confirmed:
        return

    QuoteItem.delete(quote_item.id)

    del quote_items[quote_item.id]

    refresh_table(main_window, quote_item.quote_id)

    InfoMessageBox(
            f"{quote_item.vehicle_combination_net} tonnes of "
            f"{quote_item.product_name} via {quote_item.vehicle_combination_name} successfully deleted."
    )


def save(main_window: Ui_MainWindow):

    if form_is_valid(main_window) is False:
        return

    quote_id: int = string_to_int(main_window.lblQuoteItem_QuoteId.text())
    quote: Quote = Quote.get(quote_id)
    quote_item_id: int = string_to_int(main_window.lblQuoteItemId.text())
    tonnes: float = float(main_window.txtQuoteItem_Tonnes.text())
    product_name: str = main_window.cmbQuoteItem_Product.currentText()
    charge_type_name: str = main_window.cmbQuoteItem_ProductRate.currentText()
    product_rate_ex_gst: float = float(main_window.txtQuoteItem_ProductRate.text())
    selected_vehicle_combination_name: str = (
        main_window.cmbQuoteItem_VehicleCombination.currentText()
    )

    transport_rate_ex_gst_text: str = main_window.txtQuoteItem_TransportRate.text()
    if len(transport_rate_ex_gst_text) > 0:
        transport_rate_ex_gst = string_to_float(
            transport_rate_ex_gst_text
        )
    else:
        transport_rate_ex_gst = get_transport_rate_ex_gst(quote.kilometres, selected_vehicle_combination_name)

    quote_item = QuoteItem(
        quote_item_id,
        quote_id,
        selected_vehicle_combination_name,
        tonnes,
        transport_rate_ex_gst,
        product_name,
        product_rate_ex_gst,
        charge_type_name,
    )

    quote_item.update() if quote_item_id else quote_item.insert()

    refresh_table(main_window, quote_id)

    calculate_quote_item_totals(main_window, quote_id)

    change_view(main_window.swPages, ViewPage.QUOTE_ENTRY)

    clear_entry_fields(main_window)

    InfoMessageBox(
            f"Successfully saved {quote_item.vehicle_combination_net} "
            f"tonnes of {quote_item.product_name} via {quote_item.vehicle_combination_name}."
    )


def on_row_select(main_window: Ui_MainWindow):

    selected_id: int = selected_row_id(main_window.tblQuoteItems)

    toggle_buttons(
        [
            (main_window.btnNewQuoteItem, True),
            (main_window.btnEditQuoteItem, selected_id is not None),
            (main_window.btnDeleteQuoteItem, selected_id is not None),
        ]
    )


def connect(main_window: Ui_MainWindow):

    main_window.btnNewQuoteItem.clicked.connect(lambda: new(main_window))
    main_window.btnEditQuoteItem.clicked.connect(lambda: edit(main_window))
    main_window.btnDeleteQuoteItem.clicked.connect(lambda: delete(main_window))
    main_window.btnSaveQuoteItem.clicked.connect(lambda: save(main_window))
    main_window.tblQuoteItems.selectionModel().selectionChanged.connect(
        lambda: on_row_select(main_window)
    )
    main_window.cmbQuoteItem_VehicleCombination.currentTextChanged.connect(
        lambda: on_vehicle_combination_select(main_window)
    )
    main_window.cmbQuoteItem_Product.currentTextChanged.connect(
        lambda: on_product_select(main_window)
    )
    main_window.cmbQuoteItem_ProductRate.currentTextChanged.connect(
        lambda: update_product_rate(main_window)
    )

    only_numeric_validator = QDoubleValidator()
    only_numeric_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
    only_numeric_validator.setRange(0.00, 9999.00, 2)
    main_window.txtQuoteItem_TransportRate.setValidator(only_numeric_validator)
    main_window.txtQuoteItem_Tonnes.setValidator(only_numeric_validator)
    main_window.txtQuoteItem_ProductRate.setValidator(only_numeric_validator)
