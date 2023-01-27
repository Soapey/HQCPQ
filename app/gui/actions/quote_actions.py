from app.gui.helpers import (
    toggle_buttons,
    change_view,
    selected_row_id,
    isdate,
    int_conv,
)
from app.gui.view_enum import ViewPage
from app.classes.Quote import Quote
from app.gui.components.main_window import Ui_MainWindow
from app.gui.actions.quoteitem_actions import (
    refresh_table as refresh_quote_items_table,
    calculate_quote_item_totals,
    fetch_global_entities,
)
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from tkinter import messagebox
from datetime import datetime


quotes: list[Quote] = list()


def refresh_table(main_window: Ui_MainWindow, fetched_entities=None):

    records = fetched_entities
    if fetched_entities is None:
        records = quotes

    headers: list[str] = [
        "ID",
        "Date Created",
        "Date Required",
        "Name",
        "Address",
        "Suburb",
        "Contact Number",
    ]

    tbl: QTableWidget = main_window.tblQuotes
    tbl.clear()
    tbl.setColumnCount(len(headers))
    tbl.setRowCount(len(records))
    tbl.setHorizontalHeaderLabels(headers)

    for index, quote in enumerate(records):
        tbl.setItem(index, 0, QTableWidgetItem(str(quote.id)))
        tbl.setItem(index, 1, QTableWidgetItem(str(quote.date_created)))
        tbl.setItem(index, 2, QTableWidgetItem(str(quote.date_required)))
        tbl.setItem(index, 3, QTableWidgetItem(quote.name))
        tbl.setItem(index, 4, QTableWidgetItem(quote.address))
        tbl.setItem(index, 5, QTableWidgetItem(quote.suburb))
        tbl.setItem(index, 6, QTableWidgetItem(str(quote.contact_number)))

    header = tbl.horizontalHeader()
    header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
    header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
    header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
    header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
    header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
    header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
    header.setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)


def navigate_quotes(main_window: Ui_MainWindow):

    global quotes
    quotes = Quote.get()

    refresh_table(main_window)

    toggle_buttons(
        [
            (main_window.btnNewQuote, True),
            (main_window.btnEditQuote, False),
            (main_window.btnDeleteQuote, False),
            (main_window.btnExportQuote, False),
        ]
    )

    change_view(main_window.swPages, ViewPage.QUOTES)


def clear_entry_fields(main_window: Ui_MainWindow):

    main_window.lblQuoteId.clear()
    main_window.lblQuote_DateCreated.clear()
    main_window.txtQuote_DateRequired.clear()
    main_window.txtQuote_Name.clear()
    main_window.txtQuote_Address.clear()
    main_window.txtQuote_Suburb.clear()
    main_window.txtQuote_ContactNumber.clear()
    main_window.txtQuote_Kilometres.clear()
    main_window.tblQuoteItems.clear()
    main_window.lblQuote_ProductTotalExGST.clear()
    main_window.lblQuote_TransportTotalExGST.clear()
    main_window.lblQuote_TotalExGST.clear()
    main_window.lblQuote_TotalIncGST.clear()


def form_is_valid(main_window: Ui_MainWindow):

    result: bool = True
    error_string: str = str()

    date_required_text: str = main_window.txtQuote_DateRequired.text()
    kilometres_text: str = main_window.txtQuote_Kilometres.text()

    if len(date_required_text) == 0:
        result = False
        error_string += "\n- Date Required field cannot be blank."
    elif isdate(date_required_text) is False:
        result = False
        error_string += "\n- Date Required value must be in a valid date format."

    if len(main_window.txtQuote_Name.text()) == 0:
        result = False
        error_string += "\n- Customer Name field cannot be blank."

    if len(main_window.txtQuote_Address.text()) == 0:
        result = False
        error_string += "\n- Address field cannot be blank."

    if len(main_window.txtQuote_Suburb.text()) == 0:
        result = False
        error_string += "\n- Suburb field cannot be blank."

    if len(main_window.txtQuote_ContactNumber.text()) == 0:
        result = False
        error_string += "\n- Contact Number field cannot be blank."

    if len(kilometres_text) == 0:
        result = False
        error_string += "\n- Kilometres field cannot be blank."

    if result is False:
        messagebox.showerror("Save Error", error_string)

    return result


def new(main_window: Ui_MainWindow):

    fetch_global_entities()

    clear_entry_fields(main_window)

    toggle_buttons(
        [
            (main_window.btnNewQuoteItem, False),
            (main_window.btnEditQuoteItem, False),
            (main_window.btnDeleteQuoteItem, False),
            (main_window.btnExportQuote_Entry, False),
        ]
    )

    refresh_quote_items_table(main_window)

    change_view(main_window.swPages, ViewPage.QUOTE_ENTRY)


