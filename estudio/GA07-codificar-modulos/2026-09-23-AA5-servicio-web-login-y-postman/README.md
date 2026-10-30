# Clase GA7 · AA5 · Servicio web de registro e inicio de sesión y pruebas con Postman

| Dato | Valor |
|---|---|
| Guía | GA7 · Codificar los módulos del software |
| Competencia | 220501096 · Desarrollar la solución de software de acuerdo con el diseño y metodologías de desarrollo |
| Resultado de aprendizaje | 220501096-04 · Codificar el software de acuerdo con el diseño establecido |
| Actividad | GA7-220501096-AA5 · Crear servicios web (144 h) |
| Evidencias | **AA5-EV01** (servicio web: caso registro e inicio de sesión) y **AA5-EV02** (pruebas de la API con Postman). Quedan EV03 y EV04 (la API del proyecto) |
| Fecha de la clase | 2026-09-23 (tomada del nombre del archivo de video) · 45 min |
| Transcripción y acta | En tu PC: `Claude\Projects\Sena\Clases\GA07 - Codificar modulos y versionamiento\` |
| Próxima clase | Cierra la GA7 y empieza la **GA8** |

> **En Python con FastAPI queda más corto.** La instructora hizo el servicio en **Spring Boot** y el cliente en **PHP**, programado en el Bloc de notas. Aquí está el mismo ejercicio con **FastAPI**: el DTO, el controlador y las respuestas 200 y 401. Agregué el registro con contraseña cifrada, 6 pruebas automáticas y una **colección de Postman lista para importar**.

---

## 1. Resumen en un minuto

1. **API REST**: un servicio que recibe datos en **JSON** (usuario y contraseña), los valida y responde con un **código HTTP**: **200** si la autenticación es correcta y **401** si no.
2. **DTO** (*Data Transfer Object*): la "bandeja" que lleva solo los datos necesarios. Si el usuario tiene 15 datos en la base, el DTO del login lleva solo dos.
3. En Spring Boot: una clase `UsuarioDTO` y un **controlador** `AuthController` con `@RestController`, `@RequestMapping`, `@CrossOrigin` y un método `login` (usuario `admin`, clave `1234`).
4. Prueba con **Postman**: petición **POST** a `localhost:8080/...`, *Body → raw → JSON*, enviar. Con la clave buena sale **200 OK** y con `0000` sale **401**.
5. Cliente **desacoplado** en **PHP**: `formulario.html` envía a `procesar.php`, que con **cURL** llama a la API de Java. Se levanta con `php -S` en otra ventana. Hubo que activar las extensiones `curl` y `openssl` en `php.ini`.

---

## 2. Conceptos de la clase, explicados

### 2.1 API REST, JSON y códigos HTTP

| Concepto | Qué es | En el ejemplo |
|---|---|---|
| **API REST** | Un servicio al que otros programas le piden cosas por HTTP, con rutas (*endpoints*) y métodos (GET, POST...) | `POST /api/auth/login` |
| **Endpoint** | La "puerta" o URL de cada servicio. La evidencia pide entregarlos | `/api/auth/registro`, `/api/auth/login` |
| **JSON** | Texto estructurado para enviar datos: `{"usuario": "admin", "contrasena": "1234"}` | El cuerpo de la petición |
| **200 OK** | Todo bien | Login correcto |
| **201 Created** | Se creó algo | Registro nuevo |
| **401 Unauthorized** | Credenciales inválidas | Clave errada |
| **409 Conflict** | Ya existe | Registro repetido |
| **422** | El JSON no trae lo que se espera | Falta la contraseña |

Analogía con HyD: cuando un sistema le pide a **Travel Compositor** la disponibilidad de un hotel, lo hace por una API: manda un JSON con destino y fechas y recibe otro JSON con hoteles y tarifas.

### 2.2 DTO
Su analogía: en una cocina, el **DTO es la bandeja** en la que el mesero lleva a la mesa solo lo que se pidió, no toda la despensa. Sirve para no exponer datos que no se necesitan (por ejemplo, el hash de la contraseña o el teléfono) y para validar lo que entra.

| Java (clase) | Python |
|---|---|
| `class UsuarioDTO { private String usuario; private String contrasena; ... getters y setters }` | `class UsuarioDTO(BaseModel): usuario: str; contrasena: str` |
| Validación manual | `Field(min_length=3)`: Pydantic valida solo y responde 422 si falla |

### 2.3 Las anotaciones de Spring y su equivalente

| Spring Boot | Para qué | FastAPI |
|---|---|---|
| `@RestController` | La clase responde JSON | Por defecto todo responde JSON |
| `@RequestMapping("/api/auth")` | Ruta base | `APIRouter(prefix="/api/auth")` |
| `@CrossOrigin` | Deja que otros orígenes (Postman, el formulario PHP, React) la llamen sin que el navegador bloquee | `CORSMiddleware` |
| `@PostMapping("/login")` | Atiende POST en esa ruta | `@router.post("/login")` |
| `@RequestBody UsuarioDTO dto` | Convierte el JSON en el DTO | El parámetro `datos: UsuarioDTO` |
| `ResponseEntity.ok(...)` / `.status(401)` | Responder con código | `return {...}` / `raise HTTPException(401, ...)` |

### 2.4 Arquitectura desacoplada
"Desacoplado" significa que el **cliente** (el formulario) y el **servidor** (la API) son programas separados que solo se hablan por HTTP y JSON. En clase:

```
 Navegador ──► formulario.html ──► procesar.php (cURL) ──► API Spring Boot :8080
               (servidor PHP: php -S localhost:8000)          (NetBeans)
