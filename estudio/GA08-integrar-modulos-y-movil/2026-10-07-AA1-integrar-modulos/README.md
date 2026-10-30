# Clase GA8 · AA1 · Integrar los módulos: API + base de datos + frontend

| Dato | Valor |
|---|---|
| Guía | GA8 · Codificar los módulos del software: integración, móvil y tecnologías emergentes |
| Competencia | 220501096 · Desarrollar la solución de software de acuerdo con el diseño y metodologías de desarrollo |
| Resultado de aprendizaje | 220501096-04 · Codificar el software de acuerdo con el diseño establecido |
| Actividad | GA8-220501096-AA1 · Integrar módulos (96 h) |
| Evidencias | **AA1-EV01** (desarrollar software integrando sus módulos) y **AA1-EV02** (módulos integrados) |
| Fecha de la clase | 2026-10-07 (tomada del nombre del archivo de video) · 39 min |
| Transcripción y acta | En tu PC: `Claude\Projects\Sena\Clases\GA08 - Integrar modulos y movil\` |
| **Plazo** | **Todas las evidencias hasta el 31 de octubre** (lo dijo la instructora). Ella explica dos evidencias por semana |

> **Es el cierre del proyecto web.** Las piezas de la GA7 (el login de la AA5, el CRUD de la AA5 y el frontend de la AA4) se unen en **un solo sistema conectado a MySQL**. El ejemplo de esta carpeta hace eso en Python, organizado en paquetes como pide la guía.

---

## 1. Resumen en un minuto

1. **Integrar** = unir los módulos que se hicieron por separado (login, CRUD, frontend) y conectarlos a la **base de datos real**.
2. En Spring Boot no se descarga el conector JDBC a mano: se agrega la dependencia de MySQL en **`pom.xml`** y Maven la baja.
3. En MySQL Workbench creó la tabla de productos con **`id` INT, llave primaria y autoincremento**. Luego cambió la lista `static` del controlador por **sentencias SQL** dentro de `try-catch`.
4. Probó en Postman (la lista salía vacía hasta crear el primero, y lo vio en Workbench) y luego en un **frontend HTML + JavaScript** con login y panel para crear, editar y eliminar. Falló varias veces por las **comillas invertidas** del JavaScript.
5. **Entrega:** un **PDF con normas APA** que documenta todo el proyecto (arquitectura, requerimientos, diagramas, seguridad, capas, navegación, Git, pruebas, servidores) más el código y los ejecutables. Lo siguiente es el **APK** (móvil).

---

## 2. Conceptos de la clase, explicados

### 2.1 Arquitectura cliente-servidor por capas (como la describió la instructora)

| Capa | En clase | En el ejemplo Python | Carpeta |
|---|---|---|---|
| Presentación (frontend) | HTML5, CSS3, JavaScript con Fetch API | Igual: `index.html` con `fetch` | `app/static/` |
| Controladores (API REST) | Spring Boot, `@RestController` | FastAPI, `APIRouter` | `app/rutas/` |
| Modelo / DTO | `UsuarioDTO`, `ProductoDTO` | `esquemas.py` (DTO) y `modelos.py` (tablas) | `app/` |
| Persistencia | MySQL con el conector en `pom.xml` | MySQL con SQLAlchemy + PyMySQL (o SQLite para probar) | `app/db.py` |

```
 Navegador (index.html) ──fetch JSON──► rutas/auth.py, rutas/hoteles.py ──SQLAlchemy──► MySQL
                                              ▲
                                    db.py: obtener_sesion() se inyecta en cada endpoint
