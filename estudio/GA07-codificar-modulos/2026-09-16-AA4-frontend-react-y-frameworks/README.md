# Clase GA7 · AA4 · Frameworks, Spring Boot y frontend con React

| Dato | Valor |
|---|---|
| Guía | GA7 · Codificar los módulos del software |
| Competencia | 220501096 · Desarrollar la solución de software de acuerdo con el diseño y metodologías de desarrollo |
| Resultado de aprendizaje | 220501096-04 · Codificar el software de acuerdo con el diseño establecido |
| Actividad | GA7-220501096-AA4 · Codificar el frontend utilizando framework (96 h) |
| Evidencias | AA4-EV01 (taller), AA4-EV02 (componentes y justificación), AA4-EV03 (componente frontend del proyecto) |
| Fecha de la clase | 2026-09-16 (tomada del nombre del archivo de video) · 39 min |
| Transcripción y acta | En tu PC: `Claude\Projects\Sena\Clases\GA07 - Codificar modulos y versionamiento\` |
| Próxima clase | El miércoles siguiente. La instructora enviará la presentación con los pasos por WhatsApp |

> **Esta actividad pide React, que no es Java.** React es JavaScript, así que el grupo lo puede usar tal cual. Para el backend, donde la instructora usa **Spring Boot**, nosotros usamos **FastAPI**. La instructora repitió que se puede usar "cualquier plataforma, cualquier framework". Ver el ejemplo completo en la sección 7.

---

## 1. Resumen en un minuto

1. **Framework** = un marco de trabajo ya construido (herramientas, reglas, librerías y arquitectura) para no empezar de cero. Su analogía: sin framework fabricas hasta los ladrillos; con framework compras un apartamento en obra negra y solo lo terminas.
2. Ejemplos que dio: **Spring Boot** (Java), **Django** (Python), Laravel (PHP), **React** (JavaScript) y **Hibernate** (Java: convierte tablas en objetos sin escribir SQL a mano).
3. Instaló **Spring Boot**: variable de entorno `JAVA_HOME`, proyecto creado en **start.spring.io** (Maven, Java 21, dependencia **Spring Web**), abierto en NetBeans; servidor local en el puerto **8080** mostrando un formulario HTML.
4. Instaló **Node.js** y creó un proyecto **React con Vite** (`npm create vite@latest`), que corre en el puerto **5173**, con un formulario "Registro de aprendices" que se conecta al servidor local.
5. **Frontend** = lo que ve y toca el usuario (el corazón de "me gusta" de Instagram). **Backend** = la lógica, el servidor, la base de datos y las APIs. Lo siguiente será crear servidores y **servicios web** (AA5).

---

## 2. Conceptos de la clase, explicados

### 2.1 ¿Qué es un framework y para qué sirve?

| Para qué sirve (lo dijo la instructora) | Ejemplo en el sistema de reservas |
|---|---|
| Acelera el desarrollo | FastAPI arma la API y su documentación (`/docs`) sola |
| Garantiza la seguridad | Valida los datos que llegan antes de tocar la base de datos |
| Estandariza la calidad | Todo el grupo organiza el código igual |
| Facilita el trabajo en equipo | Uno hace el frontend en React y otro la API, sin pisarse |

En tu mundo: **AppSheet** es casi un framework: ya trae formularios, vistas y seguridad; tú solo pones las reglas del negocio. Programar sin framework sería hacer AppSheet desde cero.

### 2.2 Frameworks que nombró y su equivalente

| Lenguaje | Framework que nombró | Para qué | Equivalente que usamos |
|---|---|---|---|
| Java | **Spring Boot** | Backend empresarial: servidor, base de datos, seguridad | **FastAPI** (Python) |
| Java | **Hibernate** | ORM: tablas ↔ objetos sin escribir SQL | **SQLAlchemy** (ya lo usamos en la AA3) |
| Python | **Django** | Backend completo con panel de administración | Alternativa a FastAPI si piden panel admin |
| JavaScript | **React** | Frontend: interfaces interactivas | **React** (el mismo) |
| PHP | Laravel | Backend web | (no lo usamos) |

**Inyección de dependencias:** la instructora resaltó que en Spring "no llamas la herramienta con `new`; dejas que Spring te la inyecte". FastAPI tiene lo mismo con `Depends(...)`: por ejemplo, la sesión de base de datos llega sola a cada endpoint.

### 2.3 React y JSX (pregunta 1 del taller)

| | React | JSX |
|---|---|---|
| Qué es | **Biblioteca** de JavaScript creada por Meta (Facebook) para construir interfaces con **componentes** | **Extensión de sintaxis** de JavaScript que permite escribir algo parecido a HTML dentro del código |
| Rol (según la instructora) | El **motor** que procesa la lógica y actualiza la pantalla | El **lenguaje visual** con el que le dices al motor cómo debe verse |
| Ejemplo | `useState`, `useEffect`, componentes | `<button onClick={guardar}>Guardar</button>` |
| ¿Se puede usar uno sin el otro? | Sí, con `React.createElement(...)`, pero es incómodo | No sirve sin una herramienta que lo traduzca (Vite lo hace) |

### 2.4 Clases en React (pregunta 2 del taller)
Un **componente de clase** hereda de `React.Component`, guarda su estado en `this.state`, lo cambia con `this.setState()` y dibuja con `render()`. Tiene **métodos de ciclo de vida** como `componentDidMount()` (cuando aparece en pantalla). Es la forma antigua; hoy se usan **componentes funcionales** con *hooks* (`useState`, `useEffect`). El ejemplo trae los dos: [ContadorReservas.jsx](ejemplos/frontend-react/src/componentes/ContadorReservas.jsx) (clase) y [FormularioPasajero.jsx](ejemplos/frontend-react/src/componentes/FormularioPasajero.jsx) (función).

| Componente de clase | Componente funcional |
|---|---|
| `class X extends Component` | `function X()` |
| `this.state = {...}` en el constructor | `const [valor, setValor] = useState(...)` |
| `this.setState({...})` | `setValor(...)` |
| `componentDidMount()` | `useEffect(() => {...}, [])` |
| `render() { return (...) }` | `return (...)` |

### 2.5 Principales eventos de React (pregunta 3 del taller)

| Evento | Cuándo se dispara | En el ejemplo |
|---|---|---|
| `onClick` | Clic en un botón o elemento | Botones `+`, `−` y `Eliminar` |
| `onChange` | Cambia el valor de un input o select | Cada campo del formulario |
| `onSubmit` | Se envía un formulario | `guardar` del formulario (con `preventDefault()` para no recargar) |
| `onFocus` / `onBlur` | Entra o sale el cursor de un campo | Validar un campo al salir |
| `onKeyDown` | Se presiona una tecla | Buscar al presionar Enter |
| `onMouseEnter` / `onMouseLeave` | El mouse entra o sale | Mostrar ayudas |

En React los eventos se escriben en **camelCase** (`onClick`, no `onclick`) y reciben una **función**, no un texto.

### 2.6 Mapa conceptual de React (pregunta 4 del taller)
Base para dibujarlo en el Word (por ejemplo en draw.io):

```
                               REACT (biblioteca de JavaScript, Meta)
                                              │
        ┌──────────────────┬──────────────────┼──────────────────┬───────────────────┐
   COMPONENTES            JSX              ESTADO              PROPS             EVENTOS
   ├ Funcionales     (HTML dentro de JS)  (datos que cambian) (datos del padre   onClick, onChange,
   │  + hooks                             useState            al hijo, solo      onSubmit, onFocus...
   └ De clase                             this.state          lectura)
      + ciclo de vida                          │
                                         CICLO DE VIDA / EFECTOS
                                         useEffect, componentDidMount
        │
   HERRAMIENTAS: Node.js + npm · Vite (crea el proyecto y el servidor 5173) · fetch para hablar con la API
