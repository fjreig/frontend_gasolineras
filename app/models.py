from datetime import datetime
from fasthtml.common import *
from bson.objectid import ObjectId
import math
import os
import pandas as pd

from app.database import db

last_page = 0

def obtener_skip_equipos(num_pagina):
    num_ros_pagina = int(os.environ['Num_equipos_por_pagina'])
    if num_pagina == 0:
        offset_equipos = 0
    else:
        offset_equipos = (num_pagina * num_ros_pagina)
    return(offset_equipos, num_ros_pagina)

def get_all_tasks(num_pagina):
    (offset_equipos, limit_elementos) = obtener_skip_equipos(num_pagina)
    cursor = db.gasolineras.find(
        filter={'Precio Gasoleo A': {'$gt': 0}},
        projection={},
        sort=list({'Precio Gasoleo A': 1}.items()),
        collation={},
        skip=offset_equipos,
        limit=limit_elementos
        )
    num = db.gasolineras.count_documents({})
    global last_page
    last_page = math.ceil(num / int(os.environ['Num_equipos_por_pagina']))-1
    valores = list(cursor)
    return(num, valores)

def filter_by_municipio(Municipio, num_pagina):
    (offset_equipos, limit_elementos) = obtener_skip_equipos(num_pagina)
    cursor = db.gasolineras.find(
        filter={'Municipio': {'$regex': Municipio}, 'Precio Gasoleo A': {'$gt': 0}},
        projection={},
        sort=list({'Precio Gasoleo A': 1}.items()),
        collation={},
        skip=offset_equipos,
        limit=limit_elementos
        )
    num = db.gasolineras.count_documents({"Localidad":{"$regex": Municipio}})
    global last_page
    last_page = math.ceil(num / int(os.environ['Num_equipos_por_pagina']))-1
    valores = list(cursor)
    return(num, valores)

def get_last_page():
    global last_page
    return(last_page)

def filter_by_id_info(id):
    cursor = db.gasolineras.find(
        filter={'IDEESS': id},
        projection={},
        sort=list({'Fecha': 1}.items()),
        collation={},
        limit=1
        )
    valores = list(cursor)
    return(valores[0])

def filter_by_id(id):
    cursor = db.gasolineras.find(
        filter={'IDEESS': id},
        projection={},
        collation={},
        )
    valores = list(cursor)
    return(valores)

def filter_by_municipio_all(Municipio):
    pipeline = [   
        {'$addFields': {'fecha_string': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$Fecha'}}}}, 
        {'$match': {'fecha_string': '2025-03-02', 'Municipio': Municipio} }
        ]
    cursor = db.gasolineras.aggregate(pipeline)
    valores = list(cursor)
    return(valores)

def avg_by_provincias():
    pipeline1 =[
        {'$addFields': {'fecha_string': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$Fecha'}}}}, 
        {'$match': {'fecha_string': '2025-03-03', 'Precio Gasoleo A': {'$gt': 0}}}, 
        {'$project': {'Provincia': 1, 'Precio Gasoleo A': 1} }, 
        {'$group': {'_id': '$Provincia', 'Gasoleo': {'$avg': '$Precio Gasoleo A'}}},
        {'$project': {'Gasoleo': {'$round': ['$Gasoleo', 3]}}}
    ]
    pipeline2 = [
        {'$addFields': {'fecha_string': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$Fecha'}}}}, 
        {'$match': {'fecha_string': '2025-03-03', 'Precio Gasolina 95 E5': {'$gt': 0}}}, 
        {'$project': {'Provincia': 1, 'Precio Gasolina 95 E5': 1}}, 
        {'$group': {'_id': '$Provincia', 'Gasolina': {'$avg': '$Precio Gasolina 95 E5'}}}, 
        {'$project': {'Gasolina': {'$round': ['$Gasolina', 3]}}}
    ]

    cursor1= db.gasolineras.aggregate(pipeline1)
    cursor2 = db.gasolineras.aggregate(pipeline2)
    valores1 = list(cursor1)
    valores2 = list(cursor2)
    df1 = pd.DataFrame(valores1)
    df2 = pd.DataFrame(valores2)
    df1 = df1.set_index('_id')
    df2 = df2.set_index('_id')
    result = pd.concat([df1, df2], axis=1)
    result = result.reset_index()
    result = result.to_dict('records')
    return(result)

def BuscarProvincias():
    cursor = db.gasolineras.distinct('Provincia')
    valores = list(cursor)
    return(valores)

def BuscarMunicipio():
    cursor = db.gasolineras.distinct('Municipio')
    valores = list(cursor)
    return(valores)

def BuscarRotulos():
    cursor = db.gasolineras.distinct('Rótulo')
    valores = list(cursor)
    return(valores)

def new_task(valores):
    valores.update({'fecha_creacion': datetime.now(), 'fecha_actualizacion': datetime.now()})
    db.gasolineras.insert_one(valores).inserted_id

def update_task(valores):
    a=1

def delete_task(id):
    db.gasolineras.delete_one({'_id': ObjectId(id)})

def copy_task(id):
    obj = db.gasolineras.find({'_id': ObjectId(id)})
    valores = list(obj)
    valores = valores[0]
    del valores['_id']
    valores.update({'fecha_creacion': datetime.now(), 'fecha_actualizacion': datetime.now()})
    db.gasolineras.insert_one(valores).inserted_id

def add_gasolineras(valores):
    db.gasolineras.insert_many(valores)