# Clase GA6 · AA3 · Interfaces gráficas y prototipado móvil

| Dato | Valor |
|---|---|
| Guía | GA6 · Desarrollar la estructura de datos y la interfaz de usuario del software |
| Competencia | 220501096 · Desarrollar la solución de software de acuerdo con el diseño y metodologías de desarrollo |
| Resultado de aprendizaje | 220501096-03 · Crear componentes frontend del software de acuerdo con el diseño |
| Actividad | GA6-220501096-AA3 · Crear interfaces gráficas de usuario en aplicaciones de escritorio, web y móviles (48 h) |
| Evidencias | AA3-EV01, AA3-EV02, AA3-EV03 |
| Fecha de la clase | 2026-07-25 (tomada del archivo de video) · 2 h 37 min |
| Transcripción y acta | En tu PC: `Claude\Projects\Sena\Clases\GA06 - Estructura de datos e interfaz de usuario\` (no se sube a GitHub porque trae nombres de compañeros) |
| Plazo dicho en clase | Fase de ejecución hasta el **31 de octubre**. Confírmalo con el instructor |

> **Python en vez de Java.** En clase todo se hizo en Android Studio con Java. Aquí cada cosa tiene su equivalente en Python con **Flet**, que hace escritorio, web y móvil con el mismo código. Ver [stack-python.md](../../stack-python.md).

---

## 1. Resumen en un minuto

1. La AA3 trata de **diseñar la cara del software**: primero bocetos (mockups), después interfaces reales en un IDE. Todavía **no** se programa la lógica (backend); eso llega en GA7 y GA8.
2. Hay tres evidencias: **EV01** escoger y probar una herramienta de prototipado, **EV02** hacer los mockups del proyecto con su navegación, **EV03** llevar al menos 4 de esos mockups a un entorno real.
3. El instructor usó **Dia** y **draw.io** para los bocetos y **Android Studio** (Java) para las pantallas reales. Nosotros usamos los mismos bocetos y **Flet** (Python) para las pantallas reales.
4. Conceptos que más pesan: legibilidad y contraste, tipografía, **retícula y layouts**, color e íconos, **tipos de navegación** (lineal, jerárquica, híbrida) y diseño para **pantallas de distintos tamaños**.
5. Recomendación del instructor: repasar ya los conceptos de **POO** (clase, método, herencia, interfaz) y el patrón **MVC**, porque en GA7 se empieza a codificar.

---

## 2. Conceptos de la clase, explicados

### 2.1 Interfaz de usuario (frontend)
Es lo que está **entre la persona y la máquina**: botones, etiquetas, cajas de texto, imágenes. El instructor la comparó con un control remoto. En tu mundo: el formulario de AppSheet donde un asesor crea una reserva es la interfaz; la hoja de Google Sheets detrás es el dato; las fórmulas y scripts son la lógica.

| Capa | En la clase (Android) | En Python (nuestro proyecto) | En lo que ya usas en HyD |
|---|---|---|---|
| Interfaz (frontend) | XML de layout + actividad | Controles de Flet (`TextField`, `Button`) | Vista y formulario de AppSheet |
| Lógica (backend) | Código `.java` | Funciones y clases Python, FastAPI | Apps Script, fórmulas |
| Datos | Base de datos (GA6-AA1/AA2) | MySQL con SQLAlchemy | Google Sheets / BD_HyD |

### 2.2 POO y MVC (lo que pidió leer antes de codificar)
- **Clase**: el molde. `Reserva` es una clase; `HDMDE001` es un objeto hecho con ese molde. Ya lo tienen en `reserva.py`.
- **Método**: algo que el objeto sabe hacer: `confirmar()`, `cancelar()`, `adicionar_pasajero()`.
- **Herencia**: una clase hija reutiliza a la madre. Ejemplo: `Persona` → `Pasajero` y `Usuario` comparten nombre, documento y correo.
- **Interfaz (en POO)**: un contrato de métodos que una clase promete cumplir. Ojo, es otra cosa que la "interfaz gráfica". En Java se escribe `interface`; en Python se usa `abc.ABC` o `typing.Protocol`.
- **MVC (Modelo, Vista, Controlador)**: separar **datos**, **pantalla** y **reglas**. El ejemplo [02_gestion_usuarios.py](ejemplos/02_gestion_usuarios.py) está partido así para que lo veas en código.

### 2.3 Diseño de interfaces móviles

| Concepto | Qué significa | Cómo se aplica en la app de reservas |
|---|---|---|
| Legibilidad y contraste | Texto que se lee de un vistazo, fondo y letra con buen contraste | Azul oscuro sobre fondo claro; nada de letra gris clara sobre blanco |
| Tipografía | Letra limpia, sin cursivas raras, tamaños consistentes | Una sola familia; título 20 a 22, texto 14 a 16 |
| Retícula (grid) | Cuadrícula invisible que ordena los elementos | `ResponsiveRow` de Flet usa una retícula de 12 columnas |
| Layout | Cómo se acomodan los elementos: vertical, horizontal, tabla, absoluto | `Column` (vertical), `Row` (horizontal), `ResponsiveRow` (cuadrícula), `Stack` (absoluto) |
| Color e íconos | Color con significado y un ícono de lanzamiento que identifique la app | Verde = confirmada, naranja = pendiente, rojo = cancelada |
| Tamaño de pantalla | Celulares de 5 a 7 pulgadas, tablets, escritorio | Preferir íconos vectoriales y diseños que se reacomoden |
| Diseño centrado en el usuario (DCU) | Diseñar para quien usa la app, no para el programador: diseño conceptual, prototipo, prueba, ajuste | Probar el flujo de reserva con un asesor real antes de programarlo |

### 2.4 Tipos de navegación

| Tipo | Cómo funciona | Ejemplo en reservas |
|---|---|---|
| **Lineal** | Un paso tras otro, con Siguiente y Atrás | Asistente "Nueva reserva": destino y fechas → hotel → pasajeros → confirmar |
| **Jerárquica** | Desde un menú entras a cada módulo y vuelves al menú | Menú principal → Reservas / Hoteles / Usuarios |
| **Híbrida** (el material la llama aleatoria) | Mezcla de las dos; es la más usada | Menú (jerárquica) que abre el asistente de reserva (lineal) |

El ejemplo [03_app_navegacion.py](ejemplos/03_app_navegacion.py) implementa exactamente la híbrida.

### 2.5 Plataformas nativas y entornos

| Plataforma | Lenguaje nativo | IDE | En Python |
|---|---|---|---|
| Android | Java o Kotlin | Android Studio | Flet (`flet build apk`) |
| iOS | Swift (antes Objective-C) | Xcode (solo Mac) | Flet (`flet build ipa`, requiere Mac) |
| Windows | C# | Visual Studio | Flet (`flet build windows`) |
| Web | HTML, CSS, JS | Cualquier editor | Flet (`flet run --web`) o FastAPI + plantillas HTML |

### 2.6 Android Studio, y su equivalente en Flet

| Lo que mostró el instructor | Qué es | En Flet |
|---|---|---|
| Requisitos: 64 bits, 8 GB RAM, 8 GB libres | Android Studio es pesado | Flet corre en cualquier PC con Python 3.10 o superior; mucho más liviano |
| SDK y API mínima 21 | Librerías de Android y versión mínima soportada | Lo maneja `flet build apk` por dentro |
| Gradle | Organiza y construye el proyecto | `pip` + `requirements.txt` o `pyproject.toml` |
| Actividad (Activity) | Una pantalla | Una `ft.View` con su ruta (`/login`, `/menu`) |
| `activity_main.xml` | Diseño de la pantalla | Controles de Flet escritos en Python |
| ConstraintLayout | Cada elemento anclado a bordes o vecinos | `Column`, `Row`, `ResponsiveRow`, `alignment`, `expand` |
| Emulador Nexus | Celular simulado | `flet run` con ventana de 400 × 760, o `flet run --android` en tu celular real con la app Flet |
| Play ▶ | Ejecutar | `flet run archivo.py` (se recarga sola al guardar) |

**Error típico que vio en clase:** en ConstraintLayout los botones sin anclar se desordenan en el emulador. En Flet eso no pasa porque `Column` y `Row` acomodan solos, pero el equivalente es olvidar `expand` o anchos fijos muy grandes: en celular se corta la pantalla. Prueba siempre en ventana angosta.

**Problema real de la clase:** el antivirus bloqueó Gradle y dañó la instalación de Android Studio. Si algún día usas Android Studio, agrega su carpeta a las exclusiones del antivirus.

### 2.7 Herramientas de prototipado mencionadas

| Herramienta | Tipo | Costo | Navegación entre pantallas | Comentario del instructor |
|---|---|---|---|---|
| **Dia** 0.97.2 | Escritorio | Gratis | No | La que usó; muy liviana y estable; también sirve para UML y entidad relación |
| **draw.io** (diagrams.net) | En línea | Gratis | Por enlaces | Tiene generación de bocetos con IA |
| **Figma** | En línea | Plan gratis | Sí, simula clics | Muy potente; la más usada en la industria |
| Mockflow | En línea | Plan gratis limitado | Sí | Similar a Figma |
| Balsamiq | Escritorio | De pago | Sí | Clásica para wireframes |
| Adobe XD | Escritorio | De pago | Sí | La usa con otros grupos |
| PowerPoint | Escritorio | Licencia Office | Sí, con hipervínculos | Sirve para simular navegación |

**Recomendación para el grupo:** Figma para EV01 y EV02 (simula la navegación, que es lo que pide la EV02) y Flet para EV03.

### 2.8 Consejo profesional que dio
Deja **por escrito** lo que el cliente aprueba de cada prototipo y pacta en el contrato cuánto cuesta un cambio tardío. Cambiar un botón a mitad de la programación cuesta horas. En HyD pasa igual cuando cambian una regla de negocio después de montada en AppSheet.

---

## 3. Evidencias: qué entregar y cómo hacerlo en Python

### AA3-EV01 · Selección de herramientas para prototipado (conocimiento)
- [ ] Escoger una herramienta (sugerida: Figma) y decir por qué.
- [ ] Documento: portada con integrantes, introducción, objetivo, pantallazos de las funciones principales (menús, panel de propiedades, componentes) y pantallazos de un ejemplo sencillo (un login).
- [ ] Entrega: ZIP con el Word o PDF y, si se puede, el archivo del prototipo. El instructor dijo que con el informe y los pantallazos basta.

### AA3-EV02 · Diseño del sitio web y móvil con navegación (desempeño)
- [ ] Mockups del proyecto: mínimo 5, ideal **unas 10 interfaces**.
- [ ] Cada mockup con su descripción y **hacia dónde lleva cada botón** (flechas u óvalos en el Word, o enlaces en Figma).
- [ ] Pantallas sugeridas para el sistema de reservas: ver sección 4.
- [ ] Entrega: ZIP con el Word y el archivo del prototipo.

### AA3-EV03 · Interfaces gráficas según requerimientos (producto)
- [ ] Llevar **al menos 4** mockups a un entorno real, con colores, estilos y menús definidos.
- [ ] En clase: Android Studio. **Nosotros: Flet.** Parte de [03_app_navegacion.py](ejemplos/03_app_navegacion.py) y ajústalo a sus mockups.
- [ ] Pantallazos de cada pantalla corriendo (escritorio y, si pueden, en el celular con `flet run --android`) con explicación debajo.
- [ ] Entrega: ZIP con el código y el informe.

> Pregúntale a la instructora del proyecto si acepta la EV03 en Flet con el informe de pantallazos. Ya autorizó Python, pero conviene que vea un ejemplo antes de la entrega.

---

## 4. Aplicación al proyecto: sistema de reservas hoteleras

### 4.1 Mapa de pantallas sugerido para la EV02

| # | Pantalla | Navegación | Datos que muestra o pide |
|---|---|---|---|
| 1 | Inicio de sesión | Entrada | Usuario, contraseña |
| 2 | Menú principal | Jerárquica | Accesos según el rol (ADMIN, ASESOR, OPERACION, COMERCIAL) |
| 3 | Lista de reservas | Jerárquica | Código, destino, hotel, fechas, estado; filtro por estado |
| 4 | Nueva reserva · paso 1 | Lineal | Destino, check-in, check-out |
| 5 | Nueva reserva · paso 2 | Lineal | Hotel y tipo de habitación con tarifa |
| 6 | Nueva reserva · paso 3 | Lineal | Pasajeros (titular y acompañantes), resumen, confirmar |
| 7 | Detalle de reserva | Jerárquica | Datos, pasajeros, estado; botones confirmar o cancelar |
| 8 | Hoteles | Jerárquica | CRUD de hoteles con su proveedor |
| 9 | Habitaciones y tarifas | Jerárquica | Tipo, categoría, tarifa adulto, tarifa niño |
| 10 | Usuarios | Jerárquica | CRUD de usuarios y roles |

Las pantallas salen directo de las clases que ya tienen en el repo: `Proveedor`, `Hotel`, `Habitacion`, `Pasajero`, `Reserva`, `Usuario`.

### 4.2 Ejemplos de la vida real para inspirarse

| Producto | Qué mirar | Idea para el proyecto |
|---|---|---|
| App de Booking.com | Búsqueda en pasos: destino, fechas, huéspedes | El asistente lineal de nueva reserva |
| Backoffice de Travel Compositor (el de HyD) | Lista de reservas con filtros y estados | La pantalla 3 con colores por estado |
| BD_HyD en AppSheet | Menú por roles y formularios | El menú principal que cambia según el rol |
| App de una aerolínea (check-in) | Flujo lineal con barra de progreso | La barra de progreso del asistente |

### 4.3 Problemas encontrados en el código actual del repo (para corregir en GA7)

| Archivo | Problema | Arreglo sugerido |
|---|---|---|
| `habitacion.py` y `proveedor.py` | Tienen copiadas las clases `Proveedor`, `Hotel`, `Habitacion` y `Pasajero` | Una clase por archivo dentro de una carpeta `modelos/` |
| `usuario.py` | Crea objetos de `Proveedor`, `Hotel`, `Pasajero` y `Reserva` sin importarlos: al ejecutarlo da `NameError` | Mover la prueba a un `demo.py` con sus `import` |
| `usuario.py` | Guarda la contraseña en texto plano | Guardar un hash (por ejemplo con `bcrypt`) cuando haya base de datos |
| `estilos-cotizador.css` | Está vacío | Llenarlo en la GA6-AA4 o borrarlo |

---

## 5. Qué estudiar (plan sugerido de 6 sesiones)

| Sesión | Tema | Recurso | Práctica |
|---|---|---|---|
| 1 | POO en Python: clases, métodos, herencia | [Tutorial oficial de Python: clases](https://docs.python.org/es/3/tutorial/classes.html) y tu ruta de Python en Platzi | Crear `Persona` y heredar `Pasajero` y `Usuario` |
| 2 | Principios de diseño móvil | [Material Design 3](https://m3.material.io) y [Laws of UX](https://lawsofux.com) | Revisar 3 apps de reservas y anotar layout y navegación |
| 3 | Prototipado en Figma | [Figma](https://www.figma.com) (plan gratis) o [draw.io](https://app.diagrams.net) o [Dia](http://dia-installer.de) | EV01: login de prueba con pantallazos |
| 4 | Mockups del proyecto con navegación | Tabla 4.1 de esta guía | EV02: las 10 pantallas enlazadas |
| 5 | Flet: controles y layouts | [Documentación de Flet](https://docs.flet.dev) y los ejemplos 01 y 02 | Pasar 2 mockups a Flet |
| 6 | Flet: varias pantallas y rutas | Ejemplo 03 | EV03: 4 pantallas corriendo en escritorio y celular |

---

## 6. Ejemplos de código

| Archivo | Qué enseña | Captura |
|---|---|---|
| [01_login.py](ejemplos/01_login.py) | Controles básicos, layout vertical, evento de botón | [ver](capturas/01_login.png) |
| [02_gestion_usuarios.py](ejemplos/02_gestion_usuarios.py) | Formulario CRUD, tabla, MVC, `ResponsiveRow` | [ver](capturas/02_gestion_usuarios.png) |
| [03_app_navegacion.py](ejemplos/03_app_navegacion.py) | Varias pantallas, rutas, navegación jerárquica y lineal | [menú](capturas/03_menu.png) · [reservas](capturas/03_reservas.png) · [nueva](capturas/03_nueva_reserva.png) |

### Cómo correrlos
1. Abre una terminal en la carpeta del proyecto y activa el entorno: `.venv\Scripts\activate` (si no existe, mira [stack-python.md](../../stack-python.md)).
2. Entra a la carpeta: `cd "estudio\GA06-estructura-datos-e-interfaz\2026-07-25-AA3-interfaces-y-prototipado-movil\ejemplos"`.
3. Escritorio: `flet run 01_login.py`. Navegador: `flet run --web 01_login.py`.
4. Celular: instala la app **Flet** desde la tienda, conecta el celular a la misma red Wi-Fi y corre `flet run --android 03_app_navegacion.py`; escanea el QR.
5. Usuario de prueba: `asesor` / `1234`.

### El código parte por parte (01_login.py)
1. `import flet as ft`: trae la librería. Todo lo de Flet se escribe `ft.algo`.
2. `def main(page: ft.Page)`: Flet llama a esta función al abrir la app. `page` es la pantalla, como el contenedor principal de una actividad de Android.
3. `page.title`, `page.window.width/height`: título y tamaño parecido a un celular para probar en el PC.
4. `ft.TextField(...)`: caja de texto (en Android, `EditText`). `password=True` oculta lo que se escribe.
5. `def ingresar(e)`: lo que pasa al hacer clic (en Android, el `setOnClickListener`). Lee `usuario.value`, valida y cambia `mensaje.value`.
6. `page.update()`: redibuja la pantalla con los cambios. Si lo olvidas, el mensaje no aparece.
7. `ft.Column([...])`: acomoda todo en vertical (en Android, un `LinearLayout` vertical).
8. `ft.run(main)`: arranca la app.

### El código parte por parte (03_app_navegacion.py)
1. `@dataclass class Reserva`: el **modelo**. Igual que la clase del repo pero más corta gracias a `dataclass`.
2. `vista_login()`, `vista_menu()`, `vista_reservas()`, `vista_nueva()`: cada función devuelve una pantalla (`ft.View`) con su ruta. Es una actividad de Android por función.
3. `page.navigate("/menu")`: cambia de pantalla. Equivale a `startActivity(...)` en Android.
4. `mostrar_ruta()`: el **enrutador**. Según la ruta, apila las pantallas: el menú siempre queda debajo, por eso la flecha atrás vuelve a él (jerárquica).
5. `borrador` y `paso`: guardan lo que el usuario lleva escrito en el asistente; `Siguiente` y `Atrás` cambian el paso (lineal).
6. `al_volver()`: atiende la flecha atrás del AppBar y el botón atrás del celular.

---

## 7. Repaso

<details><summary>1. ¿Qué diferencia hay entre la EV02 y la EV03?</summary>
La EV02 son mockups o bocetos con su navegación (en una herramienta de prototipado). La EV03 es llevar al menos 4 de esos bocetos a un entorno de desarrollo real con colores, estilos y menús.
</details>

<details><summary>2. ¿Cuál es la navegación híbrida y por qué es la más usada?</summary>
Combina la jerárquica (menú) con la lineal (pasos). Es la más usada porque el menú da libertad y los pasos guían procesos largos como crear una reserva.
</details>

<details><summary>3. ¿Qué es una actividad en Android y cuál es su equivalente en Flet?</summary>
Una actividad es una pantalla. En Flet es una <code>ft.View</code> con una ruta.
</details>

<details><summary>4. ¿Por qué se desordenaron los botones en el emulador del instructor?</summary>
Porque en ConstraintLayout no los ancló a los bordes ni al botón anterior, y sin referencias el emulador no sabe dónde ubicarlos.
</details>

<details><summary>5. ¿Qué es la retícula y qué control de Flet la usa?</summary>
Es una cuadrícula invisible que ordena los elementos. <code>ResponsiveRow</code> usa una retícula de 12 columnas y reacomoda según el ancho de la pantalla.
</details>

<details><summary>6. ¿Por qué conviene usar imágenes vectoriales en móvil?</summary>
Porque se agrandan o achican sin pixelarse, y la app se ve bien en pantallas de 5 o de 7 pulgadas.
</details>

<details><summary>7. ¿Qué es MVC y cómo se ve en 02_gestion_usuarios.py?</summary>
Modelo (clase Usuario y la lista), Vista (controles de Flet) y Controlador (funciones guardar, modificar, eliminar que validan y cambian datos). Separarlos permite cambiar la pantalla sin tocar las reglas.
</details>

<details><summary>8. ¿Qué hace Gradle en Android y qué lo reemplaza en Python?</summary>
Gradle organiza dependencias y construye el proyecto. En Python lo hacen <code>pip</code> con <code>requirements.txt</code> o <code>pyproject.toml</code>, y <code>flet build</code> para empaquetar.
</details>

Tarjetas para Anki: [repaso-anki.csv](repaso-anki.csv). En Anki: Archivo → Importar → separador punto y coma.