```

### 2.7 Spring Boot paso a paso (lo que hizo en clase) y su equivalente

| Paso en clase | Para qué | En Python con FastAPI |
|---|---|---|
| Variable de entorno `JAVA_HOME` y `Path` | Que Windows encuentre Java | Python ya queda en el `Path` al instalarlo |
| `java -version` en CMD | Verificar | `python --version` |
| start.spring.io: Maven, Java 21, **Spring Web**, *Generate* | Crear el esqueleto del proyecto | `pip install fastapi uvicorn` y un archivo `.py` |
| Descomprimir y abrir en NetBeans | | Abrir la carpeta en VS Code |
| *Clean and Build* cuando falla por caché | Limpiar compilados viejos | Borrar `__pycache__` (rara vez hace falta) |
| Servidor en `localhost:8080` | Tomcat embebido | `uvicorn api_pasajeros:app --port 8000` |

### 2.8 React con Vite paso a paso

1. Instalar **Node.js** (trae `npm`). Verificar: `node --version`.
2. `npm create vite@latest frontend-react` → elegir **React** y **JavaScript**. (A la instructora le falló la primera vez porque escribió el comando sin `npm`.)
3. `cd frontend-react`, `npm install`, `npm run dev` → abre en `http://localhost:5173`. **No cerrar esa terminal**: es el servidor local.
4. Reemplazar `src/App.jsx` por tu componente. Su error de clase: faltaba una **comilla invertida** `` ` `` (se usa para textos con variables: `` `Hola ${nombre}` ``).

---

## 3. Lo que se hizo en Java y cómo se hace en Python

| En clase | Nosotros |
|---|---|
| Spring Boot (backend en 8080) | **FastAPI + Uvicorn** (backend en 8000): [api_pasajeros.py](ejemplos/api_pasajeros.py) |
| HTML servido por Spring | React servido por Vite (5173), que pide datos a la API |
| Hibernate | SQLAlchemy |
| React con Vite | **Igual**: [frontend-react/](ejemplos/frontend-react/) |
| NetBeans para todo | VS Code (tiene soporte para Python y para React) |

---

## 4. Evidencias

### AA4-EV01 · Taller sobre componentes frontend (conocimiento)
- [ ] Documento en Word, entregado en **PDF**: portada, introducción, objetivo y **principales características del framework**.
- [ ] 1. Diferencia entre React y JSX → sección 2.3.
- [ ] 2. ¿Qué son clases en React? → sección 2.4 (con el código de `ContadorReservas.jsx` como ejemplo).
- [ ] 3. Principales eventos de React → sección 2.5.
- [ ] 4. Mapa conceptual de React → sección 2.6 (dibujarlo, no copiar el texto).

### AA4-EV02 · Componentes frontend del proyecto con justificación (desempeño)
- [ ] Documento (PDF) que describa **qué componentes de React** usará el proyecto y **por qué**. Base sugerida:

| Componente | Qué hace | Justificación |
|---|---|---|
| `Login` | Usuario y contraseña | Todo el sistema depende del rol (ADMIN, ASESOR...) |
| `MenuPrincipal` | Accesos según el rol | Navegación jerárquica (vista en la GA6) |
| `FormularioPasajero` | Registrar y editar pasajeros | Historia de usuario "registrar pasajero" |
| `TablaPasajeros` / `TablaReservas` | Listar con filtros | Consultar y elegir para editar |
| `BuscadorHoteles` | Destino, fechas, personas | Primer paso del asistente de reserva |
| `AsistenteReserva` | Pasos: hotel → pasajeros → confirmar | Navegación lineal (GA6) |
| `TarjetaHotel` | Foto, categoría y tarifa | Se repite en la lista: un componente reutilizable |
| `Mensaje` | Avisos de éxito o error | Un solo estilo de mensajes en toda la app |

### AA4-EV03 · Componente frontend del proyecto (producto)
- [ ] Codificar en **React** un módulo del proyecto (sugerido: pasajeros, partiendo del ejemplo).
- [ ] Basado en el diagrama de clases, los casos de uso, las historias de usuario y los prototipos.
- [ ] **Comentarios**, **estándares** y **Git**.
- [ ] ZIP `NOMBRE_APELLIDO_AA4_EV03` con el proyecto **sin `node_modules`** y el enlace del repositorio.
- [ ] La instructora pidió que se vea "llamativo, bonito": cuidar colores y estilos.

---

## 5. Aplicación al proyecto de reservas

- **Arquitectura que queda armada:** React (lo que ve el asesor) → FastAPI (reglas: no confirmar sin pasajeros, código `HDMDE001`) → MySQL. Es la misma separación que tiene **Travel Compositor**: la pantalla del backoffice es una cosa y el motor que calcula tarifas y guarda la reserva es otra.
- **Booking** está hecho con componentes: la tarjeta de cada hotel es el mismo componente repetido con datos distintos (props). En el proyecto, `TarjetaHotel` debería funcionar igual.
- La app de escritorio en **Flet** de la AA3 puede llamar a la misma API de FastAPI: así la regla de negocio se escribe una sola vez para la web y para el escritorio.

---

## 6. Qué estudiar

| Sesión | Tema | Recurso | Práctica |
|---|---|---|---|
| 1 | Qué es React, JSX y componentes | [react.dev en español: Inicio rápido](https://es.react.dev/learn) | Responder las preguntas 1 y 2 del taller |
| 2 | Estado y eventos | [react.dev: Responder a eventos](https://es.react.dev/learn/responding-to-events) y [El estado](https://es.react.dev/learn/state-a-components-memory) | Agregar un campo "teléfono" al formulario |
| 3 | Pedir datos a una API | [FastAPI: primeros pasos](https://fastapi.tiangolo.com/es/tutorial/first-steps/) | Correr el ejemplo completo |
| 4 | Componentes del proyecto | Sección 4 de esta guía | Escribir la EV02 |
| 5 | Mapa conceptual | draw.io | Pregunta 4 del taller |

Cursos completos: Platzi [Curso de FastAPI](https://platzi.com/cursos/fastapi/) y la ruta de estudio en `Claude\Projects\Sena\Ruta de estudio\`.

---

## 7. Ejemplos de código

| Archivo | Qué enseña | Captura |
|---|---|---|
| [api_pasajeros.py](ejemplos/api_pasajeros.py) | Backend con FastAPI: GET, POST, DELETE, validación con Pydantic y CORS | |
| [frontend-react/src/App.jsx](ejemplos/frontend-react/src/App.jsx) | Componente principal, `useEffect`, comunicación padre-hijo | [inicio](capturas/01_inicio.png) |
| [FormularioPasajero.jsx](ejemplos/frontend-react/src/componentes/FormularioPasajero.jsx) | Componente funcional, `useState`, `onChange`, `onSubmit`, `fetch` POST | [guardado](capturas/02_guardado.png) · [error](capturas/03_error_duplicado.png) |
| [TablaPasajeros.jsx](ejemplos/frontend-react/src/componentes/TablaPasajeros.jsx) | Props, listas con `map` y `key`, `onClick` | |
| [ContadorReservas.jsx](ejemplos/frontend-react/src/componentes/ContadorReservas.jsx) | **Componente de clase**: `this.state`, `setState`, `componentDidMount` | |
| [vite.config.js](ejemplos/frontend-react/vite.config.js) | Proxy de `/api` hacia el backend | |

### Cómo correrlo (dos terminales)
**Terminal 1, backend:**
```
cd "estudio\GA07-codificar-modulos\2026-09-16-AA4-frontend-react-y-frameworks\ejemplos"
pip install "fastapi<0.145" uvicorn
uvicorn api_pasajeros:app --reload --port 8000
```
**Terminal 2, frontend:**
```
cd "estudio\GA07-codificar-modulos\2026-09-16-AA4-frontend-react-y-frameworks\ejemplos\frontend-react"
npm install
npm run dev
```
Abrir `http://localhost:5173`. La documentación de la API queda en `http://127.0.0.1:8000/docs`.

