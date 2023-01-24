from app.gui.helpers import toggle_buttons
from app.classes.Quote import Quote
from app.gui.components.main_window import Ui_MainWindow
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


quotes: list[Quote] = list()


def refresh_table(main_window: Ui_MainWindow):

    global quotes
    quotes = Quote.get()

    tbl: QTableWidget = main_window.tblQuotes

    headers: list[str] = [
        "ID",
        "Date Created",
        "Date Required",
        "Name",
        "Address",
        "Suburb",
        "Contact Number",
    ]
    tbl.setColumnCount(len(headers))
    tbl.setRowCount(len(quotes))
    tbl.setHorizontalHeaderLabels(headers)

    for index, quote in enumerate(quotes):
        tbl.setItem(index, 0, str(quote.id))
        tbl.setItem(index, 1, str(quote.date_created))
        tbl.setItem(index, 2, str(quote.date_required))
        tbl.setItem(index, 3, quote.name)
        tbl.setItem(index, 4, quote.address)
        tbl.setItem(index, 5, quote.suburb)
        tbl.setItem(index, 6, str(quote.contact_number))


def connect():
    pass
