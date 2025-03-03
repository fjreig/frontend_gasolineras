from fasthtml.common import *
from fasthtml.components import Uk_input_tag
from fasthtml.svg import *
from monsterui.all import *

def Tabla_comparativa(valores):
    header_data = ['_id', 'Gasoleo', 'Gasolina']
    body_data = valores
    return(
        Card(
            TableFromDicts(header_data, body_data),   
            header = (H4('Precio Medio por Provincia'))
            )
        )