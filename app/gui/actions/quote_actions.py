from app.gui.view_enum import ViewPage
from app.classes.Quote import Quote
from app.classes.QuoteItem import QuoteItem
from app.gui.components.main_window import Ui_MainWindow
from app.db.SQLCursor import SQLCursor
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QIntValidator
from tkinter import messagebox
from datetime import datetime
from openpyxl import load_workbook, Workbook
from app.gui.helpers import (
    toggle_buttons,
    change_view,
    selected_row_id,
    isdate,
    int_conv,
    get_transport_rate_ex_gst,
)
from app.gui.actions.quoteitem_actions import (
    refresh_table as refresh_quote_items_table,
    calculate_quote_item_totals,
    fetch_global_entities as fetch_quote_item_globals,
)
from win32com import client

quotes: dict[int, Quote] = dict()
matches: dict[int, Quote] = dict()


def refresh_table(main_window: Ui_MainWindow):

    tbl_headers: list[str] = [
        "ID",
        "Date Created",
        "Date Required",
        "Name",
        "Address",
        "Suburb",
        "Contact Number",
        "Kilometres",
    ]

    tbl: QTableWidget = main_window.tblQuotes
    tbl.clear()
    tbl.setColumnCount(len(tbl_headers))
    tbl.setRowCount(len(matches.values()))
    tbl.setHorizontalHeaderLabels(tbl_headers)

    for index, quote in enumerate(matches.values()):
        tbl.setItem(index, 0, QTableWidgetItem(str(quote.id)))
        tbl.setItem(
            index,
            1,
            QTableWidgetItem(datetime.strftime(quote.date_created, "%d/%m/%Y")),
        )
        tbl.setItem(
            index,
            2,
            QTableWidgetItem(datetime.strftime(quote.date_required, "%d/%m/%Y")),
        )
        tbl.setItem(index, 3, QTableWidgetItem(quote.name))
        tbl.setItem(index, 4, QTableWidgetItem(quote.address))
        tbl.setItem(index, 5, QTableWidgetItem(quote.suburb))
        tbl.setItem(index, 6, QTableWidgetItem(str(quote.contact_number)))
        tbl.setItem(index, 7, QTableWidgetItem(str(quote.kilometres)))

    header: QHeaderView = tbl.horizontalHeader()
    for i in range(len(tbl_headers)):
        header.setSectionResizeMode(
            i,
            QHeaderView.ResizeMode.ResizeToContents
            if i < len(tbl_headers) - 1
            else QHeaderView.ResizeMode.Stretch,
        )


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


def navigate_to_listing_view(main_window: Ui_MainWindow):

    global quotes, matches
    quotes = Quote.get()
    matches = quotes

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


def new(main_window: Ui_MainWindow):

    fetch_quote_item_globals()

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

    # Fetch the Quote object to be edited.
    quote_id: int = selected_row_id(main_window.tblQuotes)
    quote: Quote = quotes[quote_id]

    # Write object attributes to GUI.
    main_window.lblQuoteId.setText(str(quote.id))
    main_window.txtQuote_Name.setText(quote.name)
    main_window.txtQuote_Address.setText(quote.address)
    main_window.txtQuote_Suburb.setText(quote.suburb)
    main_window.txtQuote_ContactNumber.setText(quote.contact_number)
    main_window.txtQuote_Kilometres.setText(str(quote.kilometres))
    main_window.lblQuote_DateCreated.setText(
        datetime.strftime(quote.date_created, "%d/%m/%Y")
    )
    main_window.txtQuote_DateRequired.setText(
        datetime.strftime(quote.date_required, "%d/%m/%Y")
    )

    # Write all children QuoteItem objects to GUI table.
    fetch_quote_item_globals()
    refresh_quote_items_table(main_window, quote_id)

    # Calculate and display pricing of all children QuoteItem objects on the GUI.
    calculate_quote_item_totals(main_window, quote.id)

    # Show/hide action buttons.
    toggle_buttons(
        [
            (main_window.btnNewQuoteItem, True),
            (main_window.btnEditQuoteItem, False),
            (main_window.btnDeleteQuoteItem, False),
            (main_window.btnExportQuote_Entry, True),
        ]
    )

    # Change the view to the Quote entry page.
    change_view(main_window.swPages, ViewPage.QUOTE_ENTRY)


def delete(main_window: Ui_MainWindow):

    # Fetch the Quote object to be deleted.
    quote_id: int = selected_row_id(main_window.tblQuotes)

    # Delete the Quote object from SQL database
    quotes[quote_id].delete()

    # Remove from global dictionary (avoids a second call to database).
    del quotes[quote_id]

    # Refresh the table with the new dictionary.
    refresh_table(main_window)


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


