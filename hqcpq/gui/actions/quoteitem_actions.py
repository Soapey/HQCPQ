from tkinter import messagebox
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QComboBox, QHeaderView
from PyQt5.QtGui import QDoubleValidator
from hqcpq.classes.Toast import Toast
from hqcpq.classes.VehicleCombination import VehicleCombination
from hqcpq.classes.Product import Product
from hqcpq.classes.ProductRate import ProductRate
from hqcpq.classes.RateType import RateType
from hqcpq.classes.QuoteItem import QuoteItem
from hqcpq.classes.Quote import Quote
from hqcpq.gui.components.main_window import Ui_MainWindow
from hqcpq.gui.view_enum import ViewPage
from hqcpq.helpers import int_conv, float_conv, get_transport_rate_ex_gst
from hqcpq.gui.helpers import selected_row_id, toggle_buttons, change_view


vehicle_combinations: dict[int, VehicleCombination] = dict()
products: dict[int, Product] = dict()
product_rates: dict[int, ProductRate] = dict()
rate_types: dict[int, RateType] = dict()
quotes: dict[int, Quote] = dict()
quote_items: dict[int, QuoteItem] = dict()


def fetch_global_entities():

    global vehicle_combinations, products, product_rates, rate_types, quotes, quote_items

    vehicle_combinations = VehicleCombination.get()
    products = Product.get()
    product_rates = ProductRate.get()
    rate_types = RateType.get()
    quotes = Quote.get()
    quote_items = QuoteItem.get()


def refresh_table(main_window: Ui_MainWindow, quote_id: int = None):

    fetch_global_entities()

    selected_quote_id: int = quote_id or selected_row_id(main_window.tblQuotes)
    quotes_list = list(Quote.get(selected_quote_id).values())

    if not quotes_list:
        return

    quote: Quote = quotes_list[0] if quotes_list else None

    global quote_items
    items: dict[int, QuoteItem] = quote.items(quote_items)

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
    tbl.setRowCount(len(items.values()))
    tbl.setColumnCount(len(tbl_headers))
    tbl.setHorizontalHeaderLabels(tbl_headers)

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

    header = tbl.horizontalHeader()
    for i in range(len(tbl_headers)):
        header.setSectionResizeMode(
            i,
            QHeaderView.ResizeMode.ResizeToContents
            if i < len(tbl_headers) - 1
            else QHeaderView.ResizeMode.Stretch,
        )


def calculate_quote_item_totals(main_window: Ui_MainWindow, quote_id: int = None):

    selected_id: int = quote_id or selected_row_id(main_window.tblQuotes)
    quotes_list = list(Quote.get(selected_id).values())

    transport_total_ex_gst: float = 0
    product_total_ex_gst: float = 0

    if quotes_list:

        quote: Quote = quotes_list[0] if quotes_list else None
        global quote_items
        items = quote.items(quote_items)

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
    rate_type_name = main_window.cmbQuoteItem_ProductRate.currentText()

    global product_rates

    product_rates_list = [
        pr
        for pr in product_rates.values()
        if products[pr.product_id].name == product_name
        and rate_types[pr.rate_type_id].name == rate_type_name
    ]

    product_rate: ProductRate = product_rates_list[0] if product_rates_list else None

    if product_rate:
        main_window.txtQuoteItem_ProductRate.setText(str(product_rate.rate))


def on_product_select(main_window: Ui_MainWindow):

    cmbProductRates: QComboBox = main_window.cmbQuoteItem_ProductRate

    show_hide = len(main_window.cmbQuoteItem_Product.currentText()) > 0
    main_window.lblQuoteItem_ProductRate.setVisible(show_hide)
    cmbProductRates.setVisible(show_hide)

    if show_hide is False:
        return

    selected_product_name: str = main_window.cmbQuoteItem_Product.currentText()

    global products
    products_list = [p for p in products.values() if p.name == selected_product_name]

    product: Product = products_list[0] if products_list else None

    match_product_rate_names = [
        rate_types[pr.rate_type_id].name
        for pr in sorted(
            list(product_rates.values()), key=lambda pr: pr.id, reverse=True
        )
        if pr.product_id == product.id
    ]

    cmbProductRates.clear()
    cmbProductRates.addItems(match_product_rate_names)

    update_product_rate(main_window)


