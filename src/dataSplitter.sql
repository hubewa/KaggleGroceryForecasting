-- This file does all the Data manipulations on an SQL server.
-- To use it on your own computer, change "E:\data\CorporaciónGrocerySalesForecasting" to your filesystem as needed

--Create the various tables supplied by Kaggle

--Primary Tables
CREATE TABLE shopping(  --Training set
	id integer,
    date date,
    store_nbr integer,
    item_nbr integer,
    unit_sales real,
    onpromotion boolean,
    CONSTRAINT shopping_pkey PRIMARY KEY (id)
);

CREATE TABLE test( --Test Set
    id integer,
    date date,
    store_nbr integer,
    item_nbr integer,
    onpromotion boolean,
    CONSTRAINT test_pkey PRIMARY KEY (id)
);


--Secondary Tables

CREATE TABLE items( --Items Table
    item_nbr integer,
    family character(50),
    class integer,
    perishable boolean,
    CONSTRAINT items_pkey PRIMARY KEY (item_nbr)
);

CREATE TABLE oil( --Oil Table
    date date,
    dcoilwtico real,
    CONSTRAINT oil_pkey PRIMARY KEY (date)
);


CREATE TABLE stores( --Stores Table
    store_nbr integer,
    city character(50),
    state character(50),
    type character(1),
    cluster integer,
    CONSTRAINT store_pkey PRIMARY KEY (store_nbr)
);

CREATE TABLE holidays( --Holiday Table
    date date,
    type character(50),
    locale character(50),
    locale_name character(50),
    description character(100),
    transferred character(5)
);




--Import the tables from files. Change this based on where you've put the 
COPY shopping(id, date, store_nbr, item_nbr, unit_sales, onpromotion)
FROM 'E:\data\GrocerySalesForecasting\Original\train.csv' DELIMITER ',' CSV HEADER;

COPY test(id, date, store_nbr, item_nbr, onpromotion)
FROM 'E:\data\GrocerySalesForecasting\Original\test.csv' DELIMITER ',' CSV HEADER;

COPY items(item_nbr, family, class, perishable)
FROM 'E:\data\GrocerySalesForecasting\Original\items.csv' DELIMITER ',' CSV HEADER;

COPY oil(date, dcoilwtico)
FROM 'E:\data\GrocerySalesForecasting\Original\oil.csv' DELIMITER ',' CSV HEADER;

COPY stores(store_nbr, city, state, type, cluster)
FROM 'E:\data\GrocerySalesForecasting\Original\stores.csv' DELIMITER ',' CSV HEADER;

COPY holidays(date, type, locale, locale_name, description, transferred)
FROM 'E:\data\GrocerySalesForecasting\Original\holidays_events.csv' DELIMITER ',' CSV HEADER;




--This is just test code to check whether this works before we export it to a different file
SELECT id, shopping.item_nbr, shopping.date, shopping.store_nbr, unit_sales, onpromotion, family, class, perishable, dcoilwtico, city, state, type, cluster FROM shopping
LEFT JOIN items ON shopping.item_nbr = items.item_nbr
LEFT JOIN oil ON shopping.date = oil.date
LEFT JOIN stores ON shopping.store_nbr = stores.store_nbr
WHERE shopping.date > '20170801';

--Export. Chane file location as needed
COPY (SELECT * FROM shopping WHERE date >= '20160815') TO 'E:\KaggleComp\GrocerySalesForeCasting\082016.csv' DELIMITER ',' CSV HEADER;

COPY (SELECT id, shopping.item_nbr, shopping.date, shopping.store_nbr, unit_sales, onpromotion, family, class, perishable, dcoilwtico, city, state, type, cluster FROM shopping
LEFT JOIN items ON shopping.item_nbr = items.item_nbr
LEFT JOIN oil ON shopping.date = oil.date
LEFT JOIN stores ON shopping.store_nbr = stores.store_nbr) TO 'E:\data\CorporaciónGrocerySalesForecasting\processed\fullitemsTrain.csv' DELIMITER ',' CSV HEADER;


COPY (SELECT id, shopping.item_nbr, date, store_nbr, unit_sales, onpromotion, family, class, perishable FROM shopping
LEFT JOIN items ON shopping.item_nbr = items.item_nbr
WHERE date > '20160815') TO 'E:\data\CorporaciónGrocerySalesForecasting\itemsTrain.csv' DELIMITER ',' CSV HEADER;

COPY (SELECT id, test.item_nbr, date, store_nbr, onpromotion, family, class, perishable FROM test
LEFT JOIN items ON test.item_nbr = items.item_nbr) TO 'E:\data\CorporaciónGrocerySalesForecasting\itemsTest.csv' DELIMITER ',' CSV HEADER;

