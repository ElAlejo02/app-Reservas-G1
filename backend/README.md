# Backend · Cotizador Hoteles y Destinos

API en FastAPI + MySQL para cotizar hoteles y actividades.

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.ejemplo .env          # y poner la clave real
uvicorn app.main:app --reload   # http://127.0.0.1:8000/docs
python -m unittest -v           # pruebas
```

Antes de arrancar, correr en MySQL `base_datos/01_esquema.sql` y luego
`base_datos/02_datos_prueba.sql`.

## Módulo de consola: gestión de hoteles (GA7-AA2-EV01)

CRUD de la tabla `hoteles` con SQL directo (PyMySQL, el equivalente de
JDBC). Usa el mismo `.env` y la misma base `reservas_hyd`.

```powershell
python -m gestion_hoteles
```

Todo lo demás (cómo está hecho, las cuentas, qué endpoints hay y cómo
usarlos desde el frontend) está en [docs/GUIA.md](../docs/GUIA.md).
