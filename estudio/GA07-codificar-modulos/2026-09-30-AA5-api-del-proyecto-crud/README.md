# Clase GA7 · AA5 · API del proyecto: endpoints CRUD y pruebas con Postman

| Dato | Valor |
|---|---|
| Guía | GA7 · Codificar los módulos del software |
| Competencia | 220501096 · Desarrollar la solución de software de acuerdo con el diseño y metodologías de desarrollo |
| Resultado de aprendizaje | 220501096-04 · Codificar el software de acuerdo con el diseño establecido |
| Actividad | GA7-220501096-AA5 · Crear servicios web (144 h) |
| Evidencias | **AA5-EV03** (API del proyecto) y **AA5-EV04** (pruebas en Postman). Con esta clase **termina la GA7** |
| Fecha de la clase | 2026-09-30 (tomada del nombre del archivo de video) · 31 min |
| Transcripción y acta | En tu PC: `Claude\Projects\Sena\Clases\GA07 - Codificar modulos y versionamiento\` |
| Plazo | La instructora da **una semana** para entregar y pidió no dejarlo para última hora |

> Sigue la [clase del 2026-09-23](../2026-09-23-AA5-servicio-web-login-y-postman/): a la API del login se le agregan los endpoints de un recurso. La instructora usó un **producto** genérico; aquí el recurso es **hoteles**, que sí es del proyecto, y eso es lo que pide la EV03.

> **Un comentario que conviene aclarar.** Dijo que la mayoría ha entregado en Java y que conviene "manejar un solo programa", porque cada evidencia se construye sobre la anterior. Para el grupo, ese programa es Python: el login, los pasajeros y los hoteles van en la misma API de FastAPI. **Confírmale que sigues en Python** para que no haya sorpresas al calificar.

---

## 1. Resumen en un minuto

1. **Endpoint** = la ruta exacta del controlador donde el cliente (Postman, el navegador o el frontend) "toca la puerta" del backend.
2. Al proyecto de Spring Boot de la clase anterior (login con `AuthController` y `UsuarioDTO`) le agregó `ProductoDTO` (id, nombre, precio) y `ProductoController` con los cuatro verbos: **GET** listar, **POST** crear, **PUT** actualizar y **DELETE** eliminar.
3. Sin base de datos todavía: una **lista estática en memoria** con dos productos iniciales, el "simulador de persistencia". Al reiniciar vuelven los dos.
4. Lo probó en **Postman**: listó, actualizó el 1 y el 2, eliminó, creó un "parlante" y volvió a listar. También probó otra vez el login con una clave mala.
5. **Entrega:** la EV03 es el proyecto exportado en ZIP; la EV04 es un **video** explicando cada verbo en Postman, con pantallazos.

---

## 2. Conceptos de la clase, explicados

### 2.1 Los verbos HTTP

| Verbo | Acción | Cuerpo JSON | Respuesta si sale bien | Si no existe |
|---|---|---|---|---|
| **GET** | Listar o consultar | No | 200 + los datos | 404 |
| **POST** | Crear | Sí | 201 + lo creado | |
| **PUT** | Actualizar (todos los campos) | Sí | 200 + lo actualizado | 404 |
| **DELETE** | Eliminar | No | 200 + mensaje | 404 |

En Postman, para GET y DELETE **no** se escribe nada en *Body*; para POST y PUT, *Body → raw → JSON*.

### 2.2 La metáfora del restaurante (la de la instructora)

| Restaurante | Sistema |
|---|---|
| Cliente | **Postman**, el navegador o el frontend React |
| Mesero | La **API REST**: lleva el pedido (petición HTTP) y trae la respuesta en una bandeja (JSON) |
| Cocina | El **proyecto** (NetBeans en clase, FastAPI aquí): las reglas del negocio y los datos |
| El cliente no entra a la cocina | El frontend nunca toca la base de datos directamente |

### 2.3 Anotaciones nuevas de esta clase

| Spring Boot | Para qué | FastAPI |
|---|---|---|
| `@GetMapping` | Listar | `@router.get("")` |
| `@PostMapping` + `@RequestBody` | Crear desde el JSON | `@router.post("")` con `datos: HotelDTO` |
| `@PutMapping("/{id}")` + `@PathVariable Long id` | Actualizar el de ese id, tomado de la URL | `@router.put("/{hotel_id}")` |
| `@DeleteMapping("/{id}")` + `removeIf(...)` | Eliminar | `@router.delete("/{hotel_id}")` |
| `static List<ProductoDTO>` con bloque `static` | Datos iniciales en memoria | Lista `hoteles` al inicio del archivo |
| `ResponseEntity.ok(...)` / `.status(NOT_FOUND)` | Responder 200 o 404 | `return ...` / `HTTPException(404)` |
| Tipo `long` para el id | Entero grande | `int` (en Python no tiene límite) |

### 2.4 Cómo se arma la entrega por partes
La instructora explicó que la guía se va construyendo por capas, y que el proyecto completo con base de datos llega al final:

```
AA3: escritorio + MySQL ─┐
AA4: frontend React ─────┼──► AA5: API (login + recurso CRUD) ──► después: API conectada a MySQL
AA5-EV01/EV02: login ────┘
```

---

## 3. Lo que se hizo en Java y cómo se hace en Python

| En clase | En Python |
|---|---|
| `ProductoDTO.java` | `class HotelDTO(BaseModel)` y `class Hotel(HotelDTO)` con el id ([api_hoteles.py](ejemplos/api_hoteles.py)) |
| `ProductoController.java` con 4 endpoints | `router` con 5 endpoints (más "consultar uno" y un filtro por ciudad) |
| Lista estática con 2 productos | Lista `hoteles` con 2 hoteles |
| Recorrido manual en Postman | [coleccion_postman_hoteles.json](ejemplos/coleccion_postman_hoteles.json) con 8 peticiones **y** [test_api_hoteles.py](ejemplos/test_api_hoteles.py) con 7 pruebas automáticas |
| Exportar el proyecto en ZIP desde NetBeans | Comprimir la carpeta sin `.venv` ni `__pycache__` |

---

## 4. Evidencias

### AA5-EV03 · Diseño y desarrollo de servicios web: proyecto (desempeño)
- [ ] Los servicios necesarios **del proyecto** (no un producto genérico). Mínimo: un recurso con CRUD, como hoteles, más el login de la EV01.
- [ ] **Documentación de cada servicio**: en FastAPI es la página `/docs`. Pégale pantallazos y la tabla de endpoints de la sección 4.1.
- [ ] Proyecto en **Git**. ZIP `NOMBRE_APELLIDO_AA5_EV03` con el proyecto y el enlace del repositorio.

### AA5-EV04 · API del proyecto (producto)
- [ ] **Video** en Postman explicando cada verbo: "aquí listamos (GET), aquí actualizamos (PUT) y miren que cambió...". Sugerencia: importar la colección y seguirla en orden del 1 al 8.
- [ ] **Pantallazos** de cada prueba en un documento, y archivo con los **ENDPOINTS**.
- [ ] ZIP `NOMBRE_APELLIDO_AA5_EV04` con el proyecto, el video o su enlace, el documento de pruebas, los endpoints y el enlace del repositorio.

### 4.1 Endpoints para entregar (ejemplo)

| Método | Endpoint | Cuerpo | Respuestas |
|---|---|---|---|
| POST | `/api/auth/login` | usuario, contrasena | 200 · 401 · 422 |
| POST | `/api/auth/registro` | usuario, contrasena | 201 · 409 · 422 |
| GET | `/api/hoteles` y `/api/hoteles?ciudad=Medellín` | | 200 |
| GET | `/api/hoteles/{id}` | | 200 · 404 |
| POST | `/api/hoteles` | nombre, ciudad, estrellas, tarifa_noche | 201 · 422 |
| PUT | `/api/hoteles/{id}` | nombre, ciudad, estrellas, tarifa_noche | 200 · 404 · 422 |
| DELETE | `/api/hoteles/{id}` | | 200 · 404 |

---

## 5. Aplicación al proyecto de reservas

- **Unir todo en una sola API:** `api_auth.py` (login), `api_pasajeros.py` (AA4) y `api_hoteles.py` (esta clase) pueden ser tres `APIRouter` dentro de la misma app, con `app.include_router(...)` para cada uno. Es lo que la instructora pidió: "manejar un solo programa".
- **Siguiente paso real:** reemplazar la lista en memoria por SQLAlchemy y MySQL, como en la [clase del 2026-09-03](../2026-09-03-AA3-modulo-escritorio-con-base-de-datos/ejemplos/02_repositorio_pasajeros.py). La API no cambia por fuera: los mismos endpoints y los mismos JSON.
- **En la vida real**, la API de **Travel Compositor** funciona igual: `GET` para buscar hoteles por destino, `POST` para crear la reserva y `DELETE` o `PUT` para cancelarla. Un sistema externo nunca entra a su base de datos: siempre pasa por la API, que es el mesero.

---

## 6. Qué estudiar

| Sesión | Tema | Recurso | Práctica |
|---|---|---|---|
| 1 | Verbos y códigos HTTP | [MDN: métodos HTTP](https://developer.mozilla.org/es/docs/Web/HTTP/Methods) | Explicar la tabla 2.1 con tus palabras |
| 2 | Parámetros de ruta y de consulta en FastAPI | [FastAPI: parámetros de ruta](https://fastapi.tiangolo.com/es/tutorial/path-params/) | Agregar `GET /api/hoteles?estrellas=5` |
| 3 | Organizar una API grande | [FastAPI: aplicaciones más grandes](https://fastapi.tiangolo.com/es/tutorial/bigger-applications/) | Unir login, pasajeros y hoteles en una sola app |
| 4 | Postman | [Colecciones en Postman](https://learning.postman.com/docs/collections/collections-overview/) | Grabar la EV04 con la colección |

---

## 7. Ejemplos de código

| Archivo | Qué enseña |
|---|---|
| [api_hoteles.py](ejemplos/api_hoteles.py) | CRUD con GET, POST, PUT y DELETE, id en la ruta, filtro por ciudad, 404 y 422 |
| [test_api_hoteles.py](ejemplos/test_api_hoteles.py) | 7 pruebas: el mismo recorrido de la clase, automático |
| [coleccion_postman_hoteles.json](ejemplos/coleccion_postman_hoteles.json) | 8 peticiones para importar en Postman y grabar la EV04 |

### Cómo correrlos
```
cd "estudio\GA07-codificar-modulos\2026-09-30-AA5-api-del-proyecto-crud\ejemplos"
pip install "fastapi<0.145" uvicorn pytest httpx
uvicorn api_hoteles:app --reload --port 8080
pytest -v test_api_hoteles.py
```
Documentación en `http://127.0.0.1:8080/docs`. Allí mismo se puede probar cada endpoint con *Try it out*.

