-- =====================================================================
-- Hoteles y Destinos S.A.S. | Proyecto SENA ADSO, ficha 3134707
-- 01_esquema.sql: tablas del cotizador (hoteles + actividades)
--
-- Se corre una sola vez con root (o cada vez que quiera empezar de cero).
-- Después se corre 02_datos_prueba.sql para tener hoteles y actividades.
-- =====================================================================

SET NAMES utf8mb4;

CREATE DATABASE IF NOT EXISTS reservas_hyd
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_spanish_ci;

USE reservas_hyd;

-- Destinos ------------------------------------------------------------
-- El código es de 3 letras, como los de los aeropuertos (CTG, SMR...).
-- exento_iva: San Andrés, Panamá y Punta Cana no cobran IVA colombiano.
-- tasa_por_persona: cobros fijos del destino (por ejemplo la tarjeta de
-- turismo de San Andrés). Los valores de prueba hay que confirmarlos.
CREATE TABLE IF NOT EXISTS destinos (
    codigo           CHAR(3)       NOT NULL,
    nombre           VARCHAR(60)   NOT NULL,
    exento_iva       BOOLEAN       NOT NULL DEFAULT FALSE,
    tasa_por_persona DECIMAL(12,0) NOT NULL DEFAULT 0,
    PRIMARY KEY (codigo)
);

-- Hoteles -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS hoteles (
    id_hotel       INT UNSIGNED NOT NULL AUTO_INCREMENT,
    nombre         VARCHAR(80)  NOT NULL,
    destino_codigo CHAR(3)      NOT NULL,
    estrellas      TINYINT      NOT NULL,
    activo         BOOLEAN      NOT NULL DEFAULT TRUE,
    PRIMARY KEY (id_hotel),
    CONSTRAINT fk_hoteles_destino FOREIGN KEY (destino_codigo)
        REFERENCES destinos (codigo),
    CONSTRAINT ck_hoteles_estrellas CHECK (estrellas BETWEEN 1 AND 5)
);

-- Tarifas de hotel ----------------------------------------------------
-- Una fila = un tipo de habitación en una temporada (rango de fechas).
-- Los valores son COSTO NETO (lo que nos cobra el hotel por noche).
-- El precio de venta lo calcula el backend sumando nuestro margen.
CREATE TABLE IF NOT EXISTS tarifas_hotel (
    id_tarifa          INT UNSIGNED  NOT NULL AUTO_INCREMENT,
    id_hotel           INT UNSIGNED  NOT NULL,
    tipo_habitacion    VARCHAR(40)   NOT NULL,
    temporada          ENUM('Baja', 'Media', 'Alta') NOT NULL,
    fecha_desde        DATE          NOT NULL,
    fecha_hasta        DATE          NOT NULL,
    costo_adulto_noche DECIMAL(12,0) NOT NULL,
    costo_nino_noche   DECIMAL(12,0) NOT NULL,
    capacidad_maxima   TINYINT       NOT NULL,
    PRIMARY KEY (id_tarifa),
    CONSTRAINT fk_tarifas_hotel FOREIGN KEY (id_hotel)
        REFERENCES hoteles (id_hotel),
    CONSTRAINT ck_tarifas_fechas CHECK (fecha_hasta >= fecha_desde)
);

-- Actividades ---------------------------------------------------------
-- Tours, pasadías, traslados... También en costo neto, por persona.
CREATE TABLE IF NOT EXISTS actividades (
    id_actividad   INT UNSIGNED  NOT NULL AUTO_INCREMENT,
    nombre         VARCHAR(80)   NOT NULL,
    destino_codigo CHAR(3)       NOT NULL,
    descripcion    VARCHAR(255)  NOT NULL DEFAULT '',
    costo_adulto   DECIMAL(12,0) NOT NULL,
    costo_nino     DECIMAL(12,0) NOT NULL,
    activo         BOOLEAN       NOT NULL DEFAULT TRUE,
    PRIMARY KEY (id_actividad),
    CONSTRAINT fk_actividades_destino FOREIGN KEY (destino_codigo)
        REFERENCES destinos (codigo)
);

