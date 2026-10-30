# Guía explicada del módulo de pasajeros

Esta guía va de lo simple a lo complejo. Primero la idea general, luego cada archivo en el orden en que conviene estudiarlos (cada uno usa el anterior) y al final el recorrido completo de un clic. El código solo tiene comentarios donde algo no es obvio; la explicación completa de cada parte está aquí.

Tiempo sugerido: 6 pomodoros de 25 minutos, uno por cada parte numerada del 1 al 6.

---

## 0. La idea general en una analogía

Piensa en cómo funciona una hoja de reservas de HyD en Google Sheets con Apps Script:

| En Google Workspace | En este módulo | Archivo |
|---|---|---|
| La hoja de cálculo con sus columnas | Tabla `pasajeros` en MySQL | `crear_bd_hyd.sql` |
| `SpreadsheetApp.openById(ID)` | Abrir conexión | `conexion.py` |
| Una fila como objeto `{nombre:..., ...}` | Clase `Pasajero` | `modelo.py` |
| Validación de datos de la hoja (regla "solo números") | Funciones `validar_...` | `validaciones.py` |
| `getRange().getValues()` / `setValues()` / `deleteRow()` | `listar`, `crear`, `actualizar`, `eliminar` | `repositorio.py` |
| Formulario HTML de HtmlService o AppSheet | Ventana Tkinter | `interfaz.py` |
| La función que se ejecuta al abrir | `main()` | `main.py` |

Cada archivo tiene **una sola responsabilidad**. A eso se le llama separación por capas, y es lo que permite que si mañana cambias MySQL por PostgreSQL (Supabase) solo toques `repositorio.py` y `conexion.py`; la ventana ni se entera.

```
 Usuario
   │ hace clic
   ▼
 interfaz.py ──► validaciones.py ──► modelo.py (crea un Pasajero)
   │
   ▼
 repositorio.py ──► conexion.py ──► MySQL
```

La flecha solo va hacia abajo: la base de datos no sabe que existe una ventana y la ventana no escribe SQL.

---

## 1. La base de datos: `base_datos/crear_bd_hyd.sql`

Es lo primero porque sin tabla no hay dónde guardar.

**`SET NAMES utf8mb4`** le dice a MySQL que el texto del script viene en UTF-8. Sin esto, en algunas consolas "Panamá" se guarda como "PanamÃ¡". Lo descubrimos probando: es un bug real que te puede pasar.

**`CREATE DATABASE IF NOT EXISTS`**: el `IF NOT EXISTS` hace que el script se pueda correr varias veces sin error. Es como el `if (!hoja) crearHoja()` que haces en Apps Script.

**`id_pasajero INT UNSIGNED AUTO_INCREMENT`** es la llave primaria técnica. `UNSIGNED` = sin negativos; `AUTO_INCREMENT` = MySQL pone 1, 2, 3 solo. ¿Por qué no usar el documento como llave primaria? Porque un documento puede cambiar (alguien pasa de TI a CC al cumplir 18) y si fuera llave primaria tendrías que actualizarlo en todas las tablas que lo referencian (reservas, pagos). El número interno nunca cambia.

**`CONSTRAINT uq_pasajeros_documento UNIQUE (numero_documento)`**: aunque el documento no sea llave primaria, no puede repetirse. La regla vive en la base de datos, así que aunque la app tenga un bug, MySQL lo impide. Es tu última línea de defensa.

**`ENUM('CC','CE','TI','PA')`** limita los valores posibles, como una lista desplegable en Sheets.

**`fecha_modificacion ... ON UPDATE CURRENT_TIMESTAMP`**: MySQL actualiza esa columna solo cada vez que cambias la fila. Es la semilla de tus "novedades contables": saber cuándo se tocó un registro.

**Usuario `hyd_app` con `GRANT SELECT, INSERT, UPDATE, DELETE`**: principio de mínimo privilegio. La app no puede borrar tablas ni crear usuarios, solo trabajar con filas. Si alguien roba la clave del `.env`, el daño es limitado. Nunca conectes una app como `root`.

**`INSERT IGNORE`**: si la fila ya existe (choca con la UNIQUE), la ignora en vez de fallar.

---

## 2. La conexión: `pasajeros/conexion.py`

