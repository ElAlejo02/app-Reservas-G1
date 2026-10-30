# Clase GA7 · AA2 · Estándares de codificación: CRUD con JDBC y módulo web con Servlets y JSP

| Dato | Valor |
|---|---|
| Guía | GA7 · Codificar los módulos del software |
| Competencia | 220501096 · Desarrollar la solución de software de acuerdo con el diseño y metodologías de desarrollo |
| Resultado de aprendizaje | 220501096-04 · Codificar el software de acuerdo con el diseño establecido |
| Actividad | GA7-220501096-AA2 · Aplicar estándares de codificación (96 h) |
| Evidencias | **AA2-EV01** (módulo de escritorio con JDBC y CRUD) y **AA2-EV02** (módulo web con formularios HTML, Servlets, GET, POST y JSP) |
| Fecha de la clase | 2026-08-06 (tomada del archivo de video) · 2 h 57 min · instructor de la AA1 |
| Transcripción y acta | En tu PC: `Claude\Projects\Sena\Clases\GA07 - Codificar modulos y versionamiento\` |
| Plazo dicho en clase | Plan de trabajo hasta el **31 de octubre** |

> **Esta es la clase de la AA2.** Fue la última del instructor de la AA1 antes de entregar la ficha a la instructora líder. En las clases de septiembre la instructora de programación pasó directo a la AA3, así que **esta grabación es la única explicación de la AA2**.

> **En Python:** el acceso a la base que en Java hace **JDBC** lo hace la **DB-API** (`sqlite3` o `pymysql`). Lo que hacen los **Servlets y JSP sobre Tomcat** lo hace **FastAPI con plantillas Jinja2 sobre Uvicorn**. El instructor dijo que lo que más revisa es **la codificación y los pantallazos**, no el entorno.

---

## 1. Resumen en un minuto

1. **Arquitectura de tres capas (MVC):** la **vista** (HTML o JSP), el **controlador** (Servlet: la lógica del negocio) y el **modelo** (la base de datos MySQL). El cliente nunca habla directo con la base.
2. Instalación en este orden: **Eclipse** (o NetBeans, que ya trae Tomcat), luego el **JDK** y luego **Apache Tomcat 10.1**. El conector **MySQL Connector/J** se agrega al proyecto como *external JAR*.
3. **EV01 (escritorio):** proyecto Java con paquetes y clases que respeten los estándares de nombres, y una clase de conexión con `Connection`, `Statement` y `ResultSet` que haga **SELECT, INSERT, UPDATE y DELETE** sobre la tabla `compañía`.
4. **EV02 (web):** *Dynamic Web Project* con un `index.html` cuyo formulario (`action`, `method`) envía a un **Servlet** (`doGet` / `doPost`), y páginas **JSP** con directivas, expresiones, scripts y declaraciones.
5. **Entrega:** ZIP con el código, el **script de la base de datos** y un **PDF con pantallazos** y los integrantes. El enlace del repositorio es **opcional**.

---

## 2. Conceptos de la clase, explicados

### 2.1 JDBC paso a paso y su equivalente

| Paso (Java) | Para qué | Python (DB-API) |
|---|---|---|
| Descargar **Connector/J** (*Platform Independent*, .zip) y agregarlo con *Build Path → Add External JARs* | El "puente" entre Java y MySQL | `pip install pymysql` (con SQLite no hace falta nada) |
| `import java.sql.*` | Las clases de JDBC | `import sqlite3` / `import pymysql` |
| `Class.forName(...)` | Cargar el driver | No hace falta |
| `DriverManager.getConnection("jdbc:mysql://localhost:3306/bd", "root", "root")` | Abrir la conexión | `sqlite3.connect(...)` / `pymysql.connect(host=..., user=..., password=..., database=...)` |
| `Statement st = con.createStatement()` | Objeto para enviar sentencias | `cursor = conexion.cursor()` |
| `ResultSet rs = st.executeQuery("SELECT ...")` | Consultar | `cursor.execute("SELECT ...")` |
| `while (rs.next()) { rs.getInt(...); rs.getString(...) }` | Recorrer el resultado fila por fila | `for fila in cursor.fetchall():` |
| `st.executeUpdate("INSERT/UPDATE/DELETE ...")` | Modificar datos | `cursor.execute(...)` + `conexion.commit()` |
| `con.close()` | Cerrar | `conexion.close()` |

Detalles de la clase:
- **`getInt` vs `getString`:** hay que pedir cada columna con su tipo (usar `DESCRIBE tabla` para verlo). En Python cada fila llega como una tupla con los tipos correctos.
- **Siempre `WHERE` en UPDATE y DELETE.** Sin él se modifican **todos** los registros.
- El error "duplicado" en clase salió porque **no había guardado** el archivo (Ctrl+S) y volvió a ejecutar el INSERT anterior.

### 2.2 Estándares que pide la EV01 (lo que él mostró)

| Elemento | Java (clase) | Python |
|---|---|---|
| Paquete | `producto`, `clientes`, `conexiones` (minúscula) | Carpeta en minúscula |
| Clase | `ClaseProducto`, `PrimeraConexion` (PascalCase) | `Proveedor` |
| Atributos | `private int codigo; private String nombre; private double precio;` | `self.id_proveedor`, `self.nit`, `self.nombre` |
| Métodos | `public void mostrarResultados()` (no devuelve) y `public double calcularTotal(int cantidad, double precio)` (recibe y devuelve) | `consultar_proveedores()`, `actualizar_nombre(...) -> int` |
| Visibilidad | `public` (cualquiera), `private` (solo la clase), `protected` (paquete y subclases) | Sin guion bajo, con `_`, con `__` (convención) |
| Objeto | `ClaseProducto objeto = new ClaseProducto();`: sin objeto no se accede a los métodos desde el `main` | `Proveedor(1, "...", "...")` |

### 2.3 Servlets, JSP y Tomcat

| Concepto | Qué es | Python |
|---|---|---|
| **Tomcat** | Servidor web y de aplicaciones de Apache que ejecuta Servlets y JSP. Puerto 8080 (él usó **8082** porque el 8080 estaba ocupado) | **Uvicorn** (`--port 8082`) |
| **Servlet** | Clase Java (`extends HttpServlet`) que recibe la petición del formulario y responde. Es el **controlador** | Una función con `@app.get` o `@app.post` |
| Ciclo de vida del Servlet | `init` (primera petición) → `doGet` / `doPost` (atiende) → `destroy` (libera memoria) | FastAPI lo maneja solo |
| `request.getParameter("usuario")` | Leer un campo del formulario | Parámetro de la función (`usuario: str`) |
| **GET** | Los datos viajan **en la URL** (`?usuario=root&clave=root`). Inseguro; sirve para probar | `@app.get` |
| **POST** | Los datos viajan en el cuerpo. **Lo recomendado** | `@app.post` + `Form(...)` |
| `<form action="MiPrimerServlet" method="get">` | `action` = a quién se envía; `method` = cómo. **No puede quedar vacío** | `<form action="/ingreso" method="post">` |
| **JSP** | HTML con código Java incrustado (parecido a PHP). Es la **vista** | Plantillas **Jinja2** |
| *Dynamic Web Project* | Tipo de proyecto de Eclipse para web (hay que instalar *Web, XML, Java EE*) | Una carpeta con `main.py` y `plantillas/` |
| Carpetas `src/main/java` y `src/main/webapp` | Los Servlets van en `java` y las páginas HTML y JSP en `webapp` | `main.py` y `plantillas/` |

### 2.4 Los cuatro tipos de código en una JSP (la EV02 los pide)

| JSP | Para qué | Ejemplo de clase | Jinja2 |
|---|---|---|---|
| **Directiva** `<%@ ... %>` | Metadatos e `import` | `<%@ page import="java.util.Date" %>` | No hace falta: los datos llegan desde Python |
| **Expresión** `<%= ... %>` | Una línea que se imprime | La fecha, "Juan Manuel" en mayúsculas, una suma | `{{ ahora }}`, `{{ nombre \| upper }}`, `{{ a + b }}` |
| **Scriptlet** `<% ... %>` | Varias líneas de código | Un `for` del 1 al 5 | `{% for i in range(1, 6) %} ... {% endfor %}` |
| **Declaración** `<%! ... %>` | Declarar variables y métodos | Un método `suma(a, b)` que da 15 | `{% macro suma(a, b) %}` |

---

## 3. Lo que se hizo en Java y cómo se hace en Python

| En clase | En Python |
|---|---|
| Clase `ClaseProducto` con atributos, `mostrarResultados()` y `calcularTotal()` | Ver los ejemplos de la [AA1](../2026-07-02-AA1-versionamiento-git-y-estandares/) y la clase `Proveedor` |
| `PrimeraConexion.java` con CRUD sobre `compañía` | [01_crud_proveedores_dbapi.py](ejemplos/01_crud_proveedores_dbapi.py) sobre `proveedor` |
| Script en Workbench | [crear_bd_proveedores.sql](ejemplos/crear_bd_proveedores.sql) |
| `index.html` + `MiPrimerServlet.java` | [web_servlets/plantillas/index.html](ejemplos/web_servlets/plantillas/index.html) + [web_servlets/main.py](ejemplos/web_servlets/main.py) |
| `expresiones.jsp`, `scripts.jsp`, `declaraciones.jsp` | [ejemplos_plantilla.html](ejemplos/web_servlets/plantillas/ejemplos_plantilla.html) |
| Probar en el navegador de Eclipse | [test_web.py](ejemplos/web_servlets/test_web.py) (4 pruebas) + [pantallazos](capturas/) |

> **Para profundizar (sugerencia):** en el proyecto real conviene SQLAlchemy (ver la [clase del 2026-09-03](../2026-09-03-AA3-modulo-escritorio-con-base-de-datos/)). Aquí se usa SQL directo para que se vea, línea por línea, lo mismo que hace JDBC.

---

## 4. Evidencias

> Lo que dijo el instructor: **"lo que más me interesa es la codificación"** y los **pantallazos**. El versionamiento "no es camisa de fuerza".

### AA2-EV01 · Codificación del módulo según requerimientos (desempeño)
- [ ] Módulo con conexión a la base de datos que haga **inserción, consulta, actualización y eliminación**.
- [ ] Estándares de nombres de **variables, métodos, clases y paquetes**.
- [ ] Basado en el diagrama de clases, los casos de uso, las historias de usuario y los prototipos.
- [ ] ZIP `NOMBREAPELLIDO_AA2_EV01` con:
  - [ ] el código fuente;
  - [ ] **el script de la base de datos** (lo pidió para montarlo en Workbench y probar);
  - [ ] un **PDF con los integrantes y pantallazos** de cada operación y su resultado en consola y en Workbench;
  - [ ] el enlace del repositorio, **opcional**.

### AA2-EV02 · Módulo codificado y probado, versión web (producto)
- [ ] Formularios **HTML** que envían a un controlador (**Servlet**; en Python, FastAPI).
- [ ] Usar los métodos **GET** y **POST**.
- [ ] Usar elementos de **JSP** (en Python, plantillas: expresiones, ciclos y funciones).
- [ ] ZIP `NOMBREAPELLIDO_AA2_EV02` con el código y un **PDF con pantallazos**: la instalación del servidor, el formulario, el resultado de GET y de POST, y las páginas de plantillas. Usa las 4 de [capturas/](capturas/).

> **Pregúntale a la instructora:** si la AA2 sigue abierta para entregar, porque en septiembre se pasó directo a la AA3.

---

## 5. Aplicación al proyecto de reservas

- **Proveedores** es la primera tabla natural del proyecto: el repo ya tiene la clase `Proveedor` y no depende de otras tablas.
- **Login web** (EV02) = el mismo inicio de sesión que después se convirtió en API en la AA5: aquí devuelve una página HTML; allá devuelve JSON. Comparar los dos ejemplos ayuda a entender la diferencia entre una **app web clásica** (el servidor arma el HTML) y una **API** (el servidor solo entrega datos).
- **En la vida real,** el backoffice de **Travel Compositor** usa formularios con POST para todo lo que cambia datos (crear reservas, editar tarifas) y GET solo para buscar o filtrar. Así un enlace compartido nunca lleva una contraseña.

---

## 6. Qué estudiar

| Sesión | Tema | Recurso | Práctica |
|---|---|---|---|
| 1 | SQL desde Python (DB-API) | [sqlite3 en la documentación de Python](https://docs.python.org/es/3/library/sqlite3.html) | Correr el ejemplo 01 y agregar un `SELECT` por NIT |
| 2 | MySQL desde Python | [PyMySQL](https://pymysql.readthedocs.io/en/latest/) | Cambiar `conectar()` a MySQL |
| 3 | Formularios en FastAPI | [FastAPI: datos de formulario](https://fastapi.tiangolo.com/es/tutorial/request-forms/) | Formulario de registro de proveedor con POST |
| 4 | Plantillas | [FastAPI: plantillas](https://fastapi.tiangolo.com/es/advanced/templates/) · [Jinja2](https://jinja.palletsprojects.com/en/stable/templates/) | Tabla de proveedores con `{% for %}` |
| 5 | Teoría de Servlets y JSP (para entender la guía) | Material de formación "Construcción de aplicaciones con Java" | Comparar con la sección 2.3 |

---

## 7. Ejemplos de código

| Archivo | Qué enseña | Capturas |
|---|---|---|
| [01_crud_proveedores_dbapi.py](ejemplos/01_crud_proveedores_dbapi.py) | CRUD con SQL directo (el equivalente de JDBC), estándares de nombres y error de duplicado controlado | |
| [crear_bd_proveedores.sql](ejemplos/crear_bd_proveedores.sql) | Script de la base para el ZIP | |
| [web_servlets/main.py](ejemplos/web_servlets/main.py) | Controlador web con GET y POST | [index](capturas/01_index_formularios.png) · [GET](capturas/02_get_exitoso.png) · [POST](capturas/03_post_incorrecto.png) |
| [web_servlets/plantillas/](ejemplos/web_servlets/plantillas/) | Vistas: formulario, resultado y ejemplos de plantillas | [plantillas](capturas/04_plantillas.png) |
| [web_servlets/test_web.py](ejemplos/web_servlets/test_web.py) | 4 pruebas del módulo web | |

### Cómo correrlos
```
cd "estudio\GA07-codificar-modulos\2026-08-06-AA2-estandares-jdbc-servlets\ejemplos"
python 01_crud_proveedores_dbapi.py

