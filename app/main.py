from fasthtml import FastHTML
from pathlib import Path
from fasthtml.common import *
from monsterui.all import *
from datetime import datetime

from app.models import add_gasolineras, get_all_tasks, filter_by_municipio
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
current_municipio = "" 

@rt('/')
def index():
    global current_page
    global current_municipio
    if current_municipio == "":
        (num_filas, data) = get_all_tasks(current_page)
    else:
        (num_filas, data) = filter_by_municipio(current_municipio, current_page)
    return consultar_datos(num_filas, data, current_page)

@app.post('/filtrar_municipio')
def post(FiltroMunicipio:str):
    global current_municipio
    global current_page
    current_page = 0
    current_municipio = FiltroMunicipio
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