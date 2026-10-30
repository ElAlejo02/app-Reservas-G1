# Clase GA7 · AA1 · Herramientas de versionamiento (Git) y estándares de codificación

| Dato | Valor |
|---|---|
| Guía | GA7 · Codificar los módulos del software |
| Competencia | 220501096 · Desarrollar la solución de software de acuerdo con el diseño y metodologías de desarrollo |
| Resultado de aprendizaje | 220501096-01 · Planear actividades de construcción del software de acuerdo con el diseño establecido |
| Actividad | GA7-220501096-AA1 · Configurar herramientas de versionamiento para control de código (40 h) |
| Evidencias | AA1-EV01, EV02, EV03, EV04 y EV05 (las cinco se explicaron en esta clase) |
| Fecha de la clase | 2026-07-02 (la dice el instructor y coincide con el archivo de video) · 2 h 24 min |
| Transcripción y acta | En tu PC: `Claude\Projects\Sena\Clases\GA07 - Codificar modulos y versionamiento\` (no se sube a GitHub porque trae nombres de compañeros) |
| Plazo dicho en clase | La fase de ejecución (GA7 a GA10) va hasta el **31 de octubre**. No dio fecha por evidencia: "toda esta semana y las que siguen" |

> **Python en vez de Java.** Git y GitHub son iguales para cualquier lenguaje, así que EV01, EV03, EV04 y EV05 se hacen tal cual. La única evidencia que cambia es la **EV02 (estándares)**: el instructor la explicó con Java y Eclipse; nosotros la hacemos con **PEP 8** y **Ruff**. Ver [stack-python.md](../../stack-python.md).

---

## 1. Resumen en un minuto

1. Arranca la **GA7**, la guía "más pesada" según el instructor: aquí se codifica el proyecto. La meta mínima es **un módulo conectado a la base de datos, con interfaz y funcionando**; el resto de módulos se pule hasta diciembre.
2. La **AA1** tiene 5 evidencias: EV01 informe eligiendo la herramienta (Git), EV02 estándares de codificación, EV03 tabla Git local contra Git remoto, EV04 instalación de Git y creación de cuenta en GitHub con pantallazos, EV05 laboratorio de comandos (video o informe con pantallazos).
3. **Git** guarda versiones del código en una línea de tiempo. Los archivos pasan por tres estados: **modificado** (rojo), **preparado / stage** (verde) y **confirmado / commit**.
4. Orden de comandos que dio el instructor: `git -v` → `git config --global user.name` y `user.email` → `cd` a la carpeta → `git init` → `git status` → `git add` → `git commit -m` → `git log` → `git remote add origin` → `git remote -v` → `git push -u origin master`.
5. Lo **remoto es opcional para la nota**: "me interesa la local; si lograron la remota, mejor". Al hacer el primer `push` hay que autenticarse con el **Git Credential Manager** (opción *manager*) y un código o token.

---

## 2. Conceptos de la clase, explicados

### 2.1 ¿Qué es un sistema de control de versiones?
Es un programa que toma una **foto** de tu proyecto cada vez que le dices, y guarda todas las fotos en orden. Si la versión nueva quedó mala, vuelves a la anterior.

Analogía con lo que ya usas: es el **historial de versiones de Google Sheets**, pero tú decides cuándo se guarda cada versión y le pones un nombre ("Versión 1.0: login funcionando").

Regla que repitió el instructor: **solo haz commit de lo que funciona**. Una versión es un punto al que puedes volver; si guardas algo roto, vuelves a algo roto.

### 2.2 Tres formas de versionar

| Tipo | Dónde está el código | Riesgo | Ejemplo |
|---|---|---|---|
| **Local** | Solo en tu computador | Si se daña el disco, se pierde todo | Tú solo con `git init` en tu PC |
| **Centralizado** | En un servidor; los demás se conectan a él | Si el servidor cae, nadie trabaja | Sistemas viejos como SVN |
| **Distribuido** | Cada computador tiene **copia completa** del historial | Muy bajo: cualquier copia sirve para restaurar | **Git** con GitHub |

Git es distribuido: cuando clonas el repo del grupo, tienes todas las versiones, no solo la última.

### 2.3 Git, GitHub, GitLab y Bitbucket

| Herramienta | Qué es | Dónde corre |
|---|---|---|
| **Git** | El programa que versiona (lo creó Linus Torvalds para el kernel de Linux) | En tu computador |
| **GitHub** | Sitio en la nube para guardar repos de Git y trabajar en equipo | Web (el que recomendó el instructor y el que ya usa el grupo) |
| GitLab | Igual que GitHub, con integración continua muy completa | Web o servidor propio |
| Bitbucket | Igual, de Atlassian (los de Jira y Trello) | Web |

Git ≠ GitHub: Git funciona sin internet; GitHub es donde publicas para compartir.

### 2.4 Los tres estados de un archivo

| Estado | Color en `git status` | Qué significa | Cómo llega ahí |
|---|---|---|---|
| Modificado | 🔴 Rojo | Cambiaste el archivo y Git lo nota, pero no está listo | Editas y guardas |
| Preparado (*staged*) | 🟢 Verde | Lo marcaste para la próxima versión | `git add archivo` o `git add .` |
| Confirmado (*committed*) | No aparece | Ya quedó guardado en una versión con su código (*hash*), autor y fecha | `git commit -m "mensaje"` |

### 2.5 Comandos de la clase

| # | Comando | Para qué | Local o remoto |
|---|---|---|---|
| 1 | `git -v` o `git --version` | Ver que Git está instalado y su versión (en clase: 2.55.0) | Local |
| 2 | `git config --global user.name "Tu nombre"` | Decirle a Git quién eres. **Sin esto no deja trabajar** (no está en la guía, lo agregó el instructor) | Local |
| 2 | `git config --global user.email "tu@correo.com"` | Tu correo. Usa **el mismo de GitHub** para que te reconozca como dueño | Local |
| 2 | `git config --global --list` | Ver la configuración guardada | Local |
| 3 | `cd "ruta de la carpeta"` | Pararse en la carpeta del proyecto | Local |
| 4 | `git init` | Convertir la carpeta en repositorio (crea la carpeta oculta `.git`) | Local |
| 5 | `git status` | Ver qué archivos están en rojo o verde | Local |
| 6 | `git add index.html` / `git add .` | Preparar un archivo / todos | Local |
| 7 | `git commit -m "Versión 1.0"` | Crear la versión | Local |
| 8 | `git log` | Ver el historial de versiones (hash, autor, fecha, mensaje) | Local |
| 9 | `git diff` | Ver qué cambió en un archivo modificado (líneas agregadas en verde, quitadas en rojo) | Local |
| 10 | `git branch` | Ver las ramas (en clase solo `master`) | Local |
| 11 | `git clone url` | Traer a tu PC un repositorio que está en la nube | Remoto |
| 12 | `git remote add origin url` | Conectar tu repo local con el de GitHub | Remoto |
| 13 | `git remote -v` | Ver a qué repos remotos estás conectado | Remoto |
| 14 | `git push -u origin master` | Subir tus versiones. El `-u` deja recordado el destino; después basta `git push` | Remoto |
| 15 | `git fetch` / `git pull` | Traer lo que otros subieron | Remoto |

> **Ojo con `master` y `main`.** El instructor trabajó con la rama `master`. GitHub y las versiones nuevas de Git usan `main` por defecto, y **el repo del grupo (`app-Reservas-G1`) usa `main`**. Son lo mismo con otro nombre: en el proyecto usa `git push -u origin main`. Para la EV05 puedes seguir la guía con `master` en un repo de prueba.

### 2.6 Instalación (EV04)
- **Instalador normal** desde [git-scm.com](https://git-scm.com/downloads/win): dejar todo por defecto. En credenciales, dejar **Git Credential Manager**.
- **Versión portable** (la que usó el instructor): `PortableGit-...-64-bit.7z.exe`, se descomprime en una carpeta y se abre `git-bash.exe`. No se instala, se puede llevar en una USB.
- Al primer `git push` aparece una ventana para elegir el manejador de credenciales: elegir **manager** (no `wincred`, que es viejo) y marcar *Always use this from now on*. Luego GitHub pide autenticarse en el navegador o con un código; queda guardado en Windows y no vuelve a preguntar.
- GitHub ya **no acepta contraseña** desde la consola: se usa el navegador, un código de dispositivo o un *Personal Access Token*.

### 2.7 Crear el repositorio en GitHub
1. Entrar a [github.com](https://github.com) y crear cuenta (cada integrante la suya). El **nombre de usuario** importa: aparece en todas las versiones, que sea corto y reconocible.
2. Botón verde **New** → nombre del repo → visibilidad (**privado** recomendó el instructor; la guía pide **público** con el nombre `Programa-git`) → sin README ni .gitignore para que quede vacío → **Create repository**.
3. Elegir **HTTPS** y copiar las tres últimas líneas que muestra GitHub ("…or push an existing repository").
4. Después de subir, agregar un **README**: el instructor recomendó que todo proyecto tenga uno que explique qué es y cómo se instala.

### 2.8 Estándares de codificación (EV02)
El instructor resumió el material en 5 bloques: **nombramiento de variables, declaración de clases, creación de métodos, tipos de datos y comunicación entre clases**. Pidió 5 o 6 estándares con un ejemplo cada uno. Esta es la versión Python:

| Bloque | Java (lo de la clase) | Python (PEP 8, lo nuestro) | Ejemplo del proyecto |
|---|---|---|---|
| Clases | `PascalCase`, sustantivo | Igual: `PascalCase`, sustantivo en singular | `Reserva`, `Habitacion` |
| Variables y atributos | `camelCase`: `fechaEntrada` | `snake_case`: `fecha_entrada` | `tarifa_noche` |
| Métodos | `camelCase` con verbo: `calcularTotal()` | `snake_case` con verbo: `calcular_total()` | `confirmar()`, `cancelar()` |
| Constantes | `static final IVA` | `MAYUSCULAS`: `IVA = 0.19` | `PREFIJO_CODIGO = "HD"` |
| Privado | `private String estado;` | Un guion bajo: `self._estado` (es convención, no prohibición) | `_estado` con `@property` |
| Comentarios de clase | Javadoc `/** */` | Docstring `"""..."""` | Ver ejemplo 01 |
| Constructor | `public Reserva(...)` | `def __init__(self, ...)` | |
| Sangría | Llaves `{ }` | **4 espacios** (obligatorio, es parte de la sintaxis) | |
| Largo de línea | Libre | 79 a 100 caracteres (nosotros: 100) | |
| Tipos | `int`, `double`, `String`, `boolean`, `ArrayList`, `HashMap` | `int`, `float`, `str`, `bool`, `list`, `dict` | |

Comunicación entre clases (también la pidió en la EV02):

| Relación | Qué significa | Ejemplo del sistema |
|---|---|---|
| **Asociación** | Una clase usa o conoce a otra | `Reserva` conoce al `Usuario` que la hizo |
| **Agregación** | Un todo agrupa partes que existen solas | `Proveedor` agrupa `Hotel`es; si el proveedor se va, el hotel sigue |
| **Composición** | Las partes no existen sin el todo | `Hotel` crea sus `Habitacion`es; sin hotel no hay habitación |
| **Herencia** | Una clase hija reutiliza a la madre | `Pasajero` y `Usuario` heredan de `Persona` |

Todo esto está corriendo en los ejemplos [01](ejemplos/01_estandares_pep8.py) y [02](ejemplos/02_comunicacion_entre_clases.py).

### 2.9 IDEs que mencionó (Java) y los nuestros

| En clase (Java) | Comentario del instructor | Nosotros (Python) |
|---|---|---|
| Eclipse | El que usa él y el que trae el material; se arma con plugins (Tomcat, etc.) | **VS Code** con las extensiones Python y Ruff |
| NetBeans | Viene "empaquetado" con servidor | PyCharm Community (alternativa) |
| BlueJ | Para empezar si nunca has programado | Thonny (alternativa sencilla) |

---

## 3. Lo que se hizo en Java y cómo se hace en Python

| En clase | En Python |
|---|---|
| Git y GitHub | **Igual**, no cambia nada |
| Estándares de Java (convenciones de Oracle) | **PEP 8** y docstrings (**PEP 257**) |
| Formatear desde Eclipse | `ruff format .` |
| Revisar estilo | `ruff check .` (con la configuración de [pyproject.toml](ejemplos/pyproject.toml)) |
| Archivos que no se suben (`bin/`, `.class`) | `.venv/`, `__pycache__/`, `.env` en el `.gitignore` ([plantilla](ejemplos/gitignore-python.txt)) |
| Proyecto de prueba `index.html` + `usuario.js` + `img/` | Igual, o con un `.py` del proyecto |

---

## 4. Evidencias: qué entregar

Todas en **PDF** (la EV05 en MP4), con portada **con todos los integrantes del grupo**. El instructor insistió: "si no están en la portada, no los veo y no les subo la nota".

### AA1-EV01 · Informe técnico del plan de trabajo (conocimiento)
- [ ] Portada, introducción (copiar la idea de la guía: "con base en las características del software a desarrollar..."), objetivo.
- [ ] Herramienta elegida: **Git** + **GitHub**. Qué es, sus tres estados, por qué se eligió (distribuido, gratis, el grupo ya tiene el repo).

### AA1-EV02 · Estándares de codificación (desempeño)
- [ ] Portada, introducción, objetivo.
- [ ] 5 o 6 estándares con ejemplo: nombres de variables, clases, métodos, tipos de datos, comunicación entre clases. **Hacerlo con Python**: usar la tabla de la sección 2.8 y pegar fragmentos de los ejemplos 01 y 02.
- [ ] Agregar los ejemplos de asociación, agregación, composición y herencia (el instructor los pidió aparte del resto).
- [ ] Mencionar que el estilo se revisa con Ruff y pegar el pantallazo de `ruff check` diciendo *All checks passed!*.

### AA1-EV03 · Identifica herramientas de versionamiento (conocimiento)
- [ ] Portada, introducción, objetivo.
- [ ] Tabla de dos columnas **Git local | Git remoto**: qué es, características y comandos con su descripción. Base: tabla 2.5 de esta guía.

### AA1-EV04 · Instalación y configuración local y web (desempeño)
- [ ] Pantallazos: descarga de Git, instalación o descompresión, `git-bash` abierto, `git -v`.
- [ ] Pantallazos de GitHub: crear cuenta o iniciar sesión, el *dashboard*, el usuario.

### AA1-EV05 · Git instalado y configurado (producto)
- [ ] Ejercicio de la guía: repo **público** `Programa-git`, `git remote add`, `git remote -v`, `git push`, archivo `kotlin.txt` con nombre y correo, commit `"Añadido datos."` y push.
- [ ] **Video MP4** con presentación (nombre y ejercicios) y explicando cada paso. **El instructor también acepta un informe con pantallazos de cada comando y su resultado.**
- [ ] Mínimo 6 o 7 comandos locales. La parte remota suma pero no es obligatoria si fallan las credenciales.

> Pregúntale al instructor: si la EV05 puede hacerse sobre el repo real del grupo (`app-Reservas-G1`, rama `main`) en vez del repo de prueba `Programa-git`.

---

## 5. Aplicación al proyecto de reservas

### 5.1 Usar Git de verdad en `app-Reservas-G1`

| Práctica | Cómo | Por qué |
|---|---|---|
| Una rama por módulo | `git switch -c modulo-reservas` | Que cada integrante trabaje sin pisar a los demás |
| Pull request para unir a `main` | Desde GitHub: *Compare & pull request* | Otro integrante revisa antes de unir (lo que el instructor llamó "el master aprueba") |
| Mensajes claros | `git commit -m "Reserva: valida que la salida sea después de la entrada"` | El `git log` se vuelve la bitácora del proyecto |
| `.gitignore` | Copiar [gitignore-python.txt](ejemplos/gitignore-python.txt) a `.gitignore` | Para no subir `.venv` (cientos de MB) ni contraseñas |
| `README.md` en la raíz | Qué es el sistema, cómo instalarlo, cómo correrlo | Lo recomendó el instructor y lo pide la GA10 |
| Etiquetas de versión | `git tag v1.0` cuando el primer módulo funcione | Marca la "versión 1.0" de la que habló en clase |

### 5.2 Primeras versiones sugeridas (lo que dijo el instructor: "versión 1, inicio de sesión y menú")

| Versión | Qué debe funcionar |
|---|---|
| v0.1 | Clases del dominio en `modelos/` con estándar PEP 8 y `ruff check` limpio |
| v1.0 | Login y menú principal por rol (ADMIN, ASESOR, OPERACION, COMERCIAL) |
| v1.1 | CRUD de hoteles y habitaciones contra MySQL |
| v2.0 | Crear, confirmar y cancelar reservas con código `HDMDE001` |

### 5.3 En la vida real
- **Travel Compositor** y **Booking** publican cambios varias veces por semana: sin ramas, pull requests y versiones, un error en el motor de reservas dejaría a todos los hoteles sin vender. Con Git, si una versión falla, se vuelve a la anterior en minutos.
- En **HyD**, el historial de Apps Script y las copias de AppSheet cumplen el mismo papel, pero sin ramas: por eso cuesta probar algo sin afectar lo que está en uso.

### 5.4 Problemas en el repo (revisado hoy)

| Problema | Arreglo sugerido |
|---|---|
| No hay `.gitignore` | Crear uno con la [plantilla](ejemplos/gitignore-python.txt) antes de crear el `.venv` |
| No hay `README.md` en la raíz | Crear uno con descripción, integrantes (sin datos personales) e instalación |
| Los `.py` están todos sueltos en la raíz y varias clases repetidas | Llevarlos a `modelos/`, una clase por archivo (ver GA6) |
| La carpeta `estudio/` todavía no está subida | Hacer commit cuando Alejo lo apruebe |

---

## 6. Qué estudiar (plan de 5 sesiones)

| Sesión | Tema | Recurso | Práctica |
|---|---|---|---|
| 1 | Qué es Git y los tres estados | [Pro Git en español, cap. 1 y 2](https://git-scm.com/book/es/v2) · MoureDev: [Git y GitHub desde cero](https://www.youtube.com/watch?v=3GymExBkKjE) | Instalar Git, `git config`, repo de prueba con 2 commits |
| 2 | GitHub y repos remotos | Platzi: [Curso de Git y GitHub](https://platzi.com/cursos/gitgithub/) | EV05 completa con `Programa-git` |
| 3 | Ramas, merge y pull requests | [Pro Git, cap. 3](https://git-scm.com/book/es/v2/Ramificaciones-en-Git-%C2%BFQu%C3%A9-es-una-rama%3F) | Rama `modulo-reservas` en el repo del grupo y un pull request |
| 4 | PEP 8 y Ruff | [PEP 8](https://peps.python.org/pep-0008/) · [Ruff](https://docs.astral.sh/ruff/) | Correr Ruff sobre el repo y corregir |
| 5 | POO: relaciones entre clases | Platzi: [Python Orientado a Objetos](https://platzi.com/cursos/python-poo/) · ejemplo 02 | EV02 con ejemplos del proyecto |

La ruta completa por temas está en el Word `Claude\Projects\Sena\Ruta de estudio\Ruta de estudio Python - Platzi y YouTube.docx`.

---

## 7. Ejemplos de código

| Archivo | Qué enseña |
|---|---|
| [01_estandares_pep8.py](ejemplos/01_estandares_pep8.py) | Nombres, constantes, clase con docstring, constructor, atributo privado con `@property`, métodos, tipos de datos |
| [02_comunicacion_entre_clases.py](ejemplos/02_comunicacion_entre_clases.py) | Herencia, polimorfismo, composición, agregación y asociación |
| [pyproject.toml](ejemplos/pyproject.toml) | Configuración de Ruff para revisar PEP 8 |
| [gitignore-python.txt](ejemplos/gitignore-python.txt) | Plantilla de `.gitignore` para el proyecto |

### Cómo correrlos
```
cd "estudio\GA07-codificar-modulos\2026-07-02-AA1-versionamiento-git-y-estandares\ejemplos"
python 01_estandares_pep8.py
python 02_comunicacion_entre_clases.py
pip install ruff
ruff check .
```
Salida esperada del 01: `HDMDE001 | Medellín | 3 noches | CONFIRMADA` y `Total con IVA: $892,500`.

### El código parte por parte (01_estandares_pep8.py)
1. `IVA = 0.19`, `PREFIJO_CODIGO`, `CODIGOS_CIUDAD`: **constantes en mayúscula**. Nadie debería cambiarlas mientras corre el programa.
2. `class Reserva:` con un docstring debajo: **clase en PascalCase** y su documentación (el Javadoc de Python).
3. `_consecutivo = 0`: variable **de la clase**, compartida por todas las reservas; sirve para numerar `001`, `002`...
4. `def __init__(...)`: el **constructor**. Valida que la salida sea después de la entrada y arma el código: `HD` + `MDE` + `001`.
5. `self._estado`: el guion bajo avisa "no lo cambies desde afuera". Para leerlo está `@property def estado`, que es el *getter*.
6. `noches()`, `calcular_total()`, `confirmar()`, `cancelar()`: **métodos en snake_case con verbo**. `confirmar()` aplica una regla de negocio: una reserva cancelada no se confirma.
7. `__str__`: lo que se muestra al imprimir el objeto (el `toString()` de Java).
8. `demo()`: muestra los tipos de datos básicos y usa la clase.
9. `if __name__ == "__main__":` solo ejecuta `demo()` si corres este archivo; si otro archivo lo importa, no se ejecuta.

### El código parte por parte (02_comunicacion_entre_clases.py)
1. `@dataclass`: crea el constructor automáticamente a partir de los atributos. Ahorra escribir `__init__`.
2. `class Pasajero(Persona)`: **herencia**. `Pasajero` tiene `nombre` y `documento` sin volver a escribirlos.
3. `Usuario.presentarse()` vuelve a definir el método de `Persona`: **polimorfismo**.
4. `Hotel.agregar_habitacion()` crea la habitación dentro del hotel: **composición**.
5. `Proveedor.vincular(hotel)` recibe un hotel que ya existía: **agregación**.
6. `Reserva` guarda un `Usuario`, una `Habitacion` y una lista de `Pasajero`: **asociación**.
7. `field(default_factory=list)`: cada objeto recibe su propia lista vacía (si se escribiera `= []`, todas compartirían la misma lista, un error clásico).

---

## 8. Repaso

<details><summary>1. ¿Cuáles son los tres estados de un archivo en Git y qué comando lo mueve de uno a otro?</summary>
Modificado (rojo) → <code>git add</code> → preparado (verde) → <code>git commit</code> → confirmado.
</details>

<details><summary>2. ¿Por qué hay que correr <code>git config --global user.name</code> y <code>user.email</code> antes de todo?</summary>
Porque Git firma cada versión con nombre y correo. Sin ellos no deja hacer commit. Conviene usar el mismo correo de GitHub para que te reconozca como dueño.
</details>

<details><summary>3. ¿Qué diferencia hay entre versionamiento centralizado y distribuido?</summary>
En el centralizado el historial vive solo en el servidor; si cae, se pierde. En el distribuido (Git) cada computador tiene una copia completa, y cualquiera sirve para restaurar.
</details>

<details><summary>4. ¿Qué hace <code>git push -u origin master</code> y para qué sirve el <code>-u</code>?</summary>
Sube las versiones de la rama master al remoto llamado origin. El <code>-u</code> deja ese destino recordado para que las próximas veces baste con <code>git push</code>.
</details>

<details><summary>5. ¿Para qué sirve <code>git diff</code>?</summary>
Para ver qué cambió en un archivo modificado antes de prepararlo: líneas agregadas en verde y quitadas en rojo.
</details>

<details><summary>6. ¿Cómo se nombran clases, métodos y constantes en Python según PEP 8?</summary>
Clases en PascalCase (<code>Reserva</code>), métodos y variables en snake_case (<code>calcular_total</code>), constantes en MAYÚSCULAS (<code>IVA</code>).
</details>

<details><summary>7. ¿Composición o agregación: Hotel y Habitación? ¿Proveedor y Hotel?</summary>
Hotel y Habitación es composición (la habitación no existe sin el hotel). Proveedor y Hotel es agregación (el hotel existe aunque el proveedor se vaya).
</details>

<details><summary>8. ¿Qué no se debe subir nunca a GitHub y cómo se evita?</summary>
El entorno virtual, archivos generados y credenciales (<code>.venv/</code>, <code>__pycache__/</code>, <code>.env</code>). Se evita listándolos en <code>.gitignore</code>.
</details>

<details><summary>9. ¿Qué pasa si GitHub pide contraseña en la consola?</summary>
Ya no la acepta. Se autentica con Git Credential Manager (opción manager), que abre el navegador o pide un código o token; queda guardado en Windows.
</details>

Tarjetas para Anki: [repaso-anki.csv](repaso-anki.csv). En Anki: Archivo → Importar → separador punto y coma.
