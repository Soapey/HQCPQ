from datetime import datetime

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox

from hqcpq.classes.Quote import Quote
from hqcpq.classes.QuoteSpecialCondition import QuoteSpecialCondition
from hqcpq.db.SQLiteUtil import SQLiteConnection
from hqcpq.gui.actions.quoteitem_actions import (
    refresh_table as refresh_quote_items_table,
    calculate_quote_item_totals,
    fetch_global_entities as fetch_quote_item_globals,
)
from hqcpq.gui.actions.quotespecialcondition_actions import refresh_table as refresh_quotespecialconditions_table, \
    get_checkbox_state
from hqcpq.gui.components.main_window import Ui_MainWindow
from hqcpq.gui.classes.InfoMessageBox import InfoMessageBox
from hqcpq.gui.classes.ErrorMessageBox import ErrorMessageBox
from hqcpq.gui.classes.AskYesNoMessageBox import AskYesNoMessageBox
from hqcpq.gui.helpers import toggle_buttons, change_view, selected_row_id
from hqcpq.gui.view_enum import ViewPage
from hqcpq.helpers.comparison import can_be_date
from hqcpq.helpers.conversion import string_to_int, string_to_datetime
from hqcpq.helpers.general import get_transport_rate_ex_gst, is_valid_email

quotes: dict[int, Quote] = dict()
matches: dict[int, Quote] = dict()


def fetch_global_entities():
    global quotes, matches
    quotes = Quote.get_all()
    matches = quotes


def refresh_table(main_window: Ui_MainWindow):
    global matches
    tbl_headers: list[str] = [
        "ID",
        "Date Created",
        "Date Required",
        "Name",
        "Address",
        "Suburb",
        "Contact Number",
        "Email",
        "Kilometres",
        "Completed",
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
        tbl.setItem(index, 7, QTableWidgetItem(str(quote.email)))
        tbl.setItem(index, 8, QTableWidgetItem(str(quote.kilometres)))
        tbl.setItem(index, 9, QTableWidgetItem(str(quote.completed)))

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
            (main_window.btnOpenEmailQuote, selected_id is not None),
        ]
    )


def navigate_to_listing_view(main_window: Ui_MainWindow):
    fetch_global_entities()

    refresh_table(main_window)

    toggle_buttons(
        [
            (main_window.btnNewQuote, True),
            (main_window.btnEditQuote, False),
            (main_window.btnDeleteQuote, False),
            (main_window.btnExportQuote, False),
            (main_window.btnOpenEmailQuote, False),
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
    main_window.txtQuote_Email.clear()
    main_window.txtQuote_Memo.clear()
    main_window.txtQuote_Kilometres.clear()
    main_window.chkQuote_Completed.setChecked(False)
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
            (main_window.btnOpenEmailQuote_Entry, False),
        ]
    )

    fetch_quote_item_globals()
    refresh_quote_items_table(main_window, -1)

    calculate_quote_item_totals(main_window, -1)

    refresh_quotespecialconditions_table(main_window, -1)

    change_view(main_window.swPages, ViewPage.QUOTE_ENTRY)


def edit(main_window: Ui_MainWindow):
    global quotes
    quote_id: int = selected_row_id(main_window.tblQuotes)
    quote: Quote = quotes[quote_id]

    main_window.lblQuoteId.setText(str(quote.id))
    main_window.txtQuote_Name.setText(quote.name)
    main_window.txtQuote_Address.setText(quote.address)
    main_window.txtQuote_Suburb.setText(quote.suburb)
    main_window.txtQuote_ContactNumber.setText(quote.contact_number)
    main_window.txtQuote_Email.setText(quote.email)
    main_window.txtQuote_Memo.setPlainText(quote.memo)
    main_window.txtQuote_Kilometres.setText(str(quote.kilometres))
    main_window.chkQuote_Completed.setChecked(quote.completed)
    main_window.lblQuote_DateCreated.setText(
        datetime.strftime(quote.date_created, "%d/%m/%Y")
    )
    main_window.txtQuote_DateRequired.setText(
        datetime.strftime(quote.date_required, "%d/%m/%Y")
    )

    fetch_quote_item_globals()
    refresh_quote_items_table(main_window, quote_id)

    calculate_quote_item_totals(main_window, quote.id)

    refresh_quotespecialconditions_table(main_window, quote_id)

    toggle_buttons(
        [
            (main_window.btnNewQuoteItem, True),
            (main_window.btnEditQuoteItem, False),
            (main_window.btnDeleteQuoteItem, False),
            (main_window.btnExportQuote_Entry, True),
            (main_window.btnOpenEmailQuote_Entry, True),
        ]
    )

    change_view(main_window.swPages, ViewPage.QUOTE_ENTRY)


def delete(main_window: Ui_MainWindow):
    quote_id: int = selected_row_id(main_window.tblQuotes)
    global quotes
    quote: Quote = quotes[quote_id]

    delete_confirmed: bool = AskYesNoMessageBox(
        f"Are you sure that you would like to delete {quote.name} - {quote.address}, {quote.suburb}?").state

    if not delete_confirmed:
        return

    Quote.delete(quote.id)

    del quotes[quote_id]

    refresh_table(main_window)

    InfoMessageBox(f"{quote.name} - {quote.address}, {quote.suburb} successfully deleted.")


def form_is_valid(main_window: Ui_MainWindow):
    result: bool = True
    error_string: str = str()

    date_required_text: str = main_window.txtQuote_DateRequired.text()
    kilometres_text: str = main_window.txtQuote_Kilometres.text()

    if len(date_required_text) == 0:
        result = False
        error_string += "\n- Date Required field cannot be blank."
    elif can_be_date(date_required_text) is False:
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

    if len(main_window.txtQuote_Email.text()) > 0 and is_valid_email(main_window.txtQuote_Email.text()) == False:
        result = False
        error_string += "\n- Email Address is not valid."

    if len(kilometres_text) == 0:
        result = False
        error_string += "\n- Kilometres field cannot be blank."

    if result is False:
        ErrorMessageBox(error_string)

    return result


