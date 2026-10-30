# Clase GA8 · AA2 · Primera app Android y APK

| Dato | Valor |
|---|---|
| Guía | GA8 · Codificar los módulos del software: integración, móvil y tecnologías emergentes |
| Competencia | 220501096 · Desarrollar la solución de software de acuerdo con el diseño y metodologías de desarrollo |
| Resultado de aprendizaje | 220501096-04 · Codificar el software de acuerdo con el diseño establecido |
| Actividad | GA8-220501096-AA2 · Incorporar tecnologías emergentes y disruptivas (144 h) |
| Evidencias | **AA2-EV01** (taller: investigación + primera app) y **AA2-EV02** (APK del módulo móvil del proyecto) |
| Fecha de la clase | 2026-10-14 (tomada del nombre del archivo de video) · 39 min |
| Transcripción y acta | En tu PC: `Claude\Projects\Sena\Clases\GA08 - Integrar modulos y movil\` |
| Plazo | Todas las evidencias **hasta el 31 de octubre** (clase del 2026-10-07) |
| Próxima clase | Talleres de tecnologías emergentes: video sobre **Machine Learning** y texto argumentativo sobre **Blockchain** (AA2-EV03 a EV05) |

> **"Recuerden que podemos utilizar cualquier entorno de desarrollo"**, lo dijo la instructora. En clase usó Android Studio con Java; aquí la misma app está hecha en Python con **Flet**, que genera el APK con `flet build apk`.

---

## 1. Resumen en un minuto

1. La **EV01** tiene dos partes: un **taller de investigación** (qué es Android, APK, SDK, lenguaje, IDE, multiusuario, mínimo privilegio, componentes) y **una primera app** pequeña.
2. Instaló **Android Studio** (instalación estándar, aceptar licencias), creó un proyecto **Empty Views Activity** en **Java** con **API 26 (Android 8.0)** y lo corrió en el **emulador** ("Hello World").
3. Su app: una pantalla con un campo "Ingrese su nombre completo" y un botón **Conectar**. Si hay nombre muestra "Conexión exitosa, bienvenido al sistema"; si está vacío, "Campo requerido vacío".
4. Generó el **APK** desde el menú *Build* y la probó **en su celular**: activó el **modo desarrollador** (tocar varias veces el número de compilación) y la **depuración USB**.
5. La **EV02** es un APK "con todos los juguetes": un módulo del proyecto en versión móvil.

---

## 2. Conceptos de la clase (respuestas del taller, sección 1)

| Pregunta del taller | Respuesta corta |
|---|---|
| **¿Qué es Android?** | Sistema operativo de **código abierto** de Google, basado en el **núcleo de Linux**, pensado para dispositivos con pantalla táctil. Cualquier fabricante o desarrollador lo puede adaptar |
| **¿Qué es un APK?** | *Android Package*: el archivo **instalable** de una app de Android. Es un paquete comprimido con el código compilado, los recursos (imágenes, diseños) y el manifiesto. Equivale al `.exe` de Windows o al `.dmg` de macOS |
| **¿Qué es el Android SDK?** | El **kit de desarrollo**: herramientas, bibliotecas, emuladores y utilidades para crear, compilar, probar y depurar apps |
| **¿Qué lenguaje se usa?** | **Kotlin** (el recomendado oficialmente por Google: moderno, conciso, seguro y compatible con Java) y **Java** |
| **¿Qué IDE existen?** | **Android Studio** (el oficial, de Google), **IntelliJ IDEA** (la base de Android Studio), **VS Code** con extensiones (Flutter, Flet), **Eclipse** con el plugin ADT (el histórico, antes de Android Studio) |
| **Android multiusuario** | Varios perfiles en el mismo dispositivo, cada uno con su almacenamiento, apps y configuración. Un perfil no puede ver los archivos de otro. Incluye el **perfil invitado** para prestar el celular |
| **Mínimo privilegio** | Cada app pide **solo** los permisos que necesita (cámara, ubicación, micrófono...) y el usuario los acepta. Si una app es vulnerada, el daño se limita a lo que tenía permitido |
| **Componentes esenciales** | **Actividades** (cada pantalla), **servicios** (tareas en segundo plano), **receptores de emisiones** (*broadcast receivers*, reaccionan a eventos del sistema como batería baja) y **proveedores de contenido** (comparten datos entre apps) |

### 2.1 Partes de un proyecto de Android Studio y su equivalente

| Android Studio | Para qué | En Flet |
|---|---|---|
| `AndroidManifest.xml` | "Documento de identidad" de la app: nombre, permisos, pantalla inicial | `pyproject.toml` (nombre, versión, permisos) |
| `java/.../MainActivity.java` | La lógica; `onCreate()` es lo primero que se ejecuta | La función `main(page)` |
| `res/layout/activity_main.xml` | El diseño de la pantalla | Los controles de Flet dentro de `main` |
| `res/drawable`, `mipmap` | Imágenes e íconos | Carpeta `assets/` |
| Gradle Scripts | Compilar, empaquetar y manejar dependencias | `flet build apk` + `requirements` en `pyproject.toml` |
| Emulador (AVD) | Celular simulado | `flet run` con ventana de 390×760 |
| Celular con depuración USB | Probar en un dispositivo real | `flet run --android` y escanear el QR con la app **Flet** |
| *Build → Generate APK* | Crear el `.apk` | `flet build apk` |

### 2.2 Probar en tu celular (lo que hizo la instructora)
1. *Ajustes → Acerca del teléfono → Información de software* → tocar **varias veces** el **número de compilación** hasta que diga "Modo desarrollador activado".
2. *Opciones de desarrollador* → activar **Depuración USB**.
3. Conectar por cable y elegir el celular en la barra superior de Android Studio.

Con Flet es más sencillo: instala la app **Flet** desde la tienda, conecta el celular a la **misma red Wi-Fi** que el PC, corre `flet run --android archivo.py` y escanea el QR. No hace falta cable ni modo desarrollador.

---

## 3. Lo que se hizo en Java y cómo se hace en Python

| En clase (Android Studio, Java) | En Python (Flet) |
|---|---|
| *New Project → Empty Views Activity*, lenguaje Java, API 26 | Un archivo `.py` con `ft.run(main)` |
| `LinearLayout` vertical centrado con márgenes y colores | `ft.Column(horizontal_alignment=CENTER)` |
| `EditText` + `Button` + `TextView` | `ft.TextField` + `ft.FilledButton` + `ft.Text` |
| `onCreate()` + `setOnClickListener` + `if/else` | `main(page)` + `on_click=conectar` + `if/else` |
| Correr en el emulador y en el celular por USB | `flet run` y `flet run --android` |
| *Build → Generate APK* | `flet build apk` |

---

## 4. Evidencias

### AA2-EV01 · Taller sobre integración, tecnologías emergentes y disruptivas (conocimiento)
- [ ] **Sección 1:** las 8 preguntas (respuestas base en la sección 2; ampliarlas con fuentes y citarlas en APA).
- [ ] **Sección 2:** la primera app: instalación (pantallazos), creación del proyecto, la pantalla, compilarla y ejecutarla mostrando un mensaje. En Python: [01_app_bienvenida.py](ejemplos/01_app_bienvenida.py) con sus [capturas](capturas/).
- [ ] Entrega: **RAR** con el **PDF** del taller, el código y el **`.apk`**.

### AA2-EV02 · APK: módulo móvil según requerimientos del proyecto (producto)
- [ ] Un **módulo del proyecto** en el celular. Sugerido: [02_app_hoteles_movil.py](ejemplos/02_app_hoteles_movil.py) (login + hoteles, conectado a la API de la GA8-AA1).
- [ ] La misma documentación que la GA8-AA1: diagramas (clases, paquetes, componentes), capas, navegación, Git, librerías, buenas prácticas, **pruebas unitarias**, configuración del servidor y del acceso a datos, ambientes de desarrollo y pruebas.
- [ ] Entrega: **RAR o ZIP** con el PDF y el **APK**, más el código y la URL del repositorio.

> **Pregúntale a la instructora:** si acepta un APK generado con Flet. Ella dijo que se puede usar cualquier entorno, pero conviene que vea la app funcionando en el celular antes de la entrega.

---

## 5. Aplicación al proyecto de reservas

| Pantalla móvil | Para quién | De dónde salen los datos |
|---|---|---|
| Login | Todos los roles | `POST /api/auth/login` |
| Hoteles por ciudad (el ejemplo 02) | ASESOR, COMERCIAL | `GET /api/hoteles` |
| Mis reservas del día | OPERACION (check-in en el hotel) | `GET /api/reservas?fecha=hoy` (por construir) |
| Confirmar llegada del pasajero | OPERACION | `PATCH /api/reservas/{codigo}/confirmar` (por construir) |

**En la vida real,** las apps de **Booking** y de las aerolíneas no guardan los datos en el celular: piden todo a la misma API que usa la web. Por eso el ejemplo 02 consume la API de la GA8-AA1 en lugar de tener su propia base de datos. **Ojo:** desde el celular, `127.0.0.1` es el propio celular. Hay que usar la **IP del PC** en la red Wi-Fi (`ipconfig` en Windows) y arrancar la API con `--host 0.0.0.0`.

---

## 6. Qué estudiar

| Sesión | Tema | Recurso | Práctica |
|---|---|---|---|
| 1 | Conceptos de Android para el taller | [Fundamentos de apps (Android Developers)](https://developer.android.com/guide/components/fundamentals?hl=es-419) | Responder las 8 preguntas con tus palabras |
| 2 | Flet en el celular | [Flet: publicar para Android](https://docs.flet.dev/publish/android/) | Correr el ejemplo 01 con `flet run --android` |
| 3 | Generar el APK | Misma página, sección *flet build apk* | Generar el APK del ejemplo 01 |
| 4 | App que consume una API | El ejemplo 02 y la [clase de la GA8-AA1](../2026-10-07-AA1-integrar-modulos/) | Agregar el filtro por estrellas |

---

## 7. Ejemplos de código

| Archivo | Qué enseña | Capturas |
|---|---|---|
| [01_app_bienvenida.py](ejemplos/01_app_bienvenida.py) | La app de la clase: campo, botón, validación de campo vacío | [vacío](capturas/01_campo_vacio.png) · [bienvenida](capturas/02_bienvenida.png) |
| [02_app_hoteles_movil.py](ejemplos/02_app_hoteles_movil.py) | Módulo móvil con 2 pantallas (rutas), login contra la API y lista de hoteles con filtro | [login](capturas/03_login_movil.png) · [hoteles](capturas/04_hoteles_movil.png) |

### Cómo correrlos
```
cd "estudio\GA08-integrar-modulos-y-movil\2026-10-14-AA2-apk-android\ejemplos"
pip install "flet[all]==1.0.*" httpx
flet run 01_app_bienvenida.py
```
Para el **02**, primero encender la API de la clase anterior (en otra terminal, desde `2026-10-07-AA1-integrar-modulos\ejemplos\sistema_reservas`): `uvicorn app.main:app --host 0.0.0.0 --port 8080`, y luego `flet run 02_app_hoteles_movil.py` (usuario `admin`, clave `12345`).

### Generar el APK (no se ejecutó aquí, porque descarga varios GB)
1. Crear una carpeta para la app con el código renombrado a **`main.py`** (Flet busca ese nombre) y un `pyproject.toml` con nombre y versión (`flet create` lo genera).
2. Correr **`flet build apk`**. La primera vez descarga automáticamente Flutter, el JDK y el Android SDK, así que tarda y ocupa espacio. Deja el PC conectado.
3. El archivo queda en `build/apk/`. Ese `.apk` es el que va en el RAR de la evidencia.
4. Si el 02 consume la API, en el `pyproject.toml` hay que agregar `httpx` a las dependencias y permitir la conexión a internet. Ver la [documentación de Flet para Android](https://docs.flet.dev/publish/android/).

### El código parte por parte (01_app_bienvenida.py)
1. `page.window.width/height` simula el tamaño de un celular en el PC.
2. `nombre`, `estado` y `mensaje` son los tres controles: el `EditText` y los dos `TextView` de la clase.
3. `conectar(e)`: hace lo mismo que el `onClick` de la instructora: `strip()` quita los espacios; si queda texto, "Conexión exitosa" en verde y el saludo; si no, "Campo requerido vacío" en rojo.
4. `page.update()` redibuja la pantalla.

### El código parte por parte (02_app_hoteles_movil.py)
1. `API_URL` se lee de una variable de entorno para poder cambiarla por la IP del PC al probar en el celular.
2. `vista_login()` y `vista_hoteles()` devuelven una pantalla cada una (`ft.View`), como las actividades de Android.
3. `ingresar()` hace `httpx.post(...)` al login. Si responde 200, guarda el usuario y navega a `/hoteles`; si no hay conexión, muestra el error en vez de cerrarse.
4. `cargar()` pide `GET /api/hoteles` y arma una tarjeta (`Card` + `ListTile`) por hotel, filtrando por ciudad.
5. `cambiar_ruta()` es el enrutador: sin sesión, cualquier ruta lleva al login.

---

## 8. Repaso

<details><summary>1. ¿Qué es Android y en qué se basa?</summary>
Un sistema operativo de código abierto de Google para dispositivos táctiles, basado en el núcleo de Linux.
</details>

<details><summary>2. ¿Qué es un APK y cuál es su equivalente en Windows?</summary>
El paquete instalable de una app Android, con el código compilado, los recursos y el manifiesto. En Windows equivale a un .exe.
</details>

<details><summary>3. ¿Qué es el Android SDK?</summary>
El kit de desarrollo: herramientas, bibliotecas y emuladores para crear, compilar, probar y depurar apps.
</details>

<details><summary>4. ¿Qué lenguaje recomienda Google y cuál usó la instructora?</summary>
Google recomienda Kotlin. La instructora usó Java, que también es compatible.
</details>

<details><summary>5. ¿Qué es el principio de mínimo privilegio?</summary>
Que cada app pida solo los permisos que necesita. Si es vulnerada, el daño se limita a esos permisos.
</details>

<details><summary>6. ¿Cuáles son los cuatro componentes esenciales de una app Android?</summary>
Actividades, servicios, receptores de emisiones y proveedores de contenido.
</details>

<details><summary>7. ¿Cómo se prueba una app en el celular desde Android Studio?</summary>
Activando el modo desarrollador (tocando varias veces el número de compilación) y la depuración USB, y conectando el celular por cable.
</details>

<details><summary>8. ¿Qué comando de Flet genera el APK?</summary>
flet build apk (el resultado queda en build/apk).
</details>

<details><summary>9. ¿Por qué desde el celular no sirve 127.0.0.1 para llamar a la API?</summary>
Porque en el celular 127.0.0.1 es el propio celular. Hay que usar la IP del PC en la red Wi-Fi y arrancar la API con --host 0.0.0.0.
</details>

Tarjetas para Anki: [repaso-anki.csv](repaso-anki.csv).
