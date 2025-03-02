from fasthtml import FastHTML
from pathlib import Path
from fasthtml.common import *
from monsterui.all import *
from datetime import datetime
from fh_altair import altair_headers
import pandas as pd

from app.models import add_gasolineras, get_all_tasks, filter_by_municipio, filter_by_id, filter_by_id_info, filter_by_municipio_all, get_last_page
from app.lista import consultar_datos
from app.gasolineras import ObtenerPrecio
from app.dashboard import generate_chart_Gasoil, generate_chart_Gasolina95
from app.info import (
    Info_ubicacion_Gasolinera, 
    Info_precios_carburante, 
    Info_Horario, 
    Info_ubicacion_Gasolinera_Codigos,
    Info_map,
    Info_Rotulo
)

from app.info_Municipio import (
    generarGrafica_MAP_Gasoil,
    generarGrafica_MAP_Gasolina,
    generarGrafica_Gasolina
)

hdrs = (Theme.green.headers(), altair_headers)
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

@rt('/informacion/{id}')
def index(id: str):
    df_gasolinerra = filter_by_id_info(id)
    return Title("Info Gasolinera"), Container(
        H2(f'Info Gasolinera {id}'),
        DivRAligned(
            Button("Volver", cls=ButtonT.destructive, hx_post="/return"),
        ),
        Grid(*map(Div,(
            Div(Info_ubicacion_Gasolinera(df_gasolinerra), Info_ubicacion_Gasolinera_Codigos(df_gasolinerra), cls='space-y-4'),
            Div(Info_Horario(df_gasolinerra), Info_precios_carburante(df_gasolinerra), cls='space-y-4'),
            Div(Info_Rotulo(df_gasolinerra), Info_map(df_gasolinerra), cls='space-y-4'))),
         cols_md=1, cols_lg=2, cols_xl=3),
        cls=('space-y-4', ContainerT.xl))

@rt('/graficas/{id}')
def index(id: str):
    df_gasolinerra = filter_by_id(id)
    return Title("Historicos"), Container(
        H2('Graficos'),
        DivRAligned(
            Button("Volver", cls=ButtonT.destructive, hx_post="/return"),
        ),
        Grid(
            Card(Safe(generate_chart_Gasoil(df_gasolinerra)), cls='col-span-3'),
            Card(Safe(generate_chart_Gasolina95(df_gasolinerra)), cls='col-span-3'),
            gap=2, cols_xl=6, cols_lg=6, cols_md=1, cols_sm=1, cols_xs=1),
        cls=('space-y-4', ContainerT.xl)
        )

@rt('/info_municipio/{municipio}')
def index(municipio: str):
    df_gasolinera = filter_by_municipio_all(municipio)
    df_gasolinera = pd.DataFrame.from_records(df_gasolinera)
    return Title("Info Municipio"), Container(
        H2(f'Info por Municipio {municipio}'),
        DivRAligned(
            Button("Volver", cls=ButtonT.destructive, hx_post="/return"),
        ),
        Grid(
            Card(Safe(generarGrafica_MAP_Gasoil(df_gasolinera)), cls='col-span-3'),
            Card(Safe(generarGrafica_MAP_Gasolina(df_gasolinera)), cls='col-span-3'),
            Card(Safe(generarGrafica_Gasolina(df_gasolinera)), cls='col-span-3'),
            gap=2, cols_xl=6, cols_lg=6, cols_md=1, cols_sm=1, cols_xs=1),
        cls=('space-y-4', ContainerT.xl)
        )

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

@app.post('/last_page')
def post():
    last_page = get_last_page()
    global current_page
    current_page = last_page
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

@rt('/info/{gasolinera}')
def info_gasolinera(gasolinera: str):
    valor = filter_by_id_info(gasolinera)
    gasolinera_info = valor['IDEESS']
    return Redirect(f"/informacion/{gasolinera_info}")

@rt('/charts/{gasolinera}')
def info_gasolinera(gasolinera: str):
    valor = filter_by_id_info(gasolinera)
    gasolinera_info = valor['IDEESS']
    return Redirect(f"/graficas/{gasolinera_info}")

@rt('/map/{municipio}')
def info_gasolinera(municipio: str):
    return Redirect(f"/info_municipio/{municipio}")

@rt('/return')
def info_gasolinera():
    return Redirect(f"/")

@rt('/gasolineras')
def post():
    print("Obtener Precio")
    valores = ObtenerPrecio()
    print("guardar")
    add_gasolineras(valores)
    return Redirect(f"/")


serve()