**Orden de los `import`** (PEP 8): primero librería estándar (`os`), luego terceros (`pymysql`, `dotenv`), luego tus propios módulos. Separados por una línea en blanco. Ruff lo revisa con la regla `I`.

**`load_dotenv()`** lee el archivo `.env` y convierte cada línea `CLAVE=valor` en variable de entorno. ¿Por qué no escribir la clave en el código? Porque el código va a GitHub y el `.env` no (está en `.gitignore`). Es la misma idea que guardar el token de tu API de Apps Script en `PropertiesService` y no en el código.

**`os.getenv("DB_HOST", "localhost")`**: lee la variable y, si no existe, usa el segundo valor.

**`int(os.getenv("DB_PORT", "3306"))`**: todo lo que viene del `.env` es texto; MySQL necesita el puerto como número.

**`cursorclass=DictCursor`**: cada fila llega como `{"nombre": "Ana", ...}` en vez de `("Ana", ...)`. Lees por nombre de columna y no por posición, así que si alguien reordena las columnas el código no se rompe.

**`autocommit=False`**: los cambios quedan "en borrador" hasta que llamas `commit()`. Te da control: si una operación de varios pasos falla a la mitad, no queda nada guardado a medias.

**`client_flag=CLIENT.FOUND_ROWS`**: este lo agregamos por un bug que encontramos al pensar las pruebas. Sin él, si el asesor pulsa "Modificar" sin cambiar nada, MySQL responde "0 filas cambiadas" y la app diría "el pasajero no existe". Con `FOUND_ROWS` responde "1 fila encontrada". Hay una prueba automática (`test_actualizar_sin_cambios_reporta_existente`) que protege este caso.

**El `-> pymysql.connections.Connection`** después de los paréntesis es una *anotación de tipo*: documenta qué devuelve la función. Python no la obliga, pero el editor (VS Code) la usa para autocompletar.

**El texto entre `"""` triples** es un *docstring*: la documentación oficial de la función (PEP 257). Usamos el estilo Google con secciones `Args`, `Returns` y `Raises`.

---

## 3. El modelo: `pasajeros/modelo.py`

**`@dataclass`** es un decorador: una etiqueta que le agrega superpoderes a la clase. Tú solo declaras los atributos (`nombre: str`) y Python escribe por ti el constructor `__init__`, el `__repr__` (cómo se imprime) y el `__eq__` (cómo se comparan dos pasajeros). En Java tendrías que escribir constructor, getters y setters a mano.

¿Y los getters y setters? En Python no se usan por defecto: los atributos se leen directo (`pasajero.nombre`). Si algún día necesitas lógica al asignar, se usa `@property`. Es la filosofía "somos adultos responsables" de Python.

**`id_pasajero: int | None = None`** va al final porque tiene valor por defecto. Regla de Python: primero los obligatorios, luego los opcionales. `int | None` significa "un entero o nada"; vale `None` mientras el pasajero no se haya guardado.

**`fecha_nacimiento: date`**: guardamos una fecha real, no un texto. Así podemos restar fechas y calcular la edad.

**`edad(self, hoy=None)`**: recibe `hoy` como parámetro opcional. ¿Por qué? Para poder probarlo. Si siempre usara `date.today()`, una prueba que hoy pasa podría fallar el año entrante. En las pruebas le pasamos una fecha fija.

El truco `anios - (not cumplio)`: en Python `True` vale 1 y `False` vale 0. Si no ha cumplido años este año, `not cumplio` es `True` y se resta 1.

**`(hoy.month, hoy.day) >= (mes, día)`**: Python compara tuplas elemento por elemento, primero el mes y si empata, el día. Es como ordenar una columna en Sheets por dos criterios.

**`__str__`** define qué se ve al hacer `print(pasajero)`. Los métodos con doble guion bajo se llaman "métodos mágicos" o *dunder*.

---

## 4. Las validaciones: `pasajeros/validaciones.py`

Aquí está la lógica de negocio, y por eso es el archivo con más pruebas.

**Constantes en MAYÚSCULAS** al inicio. Si mañana HyD decide que el nombre admite 60 caracteres, se cambia en un solo lugar.

**Expresiones regulares (`re.compile`)**: son patrones para revisar texto. `^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$` se lee: "desde el inicio (`^`) hasta el final (`$`), uno o más (`+`) caracteres de esta lista (`[...]`)". Si aparece un `@` o un `5`, no cumple. `re.compile` lo prepara una sola vez para reusarlo.

