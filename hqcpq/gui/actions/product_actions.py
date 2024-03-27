from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog

from hqcpq.classes.Product import Product
from hqcpq.classes.ProductRate import ProductRate
from hqcpq.gui.actions.productrate_actions import (
    refresh_table as refresh_product_rates_table,
    fetch_global_entities as fetch_productrate_global_entities,
)
from hqcpq.gui.classes.InfoMessageBox import InfoMessageBox
from hqcpq.gui.classes.ErrorMessageBox import ErrorMessageBox
from hqcpq.gui.classes.AskYesNoMessageBox import AskYesNoMessageBox
from hqcpq.gui.components.main_window import Ui_MainWindow
from hqcpq.gui.helpers import change_view, selected_row_id, toggle_buttons
from hqcpq.gui.view_enum import ViewPage
from hqcpq.helpers.conversion import string_to_int, string_to_float
import csv

products: dict[int, Product] = dict()
matches: dict[int, Product] = dict()


def fetch_global_variables():
    global products, matches
    products = Product.get_all()
    matches = products


def navigate_to_listing_view(main_window: Ui_MainWindow):
    fetch_global_variables()
    refresh_table(main_window)
    change_view(main_window.swPages, ViewPage.PRODUCTS)


def search(main_window: Ui_MainWindow, search_text: str):
    global products, matches
    matches = (
        products
        if not search_text
        else {p.id: p for p in products.values() if search_text in p.name.lower()}
    )
    refresh_table(main_window)


def on_row_select(main_window: Ui_MainWindow):
    selected_id = selected_row_id(main_window.tblProducts)
    toggle_buttons(
        [
            (main_window.btnNewProduct, True),
            (main_window.btnEditProduct, selected_id is not None),
            (main_window.btnDeleteProduct, selected_id is not None),
        ]
    )


def refresh_table(main_window: Ui_MainWindow):

    global matches

    tbl_headers = ["ID", "Name", "Weighbridge Product Id"]
    tbl: QTableWidget = main_window.tblProducts
    tbl.clear()
    tbl.setRowCount(len(matches.values()))
    tbl.setColumnCount(len(tbl_headers))
    tbl.setHorizontalHeaderLabels(tbl_headers)

    for index, product in enumerate(matches.values()):
        tbl.setItem(index, 0, QTableWidgetItem(str(product.id)))
        tbl.setItem(index, 1, QTableWidgetItem(product.name))
        tbl.setItem(index, 2, QTableWidgetItem(str(product.weighbridge_product_id)))

    header: QHeaderView = tbl.horizontalHeader()
    for i in range(len(tbl_headers)):
        header.setSectionResizeMode(
            i,
            QHeaderView.ResizeMode.ResizeToContents
            if i < len(tbl_headers) - 1
            else QHeaderView.ResizeMode.Stretch,
        )

    toggle_buttons(
        [
            (main_window.btnNewProduct, True),
            (main_window.btnEditProduct, False),
            (main_window.btnDeleteProduct, False),
        ]
    )


def clear_entry_fields(main_window: Ui_MainWindow):
    main_window.lblProductId.clear()
    main_window.txtProductWeighbridgeProductId.clear()
    main_window.txtProductName.clear()
    main_window.tblProductRates.setRowCount(0)


def new(main_window: Ui_MainWindow):
    fetch_productrate_global_entities()
    clear_entry_fields(main_window)
    toggle_buttons(
        [
            (main_window.btnNewProductRate, False),
            (main_window.btnEditProductRate, False),
            (main_window.btnDeleteProductRate, False),
        ]
    )
    change_view(main_window.swPages, ViewPage.PRODUCT_ENTRY)


