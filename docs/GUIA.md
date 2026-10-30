# Guía del proyecto Hoteles y Destinos

Guía viva del sistema de cotizaciones. Se actualiza cada vez que entra un módulo nuevo (mira la **Bitácora** al final).

Cada sección dice para quién es:

- **[Para todos]**: se entiende sin saber programar. Sirve para la sustentación.
- **[Backend]**: para quien toca la API (Alejo).
- **[Frontend]**: para quien hace las pantallas (Laura).

Equipo: Alejo (backend y API), Laura (frontend), Daniel (versiones e integración).

---

## 1. El sistema en una imagen [Para todos]

Piensa en un restaurante:

| Restaurante | Nuestro sistema | Dónde vive |
|---|---|---|
| El mesero, que toma el pedido y sirve | **Frontend**: la página que ve el asesor | `frontend/` (Laura) |
| La cocina, que prepara | **Backend**: la API en FastAPI | `backend/app/` |
| La despensa, donde están los ingredientes | **Base de datos** MySQL | `reservas_hyd` |
| La carta, que dice qué se puede pedir | **Documentación** automática | http://127.0.0.1:8000/docs |

El mesero nunca cocina: solo pide y sirve. Por eso **todas las cuentas (margen, descuento, IVA, total) las hace el backend** y la página solo las muestra.

Una cotización se arma así:

```
1. El asesor escoge destino, fechas y personas      -> POST /disponibilidad
2. La API devuelve los hoteles con cupo y su precio
3. El asesor escoge hotel y, si quiere, actividades  -> POST /cotizaciones/calcular
4. La API devuelve el desglose (subtotal, IVA, total)
5. El asesor pone los datos del cliente y guarda    -> POST /cotizaciones
6. La API responde con el código: COT-000001
7. Se le hace seguimiento cambiando el estado       -> PATCH /cotizaciones/COT-000001/estado
```

---

## 2. Palabras que vas a oír [Para todos]

| Palabra | Qué significa, sin tecnicismos |
|---|---|
| API | Un programa que no tiene pantalla: recibe pedidos y responde con datos. |
| Endpoint | Cada "puerta" de la API. Ejemplo: `/hoteles`. |
| GET, POST, PATCH | El tipo de pedido. GET = "dame", POST = "toma, guarda o calcula esto", PATCH = "cambia una parte". |
| JSON | El formato de los datos: parejas de nombre y valor, como una fila de Excel escrita en texto. |
| Código de respuesta | Número que dice cómo salió: 200 bien, 201 creado, 404 no existe, 409 no se puede, 422 dato mal escrito, 503 sin base de datos. |
| CORS | Regla del navegador que bloquea páginas que llaman a otra dirección. Se arregla en el backend. |
| Costo / precio de venta | Costo es lo que nos cobra el hotel. Precio de venta es lo que paga el cliente (costo + margen). |
| Margen | Lo que gana HyD. Se calcula sobre el precio de venta. |
| Tarifa | El costo por noche de un tipo de habitación en una temporada. |

---

## 3. Mapa de carpetas y cómo moverte [Para todos]

```
proyecto ADSO GRUPO 1/
├── backend/                 La API (FastAPI + MySQL)
│   ├── app/
│   │   ├── main.py          Arranque: junta todo y maneja los errores
│   │   ├── config.py        Lee el .env (clave, margen, IVA...)
│   │   ├── db.py            Abre la conexión a MySQL
│   │   ├── esquemas.py      Forma de los datos que entran y salen
│   │   ├── calculos.py      Las cuentas (solo matemática)
│   │   ├── servicios.py     Las reglas del negocio
│   │   ├── repositorios/    El SQL (único lugar con SQL)
│   │   └── rutas/           Los endpoints que ve el frontend
│   ├── base_datos/          Scripts para crear tablas y datos de prueba
│   └── tests/               Pruebas automáticas
├── docs/GUIA.md             Esta guía
├── antes/                   Lo que hicimos antes (pasajeros, POO, boceto)
└── estudio/                 Apuntes de cada clase
```

