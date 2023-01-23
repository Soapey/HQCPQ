from PyQt5.QtWidgets import QApplication, QMainWindow
from app.gui.components.main_window import Ui_MainWindow
from app.gui.view_enum import ViewPage
from app.gui.helpers import change_view
from app.db.config import start_db
from app.gui.actions.product_actions import connect as connect_products
from app.gui.actions.productrate_actions import connect as connect_product_rates
from app.gui.actions.ratetype_actions import connect as connect_rate_types
import sys


def connect_main_window_actions(main_window: object):

    # Set up Quote gui actions
    main_window.actionQuotes.triggered.connect(
        lambda: change_view(main_window.swPages, ViewPage.QUOTES)
    )

    # Set up Product gui actions
    connect_products(main_window)

    # Set up ProductRate gui actions
    connect_product_rates(main_window)

    # Set up RateType gui actions
    connect_rate_types(main_window)


def main():

    start_db()

    app = QApplication(sys.argv)
    main_window_root = QMainWindow()
    main_window = Ui_MainWindow()
    main_window.setupUi(main_window_root)

    change_view(main_window.swPages, ViewPage.QUOTES)
    main_window_root.show()

    connect_main_window_actions(main_window)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
