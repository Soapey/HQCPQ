from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QComboBox
from app.classes.ProductRate import ProductRate
from app.classes.RateType import RateType
from app.db.SQLCursor import SQLCursor
from tkinter import messagebox
from app.gui.helpers import selected_row_id, change_view, toggle_buttons, int_conv, float_conv


entities: list[ProductRate] = list()
rate_types: list[RateType] = list()
records = list()


def on_row_select(main_window):

    tbl: QTableWidget = main_window.tblProductRates

    selected_id = selected_row_id(tbl)

    if selected_id:
        toggle_buttons(main_window.btnNewProductRate, True, main_window.btnEditProductRate, True, main_window.btnDeleteProductRate, True)
    else:
        toggle_buttons(main_window.btnNewProductRate, True, main_window.btnEditProductRate, False, main_window.btnDeleteProductRate, False)


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

    toggle_buttons(main_window.btnNewProductRate, True, main_window.btnEditProductRate, False, main_window.btnDeleteProductRate, False)


def load_entry_page(main_window, is_new: bool):

    # Fetch all RateTypes from SQLite database.
    global rate_types
    rate_types = RateType.get()

    # Create list of RateType name options for the gui combobox.
    selectable_rate_type_names: list[str] = list()
    if is_new:
        existing_ratetype_names = [r[1] for r in records]
        selectable_rate_type_names = [rt.name for rt in rate_types if rt.name not in existing_ratetype_names]
    else:
        selectable_rate_type_names = [rt.name for rt in rate_types]

    # Clear the gui combobox and fill with RateType name options.
    productrate_ratetype_combobox: QComboBox = main_window.cmbProductRate_RateType
    productrate_ratetype_combobox.clear()
    for rate_type_name in selectable_rate_type_names:
        productrate_ratetype_combobox.addItem(rate_type_name)

    # Clear the Rate field textbox and add a numeric only validator.
    main_window.txtProductRate_Rate.clear()


def new(main_window):

    load_entry_page(main_window, is_new = True)

    change_view(main_window.swPages, 3)


def edit(main_window):

    # Find the entity to be edited by id
    selected_id = selected_row_id(main_window.tblProductRates)
    entity = list(filter(lambda r: r[0] == selected_id, records))[0]

    load_entry_page(main_window, is_new = False)

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

        id = int_conv(main_window.lblProductRateId.text())
        product_id: int = int(main_window.lblProductId.text())
        rate_type_id: int = list(filter(lambda rt: rt.name == main_window.cmbProductRate_RateType.currentText(), rate_types))[0].id
        rate: float = float(main_window.txtProductRate_Rate.text())

        pr = ProductRate(id, product_id, rate_type_id, rate)

        if id:
            pr.update()
        else:
            pr.insert()

        refresh_table(main_window, product_id)

        change_view(main_window.swPages, 2)


def form_is_valid(main_window):

    result = True
    error_string = str()

    id: int = int_conv(main_window.lblProductRateId.text())
    rate =  float_conv(main_window.txtProductRate_Rate.text())

    if rate:
        result = False
        error_string += '\n- Rate field cannot be blank.'

    else:
        product_id: int = int(main_window.lblProductId.text())
        rate_type_id: RateType = list(filter(lambda rt: rt.name == main_window.cmbProductRate_RateType.currentText(), rate_types))[0].id
       
        existing_product_rates = list(
            filter(
                lambda \
                    pr: pr.product_id == product_id and \
                    pr.rate_type_id == rate_type_id and \
                    pr.id != id, 
                entities))

        if len(existing_product_rates) > 0:
            result = False
            error_string += '\n- Product Rate with current Product and Rate Type already exists.'

    if result == False:
        messagebox.showerror('Save Error', error_string)

    return result


def connect(main_window):

    # Connect all actions to lambda functions.
    main_window.tblProductRates.selectionModel().selectionChanged.connect(lambda: on_row_select(main_window))
    main_window.btnNewProductRate.clicked.connect(lambda: new(main_window))
    main_window.btnEditProductRate.clicked.connect(lambda: edit(main_window))
    main_window.btnDeleteProductRate.clicked.connect(lambda: delete(main_window))
    main_window.btnSaveProductRate.clicked.connect(lambda: save(main_window))

    # Set numeric only validator on Rate textbox.
    onlyNumeric = QDoubleValidator()
    onlyNumeric.setBottom(0.00)
    main_window.txtProductRate_Rate.setValidator(onlyNumeric)