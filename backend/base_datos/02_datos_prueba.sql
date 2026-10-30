-- =====================================================================
-- 02_datos_prueba.sql: datos inventados para probar el cotizador.
-- Los hoteles y precios NO son reales. Las tasas por destino son de
-- ejemplo y hay que confirmarlas con operaciones antes de usarlas.
-- Se puede correr varias veces: primero limpia y luego vuelve a llenar.
-- =====================================================================

SET NAMES utf8mb4;
USE reservas_hyd;

-- Limpio en orden inverso por las llaves foráneas.
DELETE FROM cotizacion_actividades;
DELETE FROM cotizaciones;
DELETE FROM actividades;
DELETE FROM tarifas_hotel;
DELETE FROM hoteles;
DELETE FROM destinos;
ALTER TABLE cotizaciones AUTO_INCREMENT = 1;
ALTER TABLE actividades AUTO_INCREMENT = 1;
ALTER TABLE tarifas_hotel AUTO_INCREMENT = 1;
ALTER TABLE hoteles AUTO_INCREMENT = 1;

INSERT INTO destinos (codigo, nombre, exento_iva, tasa_por_persona) VALUES
    ('CTG', 'Cartagena', 0, 0),
    ('SMR', 'Santa Marta', 0, 0),
    ('ADZ', 'San Andrés', 1, 150000),
    ('RCH', 'La Guajira', 0, 0),
    ('CVE', 'Coveñas', 0, 0),
    ('NQU', 'Nuquí', 0, 0),
    ('PTY', 'Panamá', 1, 0),
    ('PUJ', 'Punta Cana', 1, 0);

INSERT INTO hoteles (nombre, destino_codigo, estrellas) VALUES
    ('Hotel Brisas de Bocagrande', 'CTG', 4),
    ('Hotel Murallas Coloniales', 'CTG', 5),
    ('Hotel Bahía Rodadero', 'SMR', 3),
    ('Hotel Sierra y Mar', 'SMR', 4),
    ('Posada Coral Azul', 'ADZ', 3),
    ('Hotel Mar de Siete Colores', 'ADZ', 4),
    ('Ecohotel Cabo de la Vela', 'RCH', 3),
    ('Hotel Golfo de Morrosquillo', 'CVE', 3),
    ('Ecolodge Selva y Ballenas', 'NQU', 3),
    ('Hotel Canal y Ciudad', 'PTY', 4),
    ('Resort Arena Blanca', 'PUJ', 5);

