CREATE TABLE IF NOT EXISTS product (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    weighbridge_product_id INTEGER NOT NULL,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS rate_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS product_rate (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    weighbridge_product_rate_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    rate REAL NOT NULL,
    product_id INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES product (id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS vehicle_combination (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT UNIQUE NOT NULL,
    net REAL NOT NULL,
    charge_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS quote (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    date_created TEXT NOT NULL,
    date_required TEXT NOT NULL,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    suburb TEXT NOT NULL,
    contact_number TEXT,
    email TEXT,
    memo TEXT,
    kilometres INTEGER NOT NULL,
    completed INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS quote_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    quote_id INTEGER NOT NULL,
    vehicle_combination_name TEXT NOT NULL,
    vehicle_combination_net REAL NOT NULL,
    transport_rate_ex_gst REAL NOT NULL,
    product_name TEXT NOT NULL,
    product_rate_ex_gst REAL NOT NULL,
    charge_type_name TEXT NOT NULL,
    FOREIGN KEY (quote_id) REFERENCES quote (id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);
