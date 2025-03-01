from fasthtml.common import *
from monsterui.all import *
from fasthtml.svg import *
from bson.objectid import ObjectId
import math
import os

from app.models import (
    get_all_tasks,
    BuscarLocalidad,
    BuscarProvincias,
    BuscarRotulos
)

Listado_Provincias = BuscarProvincias()
Listado_Localidades = BuscarLocalidad()
Listado_Rotulos = BuscarRotulos()

app, rt = fast_app(hdrs=Theme.blue.headers())

def LAlignedCheckTxt(txt): 
    return DivLAligned(UkIcon(icon='check'), P(txt, cls=TextPresets.muted_sm))

def _create_tbl_data(d):
    return {'ID': d['_id'], 'Municipio': d['Municipio'], 'Provincia': d['Provincia'], 'Localidad': d['Localidad'],
            'Latitud': d['Latitud'], 'Longitud': d['Longitud (WGS84)'] , 'GasoleoA': d['Precio Gasoleo A'],
            'Rotulo':  d['Rótulo']}

def CreateTaskModal():
    return Modal(
        Div(cls='p-6')(
            ModalTitle('Filtro Avanzado'),
            Br(),
            Form(cls='space-y-6')(
                Grid(Div(Select(*map(Option, Listado_Provincias), label='Provincias', id='Provincias', name='Provincias')),
                     Div(Select(*map(Option, Listado_Localidades), label='Localidades', id='Localidades', name='Localidades')),
                     Div(Select(*map(Option, Listado_Rotulos), label='Rotulos', id='Rotulos', name='Rotulos')),
                ),
                DivRAligned(
                    ModalCloseButton('Cancel', cls=ButtonT.ghost),
                    ModalCloseButton('Filtrar', cls=ButtonT.primary),
                    hx_post="/Filtro_Avanzado",
                    cls='space-x-5'))),
        id='FiltroForm')


def cell_render(col, val):
    global valor_id
    def _Td(*args,cls='', **kwargs): 
        return Td(*args, cls=f'p-2 {cls}',**kwargs)
    match col:
        case "ID": 
            valor_id = val
            return _Td(val, cls='uk-visible@s')
        case "Provincia": 
            return _Td(val, cls='uk-visible@s')
        case "Municipio": 
            return _Td(val, cls='uk-visible@s')
        case "Localidad":  
            return _Td(val, cls='uk-visible@s')
        case "Latitud": 
            return _Td(val, cls='font-medium')
        case "Longitud": 
            return _Td(val, cls='font-medium')
        case "Rotulo": 
            return _Td(val, cls='font-medium')
        case "GasoleoA": 
            return _Td(val, cls='font-medium')
        case "Actions": 
            return _Td(inventario_edit(valor_id), shrink=True)
        case _: raise ValueError(f"Unknown column: {col}")

def footer(num_row, current_page, total_pages):
    return DivFullySpaced(
        Div(f'1 of {num_row} row(s) selected.', cls=TextPresets.muted_sm),
        DivLAligned(
            DivCentered(f'Page {current_page + 1} of {total_pages}', cls=TextT.sm),
            DivLAligned(
                UkIconLink(icon='chevrons-left', button=True, hx_post="/first_page"),
                UkIconLink(icon='chevron-left', button=True, hx_post="/previous_page"),
                UkIconLink(icon='chevron-right', button=True, hx_post="/next_page"),
                UkIconLink(icon='chevrons-right', button=True, hx_post="/last_page") 
                )
            )
        )

def Generar_Alerta():
    return Alert(
        "Equipo Añadido Correctamente", 
        cls=AlertT.success
        )

def consultar_datos(num_row, data, current_page: int):
    page_size = int(os.environ['Num_equipos_por_pagina'])
    total_pages = math.ceil(num_row / page_size)
    data = [_create_tbl_data(d) for d in data]

    page_heading = DivFullySpaced(cls='space-y-2')(
        Div(cls='space-y-2')(
            H2('Lista de Gasolineras'),
            P("Precios del ultimo día", cls=TextPresets.muted_sm)),
        )

    table_controls =(
        DivLAligned(
            Form(DivLAligned(
                Input(cls='w-[250px]',placeholder='Filtro por localidad',name='FiltroLocalidad'),
                Button("Buscar",cls=(ButtonT.primary, TextPresets.bold_sm), hx_post="/filtrar_localidad")
            )),
            Button('Filtro',cls=(ButtonT.primary, TextPresets.bold_sm), data_uk_toggle="target: #FiltroForm"),
            Button('Gasolineras',cls=(ButtonT.primary, TextPresets.bold_sm), hx_post="/gasolineras")
            )
        )

    task_columns = ["ID", "Provincia", "Municipio", "Localidad", 'Latitud', 'Longitud', 'GasoleoA', 'Rotulo']

    tasks_table = Div(cls='mt-4')(
        TableFromDicts(
            header_data=task_columns,
            body_data=data,
            body_cell_render=cell_render,
            sortable=True,
            cls=(TableT.responsive, TableT.sm, TableT.divider)))

    tasks_ui = Div(DivFullySpaced(DivLAligned(table_controls), cls='mt-8'), tasks_table, footer(num_row, current_page, total_pages))
    return(Container(page_heading, tasks_ui, CreateTaskModal()))