def save(main_window: Ui_MainWindow):
    if form_is_valid(main_window) is False:
        return

    quote_id: int = string_to_int(main_window.lblQuoteId.text())
    quote_name: str = main_window.txtQuote_Name.text().strip()
    quote_address: str = main_window.txtQuote_Address.text().strip()
    quote_suburb: str = main_window.txtQuote_Suburb.text().strip()
    quote_contact_number: str = main_window.txtQuote_ContactNumber.text().strip()
    quote_email: str = main_window.txtQuote_Email.text().strip()
    quote_memo: str = main_window.txtQuote_Memo.toPlainText().strip()
    quote_kilometres: int = int(main_window.txtQuote_Kilometres.text().strip())
    quote_completed: bool = main_window.chkQuote_Completed.isChecked()

    if quote_id:
        quote_date_created: datetime = datetime.strptime(main_window.lblQuote_DateCreated.text().strip(), "%d/%m/%Y")
    else:
        quote_date_created: datetime = datetime.today()

    quote_date_required: datetime = string_to_datetime(main_window.txtQuote_DateRequired.text().strip())

    quote = Quote(
        quote_id,
        datetime.strptime(datetime.strftime(quote_date_created, "%Y-%m-%d"), "%Y-%m-%d"),
        datetime.strptime(datetime.strftime(quote_date_required, "%Y-%m-%d"), "%Y-%m-%d"),
        quote_name,
        quote_address,
        quote_suburb,
        quote_contact_number,
        quote_email,
        quote_memo,
        quote_kilometres,
        quote_completed,
    )

    quote.update() if quote_id else quote.insert()
    quotes[quote.id] = quote

    main_window.lblQuote_DateCreated.setText(str(datetime.strftime(quote_date_created, "%d/%m/%Y")))
    main_window.lblQuoteId.setText(str(quote.id))

    with SQLiteConnection() as cur:
        quote_item_tuples = cur.execute(
            """
            SELECT qi.id, vc.charge_type
            FROM quote_item qi
            LEFT JOIN vehicle_combination vc ON qi.vehicle_combination_name = vc.name
            WHERE qi.quote_id = ?;
            """,
            (quote.id,),
        ).fetchall()

        for t in quote_item_tuples:
            transport_rate_ex_gst = get_transport_rate_ex_gst(
                quote.kilometres, t[1]
            )

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

    toggle_buttons(
        [
            (main_window.btnNewQuoteItem, True),
            (main_window.btnEditQuoteItem, False),
            (main_window.btnDeleteQuoteItem, False),
            (main_window.btnExportQuote_Entry, True),
            (main_window.btnOpenEmailQuote_Entry, True),
        ]
    )

    quote_special_conditions_table = main_window.tblQuoteSpecialConditions
    for row in range(quote_special_conditions_table.rowCount()):
        special_condition_id = string_to_int(quote_special_conditions_table.item(row, 0).text())
        is_checked = get_checkbox_state(quote_special_conditions_table, row)

        if quote_id:
            quote_special_condition = QuoteSpecialCondition.get_by_quote_and_special_condition(quote.id,
                                                                                               special_condition_id)
            if quote_special_condition is None:
                quote_special_condition = QuoteSpecialCondition(None, quote.id, special_condition_id, is_checked)
                quote_special_condition.insert()
            else:
                quote_special_condition.is_checked = is_checked
                quote_special_condition.update()
        else:
            quote_special_condition = QuoteSpecialCondition(None, quote.id, special_condition_id, is_checked)
            quote_special_condition.insert()

    quote_id = quote.id
    InfoMessageBox(f"Successfully saved {quote.name} - {quote.address}, {quote.suburb}.")


def search(main_window: Ui_MainWindow, search_text: str):
    global quotes, matches
    matches = (
        quotes
        if not search_text
        else {
            q.id: q
            for q in quotes.values()
            if search_text
               in "".join([str(q.id), q.name.lower(), q.address.lower(), q.suburb.lower()])
        }
    )

    refresh_table(main_window)


def export(main_window: Ui_MainWindow, quote_id: int):
    if quote_id is None:
        quote_id = int(main_window.lblQuoteId.text())
    global quotes
    quotes[quote_id].export()


def open_email_from_table(main_window: Ui_MainWindow):
    quote_id = selected_row_id(main_window.tblQuotes)
    global quotes
    quotes[quote_id].create_email()

def open_email_from_entry(main_window: Ui_MainWindow):
    quote_id_text = main_window.lblQuoteId.text()
    if not quote_id_text:
        return
    quote_id = int(quote_id_text)
    global quotes
    quotes[quote_id].create_email()

def connect(main_window: Ui_MainWindow):
    main_window.btnOpenEmailQuote.clicked.connect(
        lambda: open_email_from_table(main_window)
    )
    main_window.btnExportQuote.clicked.connect(
        lambda: export(main_window, selected_row_id(main_window.tblQuotes))
    )
    main_window.btnOpenEmailQuote_Entry.clicked.connect(
        lambda: open_email_from_entry(main_window)
    )
    main_window.btnExportQuote_Entry.clicked.connect(
        lambda: export(main_window, string_to_int(main_window.lblQuoteId.text()))
    )
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
    int_only_validator = QIntValidator()
    int_only_validator.setRange(0, 9999)
    main_window.txtQuote_Kilometres.setValidator(int_only_validator)