**Por dónde empezar a leer el backend:** `main.py` → `rutas/` → `servicios.py` → `calculos.py` → `repositorios/`. Es el mismo camino que recorre un pedido.

**Atajos de VS Code que más sirven:**

| Atajo | Qué hace |
|---|---|
| `Ctrl + P` | Abrir un archivo escribiendo su nombre |
| `F12` | Ir a donde está escrita la función que tienes debajo del cursor |
| `Alt + ←` | Volver a donde estabas |
| `Ctrl + Shift + F` | Buscar un texto en todo el proyecto |
| Vista *Outline* | Índice de funciones del archivo abierto |

---

## 4. Prender todo por primera vez [Backend]

**4.1 Base de datos** (con la conexión `root` de la extensión Database Client o Workbench). Ejecuta completo, en este orden:

1. `backend/base_datos/01_esquema.sql`
2. `backend/base_datos/02_datos_prueba.sql`

El segundo borra y vuelve a llenar los datos de prueba, así que se puede correr cuando quieras empezar de cero.

**4.2 Entorno de Python** (en la terminal, dentro de `backend`):

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.ejemplo .env
```

Abre `.env` y pon en `DB_PASSWORD` la clave del usuario `hyd_app`.

**4.3 Arrancar la API:**

```powershell
uvicorn app.main:app --reload
```

`--reload` hace que se reinicie sola cada vez que guardas un archivo. Abre **http://127.0.0.1:8000/docs**: ahí están todos los endpoints con un botón **Try it out** para probarlos.

**4.4 Pruebas:**

```powershell
python -m unittest -v
```

Deben salir 28 pruebas en OK. Si MySQL está apagado, las 14 de la API se saltan y solo corren las 14 de cuentas.

---

## 5. Cómo está hecho el backend, capa por capa [Backend]

La regla de oro: **cada archivo tiene un solo trabajo** y solo habla con la capa de abajo.

```
 frontend (Laura)
      │  JSON por HTTP
      ▼
 rutas/          Recibe el pedido y devuelve la respuesta. No decide nada.
      │
 servicios.py    Decide: ¿la tarifa sirve para esas fechas? ¿se puede cambiar el estado?
      │                 │
 calculos.py     repositorios/   Cuentas puras  |  Lee y guarda en MySQL
                        │
                     db.py ──► MySQL
```

### `config.py`
Lee el `.env`. Ahí están la clave de la base, el margen (20 %), el IVA (19 %), el descuento máximo (15 %) y las páginas que pueden usar la API. Si Arnulio cambia el margen, se cambia en el `.env` y no se toca código.

### `esquemas.py`
Define la forma exacta de cada dato con Pydantic. Si el frontend manda `"adultos": 0` o una fecha mal escrita, FastAPI lo rechaza solo con un 422 antes de llegar a la lógica. Es como la validación de datos de una hoja de Sheets, pero automática para toda la API.

### `calculos.py`
Solo matemática, sin base de datos. Por eso es lo más fácil de probar. Aquí está la fórmula de HyD de margen sobre precio (ver sección 6).

### `repositorios/`
El único lugar con SQL. `catalogo.py` lee destinos, hoteles, tarifas y actividades. `cotizaciones.py` guarda y consulta. Siempre con `%s` (nunca pegando texto del usuario) para evitar la inyección SQL.

Al guardar una cotización se hacen tres cosas (insertar la cotización, ponerle código e insertar sus actividades) **en una sola transacción**: o queda todo o no queda nada.

### `servicios.py`
Las reglas del negocio:

- La tarifa escogida tiene que servir para ese destino, esas fechas y esa cantidad de personas.
- Las actividades tienen que ser del mismo destino y no pueden tener más personas que la cotización.
- Los estados solo avanzan en este orden:

```
ABIERTA ──► ENVIADA ──► APROBADA
   │           ├──────► RECHAZADA
   └──► ANULADA ◄┘
