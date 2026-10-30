# Clase GA7 · AA3 · Primer módulo de escritorio conectado a la base de datos

| Dato | Valor |
|---|---|
| Guía | GA7 · Codificar los módulos del software |
| Competencia | 220501096 · Desarrollar la solución de software de acuerdo con el diseño y metodologías de desarrollo |
| Resultado de aprendizaje | 220501096-04 · Codificar el software de acuerdo con el diseño establecido |
| Actividad | GA7-220501096-AA3 · Codificar los módulos del software stand-alone, web y móvil (122 h). La instructora la nombró así: "guía 7, actividad 3, evidencia 1" |
| Evidencias | AA3-EV01 y AA3-EV02 |
| Fecha de la clase | 2026-09-03 (tomada del nombre del archivo de video) · 1 h 33 min |
| Instructora | Primera clase de la instructora de programación (la que anunció la instructora líder el 11 de agosto) |
| Transcripción y acta | En tu PC: `Claude\Projects\Sena\Clases\GA07 - Codificar modulos y versionamiento\` |
| Plazo dicho en clase | No dio fecha. Próxima clase: el miércoles siguiente; anunció dos clases por semana |

> **Muy importante: Python está permitido.** La instructora sigue en **Java con NetBeans**, pero dijo textual que *"las evidencias me las pueden entregar en cualquier plataforma donde ustedes se sientan mejor"*. A quien programe en Python u otra plataforma le pide **pantallazos del código** porque ella solo tiene NetBeans instalado.

> **Ojo con lo que dijo de Python.** Comentó que en Python "toca crear los botones por código" y en Java no. Es cierto que NetBeans tiene un diseñador donde se arrastran los botones, pero en Python con **Flet** un botón es una línea (`ft.FilledButton(content="Guardar")`). El ejemplo 03 de esta carpeta hace el mismo formulario de la clase en unas 150 líneas, comentarios incluidos.

---

## 1. Resumen en un minuto

1. Primera clase con la instructora de programación. Instaló **Java 21** y **Apache NetBeans** y armó desde cero un proyecto **Java with Ant** con dos paquetes: uno para el modelo y otro para la vista.
2. Creó la clase **Persona** (código, nombre, edad, género) con atributos privados, **constructor**, **getters y setters** generados con *Insertar código*.
3. Diseñó un **formulario Swing** (JFrame) con JTextField, JSpinner, JComboBox, JButton y una **JTable** con `DefaultTableModel`, y programó el botón **Guardar**, que llena la tabla y limpia los campos.
4. Mostró el mismo formulario ya conectado a **MySQL** con el conector JDBC (MySQL Community Server, Workbench y Connector/J) y una clase `Conexion`.
5. Al final el grupo le dijo que iba muy rápido y que **no había programado antes en Java ni con POO**. Acordaron **empezar de cero, más despacio**, en la siguiente clase: variables, tipos, clases, y luego modificar y eliminar.

---

## 2. Conceptos de la clase, explicados

### 2.1 Lenguaje compilado y orientado a objetos
| Concepto | Qué significa | En Python |
|---|---|---|
| Java es **compilado** a bytecode y corre en la **máquina virtual** (JVM): "se escribe una vez y corre en cualquier sistema" | Por eso hay que instalar el **JDK** de la misma versión que espera el IDE (ella usó 21; la 25 le dio problemas) | Python es **interpretado**: basta con instalar Python 3.12 o 3.13 |
| Java es **tipado estático**: `int edad`, `String nombre` | Si declaras `int`, solo cabe un entero | Python es dinámico, pero con *type hints* (`edad: int`) y Ruff se logra el mismo orden |
| Java vs JavaScript | Una compañera preguntó la diferencia: JavaScript corre en el navegador; Java es compilado y se usa en backend y programas de escritorio | Python se usa para las dos cosas: backend (FastAPI) y escritorio (Flet) |

### 2.2 Paquetes, clases y objetos
- **Paquete**: una carpeta que agrupa clases. Ella creó uno para el **modelo** (la clase Persona) y otro para la **vista** (el formulario). En Python, un paquete es una carpeta con un archivo `__init__.py`.
- **Clase**: la plantilla. Define los **atributos** (datos) y los **métodos** (lo que sabe hacer).
- **Objeto**: una "copia" hecha con la plantilla: `new Persona("1", "Carol", 30, "Femenino")`. En Python, sin `new`: `Pasajero("1", "Carol", 30, "Femenino")`.
- Java distingue **mayúsculas y minúsculas**: `Persona` y `persona` son cosas distintas. Python también.

### 2.3 Constructor, getters y setters

| Java (NetBeans) | Python |
|---|---|
| `private int edad;` | `self._edad` (el guion bajo es la convención de privado) |
| Constructor `public Persona(String codigo, ...)`, generado con *Insertar código > Constructor* | `def __init__(self, documento, ...)` |
| `public int getEdad()` = leer | `@property def edad(self)` |
| `public void setEdad(int edad)` = modificar | `@edad.setter def edad(self, valor)` |
| Se generan todos "por si acaso" | **Solo** cuando hay algo que validar. Si no, se usa el atributo directo |

Así lo hace el ejemplo [01_clase_pasajero.py](ejemplos/01_clase_pasajero.py): el setter de `edad` no deja guardar 200 años.

### 2.4 El formulario Swing y su equivalente en Flet

| En NetBeans (Swing) | Para qué | En Flet |
|---|---|---|
| `JFrame Form` | La ventana | `def main(page: ft.Page)` |
| `JLabel` | Texto fijo | `ft.Text` o el `label=` del campo |
| `JTextField txtCodigo` | Caja de texto | `ft.TextField(label="Documento")` |
| `JSpinner jsEdad` + `getValue()` | Número con flechas | `ft.TextField` con `input_filter=ft.NumbersOnlyInputFilter()` |
| `JComboBox jcGenero` + `getSelectedItem()` | Lista desplegable | `ft.Dropdown(options=[ft.DropdownOption("Femenino"), ...])` |
| `JButton` + evento `ActionPerformed` | Botón y lo que hace | `ft.FilledButton(content="Guardar", on_click=funcion)` |
| `JTable` + `DefaultTableModel`, `addColumn`, `addRow` | Tabla | `ft.DataTable(columns=[...], rows=[...])` |
| `JOptionPane.showMessageDialog` | Mensaje emergente | `ft.Text` de color o `ft.SnackBar` |
| `setText("")` + `requestFocus()` | Limpiar y volver al primer campo | `campo.value = ""` + `campo.focus()` |
| Cambiar el nombre de variable de cada control (*Change Variable Name*) | Para usarlo en el código | En Flet el control **es** la variable: `documento = ft.TextField(...)` |

**El error de la clase:** a la instructora el formulario dejó de compilar porque en algún momento **borró una llave de cierre `}`** y le tomó varios minutos encontrarla. En Python no hay llaves: los bloques se marcan con la **sangría**, y VS Code con Ruff marca el error en la misma línea. La lección vale igual: **guarda y prueba seguido**, así sabes en qué cambio apareció el error.

### 2.5 Conexión a la base de datos (JDBC y su equivalente)

| Paso en Java | En Python |
|---|---|
| Instalar **MySQL Community Server** y **MySQL Workbench** (ella usó la 8.0) | Igual: el motor y el Workbench no dependen del lenguaje |
| Descargar **MySQL Connector/J** y agregarlo a *Libraries* | `pip install pymysql` |
| Paquete `conexion` con la clase `Conexion` y `DriverManager.getConnection(url, usuario, clave)` | `create_engine("mysql+pymysql://usuario:clave@localhost:3306/reservas_hyd")` |
| `PreparedStatement` con `INSERT`, `SELECT`, `UPDATE`, `DELETE` | SQLAlchemy: `sesion.add`, `select`, cambiar el atributo, `sesion.delete`, y `commit()` |
| La contraseña escrita en la clase `Conexion` | La contraseña en una **variable de entorno** (`DATABASE_URL`), nunca en el código que se sube a GitHub |

Consejo que dio: al instalar MySQL **pon una contraseña fácil de recordar** y úsala igual en la conexión; su primer error fue justamente la contraseña.

### 2.6 CRUD
**C**rear (insertar), **R**ead (consultar), **U**pdate (actualizar) y **D**elete (eliminar). La instructora mostró las cuatro en la clase del 2026-09-10 como modelo de la EV01. En clase solo alcanzó a hacer *crear*; dijo que modificar y eliminar irían en la clase siguiente. El ejemplo 03 ya trae las cuatro.

---

## 3. Lo que se hizo en Java y cómo se hace en Python

| En clase | En Python |
|---|---|
| JDK 21 + Apache NetBeans | Python 3.12/3.13 + VS Code con extensiones Python y Ruff |
| Proyecto *Java with Ant* | Carpeta del proyecto con `.venv` y `requirements.txt` |
| Paquetes `modelo` y `vista` | Carpetas `modelos/` y `app/` (ver [stack-python.md](../../stack-python.md)) |
| Clase `Persona` con getters y setters | [01_clase_pasajero.py](ejemplos/01_clase_pasajero.py) |
| Clase `Conexion` con JDBC y MySQL | [02_repositorio_pasajeros.py](ejemplos/02_repositorio_pasajeros.py) con SQLAlchemy + PyMySQL |
| JFrame con Swing | [03_formulario_pasajeros.py](ejemplos/03_formulario_pasajeros.py) con Flet |
| Crear la base en Workbench | [04_crear_bd_mysql.sql](ejemplos/04_crear_bd_mysql.sql) |
| Exportar el proyecto a ZIP desde NetBeans | Comprimir la carpeta del proyecto **sin** `.venv` ni `*.db` |

---

## 4. Evidencias

> **Es la AA3, no la AA2.** En la clase del 2026-09-10 la instructora la llamó "guía 7, actividad 3, evidencia 1" y lo que pide coincide con la AA3 de la guía. La AA2 (CRUD con JDBC y la versión web con Servlets y JSP) la explicó el instructor anterior el 2026-08-06: ver [esa clase](../2026-08-06-AA2-estandares-jdbc-servlets/). El detalle de la entrega de la AA3 está en la [clase del 2026-09-10](../2026-09-10-AA3-entrega-evidencias-crud/).

### AA3-EV01 · Codificación del módulo stand-alone, web y móvil (desempeño)
- [ ] Un módulo del proyecto (la instructora: un pequeño programa de escritorio con CRUD conectado a MySQL). Sugerido: **módulo de pasajeros** o de **hoteles**.
- [ ] Basado en los artefactos ya hechos: **diagrama de clases, casos de uso, historias de usuario, prototipos**.
- [ ] **Comentarios** en el código y **estándares de codificación** (PEP 8, de la GA7-AA1-EV02).
- [ ] El proyecto en **Git** y el enlace del repositorio dentro del ZIP.
- [ ] La guía pide usar "alguno de los frameworks" del componente (para Java: Spring). En Python el equivalente sería **FastAPI**; la instructora en clase lo resolvió con Swing sin framework.
- [ ] Entrega: ZIP `NOMBRE_APELLIDO_AA3_EV01`. **En grupos de 3 o 4, pero cada uno lo sube con su nombre.** En Python: **pantallazos del código**.

### AA3-EV02 · Módulos codificados y probados (producto)
- [ ] **Documento Word** con portada, introducción, objetivo y **normas APA**.
- [ ] **Un pantallazo por cada historia de usuario o caso de uso**: la historia escrita y debajo la pantalla de la aplicación.
- [ ] Documentar las **pruebas de validación**: fechas, números, textos, caracteres especiales, longitudes.
- [ ] **Video** mostrando toda la funcionalidad con sus validaciones. **Este es individual.** La instructora prefiere el **enlace** (YouTube u otro) a subir el archivo.
- [ ] Entrega: ZIP `NOMBRE_APELLIDO_AA3_EV02` con el proyecto, el Word, el video o su enlace y el enlace del repositorio.

---

## 5. Aplicación al proyecto de reservas

### 5.1 Qué módulo hacer primero
El instructor de la AA1 dijo "versión 1: inicio de sesión y gestión de usuarios". Con lo de esta clase, el orden práctico es:

| Paso | Módulo | Tabla | Por qué |
|---|---|---|---|
| 1 | **Pasajeros** (este ejemplo) | `pasajeros` | No depende de ninguna otra tabla: ideal para aprender el CRUD |
| 2 | Hoteles y habitaciones | `hoteles`, `habitaciones` | Relación uno a muchos (composición, vista en la AA1) |
| 3 | Usuarios y login | `usuarios` | Contraseña con hash (`bcrypt`), roles ADMIN, ASESOR, OPERACION, COMERCIAL |
| 4 | Reservas | `reservas`, `reserva_pasajero` | Junta todo; código `HDMDE001` |

### 5.2 Reglas que debería validar el formulario (como en la vida real)
| Regla | Dónde se ve en la vida real | Cómo en el código |
|---|---|---|
| El documento no se repite | Booking y las aerolíneas no dejan dos perfiles con el mismo documento | Llave primaria + mensaje "Ya existe un pasajero..." (ya está en el ejemplo) |
| Edad entre 0 y 120 | Travel Compositor pide fecha de nacimiento para tarifas de niño y adulto | Setter de `edad` y `CHECK` en la tabla |
| Un menor viaja con un adulto | Política de los hoteles y las aerolíneas | Regla en el módulo de reservas (paso 4) |
| Género con valores fijos | Formularios de check-in | `Dropdown` con opciones cerradas |

### 5.3 Problemas en el repo (siguen pendientes de la clase anterior)
| Problema | Arreglo |
|---|---|
| Las clases (`pasajero.py`, `hotel.py`...) están sueltas y repetidas | Pasarlas a `modelos/` y mapearlas con SQLAlchemy como en el ejemplo 02 |
| No hay `.gitignore` | Usar la [plantilla](../2026-07-02-AA1-versionamiento-git-y-estandares/ejemplos/gitignore-python.txt); ya incluye `*.db` |

---

## 6. Qué estudiar (lo que pidió la instructora y el grupo)

El grupo pidió ir desde las bases. Este plan cubre esas bases **en Python**, en el orden en que se necesitan:

| Sesión | Tema | Recurso | Práctica |
|---|---|---|---|
| 1 | Variables y tipos (`int`, `float`, `str`, `bool`) | [Tutorial de Python, cap. 3](https://docs.python.org/es/3/tutorial/introduction.html) · MoureDev: [Python desde cero](https://www.youtube.com/watch?v=Kp4Mvapo5kc) | Calcular el total de una reserva |
| 2 | Clases, constructor y propiedades | [Tutorial de Python, cap. 9](https://docs.python.org/es/3/tutorial/classes.html) · Platzi: [Python POO](https://platzi.com/cursos/python-poo/) | Correr y modificar el ejemplo 01 |
| 3 | SQL y MySQL | Platzi: [Fundamentos de Bases de Datos](https://platzi.com/cursos/bases-datos-2025/) · MoureDev: [SQL desde cero](https://www.youtube.com/watch?v=OuJerKzV5T0) | Correr el script 04 en Workbench |
| 4 | SQLAlchemy | [Tutorial unificado de SQLAlchemy 2](https://docs.sqlalchemy.org/en/20/tutorial/) | Ejemplo 02 contra MySQL con `DATABASE_URL` |
| 5 | Flet: formularios y tablas | [Documentación de Flet](https://docs.flet.dev/) | Ejemplo 03 y agregarle un campo "teléfono" |
| 6 | Tu módulo | Este README, sección 5 | Módulo de hoteles con CRUD = AA3-EV01 |

---

## 7. Ejemplos de código

| Archivo | Qué enseña | Captura |
|---|---|---|
| [01_clase_pasajero.py](ejemplos/01_clase_pasajero.py) | Clase, constructor, getters y setters con validación | |
| [02_repositorio_pasajeros.py](ejemplos/02_repositorio_pasajeros.py) | Conexión (SQLite o MySQL) y CRUD con SQLAlchemy | |
| [03_formulario_pasajeros.py](ejemplos/03_formulario_pasajeros.py) | Formulario de escritorio con CRUD completo | [inicio](capturas/03_formulario_inicial.png) · [guardado](capturas/03_formulario_guardado.png) · [error controlado](capturas/03_formulario_error.png) |
| [04_crear_bd_mysql.sql](ejemplos/04_crear_bd_mysql.sql) | Base y tabla en MySQL | |

### Cómo correrlos
1. Activa el entorno: `.venv\Scripts\activate` e instala: `pip install -r estudio/requirements.txt`.
2. `cd "estudio\GA07-codificar-modulos\2026-09-03-AA3-modulo-escritorio-con-base-de-datos\ejemplos"`
3. `python 01_clase_pasajero.py` y `python 02_repositorio_pasajeros.py` (crea `reservas_demo.db` con SQLite).
4. `flet run 03_formulario_pasajeros.py` abre la ventana.
5. **Con MySQL:** corre `04_crear_bd_mysql.sql` en Workbench y luego, en la misma terminal:
   `set DATABASE_URL=mysql+pymysql://root:TU_CLAVE@localhost:3306/reservas_hyd` y vuelve a correr el 02 o el 03.

