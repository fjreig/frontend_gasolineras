import urllib.request, json
import pandas as pd
import ast

def ObtenerPrecio():
    file_name = 'app/out.csv'
    #with urllib.request.urlopen("https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/") as url, open(file_name, 'wb') as out_file:
    #    data = json.load(url)
    #    df = pd.DataFrame.from_dict(data)
    #    df.to_csv(file_name, index=False)  

    df = pd.read_csv(file_name)

    df["ListaEESSPrecio"] = df["ListaEESSPrecio"].apply(lambda x: ast.literal_eval(x) if not pd.isnull(x) else x)
    df2 = pd.json_normalize(df['ListaEESSPrecio'])
    df2['Fecha'] = df['Fecha']
    valores = df2.to_dict('records')
    return(valores)
    