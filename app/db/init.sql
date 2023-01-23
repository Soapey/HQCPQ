CREATE TABLE IF NOT EXISTS product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS rate_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS product_rate (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    rate_type_id INTEGER NOT NULL,
    rate REAL NOT NULL,
    FOREIGN KEY (product_id) REFERENCES product (id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (rate_type_id) REFERENCES rate_type (id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS vehicle_combination (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    net REAL NOT NULL,
    charge_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS quote (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_created TEXT NOT NULL,
    date_required TEXT NOT NULL,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    suburb TEXT NOT NULL,
    contact_number TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS quote_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quote_id INTEGER NOT NULL,
    vehicle_combination_name TEXT NOT NULL,
    vehicle_combination_net REAL NOT NULL,
    transport_rate_ex_gst REAL NOT NULL,
    product_name TEXT NOT NULL,
    product_rate_ex_gst REAL NOT NULL,
    FOREIGN KEY (quote_id) REFERENCES quote (id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

PRAGMA foreign_keys=on;