### El código parte por parte (02_repositorio_pasajeros.py)
1. `DATABASE_URL = os.environ.get(...)`: lee la conexión de una variable de entorno; si no existe, usa SQLite para probar sin instalar MySQL.
2. `engine = create_engine(...)`: la conexión. Es el `DriverManager.getConnection` de JDBC.
3. `class Pasajero(Base)` con `__tablename__ = "pasajeros"`: la clase **es** la tabla. Cada `mapped_column` es una columna; `primary_key=True` marca la llave.
4. `CheckConstraint("edad BETWEEN 0 AND 120")`: la base de datos también valida, no solo el formulario.
5. `crear_tablas()`: hace el `CREATE TABLE` si falta.
6. `with Session(engine) as sesion:` abre una sesión y la cierra sola al terminar el bloque (en JDBC hay que hacer `close()` a mano).
7. `insertar`: revisa que el documento no exista, `sesion.add(...)` y `commit()`. **Sin commit no se guarda.**
8. `consultar_todos`: `select(Pasajero).order_by(Pasajero.nombre)` es `SELECT * FROM pasajeros ORDER BY nombre`.
9. `actualizar`: busca por llave con `sesion.get`, cambia los atributos y hace `commit()`. SQLAlchemy arma el `UPDATE`.
10. `eliminar`: `sesion.delete(...)` y `commit()`.

