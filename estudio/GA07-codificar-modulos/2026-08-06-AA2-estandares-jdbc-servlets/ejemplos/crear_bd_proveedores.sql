-- Script de la base de datos para la GA7-AA2-EV01.
-- El instructor pidió incluirlo en el ZIP para poder montarlo en Workbench y probar el proyecto.

CREATE DATABASE IF NOT EXISTS reservas_hyd CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci;
USE reservas_hyd;

CREATE TABLE IF NOT EXISTS proveedor (
  id_proveedor INT         NOT NULL PRIMARY KEY,
  nit          VARCHAR(20) NOT NULL UNIQUE,
  nombre       VARCHAR(80) NOT NULL
);

INSERT IGNORE INTO proveedor VALUES
  (1, '900111222', 'Hoteles Andinos'),
  (2, '900333444', 'Transportes del Caribe'),
  (3, '900555666', 'Tours Coral');

SELECT * FROM proveedor;
