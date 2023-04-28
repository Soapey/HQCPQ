from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from hqcpq.gui.components.main_window import Ui_MainWindow
from hqcpq.gui.helpers import change_view
from hqcpq.gui.view_enum import ViewPage
from hqcpq.helpers.io import read_config, update_config
from hqcpq.classes.Toast import Toast


def navigate_to_listing_view(main_window: Ui_MainWindow):

    refresh_table(main_window)

    change_view(main_window.swPages, ViewPage.TRANSPORT_SETTINGS)


def refresh_table(main_window: Ui_MainWindow):

    header_name = 'TransportSettings'

    config = read_config()

    if not config.has_section(header_name):
        return
    
    transportsettings_keys = [key for key in config[header_name].keys()]
    transportsettings_values = [config[header_name][key] for key in transportsettings_keys]

    # Configure the tables headers and prepare the row count before inserting data.
    tbl_headers = ["Value"]
    tbl: QTableWidget = main_window.tblTransportSettings
    tbl.clear()

    tbl.setRowCount(len(transportsettings_keys))
    tbl.setColumnCount(1)
    tbl.setHorizontalHeaderLabels(tbl_headers)

    print('attempting vertical header labels')
    tbl.setVerticalHeaderLabels(transportsettings_keys)
    print('success')

    for i, value in enumerate(transportsettings_values):
        tbl.setItem(i, 0, QTableWidgetItem(value))

    # Set all columns of the table to fit the column contents and stretch the last column.
    header: QHeaderView = tbl.horizontalHeader()
    for i in range(len(tbl_headers)):
        header.setSectionResizeMode(
            i,
            QHeaderView.ResizeMode.ResizeToContents
            if i < len(tbl_headers) - 1
            else QHeaderView.ResizeMode.Stretch,
        )


def save(main_window: Ui_MainWindow):
    config = read_config()
    tbl: QTableWidget = main_window.tblTransportSettings
    data = dict()

    for row in range(tbl.rowCount()):
        key_item = tbl.verticalHeaderItem(row)
        value_item = tbl.item(row, 0)
        if key_item and value_item:
            key = key_item.text()
            value = value_item.text()
            data[key] = value

    try:
        for key, value in data.items():
            config.set('TransportSettings', key, value)
        update_config(config)
        Toast("Save Success", "Successfully saved transport settings.").show()
    except Exception as e:
        print(f"Error while saving config: {e}")
        Toast("Save Error", "Failed to save transport settings.").show()


def connect(main_window: Ui_MainWindow):

    main_window.actionTransport_Settings.triggered.connect(
        lambda: navigate_to_listing_view(main_window)
    )
    main_window.btnSaveTransportSettings.clicked.connect(lambda: save(main_window))