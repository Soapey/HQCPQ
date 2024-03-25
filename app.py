import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from hqcpq.db.SQLiteUtil import initialise_db
from hqcpq.gui.actions.product_actions import connect as connect_products
from hqcpq.gui.actions.productrate_actions import connect as connect_product_rates
from hqcpq.gui.actions.quote_actions import (
    connect as connect_quotes,
    navigate_to_listing_view,
)
from hqcpq.gui.actions.quoteitem_actions import connect as connect_quote_items
from hqcpq.gui.actions.ratetype_actions import connect as connect_rate_types
from hqcpq.gui.actions.transportsettings_actions import connect as connect_transport_settings
from hqcpq.gui.actions.vehiclecombination_actions import (
    connect as connect_vehicle_combinations,
)
from hqcpq.gui.actions.special_condition_actions import connect as connect_special_conditions
from hqcpq.gui.components.main_window import Ui_MainWindow


def connect_main_window_actions(main_window: Ui_MainWindow):
    connect_quotes(main_window)
    connect_quote_items(main_window)
    connect_products(main_window)
    connect_product_rates(main_window)
    connect_rate_types(main_window)
    connect_vehicle_combinations(main_window)
    connect_transport_settings(main_window)
    connect_special_conditions(main_window)


def main():
    initialise_db()

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