```

### 2.2 De la lista en memoria a la base de datos

| Antes (GA7-AA5) | Ahora (GA8-AA1) |
|---|---|
| `static List<ProductoDTO>` con 2 datos | Tabla `productos` / `hoteles` en MySQL |
| Al reiniciar se perdían los cambios | Los datos **persisten** |
| El id lo calculaba el código | El id lo pone la base (`AUTO_INCREMENT`) |
| En Postman, la lista arrancaba con 2 | Arranca vacía hasta crear el primero (por eso el id 11 de la clase: los intentos anteriores ya habían consumido números) |

### 2.3 Dependencias: `pom.xml` y su equivalente

| Java (Maven) | Python |
|---|---|
| `pom.xml` con `<dependency>mysql-connector-j</dependency>` | `requirements.txt` con `sqlalchemy` y `pymysql` |
| Maven descarga la librería al construir | `pip install -r requirements.txt` |
| `application.properties` con URL, usuario y clave | Variable de entorno `DATABASE_URL` |

### 2.4 Inyección de dependencias (ya mencionada en la AA4)
En Spring se escribe `@Autowired` y el framework entrega la conexión. En FastAPI: `sesion: Session = Depends(obtener_sesion)`. Cada petición recibe su propia sesión y se cierra sola al terminar.

### 2.5 El error de la clase: comillas invertidas
En JavaScript, un texto con variables usa **comillas invertidas**: `` `/api/hoteles/${id}` ``. Al copiar código de un documento o un PDF, se convierten en comillas normales y el navegador falla sin decir mucho. **Consejo:** copia el código desde VS Code o desde el archivo `.html`, no desde Word, y abre la consola del navegador (F12) para ver el error.

---

## 3. Lo que se hizo en Java y cómo se hace en Python

| En clase | En el ejemplo |
|---|---|
| Paquete `conexion` con la clase `Conexion` | [app/db.py](ejemplos/sistema_reservas/app/db.py) |
| Dependencia MySQL en `pom.xml` | `requirements.txt`: `sqlalchemy`, `pymysql` |
| Tabla en Workbench con id autoincremental | [crear_bd_mysql.sql](ejemplos/sistema_reservas/crear_bd_mysql.sql); la app también la crea al arrancar |
| `ProductoController` con SQL y `try-catch` | [app/rutas/hoteles.py](ejemplos/sistema_reservas/app/rutas/hoteles.py) con SQLAlchemy |
| `AuthController` (admin / 12345) | [app/rutas/auth.py](ejemplos/sistema_reservas/app/rutas/auth.py) con usuarios en la tabla y contraseña con hash |
| HTML + JavaScript con login y panel | [app/static/index.html](ejemplos/sistema_reservas/app/static/index.html) |
| Probar en Postman y en Workbench | [tests/test_integracion.py](ejemplos/sistema_reservas/tests/test_integracion.py) (3 pruebas) + pantallazos |
| Clase principal de Spring Boot | [app/main.py](ejemplos/sistema_reservas/app/main.py) |

---

## 4. Evidencias

### AA1-EV01 · Desarrollar software integrando sus módulos (desempeño) y AA1-EV02 · Módulos integrados (producto)
La instructora mostró **un solo documento modelo** para las dos. Ambas se entregan en **PDF** con código fuente, compilados, documentos y URL.

**Estructura del PDF** (normas APA: portada, introducción, desarrollo, conclusiones y referencias):

| Sección | Qué poner (adaptado al sistema de reservas) |
|---|---|
| Arquitectura | Cliente-servidor por capas: HTML5/CSS3/JavaScript → FastAPI (Python) → MySQL. Diagrama de la sección 2.1 |
| Requerimientos del sistema | RF1 autenticación (login); RF2 CRUD de hoteles; RF3 pasajeros; RF4 reservas. Con su historia de usuario |
| Casos de uso | Iniciar sesión, gestionar hoteles, registrar pasajero... con pantallazos |
| Diagrama de clases | `Usuario`, `Hotel`, `Pasajero`, `Reserva` y los DTO |
| Diagrama de paquetes | `app`, `app.rutas`, `app.static`, `tests` |
| Diagrama de componentes | Frontend, módulo de autenticación, módulo de hoteles, base de datos |
| Mecanismos de seguridad | Contraseñas con **bcrypt**, mensaje 401 genérico, validación de datos con Pydantic (422), CORS (el `@CrossOrigin` de la clase) |
| Capas | Tabla 2.1 |
| Metodología | La que el grupo definió en las fases anteriores (por ejemplo, Scrum) |
| Mapa de navegación | Login → panel de hoteles → crear, editar o eliminar → cerrar sesión |
| Control de versiones | Git y enlace del repositorio en GitHub |
| Librerías y frameworks por capa | Frontend: HTML/CSS/JS. Backend: FastAPI, Pydantic, bcrypt. Datos: SQLAlchemy, PyMySQL |
| Componentes reutilizables y buenas prácticas | `buscar()` reutilizado en 3 endpoints; PEP 8 con Ruff; paquetes con nombres claros |
| Pruebas unitarias y de integración | Salida de `pytest -v` y pantallazos de Postman |
| Configuración de servidores y base de datos | Uvicorn en el 8080, `DATABASE_URL`, script SQL |
| Ambientes de desarrollo y pruebas | Windows 11, Python 3.13, VS Code, MySQL 8, navegador Edge o Chrome |
| Datos de entrada y salida por módulo (EV02) | La tabla de endpoints de la [GA7-AA5](../../GA07-codificar-modulos/2026-09-30-AA5-api-del-proyecto-crud/README.md#41-endpoints-para-entregar-ejemplo) |
| Manual técnico (EV02) | Cómo instalar y correr: sección 7 de esta guía |

- [ ] Código en Git y **URL del repositorio**.
- [ ] **URL donde está desplegado**: si no hay servidor en la nube, la instructora aceptó el servidor local (`localhost:8080`) con pantallazos.
- [ ] Ejecutables o forma de correrlo.

---

## 5. Aplicación al proyecto de reservas

- **Estructura recomendada para el repo `app-Reservas-G1`:** la misma del ejemplo (`app/db.py`, `app/modelos.py`, `app/esquemas.py`, `app/rutas/...`, `app/static/`, `tests/`). Así se cumple el punto de la guía "dividir el código en paquetes con nombres de fácil entendimiento".
- **Módulos a integrar después de hoteles:** pasajeros (ya existe en la AA4), habitaciones (relación con hotel), reservas (relaciona todo y genera `HDMDE001`).
- **En la vida real,** los motores de reserva como **Travel Compositor** tienen exactamente estas capas: el backoffice web, una API y una base de datos. Cuando cambia una tarifa en la base de datos, la ven a la vez el backoffice, la API para agencias y la app móvil.

---

## 6. Qué estudiar

| Sesión | Tema | Recurso | Práctica |
|---|---|---|---|
| 1 | SQLAlchemy con FastAPI | [FastAPI: bases de datos SQL](https://fastapi.tiangolo.com/es/tutorial/sql-databases/) | Correr el ejemplo con MySQL |
| 2 | Dependencias (`Depends`) | [FastAPI: dependencias](https://fastapi.tiangolo.com/es/tutorial/dependencies/) | Explicar `obtener_sesion` en el PDF |
| 3 | Pruebas de integración | [FastAPI: testing](https://fastapi.tiangolo.com/es/tutorial/testing/) | Agregar una prueba para pasajeros |
| 4 | Diagramas UML (clases, paquetes, componentes) | draw.io | Los tres diagramas del PDF |
| 5 | Normas APA 7 | Guía APA de la biblioteca del SENA | Portada y referencias |

---

## 7. Ejemplos de código (manual técnico)

| Archivo | Qué hace |
|---|---|
| [app/main.py](ejemplos/sistema_reservas/app/main.py) | Arranca la app, crea las tablas y datos iniciales (admin / 12345 y 2 hoteles), une los módulos y sirve el frontend |
| [app/db.py](ejemplos/sistema_reservas/app/db.py) | Conexión (SQLite por defecto, MySQL con `DATABASE_URL`) y la sesión que se inyecta |
| [app/modelos.py](ejemplos/sistema_reservas/app/modelos.py) | Tablas `usuarios` y `hoteles` |
| [app/esquemas.py](ejemplos/sistema_reservas/app/esquemas.py) | DTOs de entrada y salida |
| [app/rutas/auth.py](ejemplos/sistema_reservas/app/rutas/auth.py) | Registro e inicio de sesión contra la base de datos |
| [app/rutas/hoteles.py](ejemplos/sistema_reservas/app/rutas/hoteles.py) | CRUD de hoteles contra la base de datos |
| [app/static/index.html](ejemplos/sistema_reservas/app/static/index.html) | Login y panel de hoteles |
| [tests/test_integracion.py](ejemplos/sistema_reservas/tests/test_integracion.py) | 3 pruebas de integración con una base temporal |
| [crear_bd_mysql.sql](ejemplos/sistema_reservas/crear_bd_mysql.sql) | Script de la base para la documentación |

Capturas: [login con error](capturas/01_login_error.png) · [panel](capturas/02_panel_hoteles.png) · [hotel creado](capturas/03_hotel_creado.png).

### Cómo correrlo
```
cd "estudio\GA08-integrar-modulos-y-movil\2026-10-07-AA1-integrar-modulos\ejemplos\sistema_reservas"
pip install "fastapi<0.145" uvicorn sqlalchemy pymysql bcrypt pytest httpx
uvicorn app.main:app --reload --port 8080
```
Abrir `http://127.0.0.1:8080` y entrar con `admin` / `12345`. Pruebas: `pytest -v` (3 *passed*).

