from app.gui.components.main_window import Ui_MainWindow
from app.db.SQLCursor import SQLCursor
from app.classes.Quote import Quote
from app.classes.QuoteItem import QuoteItem
from app.gui.view_enum import ViewPage
from app.gui.helpers import (
    selected_row_id,
    toggle_buttons,
    change_view,
    int_conv,
    get_transport_rate_ex_gst,
)
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QComboBox, QHeaderView
from tkinter import messagebox


vehicle_combinations: list[tuple] = list()
products: list[tuple] = list()
product_rates: list[tuple] = list()
quote_items: list[tuple] = list()


def fetch_global_entities():

    with SQLCursor() as cur:

        global vehicle_combinations
        global products
        global product_rates
        global quote_items

        vehicle_combinations = cur.execute(
            """
            SELECT vc.id, vc.name, vc.net, vc.charge_type 
            FROM vehicle_combination vc
            """
        ).fetchall()

        products = cur.execute(
            """
            SELECT p.id, p.name
            FROM product p
            """
        ).fetchall()

        product_rates = cur.execute(
            """
            SELECT pr.id, p.id, p.name, rt.name, pr.rate
            FROM product_rate pr
            LEFT JOIN product p ON pr.product_id = p.id 
            LEFT JOIN rate_type rt ON pr.rate_type_id = rt.id 
            """
        ).fetchall()

        quote_items = cur.execute(
            """
            SELECT qi.id, qi.quote_id, qi.vehicle_combination_name, qi.vehicle_combination_net, qi.product_name, qi.transport_rate_ex_gst, qi.product_rate_ex_gst, qi.charge_type_name 
            FROM quote_item qi
            """
        ).fetchall()


def refresh_table(main_window: Ui_MainWindow, quote_id: int = None):
    """
    Refreshes the table of saved entities.
    Makes SQL request for entities, clears the table, loops through the returned entities and inserts each table cell data into correct position.
    """

    fetch_global_entities()

    selected_quote_id: int = quote_id or selected_row_id(main_window.tblQuotes)

    records = list(filter(lambda t: t[1] == selected_quote_id, quote_items))

    headers: list[str] = [
        "ID",
        "Vehicle Combination",
        "Net",
        "Product",
        "Transport Rate ex. GST",
        "Product Rate ex. GST",
    ]

    tbl: QTableWidget = main_window.tblQuoteItems
    tbl.clear()
    tbl.setRowCount(len(records))
    tbl.setColumnCount(len(headers))
    tbl.setHorizontalHeaderLabels(headers)

    for index, record in enumerate(records):
        tbl.setItem(index, 0, QTableWidgetItem(str(record[0])))
        tbl.setItem(index, 1, QTableWidgetItem(record[2]))
        tbl.setItem(index, 2, QTableWidgetItem(str(record[3])))
        tbl.setItem(index, 3, QTableWidgetItem(record[4]))
        tbl.setItem(index, 4, QTableWidgetItem(str(record[5])))
        tbl.setItem(index, 5, QTableWidgetItem(str(record[6])))

    header = tbl.horizontalHeader()
    header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
    header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
    header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
    header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
    header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
    header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)

    toggle_buttons(
        [
            (main_window.btnNewQuoteItem, True),
            (main_window.btnEditQuoteItem, False),
            (main_window.btnDeleteQuoteItem, False),
        ]
    )


def calculate_quote_item_totals(main_window: Ui_MainWindow, quote_id: int = None):

    selected_id: int = quote_id or selected_row_id(main_window.tblQuotes)

    records = filter(lambda t: t[1] == selected_id, quote_items)

    transport_total_ex_gst: float = 0
    product_total_ex_gst: float = 0
    transport_rate_ex_gst: float
    product_rate_ex_gst: float
    vehicle_combination_net: float

    for record in records:

        vehicle_combination_net = float(record[3])
        transport_rate_ex_gst = float(record[5])
        product_rate_ex_gst = float(record[6])

        transport_total_ex_gst += transport_rate_ex_gst * vehicle_combination_net
        product_total_ex_gst += product_rate_ex_gst * vehicle_combination_net

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
        "${:,.2f}".format((product_total_ex_gst + transport_total_ex_gst) * 1.1)
    )


