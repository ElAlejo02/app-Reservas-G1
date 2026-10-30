# Stack Python del proyecto (equivalente al de Java)

La instructora lleva el proyecto con herramientas de Java y autorizó al grupo a hacerlo en Python. Esta tabla dice, para cada cosa que piden las guías, qué usamos nosotros.

## 1. Equivalencias por guía

| Guía y actividad | En las guías y en clase (Java) | Nosotros (Python) | Por qué esta opción |
|---|---|---|---|
| GA6-AA1/AA2 Base de datos | MySQL Workbench, SQL, MongoDB | Lo mismo: MySQL Workbench, SQL y MongoDB. Desde Python: **SQLAlchemy**, **PyMySQL**, **pymongo** | El modelo de datos y el SQL no dependen del lenguaje |
| GA6-AA3 Interfaces | Dia, draw.io, Android Studio (actividades XML) | Figma, Dia o draw.io para bocetos; **Flet** para pantallas reales | Flet hace escritorio, web y móvil con un solo código Python |
| GA6-AA4 Plantillas y estilos | HTML, CSS, JS | HTML, CSS, JS (iguales). Servidos con **FastAPI + Jinja2** | El frontend web es el mismo en cualquier backend |
| GA7-AA1 Versionamiento | Git, GitHub | Git, GitHub (igual) | Ya tienen el repo `app-Reservas-G1` |
| GA7-AA2 Estándares de codificación | Convenciones de Java | **PEP 8**, revisado y formateado con **Ruff** (`ruff check`, `ruff format`) | Es el estándar oficial de Python; Ruff reemplaza a Black, Flake8 e isort |
| GA7-AA2 Conexión a BD | JDBC | **SQLAlchemy** (ORM) o **PyMySQL** (SQL directo) | SQLAlchemy es el estándar en Python |
| GA7-AA2 Web con formularios | Servlets y JSP, métodos GET y POST | **FastAPI** con plantillas **Jinja2** y formularios GET y POST | Mismo concepto: ruta, formulario, respuesta |
| GA7-AA3 Framework ágil | Spring Boot | **FastAPI** (o Django si quieren panel de administración) | Ya conoces FastAPI; documentación automática en `/docs` |
| GA7-AA4 Frontend con framework | React JS (taller, componentes y módulo) | **React con Vite** (es JavaScript, igual) llamando a la API de **FastAPI** | La guía exige React; el backend sigue en Python |
| GA7-AA3 Stand-alone | Java Swing o JavaFX | **Flet** en modo escritorio (`flet build windows`) | El mismo código de la app móvil |
| GA8-AA1 Integrar módulos | Paquetes Java, capas | Paquetes Python (`modelos/`, `servicios/`, `api/`, `app/`) | Misma idea de capas |
| GA8-AA2 APK Android | Android Studio, Java | **Flet**: `flet build apk` | Genera un APK real desde Python |
| GA9 Pruebas | JUnit, Selenium, JMeter | **pytest**, **Playwright** para pruebas de interfaz web, **Locust** para carga | Equivalentes directos y gratuitos |
| GA10 Puesta en marcha | Servidor de aplicaciones (Tomcat) | **Uvicorn** + **Docker** | Tienes Docker Desktop instalado |

## 2. Diccionario rápido Java → Python

| Java | Python |
|---|---|
| `public class Reserva { ... }` | `class Reserva:` |
| Constructor `public Reserva(String codigo)` | `def __init__(self, codigo):` |
| `this.codigo` | `self.codigo` |
| `private String codigo;` + getters y setters | Atributo normal; si hace falta control, `@property` |
| `interface Pagable` | `class Pagable(Protocol)` o `class Pagable(ABC)` |
| `extends Persona` | `class Pasajero(Persona):` |
| `ArrayList<Pasajero>` | `list[Pasajero]` |
| `HashMap<String, Hotel>` | `dict[str, Hotel]` |
| `System.out.println()` | `print()` |
| `try { } catch (Exception e) { }` | `try: ... except Exception as e: ...` |
| Paquete `com.hyd.reservas` | Carpeta con `__init__.py` |
| Maven o Gradle (`pom.xml`, `build.gradle`) | `pip` + `requirements.txt` o `pyproject.toml` |
| `.jar` / `.apk` | `flet build windows` / `flet build apk` |

## 3. Instalar el entorno en Windows (una sola vez)

1. Instala **Python 3.12 o 3.13** desde python.org y marca "Add python.exe to PATH".
2. Instala **VS Code** con las extensiones *Python* (Microsoft) y *Ruff*, y **Git** desde git-scm.com (con Git Credential Manager).
3. Abre la carpeta del proyecto en VS Code y una terminal (Ctrl + ñ).
4. Crea el entorno virtual: `py -3 -m venv .venv`
5. Actívalo: `.venv\Scripts\activate` (debe aparecer `(.venv)` al inicio de la línea).
6. Instala las librerías: `pip install -r estudio/requirements.txt`
7. Prueba: `flet run estudio\GA06-estructura-datos-e-interfaz\2026-07-25-AA3-interfaces-y-prototipado-movil\ejemplos\01_login.py`
8. Agrega `.venv/` al archivo `.gitignore` para no subir el entorno a GitHub.

> **Por qué un entorno virtual:** es como tener una hoja de cálculo aparte para cada proyecto. Las librerías de este proyecto no se mezclan con las de otros (por ejemplo, las de tus scripts de HyD).

> **Ojo con FastAPI:** Flet 1.0.4 en modo web falla con FastAPI 0.145 o más nuevo. Por eso `requirements.txt` la deja en una versión anterior. Si algún día ves el error `unexpected keyword argument 'openapi_prefix'`, es esto.

## 4. Estructura de carpetas recomendada para el código (desde GA7)

```
app-Reservas-G1/
├── modelos/          clases: Proveedor, Hotel, Habitacion, Pasajero, Reserva, Usuario
├── datos/            conexión a MySQL y repositorios (SQLAlchemy)
├── servicios/        reglas de negocio: confirmar, cancelar, calcular tarifa
├── api/              FastAPI: rutas REST y formularios web
├── app/              Flet: pantallas de escritorio y móvil
├── web/              HTML, CSS y JS (el index.html y el cotizador)
├── pruebas/          pytest
├── estudio/          este material
└── requirements.txt
```

## 5. Arquitectura en una imagen

```
 Celular (APK)  ┐
 Escritorio     ├──► App Flet ──┐
 Navegador      ┘               ├──► FastAPI (reglas de negocio) ──► MySQL
 Navegador ───► HTML + Bootstrap┘
```

La app Flet y la web hablan con el mismo backend FastAPI. Así las reglas (por ejemplo, que una reserva cancelada no se pueda confirmar) se escriben una sola vez.
