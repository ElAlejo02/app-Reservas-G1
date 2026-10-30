# GA7 · Codificar los módulos del software

| Dato | Valor |
|---|---|
| Fase | Ejecución |
| Competencia técnica | 220501096 · Desarrollar la solución de software de acuerdo con el diseño y metodologías de desarrollo |
| Resultados técnicos | 220501096-01 · Planear actividades de construcción del software de acuerdo con el diseño establecido<br>220501096-04 · Codificar el software de acuerdo con el diseño establecido |
| Duración | 498 h técnicas |
| PDF | `Claude\Projects\Sena\Guias\GA07 - Ejecucion - Codificar modulos y versionamiento.pdf` |

Según el instructor es la guía "más pesada" del programa: aquí se codifica el proyecto. La meta mínima es **un módulo conectado a la base de datos, con interfaz y funcionando**; los demás módulos se terminan hasta diciembre.

> **Python está permitido.** La instructora de programación (desde el 2026-09-03) enseña en Java con NetBeans, pero acepta las evidencias en cualquier plataforma, con pantallazos del código.

## Actividades técnicas y su equivalente en Python

| Actividad | Horas | Qué piden (herramienta de la guía) | Cómo lo hacemos en Python | Estado |
|---|---|---|---|---|
| **AA1** Configurar herramientas de versionamiento para control de código | 40 | EV01 informe eligiendo la herramienta<br>EV02 estándares de codificación<br>EV03 tabla Git local contra remoto<br>EV04 instalación de Git y GitHub con pantallazos<br>EV05 laboratorio de comandos (video MP4 o pantallazos) | Git y GitHub **iguales**. Estándares: **PEP 8** revisado con **Ruff** en vez de las convenciones de Java | [Clase 2026-07-02](2026-07-02-AA1-versionamiento-git-y-estandares/) |
| **AA2** Aplicar estándares de codificación | 96 | EV01 módulo de escritorio con **JDBC** y CRUD<br>EV02 módulo web con formularios HTML, **Servlets**, GET, POST y **JSP** (Tomcat) | SQL directo con **sqlite3/PyMySQL** (o SQLAlchemy); web con **FastAPI + Jinja2** | [2026-08-06](2026-08-06-AA2-estandares-jdbc-servlets/) |
| **AA3** Codificar módulos stand-alone, web y móvil | 122 | EV01 módulo del proyecto (en clase: escritorio con Swing, CRUD y MySQL)<br>EV02 Word con normas APA, pantallazo por historia de usuario, pruebas de validación y video individual | **Flet** (escritorio) + **SQLAlchemy** (MySQL) + **pytest** para las validaciones | [2026-09-03](2026-09-03-AA3-modulo-escritorio-con-base-de-datos/) · [2026-09-09](2026-09-09-AA3-poo-clases-objetos-encapsulamiento/) · [2026-09-10](2026-09-10-AA3-entrega-evidencias-crud/) |
| **AA4** Codificar el frontend con framework | 96 | EV01 taller de React (React y JSX, clases, eventos, mapa conceptual)<br>EV02 listas de chequeo de componentes frontend<br>EV03 componente frontend del proyecto | **React** (es JavaScript, se usa igual) con **Vite**, conectado a una API en **FastAPI** en vez de Spring Boot | [2026-09-16](2026-09-16-AA4-frontend-react-y-frameworks/) |
| **AA5** Crear servicios web | 144 | EV01 servicio de registro e inicio de sesión (PHP en el material)<br>EV02 pruebas con **Postman** (video, pantallazos, endpoints)<br>EV03 API del proyecto documentada<br>EV04 pruebas de la API del proyecto con Postman | **FastAPI** (DTO con Pydantic, contraseñas con bcrypt); la documentación sale sola en `/docs`. Postman funciona igual | [2026-09-23](2026-09-23-AA5-servicio-web-login-y-postman/) (EV01 y EV02) · [2026-09-30](2026-09-30-AA5-api-del-proyecto-crud/) (EV03 y EV04) |

Todas las evidencias de código (AA2 a AA5) piden: **comentarios, estándar de codificación y el proyecto en Git**. Por eso la AA1 es la base de toda la guía.

## Clases de esta guía

| Fecha | Actividad | Tema | Material |
|---|---|---|---|
| 2026-07-02 | AA1 | Herramientas de versionamiento (Git) y estándares de codificación | [Ver](2026-07-02-AA1-versionamiento-git-y-estandares/) |
| 2026-08-06 | AA2 | Estándares: CRUD con JDBC y módulo web con Servlets y JSP | [Ver](2026-08-06-AA2-estandares-jdbc-servlets/) |
| 2026-09-03 | AA3 | Primer módulo de escritorio conectado a la base de datos (CRUD) | [Ver](2026-09-03-AA3-modulo-escritorio-con-base-de-datos/) |
| 2026-09-09 | AA3 | Programación orientada a objetos desde cero (clase, objeto, constructor, encapsulamiento) | [Ver](2026-09-09-AA3-poo-clases-objetos-encapsulamiento/) |
| 2026-09-10 | AA3 | Cómo entregar las evidencias del módulo stand-alone (CRUD, try-catch, Word y video) | [Ver](2026-09-10-AA3-entrega-evidencias-crud/) |
| 2026-09-16 | AA4 | Frameworks, Spring Boot y frontend con React | [Ver](2026-09-16-AA4-frontend-react-y-frameworks/) |
| 2026-09-23 | AA5 | Servicio web de registro e inicio de sesión y pruebas con Postman | [Ver](2026-09-23-AA5-servicio-web-login-y-postman/) |
| 2026-09-30 | AA5 | API del proyecto: endpoints CRUD y pruebas con Postman (cierre de la GA7) | [Ver](2026-09-30-AA5-api-del-proyecto-crud/) |