cd web_servlets
pip install "fastapi<0.145" uvicorn jinja2 python-multipart pytest httpx
uvicorn main:app --reload --port 8082
pytest -v test_web.py
```
Abrir `http://127.0.0.1:8082` (usuario `root`, clave `root`).

### El código parte por parte (01_crud_proveedores_dbapi.py)
1. `class Proveedor`: clase con nombres según el estándar (PascalCase para la clase, snake_case para los atributos).
2. `conectar()`: abre la conexión. Trae comentada la versión MySQL con `pymysql.connect(...)`.
3. `consultar_proveedores()`: `cursor.execute("SELECT ...")` y `fetchall()`; cada fila se convierte en un objeto `Proveedor`.
4. `insertar_proveedor()`: `INSERT` con `?` (en MySQL, `%s`) y `commit()`.
5. `actualizar_nombre()` y `eliminar_proveedor()`: siempre con `WHERE id_proveedor = ?`. Devuelven `rowcount`, es decir, cuántas filas cambiaron.
6. `main()`: el mismo recorrido de la clase (consultar, insertar el 4, actualizarlo, eliminarlo) y el error de duplicado atrapado con `try`/`except`. El `finally` cierra la conexión.

### El código parte por parte (web_servlets)
1. `inicio()` devuelve el `index.html` con dos formularios: uno `method="get"` y otro `method="post"`, ambos con `action="/ingreso"`.
2. `ingreso_get()` recibe los datos desde la URL; `ingreso_post()` los recibe con `Form(...)`, desde el cuerpo. Son el `doGet` y el `doPost` del Servlet.
3. `resultado.html` usa `{% if correcto %}` para mostrar "Ingreso exitoso" o el error: es lo que el Servlet escribía con `PrintWriter`.
4. `ejemplos_plantilla.html` tiene una expresión, un ciclo y una función (`macro`): los equivalentes de las 4 páginas JSP de la clase.