-- Cada hotel tiene 2 tipos de habitación en 5 temporadas.
INSERT INTO tarifas_hotel (id_hotel, tipo_habitacion, temporada, fecha_desde,
    fecha_hasta, costo_adulto_noche, costo_nino_noche, capacidad_maxima) VALUES
    (1, 'Estándar', 'Baja', '2026-11-01', '2026-12-14', 210000, 105000, 3),
    (1, 'Estándar', 'Alta', '2026-12-15', '2027-01-15', 294000, 147000, 3),
    (1, 'Estándar', 'Baja', '2027-01-16', '2027-06-14', 210000, 105000, 3),
    (1, 'Estándar', 'Alta', '2027-06-15', '2027-07-31', 273000, 136000, 3),
    (1, 'Estándar', 'Media', '2027-08-01', '2027-12-14', 241000, 120000, 3),
    (1, 'Familiar', 'Baja', '2026-11-01', '2026-12-14', 252000, 126000, 5),
    (1, 'Familiar', 'Alta', '2026-12-15', '2027-01-15', 353000, 176000, 5),
    (1, 'Familiar', 'Baja', '2027-01-16', '2027-06-14', 252000, 126000, 5),
    (1, 'Familiar', 'Alta', '2027-06-15', '2027-07-31', 328000, 164000, 5),
    (1, 'Familiar', 'Media', '2027-08-01', '2027-12-14', 290000, 145000, 5),
    (2, 'Estándar', 'Baja', '2026-11-01', '2026-12-14', 380000, 190000, 3),
    (2, 'Estándar', 'Alta', '2026-12-15', '2027-01-15', 532000, 266000, 3),
    (2, 'Estándar', 'Baja', '2027-01-16', '2027-06-14', 380000, 190000, 3),
    (2, 'Estándar', 'Alta', '2027-06-15', '2027-07-31', 494000, 247000, 3),
    (2, 'Estándar', 'Media', '2027-08-01', '2027-12-14', 437000, 218000, 3),
    (2, 'Familiar', 'Baja', '2026-11-01', '2026-12-14', 456000, 228000, 5),
    (2, 'Familiar', 'Alta', '2026-12-15', '2027-01-15', 638000, 319000, 5),
    (2, 'Familiar', 'Baja', '2027-01-16', '2027-06-14', 456000, 228000, 5),
    (2, 'Familiar', 'Alta', '2027-06-15', '2027-07-31', 593000, 296000, 5),
    (2, 'Familiar', 'Media', '2027-08-01', '2027-12-14', 524000, 262000, 5),
    (3, 'Estándar', 'Baja', '2026-11-01', '2026-12-14', 150000, 75000, 3),
    (3, 'Estándar', 'Alta', '2026-12-15', '2027-01-15', 210000, 105000, 3),
    (3, 'Estándar', 'Baja', '2027-01-16', '2027-06-14', 150000, 75000, 3),
    (3, 'Estándar', 'Alta', '2027-06-15', '2027-07-31', 195000, 98000, 3),
    (3, 'Estándar', 'Media', '2027-08-01', '2027-12-14', 172000, 86000, 3),
    (3, 'Familiar', 'Baja', '2026-11-01', '2026-12-14', 180000, 90000, 5),
    (3, 'Familiar', 'Alta', '2026-12-15', '2027-01-15', 252000, 126000, 5),
    (3, 'Familiar', 'Baja', '2027-01-16', '2027-06-14', 180000, 90000, 5),
    (3, 'Familiar', 'Alta', '2027-06-15', '2027-07-31', 234000, 117000, 5),
    (3, 'Familiar', 'Media', '2027-08-01', '2027-12-14', 207000, 104000, 5),
    (4, 'Estándar', 'Baja', '2026-11-01', '2026-12-14', 230000, 115000, 3),
    (4, 'Estándar', 'Alta', '2026-12-15', '2027-01-15', 322000, 161000, 3),
    (4, 'Estándar', 'Baja', '2027-01-16', '2027-06-14', 230000, 115000, 3),
    (4, 'Estándar', 'Alta', '2027-06-15', '2027-07-31', 299000, 150000, 3),
    (4, 'Estándar', 'Media', '2027-08-01', '2027-12-14', 264000, 132000, 3),
    (4, 'Familiar', 'Baja', '2026-11-01', '2026-12-14', 276000, 138000, 5),
    (4, 'Familiar', 'Alta', '2026-12-15', '2027-01-15', 386000, 193000, 5),
    (4, 'Familiar', 'Baja', '2027-01-16', '2027-06-14', 276000, 138000, 5),
    (4, 'Familiar', 'Alta', '2027-06-15', '2027-07-31', 359000, 180000, 5),
    (4, 'Familiar', 'Media', '2027-08-01', '2027-12-14', 317000, 158000, 5),
    (5, 'Estándar', 'Baja', '2026-11-01', '2026-12-14', 170000, 85000, 3),
    (5, 'Estándar', 'Alta', '2026-12-15', '2027-01-15', 238000, 119000, 3),
    (5, 'Estándar', 'Baja', '2027-01-16', '2027-06-14', 170000, 85000, 3),
    (5, 'Estándar', 'Alta', '2027-06-15', '2027-07-31', 221000, 110000, 3),
    (5, 'Estándar', 'Media', '2027-08-01', '2027-12-14', 195000, 98000, 3),
    (5, 'Familiar', 'Baja', '2026-11-01', '2026-12-14', 204000, 102000, 5),
    (5, 'Familiar', 'Alta', '2026-12-15', '2027-01-15', 286000, 143000, 5),
    (5, 'Familiar', 'Baja', '2027-01-16', '2027-06-14', 204000, 102000, 5),
    (5, 'Familiar', 'Alta', '2027-06-15', '2027-07-31', 265000, 132000, 5),
    (5, 'Familiar', 'Media', '2027-08-01', '2027-12-14', 235000, 118000, 5),
    (6, 'Estándar', 'Baja', '2026-11-01', '2026-12-14', 260000, 130000, 3),
    (6, 'Estándar', 'Alta', '2026-12-15', '2027-01-15', 364000, 182000, 3),
    (6, 'Estándar', 'Baja', '2027-01-16', '2027-06-14', 260000, 130000, 3),
    (6, 'Estándar', 'Alta', '2027-06-15', '2027-07-31', 338000, 169000, 3),
    (6, 'Estándar', 'Media', '2027-08-01', '2027-12-14', 299000, 150000, 3),
    (6, 'Familiar', 'Baja', '2026-11-01', '2026-12-14', 312000, 156000, 5),
    (6, 'Familiar', 'Alta', '2026-12-15', '2027-01-15', 437000, 218000, 5),
    (6, 'Familiar', 'Baja', '2027-01-16', '2027-06-14', 312000, 156000, 5),
    (6, 'Familiar', 'Alta', '2027-06-15', '2027-07-31', 406000, 203000, 5),
    (6, 'Familiar', 'Media', '2027-08-01', '2027-12-14', 359000, 180000, 5),
    (7, 'Estándar', 'Baja', '2026-11-01', '2026-12-14', 120000, 60000, 3),
    (7, 'Estándar', 'Alta', '2026-12-15', '2027-01-15', 168000, 84000, 3),
    (7, 'Estándar', 'Baja', '2027-01-16', '2027-06-14', 120000, 60000, 3),
    (7, 'Estándar', 'Alta', '2027-06-15', '2027-07-31', 156000, 78000, 3),
    (7, 'Estándar', 'Media', '2027-08-01', '2027-12-14', 138000, 69000, 3),
    (7, 'Familiar', 'Baja', '2026-11-01', '2026-12-14', 144000, 72000, 5),
    (7, 'Familiar', 'Alta', '2026-12-15', '2027-01-15', 202000, 101000, 5),
    (7, 'Familiar', 'Baja', '2027-01-16', '2027-06-14', 144000, 72000, 5),
    (7, 'Familiar', 'Alta', '2027-06-15', '2027-07-31', 187000, 94000, 5),
    (7, 'Familiar', 'Media', '2027-08-01', '2027-12-14', 166000, 83000, 5),
    (8, 'Estándar', 'Baja', '2026-11-01', '2026-12-14', 130000, 65000, 3),
    (8, 'Estándar', 'Alta', '2026-12-15', '2027-01-15', 182000, 91000, 3),
    (8, 'Estándar', 'Baja', '2027-01-16', '2027-06-14', 130000, 65000, 3),
    (8, 'Estándar', 'Alta', '2027-06-15', '2027-07-31', 169000, 84000, 3),
    (8, 'Estándar', 'Media', '2027-08-01', '2027-12-14', 150000, 75000, 3),
    (8, 'Familiar', 'Baja', '2026-11-01', '2026-12-14', 156000, 78000, 5),
    (8, 'Familiar', 'Alta', '2026-12-15', '2027-01-15', 218000, 109000, 5),
    (8, 'Familiar', 'Baja', '2027-01-16', '2027-06-14', 156000, 78000, 5),
    (8, 'Familiar', 'Alta', '2027-06-15', '2027-07-31', 203000, 102000, 5),
    (8, 'Familiar', 'Media', '2027-08-01', '2027-12-14', 179000, 90000, 5),
    (9, 'Estándar', 'Baja', '2026-11-01', '2026-12-14', 280000, 140000, 3),
    (9, 'Estándar', 'Alta', '2026-12-15', '2027-01-15', 392000, 196000, 3),
    (9, 'Estándar', 'Baja', '2027-01-16', '2027-06-14', 280000, 140000, 3),
    (9, 'Estándar', 'Alta', '2027-06-15', '2027-07-31', 364000, 182000, 3),
    (9, 'Estándar', 'Media', '2027-08-01', '2027-12-14', 322000, 161000, 3),
    (9, 'Familiar', 'Baja', '2026-11-01', '2026-12-14', 336000, 168000, 5),
    (9, 'Familiar', 'Alta', '2026-12-15', '2027-01-15', 470000, 235000, 5),
    (9, 'Familiar', 'Baja', '2027-01-16', '2027-06-14', 336000, 168000, 5),
    (9, 'Familiar', 'Alta', '2027-06-15', '2027-07-31', 437000, 218000, 5),
    (9, 'Familiar', 'Media', '2027-08-01', '2027-12-14', 386000, 193000, 5),
    (10, 'Estándar', 'Baja', '2026-11-01', '2026-12-14', 300000, 150000, 3),
    (10, 'Estándar', 'Alta', '2026-12-15', '2027-01-15', 420000, 210000, 3),
    (10, 'Estándar', 'Baja', '2027-01-16', '2027-06-14', 300000, 150000, 3),
    (10, 'Estándar', 'Alta', '2027-06-15', '2027-07-31', 390000, 195000, 3),
    (10, 'Estándar', 'Media', '2027-08-01', '2027-12-14', 345000, 172000, 3),
    (10, 'Familiar', 'Baja', '2026-11-01', '2026-12-14', 360000, 180000, 5),
    (10, 'Familiar', 'Alta', '2026-12-15', '2027-01-15', 504000, 252000, 5),
    (10, 'Familiar', 'Baja', '2027-01-16', '2027-06-14', 360000, 180000, 5),
    (10, 'Familiar', 'Alta', '2027-06-15', '2027-07-31', 468000, 234000, 5),
    (10, 'Familiar', 'Media', '2027-08-01', '2027-12-14', 414000, 207000, 5),
    (11, 'Estándar', 'Baja', '2026-11-01', '2026-12-14', 450000, 225000, 3),
    (11, 'Estándar', 'Alta', '2026-12-15', '2027-01-15', 630000, 315000, 3),
    (11, 'Estándar', 'Baja', '2027-01-16', '2027-06-14', 450000, 225000, 3),
    (11, 'Estándar', 'Alta', '2027-06-15', '2027-07-31', 585000, 292000, 3),
    (11, 'Estándar', 'Media', '2027-08-01', '2027-12-14', 517000, 258000, 3),
    (11, 'Familiar', 'Baja', '2026-11-01', '2026-12-14', 540000, 270000, 5),
    (11, 'Familiar', 'Alta', '2026-12-15', '2027-01-15', 756000, 378000, 5),
    (11, 'Familiar', 'Baja', '2027-01-16', '2027-06-14', 540000, 270000, 5),
    (11, 'Familiar', 'Alta', '2027-06-15', '2027-07-31', 702000, 351000, 5),
    (11, 'Familiar', 'Media', '2027-08-01', '2027-12-14', 621000, 310000, 5);