-- Cotizaciones --------------------------------------------------------
-- Los valores se guardan "congelados": si mañana sube la tarifa, la
-- cotización que ya se le mandó al cliente no cambia.
CREATE TABLE IF NOT EXISTS cotizaciones (
    id_cotizacion       INT UNSIGNED  NOT NULL AUTO_INCREMENT,
    codigo              VARCHAR(12)   NULL,
    cliente_nombre      VARCHAR(100)  NOT NULL,
    cliente_correo      VARCHAR(100)  NOT NULL,
    destino_codigo      CHAR(3)       NOT NULL,
    fecha_entrada       DATE          NOT NULL,
    fecha_salida        DATE          NOT NULL,
    noches              TINYINT       NOT NULL,
    adultos             TINYINT       NOT NULL,
    ninos               TINYINT       NOT NULL DEFAULT 0,
    id_tarifa           INT UNSIGNED  NOT NULL,
    precio_hotel        DECIMAL(12,0) NOT NULL,
    precio_actividades  DECIMAL(12,0) NOT NULL,
    subtotal            DECIMAL(12,0) NOT NULL,
    descuento_porcentaje TINYINT      NOT NULL DEFAULT 0,
    descuento           DECIMAL(12,0) NOT NULL,
    iva_porcentaje      TINYINT       NOT NULL,
    iva                 DECIMAL(12,0) NOT NULL,
    tasas               DECIMAL(12,0) NOT NULL,
    total               DECIMAL(12,0) NOT NULL,
    estado              ENUM('ABIERTA', 'ENVIADA', 'APROBADA',
                             'RECHAZADA', 'ANULADA')
                        NOT NULL DEFAULT 'ABIERTA',
    fecha_creacion      TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion  TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP
                                      ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id_cotizacion),
    CONSTRAINT uq_cotizaciones_codigo UNIQUE (codigo),
    CONSTRAINT fk_cotizaciones_destino FOREIGN KEY (destino_codigo)
        REFERENCES destinos (codigo),
    CONSTRAINT fk_cotizaciones_tarifa FOREIGN KEY (id_tarifa)
        REFERENCES tarifas_hotel (id_tarifa)
);

-- Actividades de cada cotización (una cotización puede tener varias) --
CREATE TABLE IF NOT EXISTS cotizacion_actividades (
    id_linea       INT UNSIGNED  NOT NULL AUTO_INCREMENT,
    id_cotizacion  INT UNSIGNED  NOT NULL,
    id_actividad   INT UNSIGNED  NOT NULL,
    adultos        TINYINT       NOT NULL,
    ninos          TINYINT       NOT NULL DEFAULT 0,
    precio         DECIMAL(12,0) NOT NULL,
    PRIMARY KEY (id_linea),
    -- Si se borra la cotización, se borran sus actividades con ella.
    CONSTRAINT fk_lineas_cotizacion FOREIGN KEY (id_cotizacion)
        REFERENCES cotizaciones (id_cotizacion) ON DELETE CASCADE,
    CONSTRAINT fk_lineas_actividad FOREIGN KEY (id_actividad)
        REFERENCES actividades (id_actividad)
);

-- Usuario de la app ---------------------------------------------------
-- El mismo usuario del módulo de pasajeros. Si ya existe, no pasa nada.
-- La clave real va SOLO en el archivo .env, nunca en GitHub.
CREATE USER IF NOT EXISTS 'hyd_app'@'localhost'
    IDENTIFIED BY 'Cambia_Esta_Clave_123';
GRANT SELECT, INSERT, UPDATE, DELETE
    ON reservas_hyd.* TO 'hyd_app'@'localhost';
FLUSH PRIVILEGES;
