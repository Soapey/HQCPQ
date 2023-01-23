from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton, QComboBox
from app.classes.ProductRate import ProductRate
from app.classes.RateType import RateType
from app.db.SQLCursor import SQLCursor
from tkinter import messagebox
from app.gui.helpers import selected_row_id, change_view


entities: list[ProductRate] = list()
rate_types: list[RateType] = list()
records = list()


def on_row_select(main_window):

    tbl: QTableWidget = main_window.tblProductRates

    selected_id = selected_row_id(tbl)

    edit_button: QPushButton = main_window.btnEditProductRate
    delete_button: QPushButton = main_window.btnDeleteProductRate

    if selected_id:
        edit_button.setVisible(True)
        delete_button.setVisible(True)
    else:
        edit_button.setVisible(False)
        delete_button.setVisible(False)


def refresh_table(main_window):

    product_rates_tbl: QTableWidget = main_window.tblProductRates

    selected_product_id = selected_row_id(main_window.tblProducts)

    global entities
    global rate_types
    global records

    entities = ProductRate.get()
    rate_types = sorted(RateType.get(), key=lambda rt: rt.name)

    with SQLCursor() as cur:
        records = cur.execute('''
            SELECT pr.id, rt.name, pr.rate
            FROM product_rate pr
            LEFT JOIN rate_type rt ON pr.rate_type_id = rt.id
            WHERE pr.product_id = ?''',
            (selected_product_id,))

    headers = ['ID', 'Type', 'Rate']
    product_rates_tbl.setRowCount(len(entities))
    product_rates_tbl.setColumnCount(len(headers))
    product_rates_tbl.setHorizontalHeaderLabels(headers)

    for index, record in enumerate(records):
        product_rates_tbl.setItem(index, 0, QTableWidgetItem(str(record[0])))
        product_rates_tbl.setItem(index, 1, QTableWidgetItem(record[1]))
        product_rates_tbl.setItem(index, 2, QTableWidgetItem(record[2]))

    on_row_select(main_window)


def clear_entry_fields(main_window):


    productrate_ratetype_combobox: QComboBox = main_window.cmbProductRate_RateType
    productrate_ratetype_combobox.clear()
    
    for rate_type in rate_types:
        productrate_ratetype_combobox.addItem(rate_type.name)

    main_window.txtProductRate_Rate.clear()


def new(main_window):

    clear_entry_fields(main_window)

    change_view(main_window.swPages, 3)


def edit(main_window):

    selected_id = selected_row_id(main_window.tblProductRates)

    entity = list(filter(lambda r: r[0] == selected_id, records))[0]

    main_window.lblProductRateId.setText(str(entity[0]))
    main_window.cmbProductRate_RateType.setCurrentText(entity[1])
    main_window.txtProductRate_Rate.setText(str(entity[2]))

    change_view(main_window.swPages, 3)


def delete(main_window):

    selected_id = selected_row_id(main_window.tblProductRates)

    entity = list(filter(lambda e: e.id == selected_id, entities))[0]
    entity.delete()

    refresh_table(main_window)


def save(main_window):

    if form_is_valid(main_window):

        id_label_text: str = main_window.lblProductRateId.text()
        product_id: int = int(main_window.lblProductId.text())
        rate_type: RateType = filter(lambda rt: rt.name == main_window.cmbProductRate_RateType.currentText(), rate_types)[0]
        rate: float = float(main_window.txtProductRate_Rate.text())

        if len(id_label_text) > 0:
            
            ProductRate(int(id_label_text), product_id, rate_type.id, rate).update()

        else:

            ProductRate(None, product_id, rate_type, rate).insert()

        change_view(main_window.swPages, 2)


def form_is_valid(main_window):

    result = True
    error_string = str()

    entity_id: int = 0
    id_label_text = main_window.lblProductId.text()
    product_id: int = int(main_window.lblProductId.text())
    rate_type: RateType = filter(lambda rt: rt.name == main_window.cmbProductRate_RateType.currentText(), rate_types)[0]
    rate_text: str = main_window.txtProductRate_Rate.text()

    if len(id_label_text) > 0:
        entity_id = int(id_label_text)

    if len(rate_text) == 0:
        result = False
        error_string += '\n- Rate field cannot be blank.'
    else:
        
        if not rate_text.isnumeric():
            result = False
            error_string += '\n- Rate must be numeric.'
        elif float(rate_text) < 0:
            result = False
            error_string += '\n- Rate must be greater-than or equal-to zero.'
        else:
            existing_product_rates = list(
                filter(
                    lambda \
                        pr: pr.product_id == product_id and \
                        pr.rate_type_id == rate_type.id and \
                        pr.id != entity_id, 
                    entities))

            if len(existing_product_rates) > 0:
                result = False
                error_string += '\n- Product Rate with current Product and Rate Type already exists.'

    if result == False:
        messagebox.showerror('Save Error', error_string)

    return result


def connect(main_window):

    main_window.tblProductRates.selectionModel().selectionChanged.connect(lambda: on_row_select(main_window))
    main_window.btnNewProductRate.clicked.connect(lambda: new(main_window))
    main_window.btnEditProductRate.clicked.connect(lambda: edit(main_window))
    main_window.btnDeleteProductRate.clicked.connect(lambda: delete(main_window))
    main_window.btnSaveProductRate.clicked.connect(lambda: save(main_window))