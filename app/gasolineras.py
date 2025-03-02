import urllib.request, json
import pandas as pd
import ast

def ObtenerPrecio():
    file_name = 'app/out.csv'
    with urllib.request.urlopen("https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/") as url, open(file_name, 'wb') as out_file:
        data = json.load(url)
        df = pd.DataFrame.from_dict(data)
        df.to_csv(file_name, index=False)  

    df = pd.read_csv(file_name)

    df["ListaEESSPrecio"] = df["ListaEESSPrecio"].apply(lambda x: ast.literal_eval(x) if not pd.isnull(x) else x)
    df2 = pd.json_normalize(df['ListaEESSPrecio'])
    df2['Fecha'] = df['Fecha']

    df2['Localidad'] = df2['Localidad'].str.lower()
    df2['Municipio'] = df2['Municipio'].str.lower()
    df2['Provincia'] = df2['Provincia'].str.lower()
    df2['Rótulo'] = df2['Rótulo'].str.lower()

    df2['Latitud'] = pd.to_numeric(df2['Latitud'].str.replace(',','.'))
    df2['Longitud (WGS84)'] = pd.to_numeric(df2['Longitud (WGS84)'].str.replace(',','.'))
    df2['Precio Gasoleo A'] = pd.to_numeric(df2['Precio Gasoleo A'].str.replace(',','.'))
    df2['Precio Gasoleo B'] = pd.to_numeric(df2['Precio Gasoleo B'].str.replace(',','.'))
    df2['Precio Gasoleo Premium'] = pd.to_numeric(df2['Precio Gasoleo Premium'].str.replace(',','.'))
    df2['Precio Gasolina 95 E10'] = pd.to_numeric(df2['Precio Gasolina 95 E10'].str.replace(',','.'))
    df2['Precio Gasolina 95 E5'] = pd.to_numeric(df2['Precio Gasolina 95 E5'].str.replace(',','.'))
    df2['Precio Gasolina 95 E5 Premium'] = pd.to_numeric(df2['Precio Gasolina 95 E5 Premium'].str.replace(',','.'))
    df2['Precio Gasolina 98 E10'] = pd.to_numeric(df2['Precio Gasolina 98 E10'].str.replace(',','.'))
    df2['Precio Gasolina 98 E5'] = pd.to_numeric(df2['Precio Gasolina 98 E5'].str.replace(',','.'))
    df2['Precio Hidrogeno'] = pd.to_numeric(df2['Precio Hidrogeno'].str.replace(',','.'))

    valores = df2.to_dict('records')
    return(valores)