def on_vehicle_combination_select(main_window: Ui_MainWindow):

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

        quote_id: int = int_conv(main_window.lblQuoteItem_QuoteId.text())

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


def clear_entry_fields(main_window: Ui_MainWindow):

    main_window.lblQuoteItemId.clear()
    main_window.lblQuoteItem_QuoteId.clear()
    main_window.txtQuoteItem_Tonnes.clear()
    main_window.txtQuoteItem_ProductRate.clear()
    main_window.txtQuoteItem_TransportRate.clear()

    global vehicle_combinations
    cmbVehicleCombinations: QComboBox = main_window.cmbQuoteItem_VehicleCombination
    cmbVehicleCombinations.clear()
    cmbVehicleCombinations.addItems([vc.name for vc in vehicle_combinations.values()])

    global products
    cmbProducts: QComboBox = main_window.cmbQuoteItem_Product
    cmbProducts.clear()
    cmbProducts.addItems([p.name for p in products.values()])

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
        messagebox.showerror("Save Error", error_string)

    return result


def new(main_window: Ui_MainWindow):

    fetch_global_entities()

    clear_entry_fields(main_window)

    main_window.lblQuoteItem_QuoteId.setText(main_window.lblQuoteId.text())

    change_view(main_window.swPages, ViewPage.QUOTE_ITEM_ENTRY)


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

    delete_confirmed: bool = messagebox.askyesno(
        title="Confirm Delete",
        message=f"Are you sure that you would like to delete {quote_item.vehicle_combination_net} tonnes of {quote_item.product_name} via {quote_item.vehicle_combination_name}?",
    )

    if not delete_confirmed:
        return

    quote_item.delete()

    del quote_items[quote_item.id]

    refresh_table(main_window, quote_item.quote_id)

    Toast(
        "Delete Success",
        f"{quote_item.vehicle_combination_net} tonnes of {quote_item.product_name} via {quote_item.vehicle_combination_name} successfully deleted.",
    ).show()


def save(main_window: Ui_MainWindow):

    if form_is_valid(main_window) is False:
        return

    quote_id: int = int_conv(main_window.lblQuoteItem_QuoteId.text())
    quote_item_id: int = int_conv(main_window.lblQuoteItemId.text())
    tonnes: float = float(main_window.txtQuoteItem_Tonnes.text())
    product_name: str = main_window.cmbQuoteItem_Product.currentText()
    charge_type_name: str = main_window.cmbQuoteItem_ProductRate.currentText()
    product_rate_ex_gst: float = float(main_window.txtQuoteItem_ProductRate.text())
    selected_vehicle_combination_name: str = (
        main_window.cmbQuoteItem_VehicleCombination.currentText()
    )

    transport_rate_ex_gst: float = float_conv(
        main_window.txtQuoteItem_TransportRate.text()
    )

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

    Toast(
        "Save Success",
        f"Successfully saved {quote_item.vehicle_combination_net} tonnes of {quote_item.product_name} via {quote_item.vehicle_combination_name}.",
    ).show()


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

    # Set numeric only validator on Tonnes and Rate textbox.
    onlyNumeric = QDoubleValidator()
    onlyNumeric.setNotation(QDoubleValidator.Notation.StandardNotation)
    onlyNumeric.setRange(0.00, 9999.00, 2)
    main_window.txtQuoteItem_TransportRate.setValidator(onlyNumeric)
    main_window.txtQuoteItem_Tonnes.setValidator(onlyNumeric)
    main_window.txtQuoteItem_ProductRate.setValidator(onlyNumeric)
