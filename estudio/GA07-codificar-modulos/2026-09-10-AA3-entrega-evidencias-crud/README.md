# Clase GA7 · AA3 · Cómo entregar las evidencias del módulo stand-alone (CRUD completo)

| Dato | Valor |
|---|---|
| Guía | GA7 · Codificar los módulos del software |
| Competencia | 220501096 · Desarrollar la solución de software de acuerdo con el diseño y metodologías de desarrollo |
| Resultado de aprendizaje | 220501096-04 · Codificar el software de acuerdo con el diseño establecido |
| Actividad | GA7-220501096-AA3 · Codificar los módulos del software stand-alone, web y móvil (122 h) |
| Evidencias | **AA3-EV01** (programa) y **AA3-EV02** (Word + video) |
| Fecha de la clase | 2026-09-10 (tomada del nombre del archivo de video) · 25 min |
| Transcripción y acta | En tu PC: `Claude\Projects\Sena\Clases\GA07 - Codificar modulos y versionamiento\` |
| Próxima clase | El miércoles siguiente |

> Clase corta y **la más importante para la nota**: aquí la instructora dijo exactamente qué entregar y cómo. Viene después de la [clase del 2026-09-03](../2026-09-03-AA3-modulo-escritorio-con-base-de-datos/) (el formulario) y la del [2026-09-09](../2026-09-09-AA3-poo-clases-objetos-encapsulamiento/) (POO desde cero).

---

## 1. Resumen en un minuto

1. Mostró el formulario de la clase con el **CRUD completo**: guardar, buscar, modificar y eliminar, comprobando cada cambio en **MySQL Workbench**.
2. Explicó **try-catch**: si algo falla (la red, la base de datos, un dato mal escrito) el programa no se cierra; el error pasa al bloque `catch`. Y `JOptionPane` reemplaza a `System.out.println` cuando hay formulario.
3. **EV01** (el programa): en grupos de **3 o 4**, pero **cada uno la sube con su nombre**. Con comentarios en el código, estándares, Git y basado en el diagrama de clases y los casos de uso.
4. **EV02**: un **video individual** (con presentación personal) y un **Word con normas APA**. Prefiere que el video vaya como **enlace** (YouTube u otro), porque se le llena el disco.
5. Lo que sigue: leer qué es un **framework** y su componente (taller de la AA4, frontend) y luego **servicios web** (la AA5, que el material hace con PHP).

---

## 2. Conceptos de la clase, explicados

### 2.1 Aplicación stand-alone
Una **aplicación de escritorio independiente** que corre en el sistema operativo del usuario (Windows, macOS, Linux) **sin navegador** y sin depender de un servidor web para mostrar la interfaz. En Java: Swing. En Python: **Flet** en modo escritorio (`flet run`), que después se empaqueta con `flet build windows`.

### 2.2 Java Swing y JDBC
- **Swing**: la librería gráfica de Java (ventanas, botones, tablas). Se *importa* porque Java no carga todas sus librerías al inicio; si lo hiciera sería muy lento.
- **JDBC**: la forma en que Java habla con MySQL.
- En Python: **Flet** para la interfaz y **SQLAlchemy + PyMySQL** para la base de datos (ver la [clase del 2026-09-03](../2026-09-03-AA3-modulo-escritorio-con-base-de-datos/)).

### 2.3 try-catch (en Python, try-except)

| Java | Python | Cuándo |
|---|---|---|
| `try { ... }` | `try:` | El código que puede fallar |
| `catch (NumberFormatException e)` | `except ValueError:` | Escribieron letras donde iba un número |
| `catch (SQLException e)` | `except sqlalchemy.exc.SQLAlchemyError` (o `sqlite3.Error`) | Falló la base de datos |
| `finally { con.close(); }` | `finally:` o, mejor, `with Session(engine) as sesion:` | Se ejecuta siempre (cerrar la conexión) |
| `JOptionPane.showMessageDialog(this, "...")` | Un `ft.Text` de color o `ft.SnackBar` en Flet | Avisar al usuario |

La instructora reconoció que en su ejemplo **no validó** que la edad fuera número. La EV02 pide justamente documentar esas validaciones: el ejemplo [01_try_except.py](ejemplos/01_try_except.py) muestra cómo atraparlas y [test_validaciones.py](ejemplos/test_validaciones.py) cómo probarlas.

### 2.4 Del diseño al código
La instructora insistió en que el código "no se hace al azar": sale de los artefactos de las fases anteriores.

| Artefacto | En su ejercicio | En el sistema de reservas |
|---|---|---|
| Diagrama de clases | `Persona`, `Conexion` | `Pasajero`, `Hotel`, `Habitacion`, `Reserva`, `Usuario` |
| Casos de uso | Registrar, consultar, actualizar y eliminar persona | Registrar pasajero, crear reserva, confirmar, cancelar |
| Cada caso de uso = un botón | Registrar → **Guardar** | Crear reserva → botón **Reservar** |
| Historias de usuario | | "Como asesor quiero registrar un pasajero para poder asignarlo a una reserva" |

---

## 3. Lo que se hizo en Java y cómo se hace en Python

| En clase | En Python |
|---|---|
| Botones Guardar, Buscar, Modificar, Eliminar con `PreparedStatement` | [03_formulario_pasajeros.py](../2026-09-03-AA3-modulo-escritorio-con-base-de-datos/ejemplos/03_formulario_pasajeros.py) (ya trae los cuatro) |
| `try-catch` y `JOptionPane` | [01_try_except.py](ejemplos/01_try_except.py) |
| Revisar en Workbench que los datos cambiaron | Igual, o con `SELECT * FROM pasajeros;` |
| Comentarios en el código (los de ella quedaron en inglés; pide que los nuestros expliquen cada parte) | Docstrings y comentarios en español, como en los ejemplos |
| Exportar el proyecto a ZIP | Comprimir la carpeta sin `.venv`, `__pycache__` ni `*.db` |

---

## 4. Evidencias: qué entregar (lo que dijo la instructora + la guía)

### AA3-EV01 · Codificación del módulo (desempeño)
- [ ] Un programa con **CRUD** conectado a la base de datos (el modelo es su formulario de personas).
- [ ] Basado en el **diagrama de clases, casos de uso, historias de usuario y prototipos** ya hechos.
- [ ] **Comentarios** en el código: dónde empieza el constructor, dónde los getters y setters, qué hace cada botón.
- [ ] **Estándares de codificación** y **Git** (hacer commits mientras se avanza; "es una copia de seguridad").
- [ ] **Grupos de 3 o 4**, pero **cada integrante la sube** con su nombre: `NOMBRE_APELLIDO_AA3_EV01.zip` con el proyecto y un archivo con el enlace del repositorio.
- [ ] Si es en Python: **pantallazos del código** dentro del ZIP.

### AA3-EV02 · Módulo codificado y probado (producto)
- [ ] **Video individual** ("cada quien debe hacerme el video"), mejor como **enlace**. Guion sugerido en la sección 4.1.
- [ ] **Documento Word** con portada, introducción, objetivo y **normas APA**. Estructura sugerida en la sección 4.2.
- [ ] Un **pantallazo por historia de usuario o caso de uso** y las **pruebas de validación** (fechas, números, textos, caracteres especiales, longitudes).
- [ ] ZIP `NOMBRE_APELLIDO_AA3_EV02` con el proyecto, el Word, el video o su enlace y el enlace del repositorio.

### 4.1 Guion del video (basado en el ejemplo que dio la instructora)
1. **Saludo y presentación:** "Cordial saludo, estimada instructora. Mi nombre es ___, de la ficha ___. A continuación presento la evidencia GA7-220501096-AA3-EV02."
2. **Qué es:** "Demostración funcional del módulo de gestión de pasajeros del sistema de reservas: una aplicación de escritorio stand-alone desarrollada en **Python con Flet**, conectada a **MySQL**, con control de versiones en **Git**."
3. **Ejecución:** abrir la app; **guardar** un pasajero; **buscar**; **modificar**; **eliminar**.
4. **Persistencia:** después de cada operación, mostrar la tabla en **MySQL Workbench** (refrescar el esquema).
5. **Validaciones:** intentar guardar con edad en letras, documento repetido, nombre vacío o con símbolos, y mostrar el mensaje de error.
6. **Versionamiento:** mostrar `git log --oneline` o el repositorio en GitHub.
7. **Cierre:** "Con esto se demuestra que el módulo cumple los requisitos de la guía."

### 4.2 Estructura del Word de la EV02
| Sección | Qué va |
|---|---|
| Portada | Título, evidencia, integrantes, ficha, instructora, fecha (APA 7) |
| Introducción | Qué módulo es y para qué sirve en el sistema de reservas |
| Objetivo | "Verificar que el módulo de pasajeros cumple las historias de usuario..." |
| Historias de usuario / casos de uso | Una por página: texto de la historia y debajo el pantallazo de la pantalla |
| Pruebas de validación | Tabla: campo, dato de prueba, resultado esperado, resultado obtenido. **Copiar las filas de [test_validaciones.py](ejemplos/test_validaciones.py)** y el pantallazo de `pytest -v` en verde |
| Enlaces | Repositorio y video |
| Referencias | En APA |

---

## 5. Aplicación al proyecto de reservas

| Historia de usuario | Pantalla | Validación que documentar |
|---|---|---|
| Como asesor quiero registrar un pasajero | Formulario de pasajeros: Guardar | Documento solo números, 5 a 12 dígitos; nombre sin símbolos; edad 0 a 120 |
| Como asesor quiero buscar un pasajero por documento | Buscar | Documento inexistente muestra mensaje |
| Como asesor quiero corregir los datos de un pasajero | Modificar | No deja dejar el nombre vacío |
| Como administrador quiero eliminar un pasajero duplicado | Eliminar | Pide confirmación (sugerencia: `ft.AlertDialog`) |
| Como asesor quiero crear una reserva | (siguiente módulo) | Entrada no anterior a hoy; salida después de entrada; máximo 30 noches |

**En la vida real:** Booking no deja reservar con la fecha de salida antes de la de entrada y Travel Compositor rechaza documentos con letras para pasajeros colombianos. Son exactamente las reglas de [validaciones.py](ejemplos/validaciones.py).

---

## 6. Qué estudiar

| Sesión | Tema | Recurso | Práctica |
|---|---|---|---|
| 1 | Manejo de errores | [Tutorial de Python, cap. 8 Errores y excepciones](https://docs.python.org/es/3/tutorial/errors.html) | Ejemplo 01 y agregar `except` en el formulario |
| 2 | Pruebas con pytest | [Documentación de pytest](https://docs.pytest.org/) · Platzi: [Unit Testing en Python](https://platzi.com/cursos/unit-testing-python/) | Agregar casos a `test_validaciones.py` |
| 3 | Normas APA 7 | Guía APA de tu biblioteca o Word (*Referencias > Estilo APA*) | Portada y referencias del Word de la EV02 |
| 4 | Qué es un framework (lo que pidió leer) | Material de formación de la AA4 · [FastAPI](https://fastapi.tiangolo.com/es/) como ejemplo en Python | Resumen de una página para el taller |

---

## 7. Ejemplos de código

| Archivo | Qué enseña |
|---|---|
| [01_try_except.py](ejemplos/01_try_except.py) | `try` / `except` con errores de dato, de llave repetida y de base de datos |
| [validaciones.py](ejemplos/validaciones.py) | Reglas de validación del módulo (documento, nombre, edad, correo, fechas) |
| [test_validaciones.py](ejemplos/test_validaciones.py) | 28 casos de prueba con pytest: la tabla de pruebas para el Word |

### Cómo correrlos
```
cd "estudio\GA07-codificar-modulos\2026-09-10-AA3-entrega-evidencias-crud\ejemplos"
python 01_try_except.py
pip install pytest
pytest -v test_validaciones.py
```

### El código parte por parte (01_try_except.py)
1. `try:` encierra lo que puede fallar: convertir la edad con `int()` y hacer el `INSERT`.
2. `except ValueError`: si la edad no es número. Es el `NumberFormatException` de Java.
3. `except sqlite3.IntegrityError`: si el documento ya existe (llave primaria repetida).
4. `except sqlite3.Error`: cualquier otro problema con la base de datos, como la conexión cerrada que se prueba al final.
5. Los `?` en el `INSERT` evitan la **inyección SQL**; en Java es el `PreparedStatement` con `?`.

### El código parte por parte (validaciones.py y test_validaciones.py)
1. Cada `validar_...` devuelve `""` si está bien o el texto del error. Así el formulario solo muestra lo que devuelve.
2. `LETRAS_Y_ESPACIOS` es una **expresión regular**: acepta letras con tilde, ñ, apóstrofo y espacios, y rechaza números y símbolos.
3. `validar_fechas` recibe `hoy` como parámetro para que las pruebas no dependan del día en que se corren.
4. `@pytest.mark.parametrize` convierte cada tupla en un caso de prueba distinto. `pytest -v` los lista uno por uno con *PASSED*: ese pantallazo va al Word.

---

## 8. Repaso

<details><summary>1. ¿Qué es una aplicación stand-alone?</summary>
Una aplicación de escritorio que corre en el sistema operativo del usuario sin navegador ni servidor web para su interfaz.
</details>

<details><summary>2. ¿Para qué sirve try-catch?</summary>
Para que, si una operación falla (red, base de datos, dato mal escrito), el programa no se cierre: el error pasa al bloque catch, que lo maneja.
</details>

<details><summary>3. ¿Qué reemplaza a System.out.println cuando se trabaja con formulario en Swing?</summary>
JOptionPane.showMessageDialog, que muestra un cuadro de diálogo.
</details>

<details><summary>4. ¿La AA3-EV01 es individual o en grupo?</summary>
Se hace en grupos de 3 o 4, pero cada integrante la sube con su nombre.
</details>

<details><summary>5. ¿Y el video de la EV02?</summary>
Individual, con presentación personal, y preferiblemente entregado como enlace.
</details>

<details><summary>6. ¿Qué validaciones pide documentar la guía en la EV02?</summary>
Fechas, números, textos, caracteres especiales y longitudes.
</details>

<details><summary>7. ¿Qué artefactos de las fases anteriores debe seguir el código?</summary>
Diagrama de clases, casos de uso, historias de usuario, diseños y prototipos, y el informe técnico del plan de trabajo.
</details>

<details><summary>8. ¿Qué sigue después de esta actividad?</summary>
Leer qué es un framework para el taller de componentes frontend (AA4) y luego servicios web (AA5).
</details>

Tarjetas para Anki: [repaso-anki.csv](repaso-anki.csv).
