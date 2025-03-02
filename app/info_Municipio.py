from fasthtml.common import *
from fasthtml.components import Uk_input_tag
from fasthtml.svg import *
from monsterui.all import *
import plotly.express as px
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
        header=(H3('Listado de Precios'),Subtitle('Precios de la ultima fecha almacenada en la BBDD')),
        )
    )

def generarGrafica_MAP_Gasoil(df):
    fig = px.scatter_map(df, lat="Latitud", lon="Longitud (WGS84)", hover_name="Rótulo",
        color="Precio Gasoleo A", size="Precio Gasoleo A",
        color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=12)
    fig.update_layout(
        autosize=True,
        margin=dict(l=20, r=20, t=20, b=20), hovermode='x unified',
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showline=True, linewidth=1, linecolor='white', gridcolor='rgba(0,0,0,0)'),
        yaxis=dict(showline=True, linewidth=1, linecolor='white', gridcolor='rgba(0,0,0,0)'))
    return fig.to_html(include_plotlyjs=True, full_html=False, config={'displayModeBar': False})

def generarGrafica_MAP_Gasolina(df):
    df = df[df['Precio Gasolina 95 E5'].notna()]
    fig = px.scatter_map(df, lat="Latitud", lon="Longitud (WGS84)", hover_name="Rótulo",
        color="Precio Gasolina 95 E5", size="Precio Gasolina 95 E5",
        color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=12)
    fig.update_layout(
        autosize=True,
        margin=dict(l=20, r=20, t=20, b=20), hovermode='x unified',
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showline=True, linewidth=1, linecolor='white', gridcolor='rgba(0,0,0,0)'),
        yaxis=dict(showline=True, linewidth=1, linecolor='white', gridcolor='rgba(0,0,0,0)'))
    return fig.to_html(include_plotlyjs=True, full_html=False, config={'displayModeBar': False})

def generarGrafica_Gasolina(df):
    df = df[df['Precio Gasolina 95 E5'].notna()]
    fig = px.bar(df, x='IDEESS', y='Precio Gasolina 95 E5')
    fig.update_layout(
        autosize=True,
        margin=dict(l=20, r=20, t=20, b=20), hovermode='x unified',
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showline=True, linewidth=1, linecolor='white', gridcolor='rgba(0,0,0,0)'),
        yaxis=dict(showline=True, linewidth=1, linecolor='white', gridcolor='rgba(0,0,0,0)'))
    fig.update_layout(xaxis_title="Fecha", yaxis_title="Precio [€/L]")
    fig.update_yaxes(title_font_color="white", color="white", rangemode="tozero")
    fig.update_xaxes(title_font_color="white", color="white")
    return fig.to_html(include_plotlyjs=True, full_html=False, config={'displayModeBar': False})

def Info_ubicacion_Gasolinera(valor_info):
    valores =(
        ('map-pinned', "Provincia", valor_info['Provincia']), 
        ('building-2', "Municipio", valor_info['Municipio']),
        ('pin', "Localidad", valor_info['Localidad']),
        ('locate-fixed', "Dirección", valor_info['Dirección']),
        ('mail', "Código Postal", valor_info['C.P.'])
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
        ('map-pinned', "Provincia", valor_info['IDProvincia']), 
        ('map-pinned', "Municipio", valor_info['IDMunicipio']),
        ('map-pinned', "IDCCAA", valor_info['IDCCAA']),
    )
    return(
        Card(
            NavContainer(
                *[NotificationRow(*row) for row in valores],
                cls=NavT.secondary),
            header = (H4('Ubicación'),Subtitle('Códigos')),
            body_cls='pt-0')
    )

def Info_Rotulo(valor_info):
    valores =(
        ('map-pinned', "Rótulo", valor_info['Rótulo']), 
        ('map-pinned', "Tipo Venta", valor_info['Tipo Venta']),
        ('map-pinned', "Margen", valor_info['Margen']),
    )
    return(
        Card(
            NavContainer(
                *[NotificationRow(*row) for row in valores],
                cls=NavT.secondary),
            header = (H4('Ubicación'),Subtitle('Códigos')),
            body_cls='pt-0')
    )