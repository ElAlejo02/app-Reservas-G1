-- Base de datos MySQL para el sistema integrado (correr en MySQL Workbench).
-- La app también crea estas tablas sola al arrancar (create_all), pero la evidencia pide
-- documentar la configuración de la base de datos: este script es esa documentación.

CREATE DATABASE IF NOT EXISTS reservas_hyd CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci;
USE reservas_hyd;

CREATE TABLE IF NOT EXISTS usuarios (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  usuario    VARCHAR(30) NOT NULL UNIQUE,
  clave_hash BLOB        NOT NULL,          -- hash bcrypt, nunca la contraseña
  rol        VARCHAR(15) NOT NULL DEFAULT 'ASESOR'
);

CREATE TABLE IF NOT EXISTS hoteles (
  id           INT AUTO_INCREMENT PRIMARY KEY,  -- autoincremento, como en la clase
  nombre       VARCHAR(80) NOT NULL,
  ciudad       VARCHAR(40) NOT NULL,
  estrellas    INT         NOT NULL CHECK (estrellas BETWEEN 1 AND 5),
  tarifa_noche DOUBLE      NOT NULL CHECK (tarifa_noche > 0)
);