### El código parte por parte
1. **api_pasajeros.py:** `class Pasajero(BaseModel)` define qué datos acepta la API (documento de 5 a 12 dígitos, edad 0 a 120, género cerrado); si no cumplen, FastAPI responde error 422 sin que escribas nada. `@app.post` guarda y responde 409 si el documento ya existe. `CORSMiddleware` deja que el puerto 5173 le hable al 8000.
2. **vite.config.js:** el `proxy` hace que `fetch('/api/pasajeros')` desde React llegue al backend sin escribir el puerto.
3. **App.jsx:** guarda la lista en `useState`, la carga con `useEffect` al abrir, y le pasa a cada hijo lo que necesita: la lista a la tabla y la función `cargarPasajeros` al formulario (`onGuardado`).
4. **FormularioPasajero.jsx:** cada `input` tiene `value` (lo que muestra) y `onChange` (lo que actualiza). `onSubmit` hace el POST con `fetch` y, según la respuesta, muestra "Pasajero guardado" o el error que devolvió la API.
5. **TablaPasajeros.jsx:** recibe la lista por **props** y la dibuja con `map`. Cada fila lleva `key` para que React sepa cuál cambió.
6. **ContadorReservas.jsx:** el mismo tipo de lógica, pero como **clase**: estado en el constructor, `setState` en los botones y `componentDidMount` al aparecer.

