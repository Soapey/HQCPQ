from PyQt5.QtWidgets import QApplication, QMainWindow
from app.gui.components.main_window import Ui_MainWindow
from app.gui.view_enum import ViewPage
from app.db.config import start_db
from app.gui.actions.quote_actions import (
    connect as connect_quotes,
    navigate_to_listing_view,
)
from app.gui.actions.quoteitem_actions import connect as connect_quote_items
from app.gui.actions.product_actions import connect as connect_products
from app.gui.actions.productrate_actions import connect as connect_product_rates
from app.gui.actions.ratetype_actions import connect as connect_rate_types
from app.gui.actions.vehiclecombination_actions import (
    connect as connect_vehicle_combinations,
)
import sys


def connect_main_window_actions(main_window: object):

    # Set up Quote gui actions
    connect_quotes(main_window)

    # Set up QuoteItem gui actions
    connect_quote_items(main_window)

    # Set up Product gui actions
    connect_products(main_window)

    # Set up ProductRate gui actions
    connect_product_rates(main_window)

    # Set up RateType gui actions
    connect_rate_types(main_window)

    # Set up VehicleCombination gui actions
    connect_vehicle_combinations(main_window)


def main():

    start_db()

    app = QApplication(sys.argv)
    main_window_root = QMainWindow()
    main_window = Ui_MainWindow()
    main_window.setupUi(main_window_root)

    navigate_to_listing_view(main_window)
    main_window_root.showMaximized()

    connect_main_window_actions(main_window)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
