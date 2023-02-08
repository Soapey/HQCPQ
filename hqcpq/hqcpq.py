import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from hqcpq.gui.components.main_window import Ui_MainWindow
from hqcpq.db.build_type_enum import BuildType
from hqcpq.db.db import start_db
from hqcpq.gui.actions.quote_actions import (
    connect as connect_quotes,
    navigate_to_listing_view,
)
from hqcpq.gui.actions.quoteitem_actions import connect as connect_quote_items
from hqcpq.gui.actions.product_actions import connect as connect_products
from hqcpq.gui.actions.productrate_actions import connect as connect_product_rates
from hqcpq.gui.actions.ratetype_actions import connect as connect_rate_types
from hqcpq.gui.actions.vehiclecombination_actions import (
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


def main(build_type: BuildType, clean_start: bool):

    start_db(build_type, clean_start)
    start_app()


if __name__ == "__main__":

    # Establish build type.
    build_type: str
    try:
        build_type = sys.argv[1].strip().lower()
    except:
        build_type = "production"

    # Establish whether database will be clean started.
    clean_start: str
    try:
        clean_start = sys.argv[2].strip().lower()
    except:
        clean_start = "false"

    # Start the program.
    if build_type == "development":
        if clean_start == "true":
            main(build_type=BuildType.DEVELOPMENT, clean_start=True)
        elif clean_start == "false":
            main(build_type=BuildType.DEVELOPMENT, clean_start=False)

    elif build_type == "production":
        if clean_start == "true":
            main(build_type=BuildType.PRODUCTION, clean_start=True)
        elif clean_start == "false":
            main(build_type=BuildType.PRODUCTION, clean_start=False)
