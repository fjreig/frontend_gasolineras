from fasthtml.common import *
from fasthtml.components import Uk_input_tag
from fasthtml.svg import *
from monsterui.all import *
import plotly.express as px
from fh_plotly import plotly2fasthtml
from datetime import datetime
import pandas as pd

def NotificationRow(icon, name, desc):
    return Li(cls='-mx-1')(A(DivLAligned(UkIcon(icon),Div(P(name),P(desc, cls=TextPresets.muted_sm)))))

def Info_precios_carburante(valor_info):
    return(Card(
        DivLAligned(
            LabelInput(label='Gasoleo A', id='subject', value=valor_info['Precio Gasoleo A'], readonly=True),
            LabelInput(label='Gasoleo B', id='subject', value=valor_info['Precio Gasoleo B'], readonly=True),
        ),
        DivLAligned(
            LabelInput(label='Gasolina 95 E5', id='subject', value=valor_info['Precio Gasolina 95 E5'], readonly=True),
            LabelInput(label='Gasolina 95 E10', id='subject', value=valor_info['Precio Gasolina 95 E10'], readonly=True),
        ),
        DivLAligned(
            LabelInput(label='Gasolina 98 E5', id='subject', value=valor_info['Precio Gasolina 98 E5'], readonly=True),
            LabelInput(label='Gasolina 98 E10', id='subject', value=valor_info['Precio Gasolina 98 E10'], readonly=True),
        ),
        DivLAligned(
            LabelInput(label='Biodiesel', id='subject', value=valor_info['Precio Biodiesel'], readonly=True),
            LabelInput(label='Bioetanol', id='subject', placehvaluelder=valor_info['Precio Bioetanol'], readonly=True),
        ),
        DivLAligned(
            LabelInput(label='Gas Natural Licuado', id='subject', value=valor_info['Precio Gas Natural Licuado'], readonly=True),
            LabelInput(label='Gas Natural Comprimido', id='subject', value=valor_info['Precio Gas Natural Comprimido'], readonly=True),
        ),
        DivLAligned(
            LabelInput(label='Hidrogeno', id='subject', value=valor_info['Precio Hidrogeno'], readonly=True),
        ),
        header=(H3('Listado de Precios'),Subtitle('Precios de los diferente carburantes de esta gasolinera')),
        )
    )

def Info_Horario(valor_info):
    return(Card(H4("Horario"),
                Subtitle(f"Horario de la estación : {valor_info['Horario']}"),
                DivLAligned(
                        Div(datetime.now().strftime("%B %d, %Y")),
                        cls=('space-x-4',TextPresets.muted_sm)))
    )

def generarGrafica(valor_info):
    df = pd.DataFrame.from_dict(valor_info, orient='index')
    df = df.transpose()
    fig = px.scatter_map(df, lat="Latitud", lon="Longitud (WGS84)",
                    color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)
    return plotly2fasthtml(fig)

def Info_map(valor_info):
    generarGrafica(valor_info)
    return(Card(H4("Horario"),
                Subtitle(f"Mapa"),
                generarGrafica(valor_info)
        )
    )

def Info_ubicacion_Gasolinera(valor_info):
    valores =(
        ('bell', "Provincia", valor_info['Provincia']), 
        ('user', "Municipio", valor_info['Municipio']),
        ('ban', "Localidad", valor_info['Localidad']),
        ('ban', "Dirección", valor_info['Dirección']),
        ('ban', "Código Postal", valor_info['C.P.'])
    )
    return(
        Card(
            NavContainer(
                *[NotificationRow(*row) for row in valores],
                cls=NavT.secondary),
            header = (H4('Ubicación'),Subtitle('Información de la ubicación de la gasolinera seleccionada')),
            body_cls='pt-0')
    )

def Info_ubicacion_Gasolinera_Codigos(valor_info):
    valores =(
        ('bell', "Provincia", valor_info['IDProvincia']), 
        ('user', "Municipio", valor_info['IDMunicipio']),
        ('ban', "IDCCAA", valor_info['IDCCAA']),
    )
    return(
        Card(
            NavContainer(
                *[NotificationRow(*row) for row in valores],
                cls=NavT.secondary),
            header = (H4('Ubicación'),Subtitle('Códigos')),
            body_cls='pt-0')
    )