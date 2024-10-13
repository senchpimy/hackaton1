CREATE DATABASE IF NOT EXISTS fraud_detection;

USE fraud_detection;

CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    num_cliente VARCHAR(20),
    num_tarjeta VARCHAR(20),
    fecha DATE,
    establecimiento VARCHAR(255),
    importe DECIMAL(10, 2),
    fraude BOOLEAN
);

