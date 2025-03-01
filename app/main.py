from fasthtml import FastHTML
from pathlib import Path
from fasthtml.common import *
from monsterui.all import *
from datetime import datetime

from app.models import add_gasolineras, get_all_tasks, filter_by_localidad
from app.lista import consultar_datos
from app.gasolineras import ObtenerPrecio

hdrs = (Theme.green.headers())
app, rt = fast_app(hdrs=hdrs)

@dataclass
class New_Element:
    equipo: str
    categoria: str
    fabricante: str
    modelo: str
    descripcion: str
    habilitado: bool

current_page = 0
current_localidad = "" 

@rt('/')
def index():
    global current_page
    global current_localidad
    if current_localidad == "":
        (num_filas, data) = get_all_tasks(current_page)
    else:
        (num_filas, data) = filter_by_localidad(current_localidad, current_page)
    return consultar_datos(num_filas, data, current_page)

@app.post('/filtrar_localidad')
def post(FiltroLocalidad:str):
    global current_localidad
    global current_page
    current_page = 0
    current_localidad = FiltroLocalidad
    return Redirect(f"/")

@app.post('/first_page')
def post():
    global current_page
    current_page = 0
    return Redirect(f"/")

@app.post('/next_page')
def post():
    global current_page
    current_page+= 1
    return Redirect(f"/")

@app.post('/previous_page')
def post():
    global current_page
    if current_page >= 1:
        current_page-= 1
    else:
        current_page=0
    return Redirect(f"/")

@rt('/gasolineras')
def post():
    print("Obtener Precio")
    valores = ObtenerPrecio()
    print("guardar")
    add_gasolineras(valores)
    return Redirect(f"/")


serve()