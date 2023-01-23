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

    if selected_id:
        toggle_buttons(main_window, True, True, True)
    else:
        toggle_buttons(main_window, True, False, False)


def toggle_buttons(main_window, show_new: bool, show_edit: bool, show_delete: bool):

    main_window.btnNewProductRate.setVisible(show_new)
    main_window.btnEditProductRate.setVisible(show_edit)
    main_window.btnDeleteProductRate.setVisible(show_delete)


def refresh_table(main_window, selected_id: int = None):

    product_rates_tbl: QTableWidget = main_window.tblProductRates

    selected_product_id = selected_id or selected_row_id(main_window.tblProducts)

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
            (selected_product_id,)).fetchall()

    headers = ['ID', 'Type', 'Rate']
    product_rates_tbl.setRowCount(len(records))
    product_rates_tbl.setColumnCount(len(headers))
    product_rates_tbl.setHorizontalHeaderLabels(headers)

    for index, record in enumerate(records):
        product_rates_tbl.setItem(index, 0, QTableWidgetItem(str(record[0])))
        product_rates_tbl.setItem(index, 1, QTableWidgetItem(record[1]))
        product_rates_tbl.setItem(index, 2, QTableWidgetItem(str(record[2])))

    on_row_select(main_window)


def clear_entry_fields(main_window, is_new: bool):

    global rate_types
    rate_types = RateType.get()

    selectable_rate_type_names: list

    if is_new:
        selectable_rate_type_names = [rt.name for rt in rate_types if rt.name not in [r[1] for r in records]]
    else:
        selectable_rate_type_names = [rt.name for rt in rate_types]

    productrate_ratetype_combobox: QComboBox = main_window.cmbProductRate_RateType
    productrate_ratetype_combobox.clear()

    for rate_type_name in selectable_rate_type_names:
        productrate_ratetype_combobox.addItem(rate_type_name)

    main_window.txtProductRate_Rate.clear()


def new(main_window):

    clear_entry_fields(main_window, is_new = True)

    change_view(main_window.swPages, 3)


def edit(main_window):

    selected_id = selected_row_id(main_window.tblProductRates)

    entity = list(filter(lambda r: r[0] == selected_id, records))[0]

    clear_entry_fields(main_window, is_new = False)

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
        rate_type: RateType = list(filter(lambda rt: rt.name == main_window.cmbProductRate_RateType.currentText(), rate_types))[0]
        rate: float = float(main_window.txtProductRate_Rate.text())

        pr: ProductRate = None
        if len(id_label_text) > 0:
            pr = ProductRate(int(id_label_text), product_id, rate_type.id, rate)
            pr.update()
        else:
            pr = ProductRate(None, product_id, rate_type.id, rate)
            pr.insert()

        refresh_table(main_window, product_id)

        change_view(main_window.swPages, 2)


def form_is_valid(main_window):

    result = True
    error_string = str()

    entity_id: int = 0
    id_label_text = main_window.lblProductRateId.text()

    product_id: int = int(main_window.lblProductId.text())

    rate_type: RateType = list(filter(lambda rt: rt.name == main_window.cmbProductRate_RateType.currentText(), rate_types))[0]
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