CREATE TABLE verification(
	id integer,
    unit_sales real
);

CREATE TABLE prediction(
	rowNumber integer,
    id integer,
    prediction_sales real
);

COPY verification(id, unit_sales)
FROM 'E:\KaggleComp\GrocerySalesForeCasting\data\values.csv' DELIMITER ',' CSV HEADER;

COPY prediction(rowNumber, id, prediction_sales)
FROM 'E:\KaggleComp\GrocerySalesForeCasting\data\prediction1.csv' DELIMITER ',' CSV HEADER;