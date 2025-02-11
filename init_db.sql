DROP SCHEMA IF EXISTS raw CASCADE;

CREATE ROLE analytics_engineering_admins;
CREATE SCHEMA IF NOT EXISTS raw AUTHORIZATION analytics_engineering_admins;
SET ROLE analytics_engineering_admins;

CREATE TABLE IF NOT EXISTS raw.contracts (
    id SERIAL PRIMARY KEY,
    type TEXT,
    energy TEXT,
    usage INTEGER,
    usagenet INTEGER,
    createdat DATE,
    startdate DATE,
    enddate DATE NULL,
    fillingdatecancellation DATE NULL,
    cancellationreason TEXT NULL,
    city TEXT,
    status TEXT,
    productid INTEGER,
    modificationdate DATE,
    file_name TEXT,
    ingestion_time TIMESTAMP DEFAULT NOW()  
);

CREATE TABLE IF NOT EXISTS raw.products (
    id SERIAL PRIMARY KEY,
    productcode TEXT,
    productname TEXT,
    energy TEXT,
    consumptiontype TEXT,
    deleted BOOLEAN,
    modificationdate DATE,
    file_name TEXT,
    ingestion_time TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS raw.prices (
    id SERIAL PRIMARY KEY,
    productid INTEGER,
    pricecomponentid INTEGER,
    productcomponent TEXT,
    price NUMERIC,
    unit TEXT,
    valid_from DATE,
    valid_until DATE,
    modificationdate DATE,
    file_name TEXT,
    ingestion_time TIMESTAMP DEFAULT NOW()
);

