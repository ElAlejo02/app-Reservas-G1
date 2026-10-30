"""Módulo web con formulario, GET, POST y plantillas: equivale a Servlets + JSP (GA7-AA2-EV02).

Qué enseña: lo que el instructor hizo en Eclipse con Tomcat:
    index.html con <form action="MiPrimerServlet" method="get">   -> plantillas/index.html
    class MiPrimerServlet extends HttpServlet { doGet(...) / doPost(...) }
                                                                  -> funciones @app.get / @app.post
    request.getParameter("usuario")                               -> parámetros usuario y clave
    response.setContentType("text/html"); PrintWriter pw...       -> TemplateResponse(...)
    Páginas .jsp con <%@ %>, <%= %>, <% %> y <%! %>               -> plantillas Jinja2
    Tomcat en el puerto 8082                                      -> Uvicorn en el puerto 8082

Cómo correrlo (desde la carpeta web_servlets):
    pip install "fastapi<0.145" uvicorn jinja2 python-multipart
    uvicorn main:app --reload --port 8082
Abrir http://127.0.0.1:8082  (usuario root, clave root, como en clase)
"""

from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Módulo web · equivalente a Servlets y JSP")
plantillas = Jinja2Templates(directory=Path(__file__).parent / "plantillas")

USUARIO_PRUEBA, CLAVE_PRUEBA = "root", "root"


def validar(usuario: str, clave: str) -> bool:
    return usuario == USUARIO_PRUEBA and clave == CLAVE_PRUEBA


@app.get("/", response_class=HTMLResponse)
def inicio(request: Request):
    """La página index con los dos formularios (uno GET y uno POST)."""
    return plantillas.TemplateResponse(request, "index.html")


@app.get("/ingreso", response_class=HTMLResponse)
def ingreso_get(request: Request, usuario: str = "", clave: str = ""):
    """doGet: los datos llegan en la URL (?usuario=...&clave=...). Por eso GET es inseguro."""
    return plantillas.TemplateResponse(
        request,
        "resultado.html",
        {"usuario": usuario, "correcto": validar(usuario, clave), "metodo": "GET"},
    )


@app.post("/ingreso", response_class=HTMLResponse)
def ingreso_post(request: Request, usuario: str = Form(""), clave: str = Form("")):
    """doPost: los datos viajan en el cuerpo de la petición, no se ven en la URL."""
    return plantillas.TemplateResponse(
        request,
        "resultado.html",
        {"usuario": usuario, "correcto": validar(usuario, clave), "metodo": "POST"},
    )


@app.get("/ejemplos-plantilla", response_class=HTMLResponse)
def ejemplos_plantilla(request: Request):
    """Lo mismo que las páginas expresiones.jsp, scripts.jsp y declaraciones.jsp de la clase."""
    return plantillas.TemplateResponse(
        request,
        "ejemplos_plantilla.html",
        {"ahora": datetime.now(), "nombre": "Sofía Herrera", "a": 10, "b": 5},
    )
