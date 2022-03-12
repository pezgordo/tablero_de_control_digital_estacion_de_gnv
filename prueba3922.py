import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import dash_table as dt
import glob
import os
#import numpy as np

pd. set_option('display.max_rows', None)

from dash.exceptions import PreventUpdate

#Definir lista de columnas para DF Principal
col_list = ["Volumen", "Placa", "Vendedor", "Fecha", "SubTotal"]

#Juntar archivos excel dentro del folder para hacer merge
dirname = os.path.dirname(__file__)
path = os.path.join(dirname, 'otro2/')

all_files = glob.glob(path + "/*.xls")

li = []

for filename in all_files:
    df = pd.read_excel(filename, index_col=None, header=0, usecols=col_list)
    li.append(df)

sales = pd.concat(li, axis=0, ignore_index=True)

#convertir la columna FECHAS a formato datetime
sales['Fecha'] = pd.to_datetime(sales['Fecha'])
sales['Ano'] = sales['Fecha'].dt.year
sales['Mes'] = sales['Fecha'].dt.month
sales['Dia'] = sales['Fecha'].dt.day
sales['Hora'] = sales['Fecha'].dt.hour
sales['NombreDia'] = sales['Fecha'].dt.day_name()

#f2 = sales.groupby(['Ano','Mes', 'Placa'])['Volumen'].count().nlargest(n=100).reset_index()


#df3 = sales[sales['Volumen'] > 20]

#df3 = sales.sort_values('Fecha', ascending=False)

#df3 = sales.groupby("Fecha").count().reset_index()

#df3 = sales.sample(frac=0.1)

#df3 = sales[sales['Fecha'].dt.to_period('Q') == '2021Q4'] 

#df4 = sales.groupby('Ano').agg({'Volumen': [np.mean, np.sum]})

#df3 = sales.groupby(['Ano', 'Mes']).agg(Mean=('Volumen', 'mean'), Sum=('Volumen', 'sum'), Sumplata=('SubTotal', 'sum'))

#df5 = sales.groupby(['Ano','Mes', 'Placa'])['Volumen'].sum().reset_index()
#df5 = sales.groupby(['Ano','Mes', 'Placa']).agg(Sum=('Volumen', 'sum'))

#df6 = (sales.groupby(['Ano', 'Mes', 'Placa'])['Volumen'].agg([('Promedio', 'mean'), ('Total', 'sum')]).reset_index())

#df7 = (sales.groupby(['Ano', 'Mes', 'Placa'])['Volumen'].agg([('Promedio', 'mean'), ('Total', 'sum')]).reset_index())

#df8 = (sales.groupby(['Ano', 'Placa', 'Mes'])['Volumen'].agg([('Total', 'sum'), ('veces que entro', 'count')]))

#df9 = sales.groupby(['Ano', 'Placa', 'Mes'])['Volumen'].agg([('Total', 'sum'), ('veces que entro', 'count')]).nlargest(50, 'Total')
#df9 = df8.nlargest(10, 'Volumen')
#print(df3)
#print(df4)

#df3.info()

df = sales.groupby(['Ano', 'Placa', 'Mes'])['Volumen'].count().reset_index()

#df2 = sales.groupby(['Ano', 'Placa', 'Mes'])['Volumen'].count().apply(lambda x: x.div(x.iloc[0]).subtract(1).mul(100)).reset_index()

#print(df2)

#df["diferencia"] = df.groupby('Placa')['Volumen'].apply(lambda x: x.div(x.iloc[0]).subtract(1).mul(100))

df['Diferencia'] = df['Volumen'].diff()
df['Anterior'] = df['Volumen'].shift()
df['CambioPorcent'] = df['Volumen'].pct_change()

df.rename(columns={"Volumen":"Cargas"}, inplace=True)

#df['MesAnterior'] = 1 - df.Diferencia *  df.Volumen

print(df)
#df.info()



#df11['Porcentaje'] = [['Volumen'].pctchange if df11.Placa == df11.Placa else ['Volumen'] in df11.Volumen]

#df.groupby('security')['price'].apply(lambda x: x.div(x.iloc[0]).subtract(1).mul(100))

#def pct_change(df10):
#    df10['pct'] = 100 * (1 - df10.iloc[0].Volumen / df.Volumen)
#    return df

#df10.groupby('Volumen').apply(pct_change)

#df10.apply(pct_change)
#print(df10)
#df.info()
#print(df)

###if i = placa .pct_change

#sales.describe()

#print (df8)