def edit(main_window: Ui_MainWindow):
    fetch_productrate_global_entities()

    global products
    product: Product = products[selected_row_id(main_window.tblProducts)]

    main_window.lblProductId.setText(str(product.id))
    main_window.txtProductWeighbridgeProductId.setText(str(product.weighbridge_product_id))
    main_window.txtProductName.setText(product.name)

    refresh_product_rates_table(main_window)

    toggle_buttons(
        [
            (main_window.btnNewProductRate, True),
            (main_window.btnEditProductRate, False),
            (main_window.btnDeleteProductRate, False),
        ]
    )

    change_view(main_window.swPages, ViewPage.PRODUCT_ENTRY)


def delete(main_window: Ui_MainWindow):
    global products
    product: Product = products[selected_row_id(main_window.tblProducts)]

    delete_confirmed: bool = AskYesNoMessageBox(f"Are you sure that you would like to delete {product.name}?")

    if not delete_confirmed:
        return

    Product.delete(product.id)

    del products[product.id]

    refresh_table(main_window)

    InfoMessageBox(f"{product.name} successfully deleted.")


def save(main_window: Ui_MainWindow):

    if form_is_valid(main_window) is False:
        return

    product_id: int = string_to_int(main_window.lblProductId.text())
    product_weighbridgeproductid: int = string_to_int(main_window.txtProductWeighbridgeProductId.text())
    product_name: str = main_window.txtProductName.text()

    product: Product = Product(product_id, product_weighbridgeproductid, product_name)

    product.update() if product_id else product.insert()
    products[product.id] = product

    main_window.lblProductId.setText(str(product.id))

    toggle_buttons(
        [
            (main_window.btnNewProductRate, True),
            (main_window.btnEditProductRate, False),
            (main_window.btnDeleteProductRate, False),
        ]
    )

    InfoMessageBox(message=f"Successfully saved {product.name}.")


def form_is_valid(main_window: Ui_MainWindow):
    error_string = str()

    entity_id: int = string_to_int(main_window.lblProductId.text())
    entity_weighbridgeproductid: int = string_to_int(main_window.txtProductWeighbridgeProductId.text())
    entity_name = main_window.txtProductName.text()

    if entity_weighbridgeproductid is None:
        error_string += "\n- Weighbridge Product Id field cannot be blank."

    if len(entity_name) == 0:
        error_string += "\n- Name field cannot be blank."
    else:

        global products
        products_with_same_name = [
            p for p in products.values() if p.name == entity_name and p.id != entity_id
        ]

        if len(products_with_same_name) > 0:
            error_string += f"\n- {entity_name} already exists."

    if len(error_string) > 0:
        ErrorMessageBox(error_string)

    return len(error_string) == 0


def clear_import_fields(main_window: Ui_MainWindow):
    main_window.txtProduct_ImportFilePath.clear()
    main_window.cmbProduct_ImportIdColumn.clear()
    main_window.cmbProduct_ImportNameColumn.clear()

    main_window.txtProductRate_ImportFilePath.clear()
    main_window.cmbProductRate_ImportIdColumn.clear()
    main_window.cmbProductRate_ImportProductIdColumn.clear()
    main_window.cmbProductRate_ImportNameColumn.clear()
    main_window.cmbProductRate_ImportRateColumn.clear()


def start_import(main_window: Ui_MainWindow):
    clear_import_fields(main_window)

    change_view(main_window.swPages, ViewPage.PRODUCT_IMPORT)


def select_product_import_file(main_window: Ui_MainWindow):
    file_path, _ = QFileDialog.getOpenFileName(None, "Select CSV File", "", "CSV Files (*.csv)")
    if file_path:
        main_window.txtProduct_ImportFilePath.setText(file_path)

        main_window.cmbProduct_ImportIdColumn.clear()
        main_window.cmbProduct_ImportNameColumn.clear()

        with open(file_path, 'r') as file:
            header_row = file.readline().strip().split(',')

        for column_name in header_row:
            main_window.cmbProduct_ImportIdColumn.addItem(column_name)
            main_window.cmbProduct_ImportNameColumn.addItem(column_name)