**Con MySQL:** correr `crear_bd_mysql.sql` en Workbench y, antes de `uvicorn`, `set DATABASE_URL=mysql+pymysql://root:TU_CLAVE@localhost:3306/reservas_hyd`.

### El código parte por parte
1. **main.py:** `ciclo_de_vida` ejecuta `preparar_base_de_datos()` una vez al arrancar: crea las tablas que falten y, si están vacías, agrega el usuario `admin` y dos hoteles. Después incluye los dos `router` y monta la carpeta `static` en la raíz.
2. **db.py:** `obtener_sesion()` usa `yield`: entrega la sesión al endpoint y la cierra cuando termina la petición.
3. **modelos.py:** `id` con `autoincrement=True` es el `AUTO_INCREMENT` de Workbench. La contraseña se guarda como `clave_hash` (bytes).
4. **rutas/hoteles.py:** es el mismo CRUD de la GA7, pero con `sesion.add/get/delete` y `commit()`. `sesion.refresh(hotel)` trae el id que asignó la base.
5. **rutas/auth.py:** busca el usuario con `select(...).where(...)` y compara con `bcrypt.checkpw`.
6. **index.html:** dos "pantallas" en la misma página. Al iniciar sesión oculta el login y muestra el panel. El mismo formulario sirve para crear (POST) o actualizar (PUT), según si hay un id cargado.
7. **test_integracion.py:** define `DATABASE_URL` hacia una base temporal **antes** de importar la app, para que las pruebas no toquen la base real.

