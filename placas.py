
import pandas as pd

import glob
import os

pd. set_option('display.max_rows', None)

#Definir lista de columnas para DF Principal
col_list = ["Volumen", "Placa", "Fecha"]

#Juntar archivos excel dentro del folder para hacer merge
dirname = os.path.dirname(__file__)
path = os.path.join(dirname, 'otro2/')

all_files = glob.glob(path + "/*.xls")

li = []

for filename in all_files:
    df = pd.read_excel(filename, index_col=None, header=0, usecols=col_list)
    li.append(df)

sales = pd.concat(li, axis=0, ignore_index=True)


#importar 2do archivo excel y crear 3er dataframe
dfplacas = pd.read_excel('Placas2.xlsx')

#convertir la columna FECHAS a formato datetime
sales['Fecha'] = pd.to_datetime(sales['Fecha'])
sales['Ano'] = sales['Fecha'].dt.year
sales['Mes'] = sales['Fecha'].dt.month
sales['Dia'] = sales['Fecha'].dt.day
sales['Hora'] = sales['Fecha'].dt.hour
sales['NombreDia'] = sales['Fecha'].dt.day_name()

#CREAR SEGUNDO DATAFRAME
df = sales.groupby(['Ano', 'Placa' ,'Mes'])['Volumen'].count().reset_index()

df2 = sales.groupby(['Placa'])['Volumen'].count().nlargest(11000).reset_index()

#df2.to_csv('Placas2.csv')

#print(dfplacas)

#df3 = pd.concat([df2, dfplacas], axis=0)

#print(df3)

df3 = pd.merge(df2, dfplacas, how="left", on="Placa")



print(df3.columns())