**Patrón de cada función**: recibe texto, lo limpia, revisa y **devuelve el valor limpio o lanza `ValueError`**. ¿Por qué lanzar errores y no devolver `True/False`? Porque el error viaja con el mensaje para el usuario, y la interfaz solo tiene que atraparlo con `try/except` y mostrarlo. Es exactamente el `try-catch` que explicó la instructora con `JOptionPane`.

**`" ".join(valor.split())`**: `split()` sin argumentos corta por cualquier cantidad de espacios y descarta los vacíos; `" ".join` los vuelve a unir con un solo espacio. Resultado: `"  Ana   María "` queda `"Ana María"`. Es el `TRIM()` de Sheets mejorado.

**Comparación encadenada `5 <= len(x) <= 12`**: Python permite escribirla como en matemáticas.

**`validar_numero_documento` depende del tipo**: CC, CE y TI solo dígitos; pasaporte acepta letras. Por eso recibe dos parámetros. También quita puntos: los asesores escriben `1.020.304.050`.

**`validar_fecha_nacimiento`** usa `datetime.strptime(texto, "%Y-%m-%d")`: convierte texto en fecha según el formato. Si el texto es `"2001-02-30"` (no existe el 30 de febrero), Python lanza `ValueError` solo. Lo atrapamos y lanzamos uno nuevo con un mensaje amable; `from None` oculta el error técnico original.

**`validar_pasajero`** es la función "director de orquesta": llama a todas las demás en orden y arma el `Pasajero`. Al final revisa la **regla que cruza dos campos**: la TI es para menores y la CC para mayores. No se puede revisar antes porque necesita el tipo y la fecha ya validados.

**`datos.get("nombre", "")`**: si la llave no existe, devuelve `""` en vez de reventar con `KeyError`.

---

## 5. El repositorio: `pasajeros/repositorio.py`

Es el único archivo que habla SQL.

**Los `%s` son marcadores de posición**, como los `?` del `PreparedStatement` de Java. PyMySQL reemplaza cada `%s` por el valor de forma segura. Esto evita la **inyección SQL**: si alguien escribe `' OR '1'='1` en el formulario y armaras el SQL pegando textos con f-string, podría ver o borrar toda la tabla. Con `%s` ese texto se trata como un dato inofensivo. Regla de oro: **nunca** f-strings con valores del usuario dentro de SQL. (Las f-strings de `SQL_BUSCAR` solo pegan la constante `COLUMNAS`, que escribimos nosotros, nunca el usuario.)

**`with obtener_conexion() as conexion:`** abre la conexión y la cierra sola al salir del bloque, aunque haya error. Es el `try-finally { con.close(); }` de Java en una línea.

**`with conexion.cursor() as cursor:`**: el cursor es quien envía SQL y trae resultados.

**`cursor.execute(SQL, (valor,))`**: la coma en `(valor,)` es obligatoria. `(valor)` es solo un texto entre paréntesis; `(valor,)` es una tupla de un elemento.

**`fetchone()` vs `fetchall()`**: uno trae la primera fila (o `None`), el otro todas en una lista.

**`conexion.commit()`**: solo aquí el cambio queda guardado. Sin `commit`, el `INSERT` se pierde al cerrar.

**`except pymysql.err.IntegrityError`** con código `1062`: así sabemos que se violó la UNIQUE (documento repetido) y lo traducimos a un `ValueError` entendible. `raise ... from error` conserva el error original para depurar.

**`Pasajero(**fila)`**: los dos asteriscos "desempacan" el diccionario; cada llave se vuelve un argumento con nombre. Funciona porque las columnas del `SELECT` se llaman igual que los atributos. Por eso elegimos los mismos nombres en SQL y en Python.

**`_fila_a_pasajero` con guion bajo**: convención de "uso interno", lo más parecido a `private`.

**`return filas_afectadas > 0`**: `execute()` devuelve cuántas filas tocó el `WHERE`. Si es 0, el documento no existe, y devolvemos `False` para que la interfaz lo diga.

**List comprehension `[_fila_a_pasajero(f) for f in filas]`**: crea una lista nueva aplicando la función a cada fila. Equivale al `.map()` de JavaScript/Apps Script.

---