### El código parte por parte (api_hoteles.py)
1. `HotelDTO` es lo que el cliente envía (sin id). `Hotel` hereda de él y le agrega el `id` que pone el servidor. Así nadie puede inventarse el id.
2. `hoteles = [...]` es el simulador de persistencia con dos datos iniciales: el bloque `static` de la clase.
3. `buscar()` devuelve el hotel o lanza **404**. La usan consultar, actualizar y eliminar, para no repetir el mismo `for`.
4. `listar(ciudad=None)`: si llega `?ciudad=...` filtra (sin importar mayúsculas); si no, devuelve todos.
5. `crear`: calcula el siguiente id con `max(...) + 1` y responde **201**.
6. `actualizar`: busca el hotel y cambia cada campo con `setattr`, que hace el papel de los setters de Java.
7. `eliminar`: lo quita de la lista y devuelve un mensaje.

---

## 8. Repaso

<details><summary>1. ¿Qué es un endpoint?</summary>
La ruta exacta del controlador donde el cliente envía una petición HTTP para pedir o enviar datos.
</details>

<details><summary>2. ¿Qué verbo HTTP corresponde a cada operación del CRUD?</summary>
Crear: POST. Leer o listar: GET. Actualizar: PUT. Eliminar: DELETE.
</details>

<details><summary>3. ¿En qué verbos se envía cuerpo JSON en Postman?</summary>
En POST y PUT. GET y DELETE no llevan cuerpo; el id va en la URL.
</details>

<details><summary>4. ¿Qué es el simulador de persistencia de la clase?</summary>
Una lista en memoria con datos iniciales para probar sin base de datos. Al reiniciar el servidor vuelve a su estado inicial.
</details>

<details><summary>5. ¿Qué hace @PathVariable y cuál es su equivalente?</summary>
Toma un valor de la URL, como el id en /api/productos/1. En FastAPI es el parámetro con el mismo nombre que la parte de la ruta entre llaves.
</details>

<details><summary>6. ¿Qué responde la API si se actualiza un id que no existe?</summary>
404 (no encontrado).
</details>

<details><summary>7. Explica la metáfora del mesero.</summary>
El cliente (Postman o el frontend) no entra a la cocina (el proyecto y los datos): le pide al mesero (la API), que lleva la petición y trae la respuesta en JSON.
</details>

Tarjetas para Anki: [repaso-anki.csv](repaso-anki.csv).