### El código parte por parte (03_formulario_pasajeros.py)
1. `repo = importlib.import_module("02_repositorio_pasajeros")`: trae el archivo 02. Se importa así porque su nombre empieza por número.
2. Los controles (`documento`, `nombre`, `edad`, `genero`, `tabla`) son los mismos del formulario de la instructora.
3. `leer_formulario()`: valida que nada esté vacío y convierte la edad a `int` (lo que en Java hizo con `getValue()`).
4. `refrescar_tabla()`: vuelve a consultar la base y redibuja la tabla. Cada fila tiene `on_select_change` para subir sus datos al formulario.
5. `ejecutar(accion, texto_ok)`: corre la operación y, si el repositorio lanza `ValueError` (documento repetido, no existe...), muestra el mensaje en rojo en vez de cerrarse.
6. `on_guardar`, `on_modificar`, `on_eliminar`: los tres botones llaman al repositorio. Son el `ActionPerformed` de cada `JButton`.
7. `ft.run(main)`: arranca la app.

---

## 8. Repaso

<details><summary>1. ¿Qué es un paquete y para qué separó la instructora modelo y vista?</summary>
Una carpeta que agrupa clases. Separar el modelo (datos) de la vista (formulario) permite cambiar la pantalla sin tocar la clase Persona, y al revés.
</details>

