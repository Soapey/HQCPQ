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
    kilometres int NOT NULL,
    completed bit NOT NULL
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

INSERT INTO vehicle_combination (name, net, charge_type) VALUES ('Truck & Trailer', 32.5, 'Truck & Trailer');
INSERT INTO vehicle_combination (name, net, charge_type) VALUES ('Rigid', 12.5, 'Rigid');
INSERT INTO rate_type (name) VALUES ('COD');
INSERT INTO product (name) VALUES ('CMS');
INSERT INTO product_rate (product_id, rate_type_id, rate) VALUES (1, 1, 14.0);