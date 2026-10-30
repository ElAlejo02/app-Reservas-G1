-- =====================================================================
-- 03_usuarios.sql: usuarios del sistema y quién hizo cada cotización.
--
-- Se corre UNA vez, con root, después de 01 y 02.
-- Si sale "Duplicate column name 'id_usuario'", es que ya se había
-- corrido: no pasa nada.
--
-- El primer administrador se crea desde la terminal, no acá:
--     python -m app.crear_admin
-- (así su clave nunca queda escrita en un archivo).
-- =====================================================================

SET NAMES utf8mb4;
USE reservas_hyd;

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario     INT UNSIGNED  NOT NULL AUTO_INCREMENT,
    nombre         VARCHAR(80)   NOT NULL,
    correo         VARCHAR(100)  NOT NULL,
    -- Nunca la clave: solo su huella bcrypt (unos 60 caracteres).
    clave_hash     VARCHAR(100)  NOT NULL,
    rol            ENUM('ADMIN', 'ASESOR', 'OPERACION')
                   NOT NULL DEFAULT 'ASESOR',
    activo         BOOLEAN       NOT NULL DEFAULT TRUE,
    fecha_creacion TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_usuario),
    CONSTRAINT uq_usuarios_correo UNIQUE (correo)
);

-- Cada cotización guarda qué usuario la creó.
ALTER TABLE cotizaciones
    ADD COLUMN id_usuario INT UNSIGNED NULL AFTER id_tarifa,
    ADD CONSTRAINT fk_cotizaciones_usuario FOREIGN KEY (id_usuario)
        REFERENCES usuarios (id_usuario);

SELECT 'Listo: tabla usuarios creada' AS resultado;
