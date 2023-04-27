from tkinter import messagebox
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from hqcpq.classes.Toast import Toast
from hqcpq.classes.Product import Product
from hqcpq.gui.components.main_window import Ui_MainWindow
from hqcpq.gui.view_enum import ViewPage
from hqcpq.helpers.conversion import string_to_int
from hqcpq.gui.helpers import change_view, selected_row_id, toggle_buttons
from hqcpq.gui.actions.productrate_actions import (
    refresh_table as refresh_product_rates_table,
    fetch_global_entities as fetch_productrate_global_entities,
)


products: dict[int, Product] = dict()
matches: dict[int, Product] = dict()


def fetch_global_variables():
    """
    Requests the SQL database for all products and writes them to the global variables.

    Parameters
    ----------
    N/A
    """

    global products, matches
    products = Product.get()
    matches = products


def navigate_to_listing_view(main_window: Ui_MainWindow):
    """
    Prepares the GUI and then changes the stacked widget page to the Products listing view.

    Parameters
    ----------
    main_window  :  A Ui_MainWindow object as the root of the GUI; this contains the stacked widget.
    """

    # Set global variables.
    fetch_global_variables()

    # Refresh the Products listing view table with the products stored in the global matches variable.
    refresh_table(main_window)

    # Change the stacked widget page to the Products listing view.
    change_view(main_window.swPages, ViewPage.PRODUCTS)


def search(main_window: Ui_MainWindow, search_text: str):
    """
    Finds all products where their lowercased name matches the lowercased search text.
    Then writes the matches to the global matches variable.
    Then refreshes the Products listing view table with the match results.

    If the search text is empty, it will show all products.

    Parameters
    ----------
    main_window  :  A Ui_MainWindow object as the root of the GUI; this contains the stacked widget.
    search_text  :  The lowercased text (must be passed in lowercased) to be compared against each Product name.
    """

    # Loop through each product in the global products variable.
    # If the lowercased name matches the search text, add it to the result dictionary --
    # that will be written to the global matches variable.
    global products, matches
    matches = (
        products
        if not search_text
        else {p.id: p for p in products.values() if search_text in p.name.lower()}
    )

    # Refresh the Products listing view table with the products stored in the global matches variable.
    refresh_table(main_window)


def on_row_select(main_window: Ui_MainWindow):
    """
    Determines what action buttons will be shown, depending on if a row is selected in the Products listing view table.

    Parameters
    ----------
    main_window  :  A Ui_MainWindow object as the root of the GUI; this contains the stacked widget.
    """

    # Get the id of the Product on the tables selected row, this will be None if there is no row selected.
    selected_id = selected_row_id(main_window.tblProducts)

    # Show and hide action buttons according to whether a row is selected or not.
    toggle_buttons(
        [
            (main_window.btnNewProduct, True),
            (main_window.btnEditProduct, selected_id is not None),
            (main_window.btnDeleteProduct, selected_id is not None),
        ]
    )


def refresh_table(main_window: Ui_MainWindow):
    """
    Refreshes the Product listing view table with the products stored in the global matches variable.

    Parameters
    ----------
    main_window  :  A Ui_MainWindow object as the root of the GUI; this contains the stacked widget.
    """

    global matches

    # Configure the tables headers and prepare the row count before inserting data.
    tbl_headers = ["ID", "Name"]
    tbl: QTableWidget = main_window.tblProducts
    tbl.clear()
    tbl.setRowCount(len(matches.values()))
    tbl.setColumnCount(len(tbl_headers))
    tbl.setHorizontalHeaderLabels(tbl_headers)

    # Insert each data cell into table.
    for index, product in enumerate(matches.values()):
        tbl.setItem(index, 0, QTableWidgetItem(str(product.id)))
        tbl.setItem(index, 1, QTableWidgetItem(product.name))

    # Set all columns of the table to fit the column contents and stretch the last column.
    header: QHeaderView = tbl.horizontalHeader()
    for i in range(len(tbl_headers)):
        header.setSectionResizeMode(
            i,
            QHeaderView.ResizeMode.ResizeToContents
            if i < len(tbl_headers) - 1
            else QHeaderView.ResizeMode.Stretch,
        )

    # Hide edit & delete action buttons as no row will be selected once the table is refreshed.
    toggle_buttons(
        [
            (main_window.btnNewProduct, True),
            (main_window.btnEditProduct, False),
            (main_window.btnDeleteProduct, False),
        ]
    )


def clear_entry_fields(main_window: Ui_MainWindow):
    """
    Clears all entry fields to enter a new or edit a Product.

    Parameters
    ----------
    main_window  :  A Ui_MainWindow object as the root of the GUI; this contains the stacked widget.
    """

    # Clear entry fields.
    main_window.lblProductId.clear()
    main_window.txtProductName.clear()
    main_window.tblProductRates.setRowCount(0)


def new(main_window: Ui_MainWindow):
    """
    Clears all entry fields and then changes the stacked widget page to the Product entry/edit view .

    Parameters
    ----------
    main_window  :  A Ui_MainWindow object as the root of the GUI; this contains the stacked widget.
    """

    # Refresh all global variables.
    fetch_productrate_global_entities()

    # Clear entry fields.
    clear_entry_fields(main_window)

    # Hide all ProductRate action buttons.
    toggle_buttons(
        [
            (main_window.btnNewProductRate, False),
            (main_window.btnEditProductRate, False),
            (main_window.btnDeleteProductRate, False),
        ]
    )

    # Change the stacked widget page to the Product entry/edit view.
    change_view(main_window.swPages, ViewPage.PRODUCT_ENTRY)


def edit(main_window: Ui_MainWindow):

    # Refresh all global variables.
    fetch_productrate_global_entities()

    # Establish the Product to be edited.
    global products
    product: Product = products[selected_row_id(main_window.tblProducts)]

    # Pre-fill entry fields with Product attribute values.
    main_window.lblProductId.setText(str(product.id))
    main_window.txtProductName.setText(product.name)

    # Refresh ProductRate table with all ProductRates relevant to the Product.
    refresh_product_rates_table(main_window)

    # Hide edit & delete action buttons as no row will be selected once the table is refreshed.
    toggle_buttons(
        [
            (main_window.btnNewProductRate, True),
            (main_window.btnEditProductRate, False),
            (main_window.btnDeleteProductRate, False),
        ]
    )

    # Change the stacked widget page to the Product entry/edit view.
    change_view(main_window.swPages, ViewPage.PRODUCT_ENTRY)


def delete(main_window: Ui_MainWindow):

    # Establish the Product to be deleted.
    global products
    product: Product = products[selected_row_id(main_window.tblProducts)]

    # Ask user to confirm the deletion.
    delete_confirmed: bool = messagebox.askyesno(
        title="Confirm Delete",
        message=f"Are you sure that you would like to delete {product.name}?",
    )

    # If user would not like to delete, return early.
    if not delete_confirmed:
        return

    # Delete the Product
    product.delete()

    # Remove Product from global Product variable dictionary.
    del products[product.id]

    # Refresh table with current global Product variable dictionary
    refresh_table(main_window)

    # Show success toast notification.
    Toast("Delete Success", f"{product.name} successfully deleted.").show()


def save(main_window: Ui_MainWindow):

    if form_is_valid(main_window) is False:
        return

    product_id: int = string_to_int(main_window.lblProductId.text())
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

    Toast("Save Success", f"Successfully saved {product.name}.").show()


def form_is_valid(main_window: Ui_MainWindow):

    result = True
    error_string = str()

    entity_id: int = string_to_int(main_window.lblProductId.text())
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
