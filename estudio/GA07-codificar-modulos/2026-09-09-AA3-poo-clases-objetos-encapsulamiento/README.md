# Clase GA7 · AA3 · Programación orientada a objetos desde cero

| Dato | Valor |
|---|---|
| Guía | GA7 · Codificar los módulos del software |
| Competencia | 220501096 · Desarrollar la solución de software de acuerdo con el diseño y metodologías de desarrollo |
| Resultado de aprendizaje | 220501096-04 · Codificar el software de acuerdo con el diseño establecido |
| Actividad | GA7-220501096-AA3 · Codificar los módulos del software stand-alone, web y móvil (122 h). La instructora la nombró así: "guía 7, actividad 3, evidencia 1" |
| Evidencias | AA3-EV01 y AA3-EV02 (se explican en la clase del 2026-09-10) |
| Fecha de la clase | 2026-09-09 (tomada del nombre del archivo de video) · 1 h 18 min |
| Transcripción y acta | En tu PC: `Claude\Projects\Sena\Clases\GA07 - Codificar modulos y versionamiento\` |
| Plazo dicho en clase | El cronograma dice que la competencia cierra "el 31"; la instructora dijo que no alcanza y que hay que avanzar rápido |

> **Python sigue permitido, y ahora en grupo.** La instructora aceptó **grupos de 3 o 4**, pero pidió que **cada integrante suba el archivo**. Si es Java lo abre directo; **si es Python, hay que pegar pantallazos** de los ejercicios.

Esta clase repite desde cero lo que el grupo pidió en la clase anterior. Si ya leíste la [clase del 2026-09-03](../2026-09-03-AA3-modulo-escritorio-con-base-de-datos/), aquí están los mismos conceptos más despacio y con el ejercicio completo.

---

## 1. Resumen en un minuto

1. Teoría de POO con ejemplos cotidianos (un carro, un celular): **clase, objeto, estado, comportamiento, constructor y encapsulamiento**.
2. Tipos de datos de Java: `int`, `double`, `boolean`, `char` y `String`.
3. Ejercicio en NetBeans: clase `Persona` (nombre, edad) con constructor, getters, setters **con validación**, un método `saludar()`, y la clase `Main` que crea `new Persona("Carlos", 25)`, prueba el setter con `-50` y modifica a "Carlos Alberto" de 26.
4. Mostró cómo crear la base de datos y la tabla en **MySQL Workbench** (VARCHAR, llave primaria) y la clase de conexión que está terminando: el CRUD con buscar, guardar, modificar y eliminar llega en la clase siguiente.
5. Las evidencias serán **en grupos de 3 o 4**; las explica en la clase siguiente.

---

## 2. Conceptos de la clase, explicados

### 2.1 Los seis conceptos

| Concepto | Definición de la clase | Ejemplo cotidiano (clase) | Ejemplo del sistema de reservas |
|---|---|---|---|
| **Clase** | El molde o plano. Define qué datos y acciones tendrán los objetos. No ocupa memoria con datos | El plano de una casa | `Habitacion` |
| **Objeto** | La instancia concreta, creada en memoria con `new` | La casa construida | `h101 = Habitacion("101", "Estándar", 250000)` |
| **Estado** | Los atributos: lo que el objeto "sabe" de sí | Color rojo, velocidad, gasolina | número, tipo, tarifa, ocupada |
| **Comportamiento** | Los métodos: lo que el objeto "sabe hacer" | Arrancar, frenar | `ocupar()`, `liberar()`, `cotizar(noches)` |
| **Constructor** | El método especial que inicializa el objeto. Mismo nombre de la clase, sin tipo de retorno, se activa con `new`. Garantiza que ningún objeto "nazca incompleto" | | `__init__` en Python |
| **Encapsulamiento** | Atributos `private` + métodos públicos (getters y setters) con reglas. Evita que código externo modifique el estado sin validación | El nivel de batería no puede ser 150 % | La tarifa no puede ser negativa |

En tu mundo de HyD: la **plantilla** de una reserva en Travel Compositor es la clase; cada reserva con su código es un objeto; las reglas que no dejan confirmar sin pasajeros son el encapsulamiento.

### 2.2 Tipos de datos

| Java | Qué guarda | Python | Ejemplo |
|---|---|---|---|
| `int` | Enteros | `int` | noches = 3 |
| `double` | Decimales | `float` | tarifa = 250000.0 |
| `boolean` | `true` o `false` | `bool` (`True` / `False`, con mayúscula) | ocupada = False |
| `char` | Un solo símbolo (`'A'`) | No existe: se usa `str` de un carácter | categoria = "A" |
| `String` | Texto | `str` | tipo = "Suite" |
| `VARCHAR` (en MySQL) | Texto en la base de datos | `String(80)` en SQLAlchemy | |

En Java hay que **declarar** el tipo (`int edad;`). En Python no es obligatorio, pero lo escribimos como *type hint* (`edad: int`) para que se entienda y Ruff ayude.

### 2.3 `public`, `private` y `void`

| Java | Significado | Python |
|---|---|---|
| `private String nombre;` | Solo se usa dentro de esta clase | `self._nombre` (guion bajo: privado por convención) |
| `public` | Otras clases lo pueden usar | Sin guion bajo |
| `void` | "Haz tu trabajo, pero no me devuelvas nada" | `-> None` |
| `public String getNombre()` | Devuelve un valor | `def get_nombre(self) -> str:` o una `@property` |
| `System.out.println(...)` | Imprimir en la consola | `print(...)` |
| `"Hola " + nombre + " tengo " + edad` | Concatenar | `"Hola " + nombre + " tengo " + str(edad)` o mejor `f"Hola {nombre}, tengo {edad}"` |
| `Scanner` para leer del teclado | Pedir datos | `input()` (siempre devuelve texto: convertir con `int()`) |

La pregunta de clase *"¿cuál sería el input, como en Python?"*: en el ejercicio de la instructora los datos se escriben en el código (`new Persona("Carlos", 25)`); en un programa real vienen del **formulario** (clase anterior) o del teclado (`Scanner` en Java, `input()` en Python). El ejemplo 02 muestra las dos formas.

### 2.4 Errores que salieron en clase (y cómo evitarlos)
| Error | Causa | En Python |
|---|---|---|
| Faltaba un paréntesis en el `if` | `if (nuevoNombre != null` sin cerrar | Python no usa paréntesis en el `if`: `if nuevo_nombre:` |
| Faltaba `null` en la condición | Escribió `!= ` sin nada | En Python es `is not None` |
| El saludo no mostraba la edad | Faltó un `+` para unir texto y número | Con f-strings no pasa: `f"tengo {edad} años"` |
| Falta `;` al final | Toda sentencia de Java termina en punto y coma | Python no usa punto y coma |

---

## 3. Lo que se hizo en Java y cómo se hace en Python

| En clase (NetBeans) | En Python |
|---|---|
| Proyecto *Java with Ant* con la clase `Main` marcada | Un archivo `.py` con `if __name__ == "__main__":` |
| Clase `Persona` en su archivo | Clase en el mismo archivo o en `modelos/persona.py` |
| *Insertar código > Constructor* | `def __init__(self, nombre, edad):` |
| *Insertar código > Getter y Setter* | `@property` (forma recomendada) o `get_`/`set_` (forma literal, ejemplo 02) |
| `if (...) {...} else { System.out.println("Error...") }` | `if ...: ... else: print("Error...")` |
| `Persona p1 = new Persona("Carlos", 25);` | `p1 = Persona("Carlos", 25)` |
| Crear base y tabla en Workbench | Igual, o con el script de la [clase anterior](../2026-09-03-AA3-modulo-escritorio-con-base-de-datos/ejemplos/04_crear_bd_mysql.sql) |

---

## 4. Evidencias

La instructora las explicó en la clase siguiente (2026-09-10). Lo que sí quedó claro:

- [ ] **En grupos de 3 o 4**, pero **cada integrante sube** el archivo a la plataforma.
- [ ] Si es en Python: **pantallazos del código y de la ejecución**. Sugerencia: pegar el código de los ejemplos 01 y 02 corriendo, con la salida de la consola.
- [ ] Ella pidió **comentarios** en el código explicando cada parte ("aquí declaro la variable, el rango es de 0 a 100"). Los ejemplos ya los traen.
- [ ] La explicación completa de la entrega está en la [clase del 2026-09-10](../2026-09-10-AA3-entrega-evidencias-crud/).

> Pregúntale a la instructora: si con grupos de 3 o 4 cada uno sube **el mismo ZIP** o una parte distinta.

---

## 5. Aplicación al proyecto de reservas

| Clase del repo | Estado (atributos) | Comportamiento (métodos) | Regla de encapsulamiento |
|---|---|---|---|
| `Habitacion` | número, tipo, tarifa, ocupada | `ocupar()`, `liberar()`, `cotizar(noches)` | Tarifa mayor que cero |
| `Pasajero` | documento, nombre, edad, género | `es_menor()` | Edad entre 0 y 120 |
| `Reserva` | código, fechas, estado, pasajeros | `confirmar()`, `cancelar()`, `calcular_total()` | No confirmar una cancelada; salida después de entrada |
| `Usuario` | usuario, rol, contraseña (hash) | `verificar_clave()` | La contraseña nunca se lee en texto plano |
| `Hotel` | nombre, ciudad, habitaciones | `agregar_habitacion()`, `disponibles()` | No repetir número de habitación |

**En la vida real:** el motor de reservas de un hotel nunca deja escribir directamente "ocupada = verdadero": pasa por un método que revisa la fecha, el pago y la disponibilidad. Eso es el encapsulamiento.

---

## 6. Qué estudiar

| Sesión | Tema | Recurso | Práctica |
|---|---|---|---|
| 1 | Clases y objetos | [Tutorial de Python, cap. 9](https://docs.python.org/es/3/tutorial/classes.html) · Soy Dalto: [POO con Python desde cero](https://www.youtube.com/watch?v=HtKqSJX7VoM) | Correr el ejemplo 01 y agregar `Hotel` |
| 2 | Encapsulamiento y propiedades | Platzi: [Python Orientado a Objetos](https://platzi.com/cursos/python-poo/) | Agregar a `Habitacion` un setter para `tipo` que solo acepte Estándar, Superior o Suite |
| 3 | El mismo ejercicio en Java (para entender la clase) | El video de la clase | Comparar línea por línea con el ejemplo 02 |
| 4 | Entrada de datos | `input()` en el tutorial de Python | Ejemplo 02 pidiendo 3 personas en un ciclo `for` |

---

## 7. Ejemplos de código

| Archivo | Qué enseña |
|---|---|
| [01_clases_y_objetos.py](ejemplos/01_clases_y_objetos.py) | Los seis conceptos con `Habitacion`: constructor, estado, comportamiento, `@property`, métodos que devuelven y que no devuelven |
| [02_persona_con_validaciones.py](ejemplos/02_persona_con_validaciones.py) | El ejercicio exacto de la clase (Carlos, 25, -50, Carlos Alberto, 26) y la versión con `input()` |

### Cómo correrlos
```
cd "estudio\GA07-codificar-modulos\2026-09-09-AA3-poo-clases-objetos-encapsulamiento\ejemplos"
python 01_clases_y_objetos.py
python 02_persona_con_validaciones.py
```

Salida esperada del 02 (igual a la de la instructora):
```
--- Datos iniciales ---
Hola, mi nombre es Carlos y tengo 25 años
--- Regla de seguridad del setter ---
Error: ingrese una edad desde 1 hasta 119
...
--- Resultado final ---
Hola, mi nombre es Carlos Alberto y tengo 26 años
```

### El código parte por parte (01_clases_y_objetos.py)
1. `class Habitacion:` es la **clase**: todavía no existe ninguna habitación.
2. `__init__` es el **constructor**: recibe número, tipo y tarifa, y deja `ocupada = False`. Toda habitación nace completa.
3. `self.numero`, `self.tipo`, `self.ocupada` son el **estado**.
4. `@property tarifa_noche` y `@tarifa_noche.setter`: el **encapsulamiento**. Aunque se escriba `h305.tarifa_noche = -50`, Python llama al setter y este lanza un error.
5. `ocupar()` y `liberar()` devuelven `None` (el `void` de Java). `cotizar(noches)` sí devuelve un número.
6. En `main()`, `Habitacion("101", ...)` crea el **objeto** (el `new` de Java).

### El código parte por parte (02_persona_con_validaciones.py)
1. Es una traducción literal del Java de la clase, con `get_nombre()` y `set_edad()`, para que lo compares línea por línea.
2. `set_nombre` revisa que el nombre no sea `None` ni esté vacío (`strip()` quita los espacios), y si no cumple imprime el error, igual que el `else` con `System.out.println`.
3. `set_edad` acepta solo `0 < edad < 120`.
4. `saludar()` concatena con `+` y convierte la edad con `str()`, que es donde la instructora tuvo el error.
5. La última parte usa `input()` y convierte la edad con `int()`. Si escribes letras, `isdigit()` lo detecta y el setter muestra el error.

> En código real de Python se prefiere la forma del ejemplo 01 (`@property`) a escribir `get_` y `set_`. Para la evidencia puedes usar cualquiera de las dos y explicar la equivalencia.

---

## 8. Repaso

<details><summary>1. ¿Qué diferencia hay entre clase y objeto?</summary>
La clase es el molde y no ocupa memoria con datos. El objeto es la instancia concreta creada con <code>new</code> (en Python, llamando a la clase) y sí ocupa memoria.
</details>

<details><summary>2. ¿Qué es el estado y qué es el comportamiento?</summary>
El estado son los atributos (lo que el objeto sabe de sí). El comportamiento son los métodos (lo que sabe hacer).
</details>

<details><summary>3. ¿Qué tres reglas tiene el constructor en Java?</summary>
Lleva el mismo nombre de la clase, no tiene tipo de retorno y se ejecuta con <code>new</code>.
</details>

<details><summary>4. ¿Qué es el encapsulamiento y para qué sirve?</summary>
Ocultar los atributos (private) y dar acceso solo por métodos con reglas (getters y setters). Evita que se guarden datos inválidos.
</details>

<details><summary>5. ¿Qué significa void?</summary>
Que el método hace su trabajo y no devuelve nada. En Python se indica con <code>-> None</code>.
</details>

<details><summary>6. ¿Qué tipo de Java no existe en Python?</summary>
<code>char</code>. En Python un carácter es un <code>str</code> de longitud 1.
</details>

<details><summary>7. ¿Qué devuelve siempre input() en Python?</summary>
Texto (<code>str</code>). Para usarlo como número hay que convertirlo con <code>int()</code> o <code>float()</code>.
</details>

<details><summary>8. ¿Cómo se organizan las evidencias según esta clase?</summary>
En grupos de 3 o 4, pero cada integrante sube el archivo. En Python, con pantallazos del código.
</details>

Tarjetas para Anki: [repaso-anki.csv](repaso-anki.csv).
