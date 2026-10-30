# Módulo de Pasajeros · Hoteles y Destinos S.A.S.

Aplicación de escritorio (stand-alone) con el CRUD de pasajeros del
proyecto formativo **Hoteles y Destinos S.A.S.**, SENA ADSO, ficha 3134707.

Evidencia: **GA7-220501096-AA3-EV01**, codificación de módulos del software.

Equipo: Angel Daniel Burbano Amaya, Laura María Vergara Mesa y David Alejandro Alzate.

## Tecnologías

| Capa | Tecnología | Equivalente en Java |
|---|---|---|
| Lenguaje | Python 3.10+ | Java |
| Interfaz | Tkinter (incluido en Python) | Swing |
| Acceso a datos | PyMySQL | JDBC |
| Base de datos | MySQL 8 | MySQL 8 |
| Pruebas | unittest | JUnit |
| Estándar | PEP 8 revisado con Ruff | Convenciones de Oracle |
| Versionamiento | Git + GitHub | Git + GitHub |

## Estructura

```
modulo_pasajeros/
├── main.py                 Punto de entrada: abre la ventana
├── pasajeros/
│   ├── conexion.py         Conexión a MySQL (lee el .env)
│   ├── modelo.py           Clase Pasajero
│   ├── validaciones.py     Reglas de cada campo
│   ├── repositorio.py      CRUD: INSERT, SELECT, UPDATE, DELETE
│   └── interfaz.py         Ventana Tkinter con botones y tabla
├── tests/
│   ├── test_validaciones.py  31 pruebas unitarias de validación
│   └── test_repositorio.py   7 pruebas de integración contra MySQL
├── base_datos/crear_bd_hyd.sql   Crea BD, tabla, usuario y datos de prueba
├── .env.ejemplo            Plantilla de credenciales
├── .gitignore              Excluye .env y archivos temporales
├── pyproject.toml          Reglas PEP 8 para Ruff
├── requirements.txt        Librerías externas
└── GUIA_EXPLICADA.md       Explicación del código parte por parte
```

## Cómo ejecutarlo (Windows)

1. Abrir `base_datos/crear_bd_hyd.sql` en MySQL Workbench y ejecutarlo completo (rayo ⚡).
2. En la terminal, dentro de esta carpeta:
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   copy .env.ejemplo .env
   ```
3. Abrir `.env` y escribir la clave real del usuario `hyd_app`.
4. Ejecutar la aplicación: `python main.py`
5. Ejecutar las pruebas: `python -m unittest -v`
6. Revisar PEP 8: `ruff check .`

## Historias de usuario cubiertas

| HU | Como asesor quiero... | Botón |
|---|---|---|
| HU-01 | registrar un pasajero nuevo | Guardar |
| HU-02 | buscar un pasajero por documento | Buscar |
| HU-03 | ver todos los pasajeros registrados | Tabla (se actualiza sola) |
| HU-04 | modificar los datos de un pasajero | Modificar |
| HU-05 | eliminar un pasajero con confirmación | Eliminar |
