import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from app.gui.components.main_window import Ui_MainWindow
from app.db.db_type_enum import DbType
from app.db.build_type_enum import BuildType
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


def connect_main_window_actions(main_window: Ui_MainWindow):

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


def start_app():

    app = QApplication(sys.argv)
    main_window_root = QMainWindow()
    main_window = Ui_MainWindow()
    main_window.setupUi(main_window_root)

    navigate_to_listing_view(main_window)
    main_window_root.showMaximized()

    connect_main_window_actions(main_window)

    sys.exit(app.exec_())


def main(build_type: BuildType = BuildType.DEVELOPMENT, clean_start: bool = True):

    start_db(
        start_build_type=build_type,
        start_db_type=DbType.SQL_SERVER,
        clean_start=clean_start,
    )
    start_app()


if __name__ == "__main__":
    main(BuildType.PRODUCTION, clean_start=False)
