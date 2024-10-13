CREATE DATABASE IF NOT EXISTS usuarios_db;

USE usuarios_db;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
    contraseña_hash CHAR(64) NOT NULL
);