```

Aprobada, rechazada y anulada son finales. Si alguien intenta saltarse un paso, responde 409 con el motivo.

### `rutas/`
Cada función es un endpoint con nombre en español y un título (`summary`) que es el que aparece como botón en `/docs`. Están agrupadas en cuatro secciones: Sistema, Catálogo, Disponibilidad y Cotizaciones.

### `main.py`
Junta las rutas, activa CORS para la página de Laura y convierte cada error en una respuesta clara:

| Error | Código | Cuándo |
|---|---|---|
| Datos mal escritos | 422 | Falta un campo, fecha con otro formato, descuento mayor a 15 |
| `NoEncontradoError` | 404 | Destino o cotización que no existe |
| `ReglaNoCumplidaError` | 409 | Tarifa que no aplica, cambio de estado no permitido |
| Sin MySQL | 503 | La base de datos está apagada |

Todos responden igual: `{"detail": "mensaje en español"}`. Así Laura siempre muestra `detail` y listo.

---

## 6. Las cuentas de una cotización [Para todos]

Ejemplo real con los datos de prueba: Cartagena, 4 noches, 2 adultos y 1 niño, Hotel Brisas de Bocagrande (habitación estándar, temporada baja), un city tour y 5 % de descuento.

| Paso | Cuenta | Valor |
|---|---|---|
| 1. Costo hotel | 4 noches × (2 × 210.000 + 1 × 105.000) | 2.100.000 |
| 2. Precio hotel | 2.100.000 ÷ (1 − 0,20) | 2.625.000 |
| 3. Costo city tour | 2 × 90.000 + 1 × 60.000 | 240.000 |
| 4. Precio city tour | 240.000 ÷ 0,80 | 300.000 |
| 5. Subtotal | 2.625.000 + 300.000 | 2.925.000 |
| 6. Descuento 5 % | 2.925.000 × 5 % | − 146.250 |
| 7. IVA 19 % | (2.925.000 − 146.250) × 19 % | 527.963 |
| 8. Tasas | 0 por persona en Cartagena | 0 |
| **Total** | 2.778.750 + 527.963 + 0 | **3.306.713** |

**¿Por qué se divide y no se multiplica?** Porque en HyD el margen es sobre el precio de venta. Si vendo en 1.000.000 y el margen es 20 %, quiero ganar 200.000 de ese millón, entonces el costo era 800.000. Multiplicar 800.000 × 1,20 daría 960.000 y la ganancia real sería solo 16,7 %.

**¿Por qué el IVA va después del descuento?** Porque el IVA se cobra sobre lo que el cliente realmente paga.

**Destinos exentos de IVA:** San Andrés, Panamá y Punta Cana tienen `exento_iva = 1` en la tabla `destinos`. San Andrés además tiene una tasa por persona de ejemplo (la tarjeta de turismo).

> Ojo: es una regla simplificada para el proyecto. En la operación real de HyD el IVA hotelero se calcula distinto (sobre el costo y con reglas por proveedor), y los valores de tasas de prueba hay que confirmarlos con operaciones.

---

## 7. Lo que la API ofrece al frontend [Frontend]

Dirección base: `http://127.0.0.1:8000`

| Botón en /docs | Método y ruta | Para qué |
|---|---|---|
| Estado del servidor | `GET /` | Saber si la API está prendida |
| Ver destinos | `GET /destinos` | Llenar el selector de destino |
| Ver hoteles | `GET /hoteles?destino=CTG` | Listado de hoteles |
| Ver actividades con precio de venta | `GET /actividades?destino=CTG` | Casillas de actividades |
| Buscar hoteles disponibles | `POST /disponibilidad` | Resultados de la búsqueda |
| Calcular cotización (sin guardar) | `POST /cotizaciones/calcular` | Resumen con el total mientras se arma |
| Guardar cotización | `POST /cotizaciones` | Guardar y obtener el código |
| Ver cotizaciones | `GET /cotizaciones?estado=ABIERTA` | Bandeja de cotizaciones |
| Ver una cotización | `GET /cotizaciones/COT-000001` | Detalle |
| Cambiar estado de una cotización | `PATCH /cotizaciones/COT-000001/estado` | Botones Enviar, Aprobar, Rechazar, Anular |