def clear_entry_fields(main_window: Ui_MainWindow):

    main_window.lblQuoteItemId.clear()
    main_window.lblQuoteItem_QuoteId.clear()

    cmbVehicleCombinations: QComboBox = main_window.cmbQuoteItem_VehicleCombination
    cmbVehicleCombinations.clear()
    cmbVehicleCombinations.addItems([t[1] for t in vehicle_combinations])

    cmbProducts: QComboBox = main_window.cmbQuoteItem_Product
    cmbProducts.clear()
    cmbProducts.addItems([t[1] for t in products])

    on_product_select(main_window)


def on_product_select(main_window: Ui_MainWindow):

    cmbProductRates: QComboBox = main_window.cmbQuoteItem_ProductRate

    show_hide = len(main_window.cmbQuoteItem_Product.currentText()) > 0

    cmbProductRates.clear()

    if show_hide:
        selected_product_id = list(
            filter(
                lambda t: t[1] == main_window.cmbQuoteItem_Product.currentText(),
                products,
            )
        )[0][0]
        records = list(filter(lambda t: t[1] == selected_product_id, product_rates))
        cmbProductRates.addItems([t[3] for t in records])

    main_window.lblQuoteItem_ProductRate.setVisible(show_hide)
    cmbProductRates.setVisible(show_hide)


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

    selected_id: int = selected_row_id(main_window.tblQuoteItems)
    entity_tuple = list(filter(lambda e: e[0] == selected_id, quote_items))[0]

    clear_entry_fields(main_window)

    main_window.lblQuoteItemId.setText(str(entity_tuple[0]))
    main_window.lblQuoteItem_QuoteId.setText(str(entity_tuple[1]))
    main_window.cmbQuoteItem_VehicleCombination.setCurrentText(entity_tuple[2])
    main_window.cmbQuoteItem_Product.setCurrentText(entity_tuple[4])
    main_window.cmbQuoteItem_ProductRate.setCurrentText(entity_tuple[7])

    change_view(main_window.swPages, ViewPage.QUOTE_ITEM_ENTRY)


def delete(main_window: Ui_MainWindow):

    quote_id: int = selected_row_id(main_window.tblQuotes)
    selected_id: int = selected_row_id(main_window.tblQuoteItems)

    QuoteItem(selected_id, None, None, None, None, None, None, None).delete()

    refresh_table(main_window, quote_id)


def save(main_window: Ui_MainWindow):

    if form_is_valid(main_window):

        id: int = int_conv(main_window.lblQuoteItemId.text())
        quote_id: int = int_conv(main_window.lblQuoteItem_QuoteId.text())
        quote: Quote = Quote.get(quote_id)[0]

        vehicle_combination_tuple = list(
            filter(
                lambda t: t[1]
                == main_window.cmbQuoteItem_VehicleCombination.currentText(),
                vehicle_combinations,
            )
        )[0]

        vehicle_combination_name: str = vehicle_combination_tuple[1]
        vehicle_combination_net: float = vehicle_combination_tuple[2]
        vehicle_combination_charge_type: str = vehicle_combination_tuple[3]

        product_name: str = main_window.cmbQuoteItem_Product.currentText()
        charge_type_name: str = main_window.cmbQuoteItem_ProductRate.currentText()
        transport_rate_ex_gst: float = get_transport_rate_ex_gst(
            quote.kilometres, vehicle_combination_charge_type
        )
        product_rate_ex_gst: float = list(
            filter(
                lambda t: t[2] == product_name and t[3] == charge_type_name,
                product_rates,
            )
        )[0][4]

        qi = QuoteItem(
            id,
            quote_id,
            vehicle_combination_name,
            vehicle_combination_net,
            transport_rate_ex_gst,
            product_name,
            product_rate_ex_gst,
            charge_type_name,
        )

        qi.update() if id else qi.insert()

        refresh_table(main_window, quote_id)

        calculate_quote_item_totals(main_window, quote_id)

        change_view(main_window.swPages, ViewPage.QUOTE_ENTRY)

        clear_entry_fields(main_window)


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
    main_window.cmbQuoteItem_Product.currentTextChanged.connect(
        lambda: on_product_select(main_window)
    )
