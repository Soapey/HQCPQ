CREATE TABLE product (
    id int IDENTITY(1,1) PRIMARY KEY,
    name varchar(100) UNIQUE NOT NULL
);

CREATE TABLE rate_type (
    id int IDENTITY(1,1) PRIMARY KEY,
    name varchar(100) UNIQUE NOT NULL
);

CREATE TABLE product_rate (
    id int IDENTITY(1,1) PRIMARY KEY,
    product_id int NOT NULL,
    rate_type_id int NOT NULL,
    rate FLOAT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES product (id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (rate_type_id) REFERENCES rate_type (id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE vehicle_combination (
    id int IDENTITY(1,1) PRIMARY KEY,
    name varchar(100) UNIQUE NOT NULL,
    net FLOAT NOT NULL,
    charge_type nvarchar(100) NOT NULL
);

CREATE TABLE quote (
    id int IDENTITY(1,1) PRIMARY KEY,
    date_created varchar(100) NOT NULL,
    date_required varchar(100) NOT NULL,
    name varchar(100) NOT NULL,
    address varchar(100) NOT NULL,
    suburb varchar(100) NOT NULL,
    contact_number varchar(100),
    kilometres int NOT NULL
);

CREATE TABLE quote_item (
    id int IDENTITY(1,1) PRIMARY KEY,
    quote_id int NOT NULL,
    vehicle_combination_name varchar(100) NOT NULL,
    vehicle_combination_net FLOAT NOT NULL,
    transport_rate_ex_gst FLOAT NOT NULL,
    product_name varchar(100) NOT NULL,
    product_rate_ex_gst FLOAT NOT NULL,
    charge_type_name varchar(100) NOT NULL,
    FOREIGN KEY (quote_id) REFERENCES quote (id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);