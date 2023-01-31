from tkinter import messagebox
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from app.classes.Product import Product
from app.gui.components.main_window import Ui_MainWindow
from app.gui.view_enum import ViewPage
from app.gui.helpers import change_view, selected_row_id, toggle_buttons, int_conv
from app.gui.actions.productrate_actions import (
    refresh_table as refresh_product_rates_table,
    fetch_global_entities as fetch_productrate_global_entities,
)


products: dict[int, Product] = dict()
matches: dict[int, Product] = dict()


def navigate_to_listing_view(main_window: Ui_MainWindow):

    global products, matches
    products = Product.get()
    matches = products

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
    tbl_headers = ["ID", "Name"]

    tbl: QTableWidget = main_window.tblProducts
    tbl.clear()
    tbl.setRowCount(len(matches.values()))
    tbl.setColumnCount(len(tbl_headers))
    tbl.setHorizontalHeaderLabels(tbl_headers)

    for index, product in enumerate(matches.values()):
        tbl.setItem(index, 0, QTableWidgetItem(str(product.id)))
        tbl.setItem(index, 1, QTableWidgetItem(product.name))

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

    delete_confirmed: bool = messagebox.askyesno(
        title="Confirm Delete",
        message=f"Are you sure that you would like to delete {product.name}?",
    )

    if not delete_confirmed:
        return

    product.delete()

    del products[product.id]

    refresh_table(main_window)

    messagebox.showinfo(
        title="Delete Success", message=f"{product.name} successfully deleted."
    )


def save(main_window: Ui_MainWindow):

    if form_is_valid(main_window) is False:
        return

    product_id: int = int_conv(main_window.lblProductId.text())
    product_name: str = main_window.txtProductName.text()

    product: Product = Product(product_id, product_name)

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

    messagebox.showinfo(
        title="Save Success", message=f"Successfully saved {product.name}."
    )


def form_is_valid(main_window: Ui_MainWindow):

    result = True
    error_string = str()

    entity_id: int = int_conv(main_window.lblProductId.text())
    entity_name = main_window.txtProductName.text()

    if len(entity_name) == 0:
        result = False
        error_string += "\n- Name field cannot be blank."
    else:

        global products
        products_with_same_name = [
            p for p in products.values() if p.name == entity_name and p.id != entity_id
        ]

        if len(products_with_same_name) > 0:
            result = False
            error_string += f"\n- {entity_name} already exists."

    if result == False:
        messagebox.showerror("Save Error", error_string)

    return result


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
    main_window.btnSaveProduct.clicked.connect(lambda: save(main_window))
    main_window.txtProductSearch.textChanged.connect(
        lambda: search(main_window, main_window.txtProductSearch.text().lower())
    )
