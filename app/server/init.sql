-- Create fraud_detection database and its tables
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

-- Create usuarios_db database and its tables
CREATE DATABASE IF NOT EXISTS usuarios_db;
USE usuarios_db;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
    contrasena_hash CHAR(64) NOT NULL
);


-- Create user 'plof' with necessary privileges
CREATE USER IF NOT EXISTS 'plof'@'%' IDENTIFIED BY 'pass';

-- Grant all privileges to 'plof' on both databases
GRANT ALL PRIVILEGES ON fraud_detection.* TO 'plof'@'%';
GRANT ALL PRIVILEGES ON usuarios_db.* TO 'plof'@'%';

-- Apply the changes
FLUSH PRIVILEGES;