<details><summary>2. ¿Qué hace un constructor?</summary>
Inicializa el objeto recién creado con sus valores. En Java es un método con el nombre de la clase; en Python es <code>__init__</code>.
</details>

<details><summary>3. ¿Para qué sirven el getter y el setter? ¿Cuándo vale la pena escribirlos en Python?</summary>
El getter lee un atributo y el setter lo modifica. En Python solo se escriben (con <code>@property</code>) cuando hay que validar o calcular algo, como la edad entre 0 y 120.
</details>

<details><summary>4. ¿Qué control de Swing usó para la edad y cuál para el género? ¿Y en Flet?</summary>
JSpinner para la edad y JComboBox para el género. En Flet: un TextField que solo acepta números y un Dropdown.
</details>

<details><summary>5. ¿Qué tres cosas instaló para conectar Java con MySQL? ¿Qué se instala en Python?</summary>
MySQL Community Server, MySQL Workbench y el conector JDBC (Connector/J). En Python: el mismo servidor y Workbench, más <code>pip install sqlalchemy pymysql</code>.
</details>

<details><summary>6. ¿Por qué la contraseña de la base no va en el código?</summary>
Porque el código se sube a GitHub y cualquiera la vería. Se guarda en una variable de entorno (DATABASE_URL) o en un archivo .env que está en el .gitignore.
</details>

<details><summary>7. ¿Qué significa CRUD y cuál parte se alcanzó a ver en clase?</summary>
Crear, leer, actualizar y eliminar. En clase solo se hizo crear (guardar); modificar y eliminar quedaron para la clase siguiente.
</details>

<details><summary>8. ¿Qué pasa si no se hace commit después de insertar?</summary>
El cambio no queda guardado en la base de datos; se pierde al cerrar la sesión.
</details>

<details><summary>9. ¿Qué causó el error que la instructora tardó en encontrar?</summary>
Había borrado una llave de cierre. Por eso conviene guardar y ejecutar seguido: así se sabe en qué cambio apareció el error.
</details>

Tarjetas para Anki: [repaso-anki.csv](repaso-anki.csv).