### 7.1 Buscar disponibilidad

Lo que se manda:

```json
{
  "destino": "CTG",
  "fecha_entrada": "2027-02-10",
  "fecha_salida": "2027-02-14",
  "adultos": 2,
  "ninos": 1
}
```

Lo que llega (lista ordenada del más barato al más caro):

```json
[
  {
    "id_tarifa": 3,
    "id_hotel": 1,
    "hotel": "Hotel Brisas de Bocagrande",
    "estrellas": 4,
    "tipo_habitacion": "Estándar",
    "temporada": "Baja",
    "noches": 4,
    "precio_estadia": 2625000
  }
]
```

Guarda el `id_tarifa` del hotel que escoja el asesor: es lo que se manda para cotizar. Si llega `[]`, muestra "No hay disponibilidad para esas fechas".

### 7.2 Calcular y guardar

Calcular (no guarda nada, úsalo cada vez que cambie algo en la pantalla):

```json
{
  "destino": "CTG",
  "fecha_entrada": "2027-02-10",
  "fecha_salida": "2027-02-14",
  "adultos": 2,
  "ninos": 1,
  "id_tarifa": 3,
  "actividades": [{ "id_actividad": 2, "adultos": 2, "ninos": 1 }],
  "descuento_porcentaje": 5
}
```

Respuesta: el desglose ya calculado, línea por línea:

```json
{
  "destino": "Cartagena",
  "hotel": "Hotel Brisas de Bocagrande",
  "tipo_habitacion": "Estándar",
  "temporada": "Baja",
  "noches": 4,
  "precio_hotel": 2625000,
  "actividades": [
    { "id_actividad": 2, "nombre": "City tour Ciudad Amurallada",
      "adultos": 2, "ninos": 1, "precio": 300000 }
  ],
  "precio_actividades": 300000,
  "subtotal": 2925000,
  "descuento_porcentaje": 5,
  "descuento": 146250,
  "iva_porcentaje": 19,
  "iva": 527963,
  "tasas": 0,
  "total": 3306713
}
```

Para **guardar** se manda lo mismo a `POST /cotizaciones`, más `cliente_nombre` y `cliente_correo`. Responde 201 con el `codigo` (por ejemplo `COT-000001`), el `estado` y el mismo `desglose`.

### 7.3 Cambiar estado

```json
{ "estado": "ENVIADA" }
```

Valores posibles: `ENVIADA`, `APROBADA`, `RECHAZADA`, `ANULADA`. Si no se puede, llega 409 con el motivo en `detail`.

---

## 8. Cómo consumir la API desde la página [Frontend]

Va de la mano con la guía de una semana de Laura. Solo cambian las rutas y los nombres de los campos.

**Pedir datos (GET):**

```js
const API = "http://127.0.0.1:8000";

async function cargarDestinos() {
  const respuesta = await fetch(`${API}/destinos`);
  if (!respuesta.ok) throw new Error("La API respondió " + respuesta.status);
  return await respuesta.json();
}
```

**Enviar datos (POST) y mostrar el error que manda la API:**

```js
async function enviar(ruta, datos) {
  let respuesta;
  try {
    respuesta = await fetch(`${API}${ruta}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(datos),
    });
  } catch {
    throw new Error("No hay conexión con el servidor. ¿Está prendido?");
  }
  const cuerpo = await respuesta.json();
  if (!respuesta.ok) throw new Error(cuerpo.detail);
  return cuerpo;
}