INSERT INTO actividades (nombre, destino_codigo, descripcion, costo_adulto,
    costo_nino) VALUES
    ('Tour Islas del Rosario', 'CTG', 'Pasadía en lancha con almuerzo típico.', 180000, 140000),
    ('City tour Ciudad Amurallada', 'CTG', 'Recorrido guiado de 3 horas por el centro histórico.', 90000, 60000),
    ('Pasadía Parque Tayrona', 'SMR', 'Transporte, guía y entrada al parque.', 210000, 160000),
    ('Tour Minca y cascadas', 'SMR', 'Café, cascada Marinka y miradores.', 150000, 110000),
    ('Vuelta a la isla', 'ADZ', 'Recorrido en chiva por los puntos principales.', 60000, 45000),
    ('Tour Acuario y Johnny Cay', 'ADZ', 'Lancha a los cayos con tiempo libre.', 110000, 90000),
    ('Excursión Cabo de la Vela', 'RCH', 'Salida en 4x4 desde Riohacha con almuerzo.', 320000, 260000),
    ('Paseo Islas de San Bernardo', 'CVE', 'Lancha por el archipiélago con almuerzo.', 170000, 130000),
    ('Avistamiento de ballenas', 'NQU', 'Salida en lancha en temporada de ballenas.', 140000, 110000),
    ('Tour Canal de Panamá', 'PTY', 'Visita a las esclusas de Miraflores.', 160000, 120000),
    ('Isla Saona', 'PUJ', 'Catamarán, almuerzo y playa.', 380000, 290000);

-- Comprobación rápida
SELECT COUNT(*) AS hoteles FROM hoteles;
SELECT COUNT(*) AS tarifas FROM tarifas_hotel;
SELECT COUNT(*) AS actividades FROM actividades;
