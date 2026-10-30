# GA6 · Desarrollar la estructura de datos y la interfaz de usuario del software

| Dato | Valor |
|---|---|
| Fase | Ejecución |
| Competencia técnica | 220501096 · Desarrollar la solución de software de acuerdo con el diseño y metodologías de desarrollo |
| Resultados técnicos | 220501096-02 · Construir la base de datos a partir del modelo de datos<br>220501096-03 · Crear componentes frontend de acuerdo con el diseño |
| Duración | 288 h (192 técnicas) |
| PDF | `Claude\Projects\Sena\Guias\GA06 - Ejecucion - Estructura de datos e interfaz de usuario.pdf` |

## Actividades técnicas y su equivalente en Python

| Actividad | Horas | Qué piden (herramienta de la guía) | Cómo lo hacemos en Python | Estado |
|---|---|---|---|---|
| **AA1** Crear un modelo de base de datos según requerimientos | 64 | EV01 modelo relacional con cardinalidad y normalización (PDF)<br>EV02 modelo entidad relación en una herramienta<br>EV03 sentencias NoSQL (colección "carro")<br>EV04 base de datos en MongoDB, colección "parque", video | Modelo en MySQL Workbench o draw.io (no depende del lenguaje).<br>EV03 y EV04: además de la consola de MongoDB, se puede hacer con **pymongo** (`insert_many`, `find`, `update_one`, `delete_one`) | Sin clase todavía |
| **AA2** Manipular datos en el SMBD | 32 | EV01 taller SQL DDL y DML (tabla "libreta")<br>EV02 estructura de la BD con PK, FK y restricciones en MySQL Workbench (ZIP)<br>EV03 script SQL del proyecto | El SQL es igual. Para el proyecto: modelos con **SQLAlchemy** que generan las mismas tablas, y conexión a MySQL con **PyMySQL** | Sin clase todavía |
| **AA3** Crear interfaces gráficas de escritorio, web y móvil | 48 | EV01 herramienta de prototipado<br>EV02 mockups con navegación<br>EV03 interfaces reales (Android Studio en clase) | Prototipo en Figma, Dia o draw.io; interfaces reales en **Flet** | [Clase 2026-07-25](2026-07-25-AA3-interfaces-y-prototipado-movil/) |
| **AA4** Generar plantillas y estilos | 48 | EV01 página tutorial en HTML y CSS<br>EV02 documento de componentes frontend<br>EV03 diseño frontend con HTML, CSS y JS | HTML, CSS y JS son iguales en cualquier lenguaje. Para servirlo desde Python: **FastAPI** con plantillas **Jinja2**. El `index.html` del repo ya usa Bootstrap | Sin clase todavía |

## Clases de esta guía

| Fecha | Actividad | Tema | Material |
|---|---|---|---|
| 2026-07-25 | AA3 | Interfaces gráficas y prototipado móvil | [Ver](2026-07-25-AA3-interfaces-y-prototipado-movil/) |

## Competencias transversales de la guía
Actividad física y hábitos saludables (230101507) e inglés (240202501-06). No tienen material de programación; se gestionan aparte en la plataforma.