## 6. La interfaz: `pasajeros/interfaz.py`

**`class VentanaPasajeros(tk.Tk)`**: la clase *hereda* de `tk.Tk`, o sea, "es una ventana". Como `extends JFrame`.

**`super().__init__()`** ejecuta el constructor del padre. Sin él, la ventana no existe.

**El constructor solo llama métodos `_crear_...`**: cada parte de la pantalla se arma en su método. Es más fácil de leer que 150 líneas seguidas, y es lo que pide el estándar (funciones cortas, una responsabilidad).

**`self.entradas` es un diccionario de cajas**: en vez de tener `self.txt_nombre`, `self.txt_apellido`... guardamos todas por su llave. Así leemos el formulario con un ciclo:

```python
{llave: caja.get() for llave, caja in self.entradas.items()}
```

y el resultado es exactamente el diccionario que espera `validar_pasajero`. Usar las mismas llaves en todas las capas es lo que hace que todo encaje sin traducir.

**`CAMPOS` y `COLUMNAS_TABLA` como tuplas constantes**: la pantalla se *genera* desde datos. Si mañana agregas "nacionalidad", agregas una línea y no diez.

**`divmod(indice, 2)`** reparte los 8 campos en 4 filas y 2 columnas: `divmod(5, 2) = (2, 1)` = fila 2, columna 1.

**`grid` vs `pack`**: `pack` apila elementos (arriba hacia abajo); `grid` los pone en cuadrícula (fila, columna), como una hoja de cálculo. Usamos `grid` dentro del formulario y `pack` para las secciones grandes. Nunca mezcles los dos dentro del mismo contenedor.

**`ttk.Combobox(state="readonly")`** obliga a escoger una opción: es validación desde la interfaz.

**`command=self.guardar` sin paréntesis**: le entregas la función para que Tkinter la llame al hacer clic. Con paréntesis la ejecutarías ya, al construir la ventana.

**Los métodos de los botones siguen siempre el mismo esquema**:

```python
try:
    pasajero = validar_pasajero(self._leer_formulario())
    repositorio.crear(pasajero)
except ValueError as error:  # dato malo o regla de negocio
    messagebox.showwarning(...)
    return
except pymysql.MySQLError:  # MySQL apagado o clave mala
    messagebox.showerror(...)
    return
messagebox.showinfo(...)  # todo salió bien
```

Dos tipos de error, dos mensajes distintos. El programa nunca se cierra de golpe.

**`messagebox.askyesno`** antes de eliminar: borrar no tiene "deshacer", así que siempre se pide confirmación. Es una regla de usabilidad que vimos en GA5.

**`self.tabla.bind("<<TreeviewSelect>>", ...)`** conecta el evento "clic en una fila" con un método: al seleccionar, se carga el pasajero en el formulario. Es como un `onEdit` de Apps Script: una función que reacciona a algo que hace el usuario.

**`self.tabla.delete(*self.tabla.get_children())`**: el asterisco entrega cada fila como argumento separado. Borra todas las filas visibles antes de volver a llenar.

**`getattr(pasajero, llave)`** lee un atributo usando su nombre como texto. Así un solo ciclo llena todas las columnas.

**`tk.StringVar`** para la barra de estado: es una variable "observada". Cuando haces `.set("texto")`, la etiqueta se actualiza sola.

---

## 7. El arranque: `main.py`

**`if __name__ == "__main__":`** es verdadero solo cuando ejecutas `python main.py`, no cuando otro archivo hace `import main`. Es el `public static void main` de Java.

**`ventana.mainloop()`** es un ciclo infinito que espera clics y teclas hasta que cierras la ventana.

---

## 8. Las pruebas: `tests/`

**`test_validaciones.py` (31 pruebas unitarias)** prueba cada regla sin tocar la base de datos. Están agrupadas en clases según lo que pide la EV02: textos, caracteres especiales, longitudes, números, fechas y correo.

`assertEqual(a, b)` falla si son distintos. `with self.assertRaises(ValueError):` falla si el bloque **no** lanza el error. `subTest` prueba varios valores malos en una sola prueba y te dice cuál falló.

`HOY = date(2026, 10, 28)` es una fecha fija: así la prueba de edad da 36 siempre, sin importar cuándo la corras.

