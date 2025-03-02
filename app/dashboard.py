from fasthtml.common import *
import fasthtml.common as fh
from monsterui.all import *
from fasthtml.svg import *
import plotly.express as px

def generate_chart_Gasoil(df):    
    fig = px.line(df, x='Fecha', y=['Precio Gasoleo A', 'Precio Gasoleo B'],  template='plotly_white', line_shape='spline')
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
    fig = px.line(df,x='Fecha', y=['Precio Gasolina 95 E5', 'Precio Gasolina 95 E10'],template='plotly_white',line_shape='spline')
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

def Info_Horario(valor_info):
    return(Card(H4("Horario"),
                Subtitle(f"Horario de la estación : {valor_info['Horario']}"),
                DivLAligned(
                        Div(datetime.now().strftime("%B %d, %Y")),
                        cls=('space-x-4',TextPresets.muted_sm)))
    )