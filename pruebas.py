#pruebas

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import dash_table as dt
import glob
import os
import locale
locale.setlocale(locale.LC_ALL, 'es_ES.utf8')



pd.set_option('display.max_rows', 500)

col_list = ["Volumen", "Placa", "Vendedor", "Fecha"]
dirname = os.path.dirname(__file__)
path = os.path.join(dirname, 'otro2/')

all_files = glob.glob(path + "/*.xls")

li = []

for filename in all_files:
    df = pd.read_excel(filename, index_col=None, header=0, usecols=col_list)
    li.append(df)

sales = pd.concat(li, axis=0, ignore_index=True)

sales['Fecha'] = pd.to_datetime(sales['Fecha'])
sales['Ano'] = sales['Fecha'].dt.year
sales['Mes'] = sales['Fecha'].dt.month
sales['Dia'] = sales['Fecha'].dt.day
sales['Hora'] = sales['Fecha'].dt.hour
sales['NombreDia'] = sales['Fecha'].dt.day_name()

sales['NombreDia'] = sales['NombreDia'].astype('|S')

sales['NombreDia'] = sales['NombreDia'].apply(lambda s: s.decode('utf-8'))
#sales1 = sales.groupby(['Ano', 'Mes', 'Hora'])['Volumen'].sum().reset_index()
#print(sales.dtypes)
#df3 = sales.groupby(['Placa','Ano','Mes'])['Volumen'].sum().reset_index()#.nlargest(n=10, columns='Volumen')

#print(df3)

resumen = pd.read_excel('resumen.xlsx')

resumen['Revenues_Difference'] = resumen['Resultado_Bs'].diff()


# Calculate difference between two months
resumen['Revenues_Difference'] = resumen['Resultado_Bs'].diff()
# Calculate percentage change difference between two months
resumen['pct_Difference'] = (resumen['Resultado_Bs'].pct_change()) * 100
resumen['Revenues_Difference'] = resumen['Revenues_Difference'].fillna(0)
filter_month = resumen[resumen['Mes'] == 12]
revenues = filter_month['Resultado_Bs'].iloc[0]
revenues_difference = filter_month['Revenues_Difference'].iloc[0]
revenues_pct_change = filter_month['pct_Difference'].iloc[0]


print(resumen)