def edit(main_window: Ui_MainWindow):

    fetch_global_entities()

    selected_id: int = selected_row_id(main_window.tblQuotes)
    entity: Quote = list(filter(lambda e: e.id == selected_id, quotes))[0]

    main_window.lblQuoteId.setText(str(entity.id))
    main_window.lblQuote_DateCreated.setText(
        datetime.strftime(entity.date_created, "%d/%m/%Y")
    )
    main_window.txtQuote_DateRequired.setText(
        datetime.strftime(entity.date_required, "%d/%m/%Y")
    )
    main_window.txtQuote_Name.setText(entity.name)
    main_window.txtQuote_Address.setText(entity.address)
    main_window.txtQuote_Suburb.setText(entity.suburb)
    main_window.txtQuote_ContactNumber.setText(entity.contact_number)
    main_window.txtQuote_Kilometres.setText(str(entity.kilometres))

    refresh_quote_items_table(main_window, selected_id)

    calculate_quote_item_totals(main_window, entity.id)

    toggle_buttons(
        [
            (main_window.btnNewQuoteItem, True),
            (main_window.btnEditQuoteItem, False),
            (main_window.btnDeleteQuoteItem, False),
            (main_window.btnExportQuote_Entry, True),
        ]
    )

    change_view(main_window.swPages, ViewPage.QUOTE_ENTRY)


def delete(main_window: Ui_MainWindow):

    selected_id: int = selected_row_id(main_window.tblQuotes)

    entity: Quote = list(filter(lambda e: e.id == selected_id, quotes))[0]
    entity.delete()

    quotes.remove(entity)

    refresh_table(main_window)


def save(main_window: Ui_MainWindow):

    if form_is_valid(main_window):

        quote_id = int_conv(main_window.lblQuoteId.text())

        date_created: datetime = (
            datetime.strptime(
                main_window.txtQuote_DateRequired.text().strip(), "%d/%m/%Y"
            )
            if quote_id
            else datetime.today()
        )
        date_required: datetime = datetime.strptime(
            main_window.txtQuote_DateRequired.text().strip(), "%d/%m/%Y"
        )

        customer_name: str = main_window.txtQuote_Name.text().strip()
        address: str = main_window.txtQuote_Address.text().strip()
        suburb: str = main_window.txtQuote_Suburb.text().strip()
        contact_number: str = main_window.txtQuote_ContactNumber.text().strip()
        kilometres: int = int(main_window.txtQuote_Kilometres.text().strip())

        q = Quote(
            quote_id,
            date_created,
            date_required,
            customer_name,
            address,
            suburb,
            contact_number,
            kilometres,
        )

        q.update() if quote_id else q.insert()

        main_window.lblQuoteId.setText(str(q.id))

        toggle_buttons(
            [
                (main_window.btnNewQuoteItem, True),
                (main_window.btnEditQuoteItem, True),
                (main_window.btnDeleteQuoteItem, True),
                (main_window.btnExportQuote_Entry, True),
            ]
        )


def search(main_window: Ui_MainWindow):

    search_text = main_window.txtQuoteSearch.text().lower()

    matches = list(filter(lambda q: search_text in q.name.lower(), quotes))

    refresh_table(main_window, matches)


def on_row_select(main_window: Ui_MainWindow):

    selected_id: int = selected_row_id(main_window.tblQuotes)

    toggle_buttons(
        [
            (main_window.btnNewQuote, True),
            (main_window.btnEditQuote, selected_id is not None),
            (main_window.btnDeleteQuote, selected_id is not None),
            (main_window.btnExportQuote, selected_id is not None),
        ]
    )


def connect(main_window: Ui_MainWindow):

    main_window.actionQuotes.triggered.connect(lambda: navigate_quotes(main_window))
    main_window.btnNewQuote.clicked.connect(lambda: new(main_window))
    main_window.btnEditQuote.clicked.connect(lambda: edit(main_window))
    main_window.btnDeleteQuote.clicked.connect(lambda: delete(main_window))
    # Export button
    main_window.btnSaveQuote.clicked.connect(lambda: save(main_window))
    # Export button entry
    main_window.tblQuotes.selectionModel().selectionChanged.connect(
        lambda: on_row_select(main_window)
    )
    main_window.txtQuoteSearch.textChanged.connect(lambda: search(main_window))