```

En Python:

```
 Navegador ──► formulario_login.html (python -m http.server 8081) ──fetch──► API FastAPI :8080
```

**Ventaja:** la misma API sirve a la web, a la app de escritorio (Flet), al celular y a Postman. Es la idea de la AA4: el frontend en React y el backend aparte.

### 2.5 Problemas que salieron en clase

| Problema | Causa | Cómo evitarlo |
|---|---|---|
| "Error de conexión" en Postman | La URL copiada traía un **salto de línea** | Pegar la URL y revisar que no quede un espacio o salto al final |
| Postman no responde | El proyecto de NetBeans **no estaba corriendo** | El servidor tiene que estar encendido antes de probar (en Python: `uvicorn ...` abierto) |
| XAMPP choca con NetBeans | Los dos quieren el puerto 8080 | Por eso usó PHP sin XAMPP. En Python cada servidor va en su puerto (8080 la API, 8081 el formulario) |
| `procesar.php` falla | `curl` y `openssl` vienen desactivadas en PHP | Copiar `php.ini-development` como `php.ini` y quitar el `;` a `extension=curl` y `extension=openssl`. En Python no hace falta nada |

---

## 3. Lo que se hizo en Java y PHP y cómo se hace en Python

| En clase | En Python |
|---|---|
| `UsuarioDTO.java` | `class UsuarioDTO(BaseModel)` en [api_auth.py](ejemplos/api_auth.py) |
| `AuthController.java` con usuario fijo admin / 1234 | `iniciar_sesion()` con usuarios guardados y **contraseña con hash bcrypt** |
| Postman a mano | Postman con la [colección lista](ejemplos/coleccion_postman.json) **y** pruebas automáticas en [test_api_auth.py](ejemplos/test_api_auth.py) |
| `formulario.html` + `procesar.php` con cURL | [formulario_login.html](ejemplos/formulario_login.html) con `fetch` |
| `php -S localhost:8000` | `python -m http.server 8081` |
| Endpoints que hay que entregar | Salen solos en `http://127.0.0.1:8080/docs` ([captura](capturas/03_documentacion_swagger.png)) |

---

## 4. Evidencias

> Recordatorio de la instructora: **la parte programada se hace en grupos de 3 o 4 pero la sube cada uno**; **la parte de video (EV02) es individual**.

### AA5-EV01 · Diseño y desarrollo de servicios web: caso (desempeño)
- [ ] Servicio de **registro e inicio de sesión**: recibe usuario y contraseña; si es correcto, mensaje de autenticación satisfactoria; si no, error.
- [ ] Código con **comentarios** y proyecto en **Git**.
- [ ] ZIP `NOMBRE_APELLIDO_AA5_EV01` con el proyecto y el enlace del repositorio. En Python: [api_auth.py](ejemplos/api_auth.py) es la base, más los pantallazos del código.

