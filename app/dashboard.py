from fasthtml.common import *
import fasthtml.common as fh
from monsterui.all import *
from fasthtml.svg import *
import plotly.express as px

def generate_chart_Gasoil(df):    
    fig = px.line(df, x='Fecha', y=['Precio Gasoleo A'],  template='plotly_white', line_shape='spline')
    fig.update_traces(mode='lines+markers')
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20), hovermode='x unified',
        showlegend=True, legend=dict(orientation='h', yanchor='bottom', y=1.02,  xanchor='right', x=1),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showline=True, linewidth=1, linecolor='white', gridcolor='rgba(0,0,0,0)'),
        yaxis=dict(showline=True, linewidth=1, linecolor='white', gridcolor='rgba(0,0,0,0)'))
    fig.update_layout(xaxis_title="Fecha", yaxis_title="Intensidad [A]")
    fig.update_yaxes(title_font_color="white", color="white", rangemode="tozero")
    fig.update_xaxes(title_font_color="white", color="white")
    return fig.to_html(include_plotlyjs=True, full_html=False, config={'displayModeBar': False})

def generate_chart_Gasolina95(df):    
    fig = px.line(df,x='Fecha', y=['Precio Gasolina 95 E5'],template='plotly_white',line_shape='spline')
    fig.update_traces(mode='lines+markers')
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20), hovermode='x unified',
        showlegend=True, legend=dict(orientation='h', yanchor='bottom', y=1.02,  xanchor='right', x=1),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0)'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0)'))
    fig.update_layout(xaxis_title="Fecha", yaxis_title="Tension [V]")
    fig.update_yaxes(title_font_color="white", color="white", rangemode="tozero")
    fig.update_xaxes(title_font_color="white", color="white")
    return fig.to_html(include_plotlyjs=True, full_html=False, config={'displayModeBar': False})

def InfoCard(title, value, change): 
    return Card(H3(value),P(change, cls=TextPresets.muted_sm), header = H4(title))

def tipo_tarjeta(icono, name, valor1, valor2):
    return Card(
        DivLAligned(
            UkIcon(icono, height=50, width=50),
            Div(H3(name), P(valor1), P(valor2))
            ),
        )

def Generar_Cards(df):
    info_card_data = [tipo_tarjeta('plug-zap', "Potencia Activa", str(df['pa'][0]) + " kW", str(df['pa_peak'][0]) + " kW máxima de hoy"),
                    tipo_tarjeta('orbit', "Estado", int(df['estado'][0]), "+180.1% from last month"),
                    tipo_tarjeta('utility-pole', "Energía Generada", str(round(df['ea'][0])) + " kWh", str(df['ea_hoy'][0]) + " kWh generados hoy"),
                    tipo_tarjeta('thermometer', "Temperatura", str(df['temperatura'][0]) + ' ºC', "+201 since last hour")]
    return Grid(*info_card_data, cols_sm=1, cols_md=1, cols_lg=2, cols_xl=4)