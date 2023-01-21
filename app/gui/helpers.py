from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton, QLineEdit
from app.classes.Product import Product
from tkinter import messagebox


products: list[Product] = list()


def selected_row_id(tbl: QTableWidget):

    indexes = tbl.selectedIndexes()

    if len(indexes) == 0:
        return None

    selected_row = indexes[0].row()
    id_column = 0
    id = int(tbl.item(selected_row, id_column).text())

    return id


def change_view(stacked_widget, page_index: int):

    stacked_widget.setCurrentIndex(page_index)


def product_form_is_valid(main_window):

    result = True
    error_string = str()


    id_label_text = main_window.lblProductId.text()
    product_id: int = 0
    product_name = main_window.txtProductName.text()

    if len(id_label_text) > 0:
        product_id = int(id_label_text)

    if len(product_name) == 0:
        result = False
        error_string += '\n-Name field cannot be blank.'
    else:
        products_with_same_name = list(filter(lambda p: p.name == product_name and p.id != product_id, products))

        if len(products_with_same_name) > 0:
            result = False
            error_string += f'\n-{product_name} already exists.'  

    if result == False:
        messagebox.showerror('Save Error', error_string)

    return result


def new_product(main_window):

    main_window.lblProductId.clear()
    main_window.txtProductName.clear()

    change_view(main_window.swPages, 2)


def edit_product(main_window):

    selected_id = selected_row_id(main_window.tblProducts)

    product = list(filter(lambda p: p.id == selected_id, products))[0]

    main_window.lblProductId.setText(str(product.id))
    main_window.txtProductName.setText(product.name)

    change_view(main_window.swPages, 2)


def delete_product(main_window):

    selected_id = selected_row_id(main_window.tblProducts)

    product = list(filter(lambda p: p.id == selected_id, products))[0]
    product.delete()

    refresh_products_table(main_window)


def save_product(main_window):

    if product_form_is_valid(main_window):
        id_label_text = main_window.lblProductId.text()

        if len(id_label_text) > 0:
            id = int(id_label_text)
            Product(id, main_window.txtProductName.text()).update()
        else:
            Product(None, main_window.txtProductName.text()).insert()

        change_view_products(main_window)


def select_product(main_window):

    tbl: QTableWidget = main_window.tblProducts

    selected_id = selected_row_id(tbl)

    edit_button: QPushButton = main_window.btnEditProduct
    delete_button: QPushButton = main_window.btnDeleteProduct

    if selected_id:
        edit_button.setVisible(True)
        delete_button.setVisible(True)
    else:
        edit_button.setVisible(False)
        delete_button.setVisible(False)


def search_product(main_window, search_text):
    
    global products
    matching_products = list(filter(lambda p: search_text in p.name.lower(), products))

    refresh_products_table(main_window, matching_products)


def refresh_products_table(main_window, fetched_products: list[Product] = None):

    tbl: QTableWidget = main_window.tblProducts

    tbl.setRowCount(0)
    tbl.setColumnCount(0)

    tbl.setColumnCount(2)
    tbl.setHorizontalHeaderLabels(['ID', 'Name'])

    tbl.setRowCount(len(fetched_products))

    for index, product in enumerate(fetched_products):
        tbl.setItem(index, 0, QTableWidgetItem(str(product.id)))
        tbl.setItem(index, 1, QTableWidgetItem(product.name))

    select_product(main_window)


def change_view_products(main_window):

    global products
    products = Product.get()

    refresh_products_table(main_window, products)
    stacked_widget = main_window.swPages
    stacked_widget.setCurrentIndex(1)


def connect_main_window_actions(main_window: object):

    change_view(main_window.swPages, 0)

    main_window.actionQuotes.triggered.connect(lambda: change_view(main_window.swPages, 0))

    # Products
    main_window.actionProducts.triggered.connect(lambda: change_view_products(main_window))
    main_window.tblProducts.selectionModel().selectionChanged.connect(lambda: select_product(main_window))
    main_window.btnNewProduct.clicked.connect(lambda: new_product(main_window))
    main_window.btnEditProduct.clicked.connect(lambda: edit_product(main_window))
    main_window.btnDeleteProduct.clicked.connect(lambda: delete_product(main_window))
    main_window.btnSaveProduct.clicked.connect(lambda: save_product(main_window))
    main_window.txtProductSearch.textChanged.connect(lambda: search_product(main_window, main_window.txtProductSearch.text().lower()))