### AA5-EV02 · API (producto)
- [ ] Instalar **Postman** (la instructora: entrar con *Open API Client*, sin crear cuenta).
- [ ] **Video** probando la API: cuando funciona (200) y cuando no (401). Sugerido: importar [coleccion_postman.json](ejemplos/coleccion_postman.json) y correr las 5 peticiones.
- [ ] **Pantallazos** de las pruebas en un documento.
- [ ] Archivo con los **ENDPOINTS**:

| Método | Endpoint | Cuerpo | Respuesta |
|---|---|---|---|
| POST | `/api/auth/registro` | `{"usuario": "...", "contrasena": "..."}` | 201 registrado · 409 ya existe · 422 datos inválidos |
| POST | `/api/auth/login` | `{"usuario": "...", "contrasena": "..."}` | 200 autenticación exitosa · 401 error · 422 datos inválidos |

- [ ] ZIP `NOMBRE_APELLIDO_AA5_EV02` con el proyecto, el video, el documento de pruebas, el archivo de endpoints y el enlace del repositorio.

### Pendientes de la AA5 (no se explicaron en esta clase)
- **EV03**: las APIs **del proyecto** (reservas, hoteles, pasajeros), con documentación de cada servicio. FastAPI la genera en `/docs`.
- **EV04**: probar esas APIs con Postman (video, pantallazos y endpoints).

---

## 5. Aplicación al proyecto de reservas

| Endpoint sugerido para la EV03 | Para qué | Rol que puede usarlo |
|---|---|---|
| `POST /api/auth/login` | Entrar al sistema (este ejemplo) | Todos |
| `GET /api/hoteles?ciudad=MDE` | Buscar hoteles | ASESOR, COMERCIAL |
| `POST /api/pasajeros` | Registrar pasajero (ya está en la AA4) | ASESOR |
| `POST /api/reservas` | Crear reserva y generar `HDMDE001` | ASESOR |
| `PATCH /api/reservas/{codigo}/confirmar` | Confirmar | OPERACION |
| `PATCH /api/reservas/{codigo}/cancelar` | Cancelar | ASESOR, OPERACION |
| `GET /api/reportes/ventas` | Reporte | ADMIN, COMERCIAL |

**En la vida real:** las aerolíneas y **Travel Compositor** nunca guardan contraseñas en texto plano y responden 401 sin decir si falló el usuario o la clave, para no darle pistas a un atacante. El ejemplo hace lo mismo.

**Problema del repo que sigue pendiente:** `usuario.py` guarda la contraseña en texto plano. El arreglo es `bcrypt.hashpw(...)` al registrar y `bcrypt.checkpw(...)` al entrar, como en [api_auth.py](ejemplos/api_auth.py).

---

## 6. Qué estudiar

