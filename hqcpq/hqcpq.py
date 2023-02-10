import os
import sys
import shutil
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
from hqcpq.helpers import read_config, update_config
from tkinter import messagebox
from tkinter.messagebox import askyesno


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


def main():

    # Read configuration file.
    config = read_config()
    build = config["AppSettings"]["build"].strip().lower()

    # Start the program.
    if build == "d":
        start_db(start_build_type=BuildType.DEVELOPMENT, clean_start=False)
    elif build == "d_clean":
        start_db(start_build_type=BuildType.DEVELOPMENT, clean_start=True)
    elif build == "p":
        start_db(start_build_type=BuildType.PRODUCTION, clean_start=False)
    else:
        sys.exit()

    # Load the application root window and display.
    start_app()


def update():

    # Read configuration file.
    config = read_config()
    current_version = config["AppSettings"]["version"]
    update_directory = config["AppSettings"]["update_directory"]

    # Read update configuration file.
    try:
        update_config_file = read_config(f"{update_directory}\\update_config.ini")
        update_version = update_config_file["Configuration"]["version"]
        update_exe_name = update_config_file["Configuration"]["exe_name"]
    except:
        return

    # Check if current app version out of date.
    if current_version != update_version:

        # Ask user if they would like to update.
        if askyesno(
            "Update Required",
            "The current application version is out of date.\nWould you like to fetch the updated version?",
        ):

            try:
                # Copy the new .exe file from the update directory to the current directory.
                new_exe_path = os.path.join(os.path.abspath("."), update_exe_name)
                shutil.copyfile(
                    rf"{update_directory}\{update_exe_name}",
                    new_exe_path,
                )
            except:
                if os.path.exists(new_exe_path):
                    os.remove(new_exe_path)

                messagebox.showerror(
                    "Update Failed",
                    "An error occurred while trying to download the update file.\nPlease try again later.",
                )
                return

            try:
                # Change the current version in the config file.
                config.set("AppSettings", "version", update_version)
                update_config(config)
            except:
                messagebox.showerror(
                    "Update Failed",
                    "An error occurred while trying change the version number in the configuration file. Please change this manually.",
                )
                return

            # Start the updated version.
            os.startfile(new_exe_path)

            # Exit the current (older) version.
            sys.exit()


def remove_previous_versions():

    # Read configurationf file.
    config = read_config()
    base_exe_name = config["AppSettings"]["base_exe_name"]
    current_version = config["AppSettings"]["version"]

    # Loop through files in directory and remove any .exe that does not match current version.
    try:
        cwd = os.path.abspath(".")
        for filename in os.listdir(cwd):

            full_path = os.path.join(cwd, filename)
            extension = os.path.splitext(filename)[-1]

            if (
                os.path.isfile(full_path)
                and filename != f"{base_exe_name}_{current_version}.exe"
                and extension == ".exe"
            ):
                os.remove(full_path)
    except:
        pass


if __name__ == "__main__":

    update()

    remove_previous_versions()

    main()