---

## 8. Repaso

<details><summary>1. ¿Cuáles son las tres capas del modelo MVC y qué tecnología va en cada una en la clase?</summary>
Vista: HTML o JSP. Controlador: Servlet. Modelo: la base de datos MySQL.
</details>

<details><summary>2. ¿Qué es JDBC y cuál es su equivalente en Python?</summary>
El puente (driver) que conecta Java con la base de datos. En Python, la DB-API: sqlite3 o pymysql (o SQLAlchemy por encima).
</details>

<details><summary>3. ¿Qué diferencia hay entre executeQuery y executeUpdate?</summary>
executeQuery es para SELECT y devuelve un ResultSet. executeUpdate es para INSERT, UPDATE y DELETE y devuelve cuántas filas cambiaron.
</details>

<details><summary>4. ¿Qué pasa si se hace un UPDATE sin WHERE?</summary>
Se modifican todos los registros de la tabla.
</details>

<details><summary>5. ¿En qué orden se instalan Eclipse, el JDK y Tomcat?</summary>
Eclipse, luego el JDK y luego Tomcat, porque Tomcat necesita el JDK instalado.
</details>

<details><summary>6. ¿Qué diferencia hay entre GET y POST?</summary>
Con GET los datos viajan en la URL y se ven; es inseguro. Con POST viajan en el cuerpo de la petición; es lo recomendado.
</details>

<details><summary>7. ¿Qué hacen los atributos action y method del formulario?</summary>
action dice a qué Servlet o ruta se envían los datos; method dice si se envían con GET o con POST.
</details>

<details><summary>8. Nombra los cuatro tipos de código de una JSP.</summary>
Directiva &lt;%@ %&gt;, expresión &lt;%= %&gt;, scriptlet &lt;% %&gt; y declaración &lt;%! %&gt;.
</details>

<details><summary>9. ¿Qué pidió el instructor incluir en el ZIP además del código?</summary>
El script de la base de datos y un PDF con los integrantes y pantallazos de lo realizado.
</details>

Tarjetas para Anki: [repaso-anki.csv](repaso-anki.csv).
