-- =====================================================================
-- Proyecto: Hoteles y Destinos S.A.S. (HyD) - SENA ADSO Ficha 3134707
-- Evidencia: GA7-220501096-AA3-EV01 - Módulo de Pasajeros
-- Archivo : crear_bd_hyd.sql
-- Propósito: crear la base de datos, la tabla "pasajeros" y el usuario
--            que usa la aplicación. Se ejecuta UNA sola vez en
--            MySQL Workbench (o en la consola de MySQL) con un usuario
--            administrador, por ejemplo root.
-- =====================================================================

-- Fuerza a que el script se lea en utf8mb4. Sin esto, algunas consolas
-- guardan "Panamá" como "PanamÃ¡" (caracteres dañados).
SET NAMES utf8mb4;

-- 1. Base de datos ----------------------------------------------------
-- utf8mb4 guarda tildes, la ñ y cualquier carácter especial.
-- utf8mb4_spanish_ci ordena y compara "a la colombiana" e ignora
-- mayúsculas/minúsculas (ci = case insensitive).
CREATE DATABASE IF NOT EXISTS reservas_hyd
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_spanish_ci;

-- Le decimos a MySQL que lo que sigue se hace dentro de reservas_hyd.
USE reservas_hyd;

-- 2. Tabla pasajeros --------------------------------------------------
CREATE TABLE IF NOT EXISTS pasajeros (
    -- Llave primaria técnica: un número que MySQL asigna solo (1, 2, 3...).
    id_pasajero       INT UNSIGNED  NOT NULL AUTO_INCREMENT,
    -- Datos personales. NOT NULL = el campo es obligatorio.
    nombre            VARCHAR(50)   NOT NULL,
    apellido          VARCHAR(50)   NOT NULL,
    -- ENUM limita los valores posibles: Cédula de ciudadanía,
    -- Cédula de extranjería, Tarjeta de identidad y Pasaporte.
    tipo_documento    ENUM('CC', 'CE', 'TI', 'PA') NOT NULL,
    numero_documento  VARCHAR(12)   NOT NULL,
    fecha_nacimiento  DATE          NOT NULL,
    pais              VARCHAR(50)   NOT NULL DEFAULT 'Colombia',
    celular           VARCHAR(15)   NOT NULL,
    correo            VARCHAR(100)  NOT NULL,
    -- Auditoría mínima: cuándo se creó y cuándo se modificó la fila.
    fecha_creacion    TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
                                    ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id_pasajero),
    -- Regla de negocio: no pueden existir dos pasajeros con el mismo
    -- número de documento. MySQL lo impide aunque la app falle.
    CONSTRAINT uq_pasajeros_documento UNIQUE (numero_documento)
);

-- 3. Usuario de la aplicación -----------------------------------------
-- Buena práctica: la app NO se conecta como root. Se crea un usuario
-- que solo tiene permisos sobre esta base de datos (mínimo privilegio).
-- CAMBIA la clave y escribe la misma en tu archivo .env (nunca en el
-- código ni en GitHub).
-- OJO: si el usuario ya existía, IF NOT EXISTS NO le cambia la clave.
-- Para cambiarla: ALTER USER 'hyd_app'@'localhost' IDENTIFIED BY '...';
CREATE USER IF NOT EXISTS 'hyd_app'@'localhost'
    IDENTIFIED BY 'Cambia_Esta_Clave_123';
GRANT SELECT, INSERT, UPDATE, DELETE
    ON reservas_hyd.* TO 'hyd_app'@'localhost';
FLUSH PRIVILEGES;

-- 4. Datos de prueba (personas ficticias) -----------------------------
-- INSERT IGNORE no falla si el documento ya existe (por la UNIQUE),
-- así el script se puede correr varias veces sin errores.
INSERT IGNORE INTO pasajeros
    (nombre, apellido, tipo_documento, numero_documento,
     fecha_nacimiento, pais, celular, correo)
VALUES
    ('Ana', 'Ruiz', 'CC', '1020304050', '1990-04-15', 'Colombia',
     '3001112233', 'ana.ruiz@ejemplo.com'),
    ('Luis', 'Mora', 'PA', 'AB123456', '1985-11-02', 'Panamá',
     '5076001122', 'luis.mora@ejemplo.com');

-- 5. Comprobación -----------------------------------------------------
SELECT * FROM pasajeros;