---

## 8. Repaso

<details><summary>1. ¿Qué es un framework, con la analogía de la clase?</summary>
Un marco de trabajo con herramientas, reglas y arquitectura ya construidas. Sin framework fabricas hasta los ladrillos; con framework compras el apartamento en obra negra y solo lo terminas.
</details>

<details><summary>2. ¿Qué diferencia hay entre React y JSX?</summary>
React es la biblioteca (el motor que maneja componentes y estado). JSX es la sintaxis parecida a HTML con la que se describe cómo se ve cada componente.
</details>

<details><summary>3. ¿Qué es un componente de clase y qué lo reemplazó?</summary>
Un componente que hereda de React.Component, con this.state, setState y métodos de ciclo de vida. Hoy se usan componentes funcionales con hooks como useState y useEffect.
</details>

<details><summary>4. Nombra cuatro eventos de React.</summary>
onClick, onChange, onSubmit y onFocus (también onBlur, onKeyDown, onMouseEnter).
</details>

<details><summary>5. ¿Qué es Spring Boot y cuál es su equivalente en Python?</summary>
El framework empresarial de Java para backend. En Python: FastAPI (o Django si se necesita panel de administración).
</details>

<details><summary>6. ¿Qué hace Hibernate y cuál es su equivalente?</summary>
Convierte tablas de la base de datos en objetos de Java sin escribir SQL a mano. En Python: SQLAlchemy.
</details>

<details><summary>7. ¿En qué puertos corrían Spring Boot y Vite en la clase?</summary>
Spring Boot en el 8080 y Vite (React) en el 5173. En nuestro ejemplo FastAPI usa el 8000.
</details>

<details><summary>8. ¿Qué diferencia hay entre frontend y backend?</summary>
El frontend es lo que el usuario ve y toca en el navegador. El backend maneja la lógica, el servidor, la base de datos y las APIs.
</details>

<details><summary>9. ¿Qué carpeta nunca se sube en el ZIP ni a Git en un proyecto de React?</summary>
node_modules (se vuelve a crear con npm install). También dist.
</details>

Tarjetas para Anki: [repaso-anki.csv](repaso-anki.csv).
