-- Crea la base de datos y la tabla de pasajeros en MySQL (correr en MySQL Workbench).
-- Es la misma tabla que crea 02_repositorio_pasajeros.py con crear_tablas().

CREATE DATABASE IF NOT EXISTS reservas_hyd
  CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci;

USE reservas_hyd;

CREATE TABLE IF NOT EXISTS pasajeros (
  documento VARCHAR(20) NOT NULL,
  nombre    VARCHAR(80) NOT NULL,
  edad      INT         NOT NULL,
  genero    VARCHAR(10) NOT NULL,
  PRIMARY KEY (documento),
  CONSTRAINT ck_edad CHECK (edad BETWEEN 0 AND 120)
);

-- Datos de prueba (nombres ficticios)
INSERT IGNORE INTO pasajeros VALUES
  ('900001', 'Ana Ruiz', 34, 'Femenino'),
  ('900002', 'Luis Mora', 41, 'Masculino');

SELECT * FROM pasajeros;