def save(main_window: Ui_MainWindow):

    # Check that all input fields are valid before continuing.
    if form_is_valid(main_window) is False:
        return

    # Read GUI fields to variables for readability.
    quote_id: int = int_conv(main_window.lblQuoteId.text())
    quote_name: str = main_window.txtQuote_Name.text().strip()
    quote_address: str = main_window.txtQuote_Address.text().strip()
    quote_suburb: str = main_window.txtQuote_Suburb.text().strip()
    quote_contact_number: str = main_window.txtQuote_ContactNumber.text().strip()
    quote_kilometres: int = int(main_window.txtQuote_Kilometres.text().strip())
    quote_date_created: datetime = (
        datetime.strptime(main_window.txtQuote_DateRequired.text().strip(), "%d/%m/%Y")
        if quote_id
        else datetime.today()
    )
    quote_date_required: datetime = datetime.strptime(
        main_window.txtQuote_DateRequired.text().strip(), "%d/%m/%Y"
    )

    # Instantiate Quote object to be saved.
    quote = Quote(
        quote_id,
        quote_date_created,
        quote_date_required,
        quote_name,
        quote_address,
        quote_suburb,
        quote_contact_number,
        quote_kilometres,
    )

    # Save the Quote object.
    quote.update() if quote_id else quote.insert()

    # Set the GUI id field to display the saved Quote object id.
    main_window.lblQuoteId.setText(str(quote.id))

    # Update all children QuoteItem objects to use the most updated kilometres for their transport_rate_ex_gst.
    with SQLCursor() as cur:
        quote_item_tuples = cur.execute(
            """
        SELECT qi.id, vc.charge_type
        FROM quote_item qi
        LEFT JOIN vehicle_combination vc ON qi.vehicle_combination_name = vc.name
        WHERE qi.quote_id = ?
        """,
            (quote.id,),
        ).fetchall()

        for t in quote_item_tuples:

            transport_rate_ex_gst = get_transport_rate_ex_gst(quote.kilometres, t[1])

            cur.execute(
                """
            UPDATE quote_item 
            SET transport_rate_ex_gst = ? 
            WHERE id = ?;
            """,
                (
                    transport_rate_ex_gst,
                    t[0],
                ),
            )

    refresh_quote_items_table(main_window, quote.id)

    # Show all QuoteItem action buttons.
    toggle_buttons(
        [
            (main_window.btnNewQuoteItem, True),
            (main_window.btnEditQuoteItem, False),
            (main_window.btnDeleteQuoteItem, False),
            (main_window.btnExportQuote_Entry, True),
        ]
    )


def search(main_window: Ui_MainWindow, search_text: str):

    global matches
    matches = (
        quotes
        if not search_text
        else {
            q.id: q
            for q in quotes.values()
            if search_text
            in "".join([q.name.lower(), q.address.lower(), q.suburb.lower()])
        }
    )

    refresh_table(main_window)


def export(main_window: Ui_MainWindow):

    quote_id: int = selected_row_id(main_window.tblQuotes)
    quote: Quote = quotes[quote_id]
    quote_items = quote.items()

    wkb = load_workbook(filename="app/quote_template.xlsx")
    sheet = wkb["Sheet1"]
    sheet["A9"] = quote.name
    sheet["A10"] = quote.address
    sheet["A11"] = quote.suburb
    sheet["A12"] = quote.contact_number
    sheet["D8"] = quote.id
    sheet["D9"] = quote.date_created

    for index, quote_item in enumerate(quote_items.values()):
        sheet[f"A{20 + index}"] = quote_item.vehicle_combination_net
        sheet[f"B{20 + index}"] = quote_item.product_name
        sheet[f"C{20 + index}"] = quote_item.vehicle_combination_name
        sheet[f"D{20 + index}"] = quote_item.total_inc_gst()

    wkb.save("test.xlsx")

    excel = client.Dispatch("Excel.Application")
    sheets = excel.Workbooks.Open('test.xlsx')
    work_sheets = sheets.Worksheets[0]
    work_sheets.ExportAsFixedFormat(0, 'test.pdf')

def connect(main_window: Ui_MainWindow):

    main_window.btnExportQuote.clicked.connect(lambda: export(main_window))
    # Export button entry
    main_window.btnNewQuote.clicked.connect(lambda: new(main_window))
    main_window.btnEditQuote.clicked.connect(lambda: edit(main_window))
    main_window.btnDeleteQuote.clicked.connect(lambda: delete(main_window))
    main_window.btnSaveQuote.clicked.connect(lambda: save(main_window))
    main_window.txtQuoteSearch.textChanged.connect(
        lambda: search(main_window, main_window.txtQuoteSearch.text().lower())
    )
    main_window.actionQuotes.triggered.connect(
        lambda: navigate_to_listing_view(main_window)
    )
    main_window.tblQuotes.selectionModel().selectionChanged.connect(
        lambda: on_row_select(main_window)
    )

    # Set integer only validator on Kilometres textbox.
    intOnly = QIntValidator()
    intOnly.setRange(0, 9999)
    main_window.txtQuote_Kilometres.setValidator(intOnly)
