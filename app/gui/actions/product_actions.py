from tkinter import messagebox
from app.classes.Product import Product
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton
from app.gui.view_enum import ViewPage
from app.gui.helpers import change_view, selected_row_id, toggle_buttons
from app.gui.actions.productrate_actions import (
    refresh_table as refresh_product_rates_table,
    on_row_select as on_product_rate_row_select,
    fetch_global_entities as fetch_productrate_global_entities,
)


entities: list[Product] = list()


def change_to_product_view(main_window):

    global entities
    entities = Product.get()

    refresh_table(main_window, entities)

    main_window.swPages.setCurrentIndex(1)


def change_to_product_entry_view(main_window):

    fetch_productrate_global_entities()

    change_view(main_window.swPages, ViewPage.PRODUCT_ENTRY)


def search(main_window, search_text):

    global entities
    matching_products = list(filter(lambda e: search_text in e.name.lower(), entities))

    refresh_table(main_window, matching_products)


def on_row_select(main_window):

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


def refresh_table(main_window, fetched_entities: list[Product] = None):

    fetched_entities = fetched_entities or entities

    tbl: QTableWidget = main_window.tblProducts

    headers = ["ID", "Name"]

    tbl.setRowCount(len(fetched_entities))
    tbl.setColumnCount(len(headers))
    tbl.setHorizontalHeaderLabels(headers)

    for index, entity in enumerate(fetched_entities):
        tbl.setItem(index, 0, QTableWidgetItem(str(entity.id)))
        tbl.setItem(index, 1, QTableWidgetItem(entity.name))

    on_row_select(main_window)


def clear_entry_fields(main_window):

    main_window.lblProductId.clear()
    main_window.txtProductName.clear()
    main_window.tblProductRates.setRowCount(0)


def new(main_window):

    clear_entry_fields(main_window)

    toggle_buttons(
        main_window.btnNewProductRate,
        False,
        main_window.btnEditProductRate,
        False,
        main_window.btnDeleteProductRate,
        False,
    )

    change_to_product_entry_view(main_window)


def edit(main_window):

    selected_id = selected_row_id(main_window.tblProducts)

    entity = list(filter(lambda e: e.id == selected_id, entities))[0]

    main_window.lblProductId.setText(str(entity.id))
    main_window.txtProductName.setText(entity.name)

    refresh_product_rates_table(main_window)

    toggle_buttons(
        main_window.btnNewProductRate,
        True,
        main_window.btnEditProductRate,
        False,
        main_window.btnDeleteProductRate,
        False,
    )

    change_to_product_entry_view()


def delete(main_window):

    selected_id = selected_row_id(main_window.tblProducts)

    entity = list(filter(lambda e: e.id == selected_id, entities))[0]
    entity.delete()
    entities.remove(entity)

    refresh_table(main_window)


def save(main_window):

    if form_is_valid(main_window):

        id_label_text = main_window.lblProductId.text()

        p: Product = None
        if len(id_label_text) > 0:
            p = Product(int(id_label_text), main_window.txtProductName.text())
            p.update()
        else:
            p = Product(None, main_window.txtProductName.text())
            p.insert()

        main_window.lblProductId.setText(str(p.id))

        on_product_rate_row_select(main_window)


def form_is_valid(main_window):

    result = True
    error_string = str()

    entity_id: int = 0
    entity_name = main_window.txtProductName.text()
    id_label_text = main_window.lblProductId.text()

    if len(id_label_text) > 0:
        entity_id = int(id_label_text)

    if len(entity_name) == 0:
        result = False
        error_string += "\n- Name field cannot be blank."
    else:
        products_with_same_name = list(
            filter(lambda e: e.name == entity_name and e.id != entity_id, entities)
        )

        if len(products_with_same_name) > 0:
            result = False
            error_string += f"\n- {entity_name} already exists."

    if result == False:
        messagebox.showerror("Save Error", error_string)

    return result


def connect(main_window):

    main_window.actionProducts.triggered.connect(
        lambda: change_to_product_view(main_window)
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
