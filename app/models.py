from datetime import datetime
from fasthtml.common import *
from bson.objectid import ObjectId
import os

from app.database import db

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
    valores = list(cursor)
    return(num, valores)

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