| Sesión | Tema | Recurso | Práctica |
|---|---|---|---|
| 1 | Qué es una API REST y los códigos HTTP | [MDN: códigos de estado HTTP](https://developer.mozilla.org/es/docs/Web/HTTP/Status) | Explicar los 5 códigos del ejemplo |
| 2 | FastAPI: rutas, cuerpo y validación | [FastAPI: cuerpo de la petición](https://fastapi.tiangolo.com/es/tutorial/body/) · MoureDev: [Backend con Python y FastAPI](https://www.youtube.com/watch?v=TLftm_iO2o8) | Agregar `GET /api/auth/usuarios` |
| 3 | Postman | [Aprender Postman](https://learning.postman.com/docs/getting-started/overview/) | Importar la colección y grabar la EV02 |
| 4 | Contraseñas seguras | [bcrypt en PyPI](https://pypi.org/project/bcrypt/) | Arreglar `usuario.py` del repo |
| 5 | La API del proyecto (EV03) | Tabla de la sección 5 | Endpoints de hoteles y reservas |

---

## 7. Ejemplos de código

| Archivo | Qué enseña | Captura |
|---|---|---|
| [api_auth.py](ejemplos/api_auth.py) | API REST con DTO, registro, login, bcrypt, CORS y códigos 200/201/401/409/422 | [docs](capturas/03_documentacion_swagger.png) |
| [formulario_login.html](ejemplos/formulario_login.html) | Cliente desacoplado (el `formulario.html` + `procesar.php` de la clase) | [200](capturas/01_login_exitoso_200.png) · [401](capturas/02_login_fallido_401.png) |
| [test_api_auth.py](ejemplos/test_api_auth.py) | 6 pruebas automáticas (lo mismo que Postman) | |
| [coleccion_postman.json](ejemplos/coleccion_postman.json) | 5 peticiones listas para importar en Postman | |

### Cómo correrlos
**Terminal 1, la API:**
```
cd "estudio\GA07-codificar-modulos\2026-09-23-AA5-servicio-web-login-y-postman\ejemplos"
pip install "fastapi<0.145" uvicorn bcrypt
uvicorn api_auth:app --reload --port 8080
```
**Terminal 2, el formulario:**
```
cd "estudio\GA07-codificar-modulos\2026-09-23-AA5-servicio-web-login-y-postman\ejemplos"
python -m http.server 8081
```
Abrir `http://localhost:8081/formulario_login.html` y probar `admin` / `1234`, y luego con `0000`.

**Pruebas automáticas:** `pip install pytest httpx` y `pytest -v test_api_auth.py` (6 *passed*).

**Postman:** *Import* → `coleccion_postman.json` → abrir cada petición → *Send*.

### El código parte por parte (api_auth.py)
1. `class UsuarioDTO(BaseModel)`: el **DTO**. `Field(min_length=...)` hace que FastAPI rechace con 422 un usuario muy corto o una contraseña vacía.
2. `usuarios: dict[str, bytes]`: la "base de datos" en memoria. Guarda el **hash** de la contraseña, no la contraseña. `admin` / `1234` queda creado para probar como en clase.
3. `router = APIRouter(prefix="/api/auth")`: la ruta base (el `@RequestMapping`).
4. `registrar`: si el usuario existe responde **409**; si no, guarda `bcrypt.hashpw(...)` y responde **201**.
5. `iniciar_sesion`: compara con `bcrypt.checkpw(...)`. Si no coincide, **401** con el mismo mensaje para usuario inexistente o clave errada.
6. `CORSMiddleware`: deja que el formulario del puerto 8081 llame a la API del 8080 (el `@CrossOrigin`).

### El código parte por parte (formulario_login.html)
1. Al enviar el formulario, `preventDefault()` evita que la página se recargue.
2. `fetch(..., {method: 'POST', body: JSON.stringify({...})})` arma el JSON del DTO y lo envía: es lo que hacía `procesar.php` con cURL.
3. Muestra el **código HTTP** y el mensaje, como el PHP de la clase.

---

## 8. Repaso

<details><summary>1. ¿Qué es una API REST?</summary>
Un servicio que recibe peticiones HTTP en rutas (endpoints), normalmente con datos en JSON, y responde con datos y un código de estado.
</details>

<details><summary>2. ¿Qué es un DTO y para qué sirve?</summary>
Un objeto que transporta solo los datos necesarios entre el cliente y el servidor. Evita exponer datos de más y facilita validar lo que entra.
</details>

<details><summary>3. ¿Qué significan 200 y 401?</summary>
200: la petición salió bien (autenticación exitosa). 401: no autorizado (usuario o contraseña incorrectos).
</details>

<details><summary>4. ¿Para qué sirve @CrossOrigin y cuál es su equivalente en FastAPI?</summary>
Permite que clientes de otro origen (otro puerto o dominio) consuman la API sin que el navegador la bloquee. En FastAPI: CORSMiddleware.
</details>

<details><summary>5. ¿Qué significa que la arquitectura sea desacoplada?</summary>
Que el cliente (formulario) y el servidor (API) son programas separados que solo se comunican por HTTP y JSON. La misma API sirve a la web, al escritorio y al celular.
</details>

<details><summary>6. ¿Cómo se prueba una API en Postman?</summary>
Nueva petición, método POST, la URL del endpoint, Body → raw → JSON con los datos, y Send. Se revisa el código y el mensaje de respuesta.
</details>

<details><summary>7. ¿Por qué la contraseña se guarda con hash?</summary>
Para que, si alguien obtiene la base de datos, no pueda leer las contraseñas. Al iniciar sesión se compara el hash, no el texto.
</details>

<details><summary>8. ¿Qué dos errores típicos aparecieron en Postman en clase?</summary>
Un salto de línea pegado en la URL y el servidor de NetBeans apagado.
</details>

Tarjetas para Anki: [repaso-anki.csv](repaso-anki.csv).