`datos_validos(**cambios)` arma un formulario perfecto y cambia solo un campo. Cada prueba rompe una sola cosa: si falla, sabes exactamente qué regla está mal.

**`test_repositorio.py` (7 pruebas de integración)** sí escribe en MySQL. `setUp` se ejecuta antes de cada prueba y `tearDown` después: limpian el documento de prueba `99999999` para que no queden residuos. `@unittest.skipUnless(hay_base_de_datos(), ...)` las salta si MySQL está apagado, en vez de fallar.

Resultado esperado: `Ran 38 tests ... OK`.

---

## 9. Recorrido completo de un clic en "Guardar"

1. El asesor llena el formulario y hace clic. Tkinter llama `VentanaPasajeros.guardar()`.
2. `_leer_formulario()` arma `{"nombre": "Carlos Andrés", ..., "fecha_nacimiento": "1992-08-21"}` (todo texto).
3. `validar_pasajero()` limpia y revisa campo por campo. Si algo falla, lanza `ValueError("El campo nombre solo admite letras...")`, el `except ValueError` lo atrapa y aparece la ventana amarilla. Fin.
4. Si todo está bien, devuelve un `Pasajero` con `fecha_nacimiento=date(1992, 8, 21)` y el documento sin puntos.
5. `repositorio.crear(pasajero)` abre conexión, ejecuta el `INSERT` con `%s`, hace `commit` y cierra.
6. Si el documento ya existía, MySQL responde error 1062, se convierte en `ValueError("Ya existe...")` y vuelve al paso 3.
7. Si todo salió bien: ventana azul de confirmación, se limpia el formulario y `refrescar_tabla()` hace un `SELECT` y redibuja la tabla.

---

## 10. Estándares de codificación aplicados (PEP 8)

| Regla PEP 8 | Dónde se ve |
|---|---|
| Máximo 79 caracteres por línea | Todo el código (`line-length = 79`) |
| `snake_case` para funciones y variables | `validar_correo`, `numero_documento` |
| `PascalCase` para clases | `Pasajero`, `VentanaPasajeros` |
| `MAYUSCULAS` para constantes | `TIPOS_DOCUMENTO`, `SQL_INSERTAR` |
| `_prefijo` para uso interno | `_fila_a_pasajero`, `_crear_tabla` |
| Imports ordenados en 3 grupos | Inicio de cada archivo |
| 4 espacios de sangría, nunca tabulaciones | Todo el código |
| Dos líneas en blanco entre funciones de nivel superior | Todo el código |
| Docstrings en módulos, clases y funciones (PEP 257) | Todo el código |
| Identificadores ASCII | `anios` en lugar de `años` |

Para comprobarlo: `ruff check .` debe responder `All checks passed!` y `ruff format --check .` no debe pedir cambios.

---

## 11. Versionamiento con Git (paso a paso)

Desde la carpeta del repositorio `proyecto ADSO GRUPO 1`:

```powershell
git status                                  # ver qué cambió
git add modulo_pasajeros                    # preparar SOLO el módulo
git status                                  # confirmar que .env NO aparece
git commit -m "feat(pasajeros): CRUD de pasajeros con Tkinter y MySQL"
git push origin main
```

Si en `git status` aparece `.env`, detente: revisa que el `.gitignore` esté en la carpeta. Los mensajes de commit siguen la convención *Conventional Commits* (`feat:`, `fix:`, `docs:`, `test:`), que deja el historial legible para el instructor.

Commits sugeridos si quieres mostrar el avance por partes (mejor práctica que uno solo gigante):

```
feat(bd): script de creación de la tabla pasajeros
feat(pasajeros): modelo y validaciones
feat(pasajeros): repositorio CRUD con PyMySQL
feat(pasajeros): interfaz Tkinter
test(pasajeros): pruebas unitarias y de integración
docs(pasajeros): README y guía explicada
```

---

## 12. Retos para practicar (cuando lo entiendas todo)

Nivel 1: agrega el campo `genero` (SQL, modelo, validación, interfaz, prueba). Te obliga a tocar todas las capas.

Nivel 2: agrega un botón "Buscar por apellido" que use `LIKE %s` y muestre los resultados en la tabla.

Nivel 3: crea una tabla `novedades_pasajeros` que guarde cada modificación (quién, cuándo, valor anterior, valor nuevo). Es tu proceso de novedades contables en pequeño.