def select_product_rate_import_file(main_window: Ui_MainWindow):
    file_path, _ = QFileDialog.getOpenFileName(None, "Select CSV File", "", "CSV Files (*.csv)")
    if file_path:
        main_window.txtProductRate_ImportFilePath.setText(file_path)

        main_window.cmbProductRate_ImportIdColumn.clear()
        main_window.cmbProductRate_ImportProductIdColumn.clear()
        main_window.cmbProductRate_ImportNameColumn.clear()
        main_window.cmbProductRate_ImportRateColumn.clear()

        with open(file_path, 'r') as file:
            header_row = file.readline().strip().split(',')

        for column_name in header_row:
            main_window.cmbProductRate_ImportIdColumn.addItem(column_name)
            main_window.cmbProductRate_ImportProductIdColumn.addItem(column_name)
            main_window.cmbProductRate_ImportNameColumn.addItem(column_name)
            main_window.cmbProductRate_ImportRateColumn.addItem(column_name)


def import_form_is_valid(main_window: Ui_MainWindow):
    error_string = str()

    if not main_window.txtProduct_ImportFilePath.text():
        error_string += "\n- PRODUCT: File Path field cannot be blank."

    if not main_window.cmbProduct_ImportIdColumn.currentText():
        error_string += "\n- PRODUCT: Please select the file ID column from the dropdown."

    if not main_window.cmbProduct_ImportNameColumn.currentText():
        error_string += "\n- PRODUCT: Please select the file Name column from the dropdown."

    if not main_window.txtProductRate_ImportFilePath.text():
        error_string += "\n- PRODUCT RATE: File Path field cannot be blank."

    if not main_window.cmbProductRate_ImportIdColumn.currentText():
        error_string += "\n- PRODUCT RATE: Please select the file ID column from the dropdown."

    if not main_window.cmbProductRate_ImportProductIdColumn.currentText():
        error_string += "\n- PRODUCT RATE: Please select the file Product ID column from the dropdown."

    if not main_window.cmbProductRate_ImportNameColumn.currentText():
        error_string += "\n- PRODUCT RATE: Please select the file Name column from the dropdown."

    if not main_window.cmbProductRate_ImportRateColumn.currentText():
        error_string += "\n- PRODUCT RATE: Please select the file Rate column from the dropdown."

    if len(error_string) > 0:
        ErrorMessageBox(error_string)

    return len(error_string) == 0


def read_csv_and_perform_updates(main_window: Ui_MainWindow):
    inserted_product_count, updated_product_count = read_product_csv_and_extract_columns(main_window)
    inserted_product_rate_count, updated_product_rate_count = read_product_rate_csv_and_extract_columns(main_window)
    change_view(main_window.swPages, ViewPage.PRODUCTS)
    InfoMessageBox(f"PRODUCTS:\nInserted: {inserted_product_count}\nUpdated: {updated_product_count}\n\nPRODUCT "
                   f"RATES:\nInserted: {inserted_product_rate_count}\nUpdated: {updated_product_rate_count}")