// Uso:
// const opciones = await enviar("/disponibilidad", { destino: "CTG", ... });
// const desglose = await enviar("/cotizaciones/calcular", { ... });
```

`cuerpo.detail` siempre trae un mensaje en español listo para mostrar.

**Precios en pesos colombianos:**

```js
const pesos = new Intl.NumberFormat("es-CO", {
  style: "currency", currency: "COP", maximumFractionDigits: 0,
});
pesos.format(3306713); // "$ 3.306.713"
```

**Tres reglas que evitan dolores de cabeza:**

1. Usa `textContent`, no `innerHTML`, para poner datos de la API en la página.
2. `event.preventDefault()` en el `submit` del formulario, o la página se recarga y borra todo.
3. Si en la consola aparece **CORS**: avísale a Alejo. La página tiene que abrirse con Live Server en el puerto 5500 (está permitido en el `.env` del backend).

**Nombres sugeridos para los botones de la pantalla** (iguales a los de `/docs`, para que en la presentación se note que todo es un solo sistema):

| Pantalla | Botones |
|---|---|
| Búsqueda | Buscar hoteles disponibles |
| Cotización | Agregar actividad · Calcular · Guardar cotización |
| Bandeja | Ver cotización · Enviar · Aprobar · Rechazar · Anular |

---

## 9. Pruebas automáticas [Backend]

| Archivo | Qué prueba | Necesita MySQL |
|---|---|---|
| `tests/test_calculos.py` | Noches, margen, redondeo, descuento, IVA, exentos, tasas | No |
| `tests/test_api.py` | Cada endpoint, errores 404/409/422 y el flujo de estados | Sí |

Las de la API crean cotizaciones de prueba y las borran al terminar.

---

## 10. Cuando algo falla [Para todos]

| Lo que ves | Por qué pasa | Qué hacer |
|---|---|---|
| `uvicorn` no se reconoce | No activaste el entorno | `.venv\Scripts\activate` |
| `ModuleNotFoundError: app` | Estás en otra carpeta | Párate en `backend` |
| 503 "No hay conexión con la base de datos" | MySQL apagado o clave mala en `.env` | Prende el servicio MySQL80 y revisa el `.env` |
| Error de CORS en la consola del navegador | La página no está en la lista permitida | Abrirla con Live Server (puerto 5500) o agregarla a `ORIGENES_PERMITIDOS` |
| "Internal Server Error" y en la terminal `'cryptography' package is required` | MySQL 8 usa un método de clave que PyMySQL solo entiende con esa librería | `pip install cryptography` y reiniciar uvicorn |
| `/disponibilidad` devuelve `[]` | Fechas fuera de las temporadas cargadas, o la estadía cruza dos temporadas, o son demasiadas personas | Probar con fechas entre el 16 de enero y el 14 de junio de 2027 |
| 409 "Esa tarifa no aplica" | Se mandó un `id_tarifa` de otra búsqueda | Volver a buscar disponibilidad |

---

## 11. Lo que sigue

**Próximos módulos** (en este orden, porque cada uno usa el anterior):

1. **Reservas**: convertir una cotización APROBADA en reserva con código `HDMDE001`, pasajeros y un titular. Reutiliza las validaciones del módulo de pasajeros que está en `antes/`.
2. **Novedades contables**: guardar cada cambio de una reserva (quién, cuándo, valor antes y después).
3. **Usuarios y login** con roles ADMIN, ASESOR y OPERACIÓN.

**Pendientes conocidos del cotizador:**

- Una estadía que cruza dos temporadas no aparece en la búsqueda.
- Los catálogos (hoteles, tarifas, actividades) solo se cargan por SQL; falta la pantalla de administración.

**Retos para practicar:**

- Fácil: agregar el filtro `?estrellas=4` a `GET /hoteles`.
- Medio: un endpoint `GET /cotizaciones/{codigo}/resumen` que devuelva solo cliente, total y estado.
- Difícil: que la búsqueda acepte estadías que cruzan dos temporadas (sumando noche por noche).

---

## Bitácora

| Fecha | Cambio |
|---|---|
| 2026-10-29 | Se mueve lo anterior a `antes/` (la entrega de la GA7-AA3 queda con la etiqueta `aa3-pasajeros`). Primera versión del cotizador: catálogo, disponibilidad, cálculo, guardado y estados de cotizaciones. 28 pruebas. |