---

## 8. Repaso

<details><summary>1. ¿Qué significa integrar módulos?</summary>
Unir los módulos hechos por separado (login, CRUD, frontend) en un solo sistema conectado a la base de datos real.
</details>

<details><summary>2. ¿Dónde se agrega el conector de MySQL en Spring Boot y en Python?</summary>
En Spring Boot, como dependencia en pom.xml. En Python, sqlalchemy y pymysql en requirements.txt.
</details>

<details><summary>3. ¿Qué cambia al pasar de la lista static a la base de datos?</summary>
Los datos persisten al reiniciar, el id lo asigna la base con autoincremento y la lista arranca vacía.
</details>

<details><summary>4. ¿Cuáles son las capas del sistema integrado?</summary>
Presentación (HTML, CSS, JavaScript), controladores (API REST), modelo y DTO, y persistencia (MySQL).
</details>

<details><summary>5. ¿Qué causó los errores del JavaScript en clase?</summary>
Las comillas invertidas se perdieron al copiar el código; los textos con ${variable} las necesitan.
</details>

<details><summary>6. ¿Qué secciones lleva el PDF de la GA8-AA1?</summary>
Arquitectura, requerimientos, casos de uso, diagramas de clases, paquetes y componentes, seguridad, capas, navegación, Git, librerías y frameworks, pruebas, configuración de servidores y base de datos, y ambientes, con normas APA.
</details>

<details><summary>7. ¿Hasta cuándo hay plazo para entregar?</summary>
Hasta el 31 de octubre, todas las evidencias.
</details>

Tarjetas para Anki: [repaso-anki.csv](repaso-anki.csv).