def read_product_rate_csv_and_extract_columns(main_window: Ui_MainWindow):

    if import_form_is_valid(main_window) is False:
        return

    file_path = main_window.txtProductRate_ImportFilePath.text()
    id_column_header = main_window.cmbProductRate_ImportIdColumn.currentText()
    product_name_column_header = main_window.cmbProductRate_ImportProductIdColumn.currentText()
    name_column_header = main_window.cmbProductRate_ImportNameColumn.currentText()
    rate_column_header = main_window.cmbProductRate_ImportRateColumn.currentText()

    try:
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            header_row = next(reader)

            id_index = header_row.index(id_column_header) if id_column_header in header_row else None
            product_name_index = header_row.index(product_name_column_header) if product_name_column_header in header_row else None
            name_index = header_row.index(name_column_header) if name_column_header in header_row else None
            rate_index = header_row.index(rate_column_header) if rate_column_header in header_row else None

            print(id_index, product_name_index, name_index, rate_index)

            inserted_product_rate_count = 0
            updated_product_rate_count = 0
            global products
            for row in reader:
                if id_index is not None and product_name_index is not None and name_index is not None and rate_index is not None:
                    if 0 <= id_index < len(row) and 0 <= product_name_index < len(row) and 0 <= name_index < len(row) and 0 <= rate_index < len(row):
                        id_value = string_to_int(row[id_index])
                        product_name_value = row[product_name_index]
                        name_value = row[name_index]
                        rate_value = string_to_float(row[rate_index])

                        match_product_rate = ProductRate.get_by_productname_and_name(product_name=product_name_value, name=name_value)
                        if match_product_rate is None:
                            product_matches = [p for p in products.values() if p.name == product_name_value]
                            referenced_product = None
                            if product_matches:
                                referenced_product = product_matches[0]
                            if referenced_product:
                                ProductRate.insert(ProductRate(None, id_value, name_value, rate_value, referenced_product.id))
                                inserted_product_rate_count += 1
                        else:
                            print("UPDATING", name_value, rate_value)
                            match_product_rate.name = name_value
                            match_product_rate.rate = rate_value
                            match_product_rate.weighbridge_product_rate_id = id_value
                            match_product_rate.update()
                            updated_product_rate_count += 1

    except Exception as e:
        ErrorMessageBox(message=f"An error occured:{str(e)}\nInserted Product Rates: {inserted_product_rate_count}\nUpdated Product Rates: {updated_product_rate_count}")

    return inserted_product_rate_count, updated_product_rate_count


def read_product_csv_and_extract_columns(main_window: Ui_MainWindow):

    if import_form_is_valid(main_window) is False:
        return

    file_path = main_window.txtProduct_ImportFilePath.text()
    id_column_header = main_window.cmbProduct_ImportIdColumn.currentText()
    name_column_header = main_window.cmbProduct_ImportNameColumn.currentText()

    try:
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            header_row = next(reader)

            id_index = header_row.index(id_column_header) if id_column_header in header_row else None
            name_index = header_row.index(name_column_header) if name_column_header in header_row else None

            inserted_product_count = 0
            updated_product_count = 0
            for row in reader:
                if id_index is not None and name_index is not None:
                    if 0 <= id_index < len(row) and 0 <= name_index < len(row):
                        id_value = string_to_int(row[id_index])
                        name_value = row[name_index]

                        if Product.get_by_weighbridge_product_id(id_value) is None:
                            Product.insert(Product(None, id_value, name_value))
                            inserted_product_count += 1
                        else:
                            Product.update_by_weighbridge_product_id(name_value, id_value)
                            updated_product_count += 1

    except Exception as e:
        ErrorMessageBox(message=f"An error occured:{str(e)}\nInserted Products: {inserted_product_count}\nUpdated Products: {updated_product_count}")

    return inserted_product_count, updated_product_count


def connect(main_window: Ui_MainWindow):

    main_window.actionProducts.triggered.connect(
        lambda: navigate_to_listing_view(main_window)
    )
    main_window.tblProducts.selectionModel().selectionChanged.connect(
        lambda: on_row_select(main_window)
    )
    main_window.btnNewProduct.clicked.connect(lambda: new(main_window))
    main_window.btnEditProduct.clicked.connect(lambda: edit(main_window))
    main_window.btnDeleteProduct.clicked.connect(lambda: delete(main_window))
    main_window.btnImportProduct.clicked.connect(lambda: start_import(main_window))

    main_window.btnProduct_SelectImportFile.clicked.connect(lambda: select_product_import_file(main_window))
    main_window.btnProductRate_SelectImportFile.clicked.connect(lambda: select_product_rate_import_file(main_window))

    main_window.btnProductImportConfirm.clicked.connect(lambda: read_csv_and_perform_updates(main_window))

    main_window.btnSaveProduct.clicked.connect(lambda: save(main_window))
    main_window.txtProductSearch.textChanged.connect(
        lambda: search(main_window, main_window.txtProductSearch.text().lower())
    )
