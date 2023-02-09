import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
import AutoUpdate
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
from hqcpq.helpers import read_config


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

    config = read_config()

    AutoUpdate.set_url(config["AppSettings"]["update_version_url"])
    AutoUpdate.set_current_version(config["AppSettings"]["version"])

    if not AutoUpdate.is_up_to_date():
        AutoUpdate.download(config["AppSettings"]["update_file_url"])
        sys.exit()

    # Establish build type.
    build = config["AppSettings"]["build"].strip().lower()

    # Start the program.
    if build == "d":
        main(build_type=BuildType.DEVELOPMENT, clean_start=False)
    elif build == "d_clean":
        main(build_type=BuildType.DEVELOPMENT, clean_start=True)
    elif build == "p":
        main(build_type=BuildType.PRODUCTION, clean_start=False)