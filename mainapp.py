#importar librerias
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import dash_table as dt
import glob
import os
import plotly.express as px

from dash.exceptions import PreventUpdate



#Definir lista de columnas para DF Principal
col_list = ["Volumen", "Placa", "Vendedor", "Fecha"]

#Juntar archivos excel dentro del folder para hacer merge
dirname = os.path.dirname(__file__)
path = os.path.join(dirname, 'otro/')

all_files = glob.glob(path + "/*.xls")

li = []

for filename in all_files:
    df = pd.read_excel(filename, index_col=None, header=0, usecols=col_list)
    li.append(df)

sales = pd.concat(li, axis=0, ignore_index=True)


#importar 2do archivo excel y crear 3er dataframe
resumen = pd.read_excel('resumen.xlsx')


#convertir la columna FECHAS a formato datetime
sales['Fecha'] = pd.to_datetime(sales['Fecha'])
sales['Ano'] = sales['Fecha'].dt.year
sales['Mes'] = sales['Fecha'].dt.month
sales['Dia'] = sales['Fecha'].dt.day
sales['Hora'] = sales['Fecha'].dt.hour
sales['NombreDia'] = sales['Fecha'].dt.day_name()



#CREAR SEGUNDO DATAFRAME
df = sales.groupby(['Ano', 'Placa' ,'Mes'])['Volumen'].count().reset_index()

#df3 = sales.groupby(['Ano', 'Placa', 'Mes'])['Volumen'].count().reset_index()

#df2["Diferencia"] = df2.groupby('Placa')['Volumen'].apply(lambda x: x.div(x.iloc[0]).subtract(1).mul(100))

df['Diferencia'] = (df['Volumen'].diff())

df2 = df.sort_values(by='Volumen', ascending=False)

df2.rename(columns={"Volumen":"Cargas"}, inplace=True)


#CREAR TERCER DATAFRAME
dfplacas = pd.read_excel('Placas2.xlsx')

df3 = pd.merge(sales, dfplacas, how="left", on="Placa")





font_awesome = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"
meta_tags = [{"name": "viewport", "content": "width=device-width"}]
external_stylesheets = [meta_tags, font_awesome]


app = dash.Dash(__name__, external_stylesheets = external_stylesheets)
server = app.server

#EMPIEZA LA APLICACION DASH
app.layout = html.Div([

# INICIO DIV 1
html.Div([

    #1.1 DIV SUPERIOR LOGO
    html.Div([
         html.Img(src = app.get_asset_url('logo.png'),
                     style = {'height': '150px'},
                     className = 'title_image'
                     ),
            


    ], className='one-third column', id = 'title11'),

    #1.2 TITULO
    html.Div([
        html.H6('Cuadro de control - El Cañaveral S.R.L.',
                    style = {'color': '#00622b'},
                    className = 'title'
                    
                    ),

    ], className='one-third column', id = 'title111')

# FIN DE DIV 1
], className = 'flex_container2'), 


# INICIO DIV 2 
html.Div([
        #2.1 SLIDER PARA ESCOGER EL AÑO
        html.Div([
            html.P('Año', className='fix_label', style= {'color': '#00622b'}),
            dcc.Slider(id = 'select_years',
                       included=False,
                       updatemode='drag',
                       tooltip={'always_visible': True},
                       min = 2017,
                       max = 2022,
                       step = 1,
                       value= 2022,                  
                       marks={
                           2017: '2017',
                           2018: '2018',
                           2019: '2019',
                           2020: '2020',
                           2021: '2021',
                           2022: '2022',
                       },
                       className='dcc_compon'),
                        
                    ], className='one-third column', id = 'title1'),

        #2.2 SLIDER PARA ESCOGER EL MES
        html.Div([
            html.P('Mes', className='fix_label', style= {'color': '#00622b'}),
            dcc.Slider(id = 'select_months',
                       included=False,
                       updatemode='drag',
                       tooltip={'always_visible': True},
                       min = 1,
                       max = 12,
                       step = 1,
                       #CAMBIAR ESTO AL MES CORRESPONDIENTE CADA MES###################################3
                       value= 6,                     

                       marks={
                           1: 'Ene',
                           2: 'Feb',
                           3: 'Mar',
                           4: 'Abr',
                           5: 'May',
                           6: 'Jun',
                           7: 'Jul',
                           8: 'Ago',
                           9: 'Sep',
                           10: 'Oct',
                           11: 'Nov',
                           12: 'Dic',

                       
                       
                       },

                       className='dcc_compon'),

        ], className='one-half column', id = 'title2'),
#FIN DE DIV 2
], className = 'flex_container'),


# INICIO DIV 3
html.Div([

    #3.1 PRIMER DIV KPIs 
    html.Div([
           
            html.Div(id = 'text2'),
            html.Div(id = 'text6'),
            html.Div(id = 'text5'),
            html.Div(id = 'text1'),
            html.Div(id = 'text3'),
            html.Div(id = 'text4'),
            
            

        ], className='create_container2 two columns', style={'height': '420px'}),


    #3.2 SEGUNDO DIV LINECHART
    html.Div([

            dcc.Graph(id = 'line_chart', config={'displayModeBar': 'hover'},
                      style={'height': '350px'})

        ], className='create_container2 six columns', style={'height': '420px'}),


    #3.3 TERCER DIV DATATABLE
    html.Div([
            html.Label("Top clientes del mes", style={'color': '#00622b', 
                                                    'font' : 'Arial',
                                                    'font-weight': 'bold',
                                                    'fontSize': 17,}),
            dt.DataTable(id = 'my_datatable',
                         columns=[{'name': i, 'id': i} for i in
                                  df2.loc[:, ["Placa", "Cargas", "Diferencia"]]],
                        
                         virtualization=True,
                         style_cell={'textAlign': 'left',
                                     'min-width': '10px',
                                     'backgroundColor': '#ffffff',
                                     'color': '#00622b',
                                     'border-bottom': '0.01rem solid #19AAE1'},
                         style_header={'backgroundColor': '#ffffff',
                                       'fontWeight': 'bold',
                                       'font': 'Lato, sans-serif',
                                       'color': '#00622b',
                                       'border': '#00622b'},
                         style_as_list_view=True,
                         style_table={'height': '320px', 'overflowY': 'auto'},
                         style_data={'styleOverflow': 'hidden', 'color': '#00622b'},

                         style_data_conditional=[
                            
                                                        {
                                'if': {
                                    'filter_query': '{Diferencia} > 1 && {Diferencia} < 411',
                                    'column_id': 'Diferencia'
                                },
                                'backgroundColor': 'green',
                                'color': 'white'
                                 },
                                {
                                'if': {
                                    'filter_query': '{Diferencia} < 1 && {Diferencia} > -411',
                                    'column_id': 'Diferencia'
                                },
                                'backgroundColor': 'red',
                                'color': 'white'
                            },
                            
                            
                            ],




                         fixed_rows={'headers': True},
                         sort_action='native',
                         sort_mode='multi')


        ], className='create_container2 two columns', style={'height': '420px'}),


#FIN DE DIV 3 
], className = 'flex_container'),






#4 DIV GRANDE DE CUADRO DE KPIS2   
html.Div([

        #KPI de Total_Ingresos
        html.Div([
            html.Div(id = 'text11',
                     className = 'card_size'),
            html.Div([
                dcc.Graph(id = 'chart11',
                          config = {'displayModeBar': False}),
            ], className = 'chart')
        ], className = 'text_graph_column'),

        #KPI de Costo_GNV
        html.Div([
            html.Div(id = 'text22',
                     className = 'card_size'),
            html.Div([
                dcc.Graph(id = 'chart22',
                          config = {'displayModeBar': False}),
            ], className = 'chart')
        ], className = 'text_graph_column'),

        #KPI de Gastos_Operacion
        html.Div([
            html.Div(id = 'text33',
                     className = 'card_size'),
            html.Div([
                dcc.Graph(id = 'chart33',
                          config = {'displayModeBar': False}),
            ], className = 'chart')
        ], className = 'text_graph_column'),

        #KPI de Gastos_Administracion
        html.Div([
            html.Div(id = 'text44',
                     className = 'card_size'),
            html.Div([
                dcc.Graph(id = 'chart44',
                          config = {'displayModeBar': False}),
            ], className = 'chart')
        ], className = 'text_graph_column'),

        #KPI de Gastos_CG
        html.Div([
            html.Div(id = 'text55',
                     className = 'card_size'),
            html.Div([
                dcc.Graph(id = 'chart55',
                          config = {'displayModeBar': False}),
            ], className = 'chart')
        ], className = 'text_graph_column'),

        #KPI de Impuestos
        html.Div([
            html.Div(id = 'text66',
                     className = 'card_size'),
            html.Div([
                dcc.Graph(id = 'chart66',
                          config = {'displayModeBar': False}),
            ], className = 'chart')
        ], className = 'text_graph_column'),

        #KPI de Total_Egresos
        html.Div([
            html.Div(id = 'text77',
                     className = 'card_size'),
            html.Div([
                dcc.Graph(id = 'chart77',
                          config = {'displayModeBar': False}),
            ], className = 'chart')
        ], className = 'text_graph_column'),

        #KPI de Resultado_Bs
        html.Div([
            html.Div(id = 'text88',
                     className = 'card_size'),
            html.Div([
                dcc.Graph(id = 'chart88',
                          config = {'displayModeBar': False}),
            ], className = 'chart')
        ], className = 'text_graph_column'),

#Fin de DIV 4.1

], className = 'flex_container'),






# INICIO DIV 5
html.Div([

    #5.1  DIV BARCHART VENDEDORES

    html.Div([

            dcc.Graph(id = 'bar_chart_1', config={'displayModeBar': 'hover'},
                      ),

        ], className='create_container2 two columns', style={'height': '400px'}),
        

    #5.2 DIV LINECHART AÑO A AÑO

    html.Div([

            dcc.Graph(id = 'line_chart2', config={'displayModeBar': 'hover'},
                      style={'height': '350px'})

        ], className='create_container2 six columns', style={'height': '400px'}),

    #5.3 DIV BARCHART VENDEDORES

    html.Div([

            dcc.Graph(id = 'bar_chart_2', config={'displayModeBar': 'hover'},
                      ),

        ], className='create_container2 two columns', style={'height': '400px'}),


#FIN DE DIV 5
], className = 'flex_container'), 

# INICIO DE DIV 6
html.Div([

    #6.1 BARCHART RANKING DIA DE LA SEMANA
    html.Div([

            dcc.Graph(id = 'bar_chart_3', config={'displayModeBar': 'hover'},
                      ),

        ], className='create_container2 two columns', style={'height': '400px'}),

    #6.2 DONUT CHART SINDICATOS
    html.Div([

            dcc.Graph(id = 'donut_chart', config={'displayModeBar': 'hover'},
                      style={'height': '600px'})

        ], className='create_container2 eight columns', style={'height': '400px'}),

# FIN DE DIV 6
], className = 'flex_container'), 

# FIN DE MAIN APP
], id = 'mainContainer', style={'display': 'flex', 'flex-direction': 'column'})


#****CALLBACKS***CALLBACKS***CALLBACKS***CALLBACKS***CALLBACKS***

#CB 3.1.1 - CALLBACK KPI 1
@app.callback(Output('text1', 'children'),
              [Input('select_years','value')])
def update_graph(select_years):
    sales8 = sales.groupby(['Ano'])['Volumen'].sum().reset_index()
    current_year = sales8[(sales8['Ano'] == select_years)]['Volumen'].sum()

    return [

        html.H6(children='Ventas por Año',
                style={'textAlign': 'center',
                       'font':'Arial',
                       'font-weight':'bold',
                       'fontSize':15,
                       'color': '#00622b'}),

        html.P('m3  {0:,.2f}'.format(current_year),
               style={'textAlign': 'center',
                      'color': '#f18c24',
                      'font-weight': 'bold',
                      'fontSize': 17,
                      'margin-top': '-10px'})

    ]

#CB 3.1.2 - CALLBACK KPI 2
@app.callback(Output('text2', 'children'),
              [Input('select_years','value')],
              [Input('select_months', 'value')]
              )
def update_graph(select_years, select_months):
    sales88 = sales.groupby(['Ano', 'Mes'])['Volumen'].sum().reset_index()
    current_month = sales88[(sales88['Ano'] == select_years) & (sales88['Mes'] == select_months)]['Volumen'].sum()

            
    

    return [

        html.H6(children='Ventas por Mes',
                style={'textAlign': 'center',
                       'font':'Arial',
                       'font-weight':'bold',
                       'fontSize':15,
                       'color': '#00622b'}),

        html.P('m3  {0:,.2f}'.format(current_month),
               style={'textAlign': 'center',
                      'color': '#f18c24',
                      'font-weight': 'bold',
                      'fontSize': 17,
                      'margin-top': '-10px'})

    ]

#CB 3.1.3 - CALLBACK KPI 3


@app.callback(Output('text3', 'children'),
              [Input('select_years','value')])
def update_graph(select_years):
    sales10 = sales.groupby(['Ano'])['Volumen'].sum().reset_index()
    sales10['PY'] = sales10['Volumen'].shift(1)
    previous_year = sales10[(sales10['Ano'] == select_years)]['PY'].sum()

    return [

        html.H6(children='Ventas Año Pasado',
                style={'textAlign': 'center',
                       'font':'Arial',
                       'font-weight':'bold',
                       'fontSize':15,
                       'color': '#00622b'}),

        html.P('m3  {0:,.2f}'.format(previous_year),
               style={'textAlign': 'center',
                      'color': '#f18c24',
                      'font-weight': 'bold',
                      'fontSize': 17,
                      'margin-top': '-10px'})

    ]

#CB 3.1.4 - CALLBACK KPI 4 DIFERENCIAL ANUAL
@app.callback(Output('text4', 'children'),
              [Input('select_years','value')])
def update_graph(select_years):
    sales11 = sales.groupby(['Ano'])['Volumen'].sum().reset_index()
    sales11['YOY Growth'] = sales11['Volumen'].pct_change()
    sales11['YOY Growth'] = sales11['YOY Growth'] * 100
    growth_year = sales11[(sales11['Ano'] == select_years)]['YOY Growth'].sum()

    return [

        html.H6(children='Diferencia Anual',
                style={'textAlign': 'center',
                       'font':'Arial',
                       'font-weight':'bold',
                       'fontSize':15,
                       'color': '#00622b'}),

        html.P('{0:,.2f}%'.format(growth_year),
               style={'textAlign': 'center',
                      'color': '#f18c24',
                      'font-weight': 'bold',
                      'fontSize': 17,
                      'margin-top': '-10px'})

    ]

#CB 3.1.5 - CALLBACK KPI 5 DIFERENCIA MENSUAL
@app.callback(Output('text5', 'children'),
              [Input('select_years','value')],
              [Input('select_months', 'value')]
              )
def update_graph(select_years, select_months):
    sales11 = sales.groupby(['Ano', 'Mes'])['Volumen'].sum().reset_index()
    sales11['YOY Growth'] = sales11['Volumen'].pct_change()
    sales11['YOY Growth'] = sales11['YOY Growth'] * 100
    growth_year = sales11[(sales11['Ano'] == select_years) & (sales11['Mes'] == select_months)]['YOY Growth'].sum()

    return [

        html.H6(children='Diferencia Mensual',
                style={'textAlign': 'center',
                       'font':'Arial',
                       'font-weight':'bold',
                       'fontSize':15,
                       'color': '#00622b'}),

        html.P('{0:,.2f}%'.format(growth_year),
               style={'textAlign': 'center',
                      'color': '#f18c24',
                      'font-weight': 'bold',
                      'fontSize': 17,
                      'margin-top': '-10px'})

    ]


#CB3.1.6 - CALLBACK KPI 6 VENTAS MES PASADO


@app.callback(Output('text6', 'children'),
              [Input('select_years','value')],
              [Input('select_months', 'value')]
              )
def update_graph(select_years, select_months):
    sales10 = sales.groupby(['Ano', 'Mes'])['Volumen'].sum().reset_index()
    sales10['PY'] = sales10['Volumen'].shift(1)
    previous_year = sales10[(sales10['Ano'] == select_years) & (sales10['Mes'] == select_months)]['PY'].sum()

    return [

        html.H6(children='Ventas Mes Pasado',
                style={'textAlign': 'center',
                       'font':'Arial',
                       'font-weight':'bold',
                       'fontSize':15,
                       'color': '#00622b'}),

        html.P('m3  {0:,.2f}'.format(previous_year),
               style={'textAlign': 'center',
                      'color': '#f18c24',
                      'font-weight': 'bold',
                      'fontSize': 17,
                      'margin-top': '-10px'})

    ]
    

#CB 3.2 - CALLBACK PARA LINE CHART MES X MES
@app.callback(Output('line_chart', 'figure'),
              [Input('select_years','value')],
              [Input('select_months','value')]
              )
              
def update_graph(select_years, select_months):
    sales6 = sales.groupby(['Ano','Mes', 'Dia', 'NombreDia'])['Volumen'].sum().reset_index()
    sales7 = sales6[(sales6['Ano'] == select_years) & (sales6['Mes'] == select_months)]

   



    return {
        'data': [
            go.Scatter(
                x=sales7['Dia'],
                y=sales7['Volumen'],
                text = sales7['Volumen'],
                texttemplate= '%{text:,.2s}',
                textposition='bottom left',
                mode='markers+lines+text',
                line=dict(width=3, color='#00622b'),
                marker=dict(color='#ff8800', size=8, symbol='circle',
                            line=dict(color='#ff8800', width=2)),
                hoverinfo='text',
                hovertext=
                '<b>Mes</b>: ' + sales7['Mes'].astype(str) + '<br>' +
                '<b>Dia</b>: ' + sales7['Dia'].astype(str) + '<br>' +
                '<b>Dia Semana</b>: ' + sales7['NombreDia'].astype(str) + '<br>' +
                '<b>Ventas</b>: m3  ' + [f'{x:,.0f}' for x in sales7['Volumen']] + '<br>'

            ),

        ],


        'layout': go.Layout(
            title={'text': 'Total m3 Mes' + ' ' + str((select_months)),
                   'y': 0.99,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': '#00622b',
                       'size': 15,
                       'family':'Arial'},
            font=dict(family='sans-serif',
                      color='#00622b',
                      size=12),
            hovermode='closest',
            paper_bgcolor='#ffffff',
            plot_bgcolor='#ffffff',
            legend={'orientation': 'h',
                    'bgcolor': '#010915',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            margin=dict(t = 5, l = 0, r=0),

            
            
            xaxis=dict(title='<b></b>',
                       color = '#00622b',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='#00622b',
                       linewidth=1,
                       tickangle = 90,
                       ticks='outside',
                       tickformat='%A',
                       tickfont=dict(
                           family='Aerial',
                           color='#00622b',
                           size=12
                       )),
            yaxis=dict(title='<b>Metros Cubicos</b>',
                       range=[0, 5000],
                       color='#00622b',
                       showline=True,
                       showgrid=False,
                       showticklabels=True,
                       linecolor='#00622b',
                       linewidth=1,
                       tick0=0,
                       dtick=1000,
                       ticks='inside',
                       tickfont=dict(
                           family='Aerial',
                           color='#00622b',
                           size=12
                       )
                       )


        )
    }


#CB 3.3 - CALLBACK PARA DATATABLE
@app.callback(Output('my_datatable', 'data'),
              [Input('select_years','value')],
              [Input('select_months','value')]
              )
def update_graph(select_years, select_months):
    data_table = df2[(df2['Mes'] == select_months) & (df2['Ano'] == select_years) ]
    #print(df2['Volumen'].value_counts())
    return data_table.to_dict('records')



#CB 4.1 - CALLBACK BAR CHART
@app.callback(Output('bar_chart_1', 'figure'),
              [Input('select_years','value')],
              [Input('select_months','value')]
              )
def update_graph(select_years, select_months):
    sales1 = sales.groupby(['Ano', 'Mes', 'Vendedor'])['Volumen'].sum().reset_index()
    sales2 = sales1[(sales1['Ano'] == select_years) & (sales1['Mes'] == select_months)].sort_values(by = ['Volumen'], ascending = False).nlargest(7, columns = ['Volumen'])
    

    
    return {
        'data': [
            go.Bar(
                x=sales2['Volumen'],
                y=sales2['Vendedor'],
                text = sales2['Volumen'],
                #texttemplate=  '%{text:,.2s}',
                textposition='auto',
                orientation= 'h',
                marker=dict(color='#f18c24'),
                hoverinfo='text',
                hovertext=
                '<b>Año</b>: ' + sales2['Ano'].astype(str) + '<br>' +
                '<b>Vendedor</b>: ' + sales2['Vendedor'].astype(str) + '<br>' +
                #'<b>Sub-Category</b>: ' + sales2['Sub-Category'].astype(str) + '<br>' +
                '<b>Volumen</b>: m3  ' + [f'{x:,.0f}' for x in sales2['Volumen']] + '<br>'

            ),

        ],


        'layout': go.Layout(
            title={'text': 'Top Vendedores' + ' ' + str(select_months) + str(" ") + str((select_years)),
                   'y': 0.99,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': '#00622b',
                       'size': 14},
            font=dict(family='sans-serif',
                      color='#00622b',
                      size=12),
            hovermode='closest',
            paper_bgcolor='#FFFFFF',
            plot_bgcolor='#FFFFFF',
            legend={'orientation': 'h',
                    'bgcolor': '#f18c24',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            margin=dict(t = 40, r=0, l=70),
            xaxis=dict(title='<b></b>',
                       color = '#00622b',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='#00622b',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='#00622b',
                           size=10
                       )),
            yaxis=dict(title='<b></b>',
                       color='#00622b',
                       autorange = 'reversed',
                       showline=False,
                       showgrid=False,
                       showticklabels=True,
                       linecolor='#00622b',
                       linewidth=1.5,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='#00622b',
                           size=10
                       )
                       )


        )
    }


#CB 4.2 - CALLBACK PARA LINE CHART 2 AÑO X AÑO

@app.callback(Output('line_chart2', 'figure'),
              [Input('select_years','value')]
              )
              
def update_graph(select_years):
    sales6 = sales.groupby(['Ano','Mes'])['Volumen'].sum().reset_index()
    sales7 = sales6[(sales6['Ano'] == select_years)]

   



    return {
        'data': [
            go.Scatter(
                x=sales7['Mes'],
                y=sales7['Volumen'],
                text = sales7['Volumen'],
                texttemplate= '%{text:,.2s}',
                textposition='bottom left',
                mode='markers+lines+text',
                line=dict(width=3, color='#00622b'),
                marker=dict(color='#ff8800', size=8, symbol='circle',
                            line=dict(color='#ff8800', width=2)),
                hoverinfo='text',
                hovertext=
                '<b>Mes</b>: ' + sales7['Mes'].astype(str) + '<br>' +
                #'<b>Dia</b>: ' + sales7['Dia'].astype(str) + '<br>' +
                
                '<b>Ventas M3  </b>: Bs  ' + [f'{x:,.0f}' for x in sales7['Volumen']] + '<br>'

            ),

        ],


        'layout': go.Layout(
            title={'text': 'Total m3 Año' + ' ' + str((select_years)),
                   'y': 0.99,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': '#00622b',
                       'size': 12},
            font=dict(family='sans-serif',
                      color='#00622b',
                      size=12),
            hovermode='closest',
            paper_bgcolor='#ffffff',
            plot_bgcolor='#ffffff',
            legend={'orientation': 'h',
                    'bgcolor': '#010915',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            margin=dict(t = 5, l = 0, r=0),

            
            
            xaxis=dict(title='<b></b>',
                       color = '#00622b',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='#00622b',
                       linewidth=1,
                       tickangle = 90,
                       ticks='outside',
                       tickformat='%B',
                       #tickmode = 'array',
                       #ticktext = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', "Ago", "Sep", "Oct", "Nov", "Dic"],
                       tickfont=dict(
                           family='Aerial',
                           color='#00622b',
                           size=12
                       )),
            yaxis=dict(title='<b>Metros Cubicos</b>',
                       #range=[0, 5000],
                       color='#00622b',
                       showline=True,
                       showgrid=False,
                       showticklabels=True,
                       linecolor='#00622b',
                       linewidth=1,
                       tick0=0,
                       dtick=1000,
                       ticks='inside',
                       tickfont=dict(
                           family='Aerial',
                           color='#00622b',
                           size=12
                       )
                       )


        )
    }

#CB 4.3 - CALLBACK BAR CHART 2 volumen por dias
@app.callback(Output('bar_chart_2', 'figure'),
              [Input('select_years','value')],
              [Input('select_months','value')]
              )
def update_graph(select_years, select_months):
    sales1 = sales.groupby(['Ano', 'Mes', 'Hora'])['Volumen'].sum().reset_index()
    sales2 = sales1[(sales1['Ano'] == select_years) & (sales1['Mes'] == select_months)].sort_values(by = ['Volumen'], ascending = False).nlargest(24, columns = ['Volumen'])
    

    
    return {
        'data': [
            go.Bar(
                x=sales2['Volumen'],
                y=sales2['Hora'],
                text = sales2['Volumen'],
                #texttemplate=  '%{text:,.2s}',
                textposition='auto',
                orientation= 'h',
                marker=dict(color='#f18c24'),
                hoverinfo='text',
                hovertext=
                '<b>Año</b>: ' + sales2['Ano'].astype(str) + '<br>' +
                '<b>Mes</b>: ' + sales2['Mes'].astype(str) + '<br>' +
                '<b>Hora</b>: ' + sales2['Hora'].astype(str) + '<br>' +
                #'<b>Sub-Category</b>: ' + sales2['Sub-Category'].astype(str) + '<br>' +
                '<b>Volumen</b>: m3  ' + [f'{x:,.0f}' for x in sales2['Volumen']] + '<br>'

            ),

        ],


        'layout': go.Layout(
            title={'text': 'Horas del dia' + ' ' + str(select_months) + str(" ") + str((select_years)),
                   'y': 0.99,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': '#00622b',
                       'size': 14},
            font=dict(family='sans-serif',
                      color='#00622b',
                      size=12),
            hovermode='closest',
            paper_bgcolor='#FFFFFF',
            plot_bgcolor='#FFFFFF',
            legend={'orientation': 'h',
                    'bgcolor': '#f18c24',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            margin=dict(t = 40, r=0, l=20),
            xaxis=dict(title='<b></b>',
                       color = '#00622b',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='#00622b',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='#00622b',
                           size=10
                       )),
            yaxis=dict(title='<b></b>',
                       color='#00622b',
                       autorange = 'reversed',
                       showline=False,
                       showgrid=False,
                       showticklabels=True,
                       linecolor='#00622b',
                       linewidth=1.5,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='#00622b',
                           size=10
                       )
                       )


        )
    }

#CB 5
#CB 5.1 - CALLBACK BAR CHART 2 volumen por dias
@app.callback(Output('bar_chart_3', 'figure'),
              [Input('select_years','value')],
              [Input('select_months','value')]
              )
def update_graph(select_years, select_months):
    sales1 = sales.groupby(['Ano', 'Mes', 'NombreDia'])['Volumen'].sum().reset_index()
    sales2 = sales1[(sales1['Ano'] == select_years) & (sales1['Mes'] == select_months)].sort_values(by = ['Volumen'], ascending = False)#.nlargest(7, columns = ['Volumen'])
    

    
    return {
        'data': [
            go.Bar(
                x=sales2['Volumen'],
                y=sales2['NombreDia'],
                text = sales2['Volumen'],
                #texttemplate=  '%{text:,.2s}',
                textposition='auto',
                orientation= 'h',
                marker=dict(color='#f18c24'),
                hoverinfo='text',
                hovertext=
                '<b>Año</b>: ' + sales2['Ano'].astype(str) + '<br>' +
                '<b>Mes</b>: ' + sales2['Mes'].astype(str) + '<br>' +
                '<b>Dia</b>: ' + sales2['NombreDia'].astype(str) + '<br>' +
                #'<b>Sub-Category</b>: ' + sales2['Sub-Category'].astype(str) + '<br>' +
                '<b>Volumen</b>: m3  ' + [f'{x:,.0f}' for x in sales2['Volumen']] + '<br>'

            ),

        ],


        'layout': go.Layout(
            title={'text': 'Dia de la Semana' + ' ' + str(select_months) + str(" ") + str((select_years)),
                   'y': 0.99,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': '#00622b',
                       'size': 14},
            font=dict(family='sans-serif',
                      color='#00622b',
                      size=12),
            hovermode='closest',
            paper_bgcolor='#FFFFFF',
            plot_bgcolor='#FFFFFF',
            legend={'orientation': 'h',
                    'bgcolor': '#f18c24',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            margin=dict(t = 40, r=0),
            xaxis=dict(title='<b></b>',
                       color = '#00622b',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='#00622b',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='#00622b',
                           size=10
                       )),
            yaxis=dict(title='<b></b>',
                       color='#00622b',
                       autorange = 'reversed',
                       showline=False,
                       showgrid=False,
                       showticklabels=True,
                       linecolor='#00622b',
                       linewidth=1.5,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='#00622b',
                           size=10
                       )
                       )


        )
    }



######EMPIEZA CALLBACK DE TEXT11 Y CHART11###### TOTAL INGRESOS
#CB 
@app.callback(Output('text11', 'children'),
              [Input('select_months', 'value')],
              [Input('select_years', 'value')]
              )
def update_text(select_months, select_years):
    if select_months is None:
        raise PreventUpdate
    else:
        # Calculate difference between two months
        resumen['Revenues_Difference'] = resumen['Total_Ingresos'].diff()
        # Calculate percentage change difference between two months
        resumen['pct_Difference'] = (resumen['Total_Ingresos'].pct_change()) * 100
        resumen['Revenues_Difference'] = resumen['Revenues_Difference'].fillna(0)
        #filter_year = resumen[resumen['Ano'] == select_years]
        
        filter_month = resumen[(resumen['Año'] == select_years) & (resumen['Mes'] == select_months)]
        revenues = filter_month['Total_Ingresos'].iloc[0]
        revenues_difference = filter_month['Revenues_Difference'].iloc[0]
        revenues_pct_change = filter_month['pct_Difference'].iloc[0]

    if revenues_difference > 0:
        return [
            html.P('Total Ingresos',
                   style = {
                       'color': '#00622b',
                       'fontSize': 15,
                       'font-weight': 'bold',
                       
                   },
                   className = 'card_title'
                   ),

            html.Div([
                html.P('Bs  {0:,.0f}'.format(revenues),
                       style = {
                           'color': '#f18c24',
                           'fontSize': 17,
                           'font-weight': 'bold'
                       }, className = 'monthly_value'
                       ),

                html.Div([
                    html.I(className = "fas fa-caret-up",
                           style = {"font-size": "25px",
                                    'color': '#00cc00'},
                           ),
                ], className = 'value_indicator'),
            ], className = 'value_and_indicator'),

            html.Div([
                html.Div([
                    html.P('+Bs  {0:,.2f}'.format(revenues_difference),
                           style = {
                               'color': '#00cc00',
                               'fontSize': 12,
                           }, className = 'monthly_difference_value'
                           ),

                    html.P('+{0:,.1f}%'.format(revenues_pct_change),
                           style = {
                               'color': '#00cc00',
                               'fontSize': 12,
                           }, className = 'monthly_pct_change'
                           ),
                ], className = 'difference_value_row'),

                html.P('vs mes anterior',
                       style = {
                           'color': '#f18c24',
                           'fontSize': 13,
                           'font-weight': 'bold'
                       },
                       className = 'text_previous_month'
                       ),
            ], className = 'difference_value_column')
        ]

    elif revenues_difference < 0:
        return [
            html.P('Total Ingresos',
                   style = {
                       'color': '#00622b',
                       'fontSize': 15,
                       'font-weight': 'bold'
                   },
                   className = 'card_title'
                   ),

            html.Div([
                html.P('Bs  {0:,.0f}'.format(revenues),
                       style = {
                           'color': '#f18c24',
                           'fontSize': 17,
                           'font-weight': 'bold'
                       }, className = 'monthly_value'
                       ),

                html.Div([
                    html.I(className = "fas fa-caret-down",
                           style = {"font-size": "25px",
                                    'color': '#EC1E3D'},
                           ),
                ], className = 'value_indicator'),
            ], className = 'value_and_indicator'),

            html.Div([
                html.Div([
                    html.P('-Bs  {0:,.2f}'.format(abs(revenues_difference)),
                           style = {
                               'color': '#EC1E3D',
                               'fontSize': 12,
                           }, className = 'monthly_difference_value'
                           ),

                    html.P('{0:,.1f}%'.format(revenues_pct_change),
                           style = {
                               'color': '#EC1E3D',
                               'fontSize': 12,
                           }, className = 'monthly_pct_change'
                           ),
                ], className = 'difference_value_row'),

                html.P('vs mes anterior',
                       style = {
                           'color': '#f18c24',
                           'fontSize': 13,
                           'font-weight': 'bold'
                       },
                       className = 'text_previous_month'
                       ),
            ], className = 'difference_value_column')
        ]

    elif revenues_difference == 0:
        return [
            html.P('Resultado Bs',
                   style = {
                       'color': '#00622b',
                       'fontSize': 17,
                       'font-weight': 'bold'
                   },
                   className = 'card_title'
                   ),

            html.Div([
                html.P('Bs  {0:,.0f}'.format(revenues),
                       style = {
                           'color': 'white',
                           'fontSize': 25,
                           'font-weight': 'bold'
                       }, className = 'monthly_value'
                       ),
            ], className = 'value_and_indicator'),

            html.Div([
                html.Div([
                    html.P('0.00',
                           style = {
                               'color': 'white',
                               'fontSize': 14,
                           }, className = 'monthly_difference_value'
                           ),

                    html.P('0.0%',
                           style = {
                               'color': 'white',
                               'fontSize': 14,
                           }, className = 'monthly_pct_change'
                           ),
                ], className = 'difference_value_row'),

                html.P('vs previous month',
                       style = {
                           'color': 'white',
                           'fontSize': 13,
                           'font-weight': 'bold'
                       },
                       className = 'text_previous_month'
                       ),
            ], className = 'difference_value_column')
        ]


@app.callback(Output('chart11', 'figure'),
              [Input('select_years','value')]
              )
              
def update_graph(select_years):
    resumen6 = resumen.groupby(['Año','Mes'])['Total_Ingresos'].sum().reset_index()
    resumen7 = resumen6[(resumen6['Año'] == select_years)]


    return {
        'data': [go.Scatter(
            x = resumen7['Mes'],
            y = resumen7['Total_Ingresos'],
            mode = 'lines',
            line = dict(width = 3, color = '#00b300'),
            hoverinfo = 'skip',
        )],

        'layout': go.Layout(
            height = 50,
            width = 150,
            plot_bgcolor = 'rgba(0, 0, 0, 0)',
            paper_bgcolor = 'rgba(0, 0, 0, 0)',
            margin = dict(t = 0, b = 0, r = 0, l = 0),
            xaxis = dict(showline = False,
                         showgrid = False,
                         linecolor = 'white',
                         linewidth = 1,
                         ticks = 'outside',
                         tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'white')

                         ),

            yaxis = dict(showline = False,
                         showgrid = False,
                         linecolor = 'white',
                         linewidth = 1,
                         ticks = 'outside',
                         tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'white')

                         ),
        )

    }

#######TERMINA CALLBACK DE TEXT11 Y CHART11####### TOTAL INGRESOS

#

#

#

######EMPIEZA CALLBACK DE TEXT22 Y CHART22###### COSTO GNV



@app.callback(Output('text22', 'children'),
              [Input('select_months', 'value')],
              [Input('select_years', 'value')]
              )
def update_text(select_months, select_years):
    if select_months is None:
        raise PreventUpdate
    else:
        # Calculate difference between two months
        resumen['Revenues_Difference'] = resumen['Costo_GNV'].diff()
        # Calculate percentage change difference between two months
        resumen['pct_Difference'] = (resumen['Costo_GNV'].pct_change()) * 100
        resumen['Revenues_Difference'] = resumen['Revenues_Difference'].fillna(0)
        #filter_year = resumen[resumen['Ano'] == select_years]
        
        filter_month = resumen[(resumen['Año'] == select_years) & (resumen['Mes'] == select_months)]
        revenues = filter_month['Costo_GNV'].iloc[0]
        revenues_difference = filter_month['Revenues_Difference'].iloc[0]
        revenues_pct_change = filter_month['pct_Difference'].iloc[0]

    if revenues_difference > 0:
        return [
            html.P('Costo GNV',
                   style = {
                       'color': '#00622b',
                       'fontSize': 15,
                       'font-weight': 'bold',
                       
                   },
                   className = 'card_title'
                   ),

            html.Div([
                html.P('Bs  {0:,.0f}'.format(revenues),
                       style = {
                           'color': '#f18c24',
                           'fontSize': 17,
                           'font-weight': 'bold'
                       }, className = 'monthly_value'
                       ),

                html.Div([
                    html.I(className = "fas fa-caret-up",
                           style = {"font-size": "25px",
                                    'color': '#00cc00'},
                           ),
                ], className = 'value_indicator'),
            ], className = 'value_and_indicator'),

            html.Div([
                html.Div([
                    html.P('+Bs  {0:,.2f}'.format(revenues_difference),
                           style = {
                               'color': '#00cc00',
                               'fontSize': 12,
                           }, className = 'monthly_difference_value'
                           ),

                    html.P('+{0:,.1f}%'.format(revenues_pct_change),
                           style = {
                               'color': '#00cc00',
                               'fontSize': 12,
                           }, className = 'monthly_pct_change'
                           ),
                ], className = 'difference_value_row'),

                html.P('vs mes anterior',
                       style = {
                           'color': '#f18c24',
                           'fontSize': 13,
                           'font-weight': 'bold'
                       },
                       className = 'text_previous_month'
                       ),
            ], className = 'difference_value_column')
        ]

    elif revenues_difference < 0:
        return [
            html.P('Costo GNV',
                   style = {
                       'color': '#00622b',
                       'fontSize': 15,
                       'font-weight': 'bold'
                   },
                   className = 'card_title'
                   ),

            html.Div([
                html.P('Bs {0:,.0f}'.format(revenues),
                       style = {
                           'color': '#f18c24',
                           'fontSize': 17,
                           'font-weight': 'bold'
                       }, className = 'monthly_value'
                       ),

                html.Div([
                    html.I(className = "fas fa-caret-down",
                           style = {"font-size": "25px",
                                    'color': '#EC1E3D'},
                           ),
                ], className = 'value_indicator'),
            ], className = 'value_and_indicator'),

            html.Div([
                html.Div([
                    html.P('-Bs  {0:,.2f}'.format(abs(revenues_difference)),
                           style = {
                               'color': '#EC1E3D',
                               'fontSize': 12,
                           }, className = 'monthly_difference_value'
                           ),

                    html.P('{0:,.1f}%'.format(revenues_pct_change),
                           style = {
                               'color': '#EC1E3D',
                               'fontSize': 12,
                           }, className = 'monthly_pct_change'
                           ),
                ], className = 'difference_value_row'),

                html.P('vs mes anterior',
                       style = {
                           'color': '#f18c24',
                           'fontSize': 13,
                           'font-weight': 'bold'
                       },
                       className = 'text_previous_month'
                       ),
            ], className = 'difference_value_column')
        ]

    elif revenues_difference == 0:
        return [
            html.P('Costo GNV',
                   style = {
                       'color': '#00622b',
                       'fontSize': 17,
                       'font-weight': 'bold'
                   },
                   className = 'card_title'
                   ),

            html.Div([
                html.P('Bs  {0:,.0f}'.format(revenues),
                       style = {
                           'color': 'white',
                           'fontSize': 25,
                           'font-weight': 'bold'
                       }, className = 'monthly_value'
                       ),
            ], className = 'value_and_indicator'),

            html.Div([
                html.Div([
                    html.P('0.00',
                           style = {
                               'color': 'white',
                               'fontSize': 14,
                           }, className = 'monthly_difference_value'
                           ),

                    html.P('0.0%',
                           style = {
                               'color': 'white',
                               'fontSize': 14,
                           }, className = 'monthly_pct_change'
                           ),
                ], className = 'difference_value_row'),

                html.P('vs previous month',
                       style = {
                           'color': 'white',
                           'fontSize': 13,
                           'font-weight': 'bold'
                       },
                       className = 'text_previous_month'
                       ),
            ], className = 'difference_value_column')
        ]


@app.callback(Output('chart22', 'figure'),
              [Input('select_years','value')]
              )
              
def update_graph(select_years):
    resumen6 = resumen.groupby(['Año','Mes'])['Costo_GNV'].sum().reset_index()
    resumen7 = resumen6[(resumen6['Año'] == select_years)]


    return {
        'data': [go.Scatter(
            x = resumen7['Mes'],
            y = resumen7['Costo_GNV'],
            mode = 'lines',
            line = dict(width = 3, color = '#00b300'),
            hoverinfo = 'skip',
        )],

        'layout': go.Layout(
            height = 50,
            width = 150,
            plot_bgcolor = 'rgba(0, 0, 0, 0)',
            paper_bgcolor = 'rgba(0, 0, 0, 0)',
            margin = dict(t = 0, b = 0, r = 0, l = 0),
            xaxis = dict(showline = False,
                         showgrid = False,
                         linecolor = 'white',
                         linewidth = 1,
                         ticks = 'outside',
                         tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'white')

                         ),

            yaxis = dict(showline = False,
                         showgrid = False,
                         linecolor = 'white',
                         linewidth = 1,
                         ticks = 'outside',
                         tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'white')

                         ),
        )

    }

####### TERMINA CALLBACK DE TEXT22 Y CHART22 ####### COSTO GNV

#

#

#


###### EMPIEZA CALLBACK DE TEXT33 Y CHART33###### GASTOS DE OPERACION



@app.callback(Output('text33', 'children'),
              [Input('select_months', 'value')],
              [Input('select_years', 'value')]
              )
def update_text(select_months, select_years):
    if select_months is None:
        raise PreventUpdate
    else:
        # Calculate difference between two months
        resumen['Revenues_Difference'] = resumen['Gastos_Operacion'].diff()
        # Calculate percentage change difference between two months
        resumen['pct_Difference'] = (resumen['Gastos_Operacion'].pct_change()) * 100
        resumen['Revenues_Difference'] = resumen['Revenues_Difference'].fillna(0)
        #filter_year = resumen[resumen['Ano'] == select_years]
        
        filter_month = resumen[(resumen['Año'] == select_years) & (resumen['Mes'] == select_months)]
        revenues = filter_month['Gastos_Operacion'].iloc[0]
        revenues_difference = filter_month['Revenues_Difference'].iloc[0]
        revenues_pct_change = filter_month['pct_Difference'].iloc[0]

    if revenues_difference > 0:
        return [
            html.P('Gastos Operacion',
                   style = {
                       'color': '#00622b',
                       'fontSize': 15,
                       'font-weight': 'bold',
                       
                   },
                   className = 'card_title'
                   ),

            html.Div([
                html.P('Bs  {0:,.0f}'.format(revenues),
                       style = {
                           'color': '#f18c24',
                           'fontSize': 17,
                           'font-weight': 'bold'
                       }, className = 'monthly_value'
                       ),

                html.Div([
                    html.I(className = "fas fa-caret-up",
                           style = {"font-size": "25px",
                                    'color': '#00cc00'},
                           ),
                ], className = 'value_indicator'),
            ], className = 'value_and_indicator'),

            html.Div([
                html.Div([
                    html.P('+Bs  {0:,.2f}'.format(revenues_difference),
                           style = {
                               'color': '#00cc00',
                               'fontSize': 12,
                           }, className = 'monthly_difference_value'
                           ),

                    html.P('+{0:,.1f}%'.format(revenues_pct_change),
                           style = {
                               'color': '#00cc00',
                               'fontSize': 12,
                           }, className = 'monthly_pct_change'
                           ),
                ], className = 'difference_value_row'),

                html.P('vs mes anterior',
                       style = {
                           'color': '#f18c24',
                           'fontSize': 13,
                           'font-weight': 'bold'
                       },
                       className = 'text_previous_month'
                       ),
            ], className = 'difference_value_column')
        ]

    elif revenues_difference < 0:
        return [
            html.P('Gastos Operacion',
                   style = {
                       'color': '#00622b',
                       'fontSize': 15,
                       'font-weight': 'bold'
                   },
                   className = 'card_title'
                   ),

            html.Div([
                html.P('Bs {0:,.0f}'.format(revenues),
                       style = {
                           'color': '#f18c24',
                           'fontSize': 17,
                           'font-weight': 'bold'
                       }, className = 'monthly_value'
                       ),

                html.Div([
                    html.I(className = "fas fa-caret-down",
                           style = {"font-size": "25px",
                                    'color': '#EC1E3D'},
                           ),
                ], className = 'value_indicator'),
            ], className = 'value_and_indicator'),

            html.Div([
                html.Div([
                    html.P('-Bs  {0:,.2f}'.format(abs(revenues_difference)),
                           style = {
                               'color': '#EC1E3D',
                               'fontSize': 12,
                           }, className = 'monthly_difference_value'
                           ),

                    html.P('{0:,.1f}%'.format(revenues_pct_change),
                           style = {
                               'color': '#EC1E3D',
                               'fontSize': 12,
                           }, className = 'monthly_pct_change'
                           ),
                ], className = 'difference_value_row'),

                html.P('vs mes anterior',
                       style = {
                           'color': '#f18c24',
                           'fontSize': 13,
                           'font-weight': 'bold'
                       },
                       className = 'text_previous_month'
                       ),
            ], className = 'difference_value_column')
        ]

    elif revenues_difference == 0:
        return [
            html.P('Costo GNV',
                   style = {
                       'color': '#00622b',
                       'fontSize': 17,
                       'font-weight': 'bold'
                   },
                   className = 'card_title'
                   ),

            html.Div([
                html.P('Bs  {0:,.0f}'.format(revenues),
                       style = {
                           'color': 'white',
                           'fontSize': 25,
                           'font-weight': 'bold'
                       }, className = 'monthly_value'
                       ),
            ], className = 'value_and_indicator'),

            html.Div([
                html.Div([
                    html.P('0.00',
                           style = {
                               'color': 'white',
                               'fontSize': 14,
                           }, className = 'monthly_difference_value'
                           ),

                    html.P('0.0%',
                           style = {
                               'color': 'white',
                               'fontSize': 14,
                           }, className = 'monthly_pct_change'
                           ),
                ], className = 'difference_value_row'),

                html.P('vs previous month',
                       style = {
                           'color': 'white',
                           'fontSize': 13,
                           'font-weight': 'bold'
                       },
                       className = 'text_previous_month'
                       ),
            ], className = 'difference_value_column')
        ]


@app.callback(Output('chart33', 'figure'),
              [Input('select_years','value')]
              )
              
def update_graph(select_years):
    resumen6 = resumen.groupby(['Año','Mes'])['Gastos_Operacion'].sum().reset_index()
    resumen7 = resumen6[(resumen6['Año'] == select_years)]


    return {
        'data': [go.Scatter(
            x = resumen7['Mes'],
            y = resumen7['Gastos_Operacion'],
            mode = 'lines',
            line = dict(width = 3, color = '#00b300'),
            hoverinfo = 'skip',
        )],

        'layout': go.Layout(
            height = 50,
            width = 150,
            plot_bgcolor = 'rgba(0, 0, 0, 0)',
            paper_bgcolor = 'rgba(0, 0, 0, 0)',
            margin = dict(t = 0, b = 0, r = 0, l = 0),
            xaxis = dict(showline = False,
                         showgrid = False,
                         linecolor = 'white',
                         linewidth = 1,
                         ticks = 'outside',
                         tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'white')

                         ),

            yaxis = dict(showline = False,
                         showgrid = False,
                         linecolor = 'white',
                         linewidth = 1,
                         ticks = 'outside',
                         tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'white')

                         ),
        )

    }

####### TERMINA CALLBACK DE TEXT33 Y CHART33 ####### GASTOS OPERACION

#

#

#

###### EMPIEZA CALLBACK DE TEXT44 Y CHART44###### GASTOS DE ADMINISTRACION



@app.callback(Output('text44', 'children'),
              [Input('select_months', 'value')],
              [Input('select_years', 'value')]
              )
def update_text(select_months, select_years):
    if select_months is None:
        raise PreventUpdate
    else:
        # Calculate difference between two months
        resumen['Revenues_Difference'] = resumen['Gastos_Admin'].diff()
        # Calculate percentage change difference between two months
        resumen['pct_Difference'] = (resumen['Gastos_Admin'].pct_change()) * 100
        resumen['Revenues_Difference'] = resumen['Revenues_Difference'].fillna(0)
        #filter_year = resumen[resumen['Ano'] == select_years]
        
        filter_month = resumen[(resumen['Año'] == select_years) & (resumen['Mes'] == select_months)]
        revenues = filter_month['Gastos_Admin'].iloc[0]
        revenues_difference = filter_month['Revenues_Difference'].iloc[0]
        revenues_pct_change = filter_month['pct_Difference'].iloc[0]

    if revenues_difference > 0:
        return [
            html.P('Gastos Administracion',
                   style = {
                       'color': '#00622b',
                       'fontSize': 15,
                       'font-weight': 'bold',
                       
                   },
                   className = 'card_title'
                   ),

            html.Div([
                html.P('Bs  {0:,.0f}'.format(revenues),
                       style = {
                           'color': '#f18c24',
                           'fontSize': 17,
                           'font-weight': 'bold'
                       }, className = 'monthly_value'
                       ),

                html.Div([
                    html.I(className = "fas fa-caret-up",
                           style = {"font-size": "25px",
                                    'color': '#00cc00'},
                           ),
                ], className = 'value_indicator'),
            ], className = 'value_and_indicator'),

            html.Div([
                html.Div([
                    html.P('+Bs  {0:,.2f}'.format(revenues_difference),
                           style = {
                               'color': '#00cc00',
                               'fontSize': 12,
                           }, className = 'monthly_difference_value'
                           ),

                    html.P('+{0:,.1f}%'.format(revenues_pct_change),
                           style = {
                               'color': '#00cc00',
                               'fontSize': 12,
                           }, className = 'monthly_pct_change'
                           ),
                ], className = 'difference_value_row'),

                html.P('vs mes anterior',
                       style = {
                           'color': '#f18c24',
                           'fontSize': 13,
                           'font-weight': 'bold'
                       },
                       className = 'text_previous_month'
                       ),
            ], className = 'difference_value_column')
        ]

    elif revenues_difference < 0:
        return [
            html.P('Gastos Admin',
                   style = {
                       'color': '#00622b',
                       'fontSize': 15,
                       'font-weight': 'bold'
                   },
                   className = 'card_title'
                   ),

            html.Div([
                html.P('Bs {0:,.0f}'.format(revenues),
                       style = {
                           'color': '#f18c24',
                           'fontSize': 17,
                           'font-weight': 'bold'
                       }, className = 'monthly_value'
                       ),

                html.Div([
                    html.I(className = "fas fa-caret-down",
                           style = {"font-size": "25px",
                                    'color': '#EC1E3D'},
                           ),
                ], className = 'value_indicator'),
            ], className = 'value_and_indicator'),

            html.Div([
                html.Div([
                    html.P('-Bs  {0:,.2f}'.format(abs(revenues_difference)),
                           style = {
                               'color': '#EC1E3D',
                               'fontSize': 12,
                           }, className = 'monthly_difference_value'
                           ),

                    html.P('{0:,.1f}%'.format(revenues_pct_change),
                           style = {
                               'color': '#EC1E3D',
                               'fontSize': 12,
                           }, className = 'monthly_pct_change'
                           ),
                ], className = 'difference_value_row'),

                html.P('vs mes anterior',
                       style = {
                           'color': '#f18c24',
                           'fontSize': 13,
                           'font-weight': 'bold'
                       },
                       className = 'text_previous_month'
                       ),
            ], className = 'difference_value_column')
        ]

    elif revenues_difference == 0:
        return [
            html.P('Gastos Admin',
                   style = {
                       'color': '#00622b',
                       'fontSize': 17,
                       'font-weight': 'bold'
                   },
                   className = 'card_title'
                   ),

            html.Div([
                html.P('Bs  {0:,.0f}'.format(revenues),
                       style = {
                           'color': 'white',
                           'fontSize': 25,
                           'font-weight': 'bold'
                       }, className = 'monthly_value'
                       ),
            ], className = 'value_and_indicator'),

            html.Div([
                html.Div([
                    html.P('0.00',
                           style = {
                               'color': 'white',
                               'fontSize': 14,
                           }, className = 'monthly_difference_value'
                           ),

                    html.P('0.0%',
                           style = {
                               'color': 'white',
                               'fontSize': 14,
                           }, className = 'monthly_pct_change'
                           ),
                ], className = 'difference_value_row'),

                html.P('vs previous month',
                       style = {
                           'color': 'white',
                           'fontSize': 13,
                           'font-weight': 'bold'
                       },
                       className = 'text_previous_month'
                       ),
            ], className = 'difference_value_column')
        ]


@app.callback(Output('chart44', 'figure'),
              [Input('select_years','value')]
              )
              
def update_graph(select_years):
    resumen6 = resumen.groupby(['Año','Mes'])['Gastos_Admin'].sum().reset_index()
    resumen7 = resumen6[(resumen6['Año'] == select_years)]


    return {
        'data': [go.Scatter(
            x = resumen7['Mes'],
            y = resumen7['Gastos_Admin'],
            mode = 'lines',
            line = dict(width = 3, color = '#00b300'),
            hoverinfo = 'skip',
        )],

        'layout': go.Layout(
            height = 50,
            width = 150,
            plot_bgcolor = 'rgba(0, 0, 0, 0)',
            paper_bgcolor = 'rgba(0, 0, 0, 0)',
            margin = dict(t = 0, b = 0, r = 0, l = 0),
            xaxis = dict(showline = False,
                         showgrid = False,
                         linecolor = 'white',
                         linewidth = 1,
                         ticks = 'outside',
                         tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'white')

                         ),

            yaxis = dict(showline = False,
                         showgrid = False,
                         linecolor = 'white',
                         linewidth = 1,
                         ticks = 'outside',
                         tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'white')

                         ),
        )

    }

####### TERMINA CALLBACK DE TEXT44 Y CHART44 ####### GASTOS ADMINISTRACION







###### EMPIEZA CALLBACK DE TEXT55 Y CHART55###### GASTOS CAJA GENERAL



@app.callback(Output('text55', 'children'),
              [Input('select_months', 'value')],
              [Input('select_years', 'value')]
              )
def update_text(select_months, select_years):
    if select_months is None:
        raise PreventUpdate
    else:
        # Calculate difference between two months
        resumen['Revenues_Difference'] = resumen['Gastos_CG'].diff()
        # Calculate percentage change difference between two months
        resumen['pct_Difference'] = (resumen['Gastos_CG'].pct_change()) * 100
        resumen['Revenues_Difference'] = resumen['Revenues_Difference'].fillna(0)
        #filter_year = resumen[resumen['Ano'] == select_years]
        
        filter_month = resumen[(resumen['Año'] == select_years) & (resumen['Mes'] == select_months)]
        revenues = filter_month['Gastos_CG'].iloc[0]
        revenues_difference = filter_month['Revenues_Difference'].iloc[0]
        revenues_pct_change = filter_month['pct_Difference'].iloc[0]

    if revenues_difference > 0:
        return [
            html.P('Gastos Caja General',
                   style = {
                       'color': '#00622b',
                       'fontSize': 15,
                       'font-weight': 'bold',
                       
                   },
                   className = 'card_title'
                   ),

            html.Div([
                html.P('Bs  {0:,.0f}'.format(revenues),
                       style = {
                           'color': '#f18c24',
                           'fontSize': 17,
                           'font-weight': 'bold'
                       }, className = 'monthly_value'
                       ),

                html.Div([
                    html.I(className = "fas fa-caret-up",
                           style = {"font-size": "25px",
                                    'color': '#00cc00'},
                           ),
                ], className = 'value_indicator'),
            ], className = 'value_and_indicator'),

            html.Div([
                html.Div([
                    html.P('+Bs  {0:,.2f}'.format(revenues_difference),
                           style = {
                               'color': '#00cc00',
                               'fontSize': 12,
                           }, className = 'monthly_difference_value'
                           ),

                    html.P('+{0:,.1f}%'.format(revenues_pct_change),
                           style = {
                               'color': '#00cc00',
                               'fontSize': 12,
                           }, className = 'monthly_pct_change'
                           ),
                ], className = 'difference_value_row'),

                html.P('vs mes anterior',
                       style = {
                           'color': '#f18c24',
                           'fontSize': 13,
                           'font-weight': 'bold'
                       },
                       className = 'text_previous_month'
                       ),
            ], className = 'difference_value_column')
        ]

    elif revenues_difference < 0:
        return [
            html.P('Gastos Caja General',
                   style = {
                       'color': '#00622b',
                       'fontSize': 15,
                       'font-weight': 'bold'
                   },
                   className = 'card_title'
                   ),

            html.Div([
                html.P('Bs {0:,.0f}'.format(revenues),
                       style = {
                           'color': '#f18c24',
                           'fontSize': 17,
                           'font-weight': 'bold'
                       }, className = 'monthly_value'
                       ),

                html.Div([
                    html.I(className = "fas fa-caret-down",
                           style = {"font-size": "25px",
                                    'color': '#EC1E3D'},
                           ),
                ], className = 'value_indicator'),
            ], className = 'value_and_indicator'),

            html.Div([
                html.Div([
                    html.P('-Bs  {0:,.2f}'.format(abs(revenues_difference)),
                           style = {
                               'color': '#EC1E3D',
                               'fontSize': 12,
                           }, className = 'monthly_difference_value'
                           ),

                    html.P('{0:,.1f}%'.format(revenues_pct_change),
                           style = {
                               'color': '#EC1E3D',
                               'fontSize': 12,
                           }, className = 'monthly_pct_change'
                           ),
                ], className = 'difference_value_row'),

                html.P('vs mes anterior',
                       style = {
                           'color': '#f18c24',
                           'fontSize': 13,
                           'font-weight': 'bold'
                       },
                       className = 'text_previous_month'
                       ),
            ], className = 'difference_value_column')
        ]

    elif revenues_difference == 0:
        return [
            html.P('Gastos Caja General',
                   style = {
                       'color': '#00622b',
                       'fontSize': 17,
                       'font-weight': 'bold'
                   },
                   className = 'card_title'
                   ),

            html.Div([
                html.P('Bs  {0:,.0f}'.format(revenues),
                       style = {
                           'color': 'white',
                           'fontSize': 25,
                           'font-weight': 'bold'
                       }, className = 'monthly_value'
                       ),
            ], className = 'value_and_indicator'),

            html.Div([
                html.Div([
                    html.P('0.00',
                           style = {
                               'color': 'white',
                               'fontSize': 14,
                           }, className = 'monthly_difference_value'
                           ),

                    html.P('0.0%',
                           style = {
                               'color': 'white',
                               'fontSize': 14,
                           }, className = 'monthly_pct_change'
                           ),
                ], className = 'difference_value_row'),

                html.P('vs previous month',
                       style = {
                           'color': 'white',
                           'fontSize': 13,
                           'font-weight': 'bold'
                       },
                       className = 'text_previous_month'
                       ),
            ], className = 'difference_value_column')
        ]


@app.callback(Output('chart55', 'figure'),
              [Input('select_years','value')]
              )
              
def update_graph(select_years):
    resumen6 = resumen.groupby(['Año','Mes'])['Gastos_CG'].sum().reset_index()
    resumen7 = resumen6[(resumen6['Año'] == select_years)]


    return {
        'data': [go.Scatter(
            x = resumen7['Mes'],
            y = resumen7['Gastos_CG'],
            mode = 'lines',
            line = dict(width = 3, color = '#00b300'),
            hoverinfo = 'skip',
        )],

        'layout': go.Layout(
            height = 50,
            width = 150,
            plot_bgcolor = 'rgba(0, 0, 0, 0)',
            paper_bgcolor = 'rgba(0, 0, 0, 0)',
            margin = dict(t = 0, b = 0, r = 0, l = 0),
            xaxis = dict(showline = False,
                         showgrid = False,
                         linecolor = 'white',
                         linewidth = 1,
                         ticks = 'outside',
                         tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'white')

                         ),

            yaxis = dict(showline = False,
                         showgrid = False,
                         linecolor = 'white',
                         linewidth = 1,
                         ticks = 'outside',
                         tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'white')

                         ),
        )

    }

####### TERMINA CALLBACK DE TEXT55 Y CHART55 ####### GASTOS CAJA GENERAL






###### EMPIEZA CALLBACK DE TEXT66 Y CHART66###### IMPUESTOS



@app.callback(Output('text66', 'children'),
              [Input('select_months', 'value')],
              [Input('select_years', 'value')]
              )
def update_text(select_months, select_years):
    if select_months is None:
        raise PreventUpdate
    else:
        # Calculate difference between two months
        resumen['Revenues_Difference'] = resumen['Impuestos'].diff()
        # Calculate percentage change difference between two months
        resumen['pct_Difference'] = (resumen['Impuestos'].pct_change()) * 100
        resumen['Revenues_Difference'] = resumen['Revenues_Difference'].fillna(0)
        #filter_year = resumen[resumen['Ano'] == select_years]
        
        filter_month = resumen[(resumen['Año'] == select_years) & (resumen['Mes'] == select_months)]
        revenues = filter_month['Impuestos'].iloc[0]
        revenues_difference = filter_month['Revenues_Difference'].iloc[0]
        revenues_pct_change = filter_month['pct_Difference'].iloc[0]

    if revenues_difference > 0:
        return [
            html.P('Impuestos',
                   style = {
                       'color': '#00622b',
                       'fontSize': 15,
                       'font-weight': 'bold',
                       
                   },
                   className = 'card_title'
                   ),

            html.Div([
                html.P('Bs  {0:,.0f}'.format(revenues),
                       style = {
                           'color': '#f18c24',
                           'fontSize': 17,
                           'font-weight': 'bold'
                       }, className = 'monthly_value'
                       ),

                html.Div([
                    html.I(className = "fas fa-caret-up",
                           style = {"font-size": "25px",
                                    'color': '#00cc00'},
                           ),
                ], className = 'value_indicator'),
            ], className = 'value_and_indicator'),

            html.Div([
                html.Div([
                    html.P('+Bs  {0:,.2f}'.format(revenues_difference),
                           style = {
                               'color': '#00cc00',
                               'fontSize': 12,
                           }, className = 'monthly_difference_value'
                           ),

                    html.P('+{0:,.1f}%'.format(revenues_pct_change),
                           style = {
                               'color': '#00cc00',
                               'fontSize': 12,
                           }, className = 'monthly_pct_change'
                           ),
                ], className = 'difference_value_row'),

                html.P('vs mes anterior',
                       style = {
                           'color': '#f18c24',
                           'fontSize': 13,
                           'font-weight': 'bold'
                       },
                       className = 'text_previous_month'
                       ),
            ], className = 'difference_value_column')
        ]

    elif revenues_difference < 0:
        return [
            html.P('Impuestos',
                   style = {
                       'color': '#00622b',
                       'fontSize': 15,
                       'font-weight': 'bold'
                   },
                   className = 'card_title'
                   ),

            html.Div([
                html.P('Bs {0:,.0f}'.format(revenues),
                       style = {
                           'color': '#f18c24',
                           'fontSize': 17,
                           'font-weight': 'bold'
                       }, className = 'monthly_value'
                       ),

                html.Div([
                    html.I(className = "fas fa-caret-down",
                           style = {"font-size": "25px",
                                    'color': '#EC1E3D'},
                           ),
                ], className = 'value_indicator'),
            ], className = 'value_and_indicator'),

            html.Div([
                html.Div([
                    html.P('-Bs  {0:,.2f}'.format(abs(revenues_difference)),
                           style = {
                               'color': '#EC1E3D',
                               'fontSize': 12,
                           }, className = 'monthly_difference_value'
                           ),

                    html.P('{0:,.1f}%'.format(revenues_pct_change),
                           style = {
                               'color': '#EC1E3D',
                               'fontSize': 12,
                           }, className = 'monthly_pct_change'
                           ),
                ], className = 'difference_value_row'),

                html.P('vs mes anterior',
                       style = {
                           'color': '#f18c24',
                           'fontSize': 13,
                           'font-weight': 'bold'
                       },
                       className = 'text_previous_month'
                       ),
            ], className = 'difference_value_column')
        ]

    elif revenues_difference == 0:
        return [
            html.P('Impuestos',
                   style = {
                       'color': '#00622b',
                       'fontSize': 17,
                       'font-weight': 'bold'
                   },
                   className = 'card_title'
                   ),

            html.Div([
                html.P('Bs  {0:,.0f}'.format(revenues),
                       style = {
                           'color': 'white',
                           'fontSize': 25,
                           'font-weight': 'bold'
                       }, className = 'monthly_value'
                       ),
            ], className = 'value_and_indicator'),

            html.Div([
                html.Div([
                    html.P('0.00',
                           style = {
                               'color': 'white',
                               'fontSize': 14,
                           }, className = 'monthly_difference_value'
                           ),

                    html.P('0.0%',
                           style = {
                               'color': 'white',
                               'fontSize': 14,
                           }, className = 'monthly_pct_change'
                           ),
                ], className = 'difference_value_row'),

                html.P('vs previous month',
                       style = {
                           'color': 'white',
                           'fontSize': 13,
                           'font-weight': 'bold'
                       },
                       className = 'text_previous_month'
                       ),
            ], className = 'difference_value_column')
        ]


@app.callback(Output('chart66', 'figure'),
              [Input('select_years','value')]
              )
              
def update_graph(select_years):
    resumen6 = resumen.groupby(['Año','Mes'])['Impuestos'].sum().reset_index()
    resumen7 = resumen6[(resumen6['Año'] == select_years)]


    return {
        'data': [go.Scatter(
            x = resumen7['Mes'],
            y = resumen7['Impuestos'],
            mode = 'lines',
            line = dict(width = 3, color = '#00b300'),
            hoverinfo = 'skip',
        )],

        'layout': go.Layout(
            height = 50,
            width = 150,
            plot_bgcolor = 'rgba(0, 0, 0, 0)',
            paper_bgcolor = 'rgba(0, 0, 0, 0)',
            margin = dict(t = 0, b = 0, r = 0, l = 0),
            xaxis = dict(showline = False,
                         showgrid = False,
                         linecolor = 'white',
                         linewidth = 1,
                         ticks = 'outside',
                         tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'white')

                         ),

            yaxis = dict(showline = False,
                         showgrid = False,
                         linecolor = 'white',
                         linewidth = 1,
                         ticks = 'outside',
                         tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'white')

                         ),
        )

    }

####### TERMINA CALLBACK DE TEXT66 Y CHART66 ####### IMPUESTOS

#

#

#

###### EMPIEZA CALLBACK DE TEXT77 Y CHART77###### TOTAL EGRESOS



@app.callback(Output('text77', 'children'),
              [Input('select_months', 'value')],
              [Input('select_years', 'value')]
              )
def update_text(select_months, select_years):
    if select_months is None:
        raise PreventUpdate
    else:
        # Calculate difference between two months
        resumen['Revenues_Difference'] = resumen['Total_Egresos'].diff()
        # Calculate percentage change difference between two months
        resumen['pct_Difference'] = (resumen['Total_Egresos'].pct_change()) * 100
        resumen['Revenues_Difference'] = resumen['Revenues_Difference'].fillna(0)
        #filter_year = resumen[resumen['Ano'] == select_years]
        
        filter_month = resumen[(resumen['Año'] == select_years) & (resumen['Mes'] == select_months)]
        revenues = filter_month['Total_Egresos'].iloc[0]
        revenues_difference = filter_month['Revenues_Difference'].iloc[0]
        revenues_pct_change = filter_month['pct_Difference'].iloc[0]

    if revenues_difference > 0:
        return [
            html.P('Total Egresos',
                   style = {
                       'color': '#00622b',
                       'fontSize': 15,
                       'font-weight': 'bold',
                       
                   },
                   className = 'card_title'
                   ),

            html.Div([
                html.P('Bs  {0:,.0f}'.format(revenues),
                       style = {
                           'color': '#f18c24',
                           'fontSize': 17,
                           'font-weight': 'bold'
                       }, className = 'monthly_value'
                       ),

                html.Div([
                    html.I(className = "fas fa-caret-up",
                           style = {"font-size": "25px",
                                    'color': '#00cc00'},
                           ),
                ], className = 'value_indicator'),
            ], className = 'value_and_indicator'),

            html.Div([
                html.Div([
                    html.P('+Bs  {0:,.2f}'.format(revenues_difference),
                           style = {
                               'color': '#00cc00',
                               'fontSize': 12,
                           }, className = 'monthly_difference_value'
                           ),

                    html.P('+{0:,.1f}%'.format(revenues_pct_change),
                           style = {
                               'color': '#00cc00',
                               'fontSize': 12,
                           }, className = 'monthly_pct_change'
                           ),
                ], className = 'difference_value_row'),

                html.P('vs mes anterior',
                       style = {
                           'color': '#f18c24',
                           'fontSize': 13,
                           'font-weight': 'bold'
                       },
                       className = 'text_previous_month'
                       ),
            ], className = 'difference_value_column')
        ]

    elif revenues_difference < 0:
        return [
            html.P('Total Egresos',
                   style = {
                       'color': '#00622b',
                       'fontSize': 15,
                       'font-weight': 'bold'
                   },
                   className = 'card_title'
                   ),

            html.Div([
                html.P('Bs {0:,.0f}'.format(revenues),
                       style = {
                           'color': '#f18c24',
                           'fontSize': 17,
                           'font-weight': 'bold'
                       }, className = 'monthly_value'
                       ),

                html.Div([
                    html.I(className = "fas fa-caret-down",
                           style = {"font-size": "25px",
                                    'color': '#EC1E3D'},
                           ),
                ], className = 'value_indicator'),
            ], className = 'value_and_indicator'),

            html.Div([
                html.Div([
                    html.P('-Bs  {0:,.2f}'.format(abs(revenues_difference)),
                           style = {
                               'color': '#EC1E3D',
                               'fontSize': 12,
                           }, className = 'monthly_difference_value'
                           ),

                    html.P('{0:,.1f}%'.format(revenues_pct_change),
                           style = {
                               'color': '#EC1E3D',
                               'fontSize': 12,
                           }, className = 'monthly_pct_change'
                           ),
                ], className = 'difference_value_row'),

                html.P('vs mes anterior',
                       style = {
                           'color': '#f18c24',
                           'fontSize': 13,
                           'font-weight': 'bold'
                       },
                       className = 'text_previous_month'
                       ),
            ], className = 'difference_value_column')
        ]

    elif revenues_difference == 0:
        return [
            html.P('Total Egresos',
                   style = {
                       'color': '#00622b',
                       'fontSize': 17,
                       'font-weight': 'bold'
                   },
                   className = 'card_title'
                   ),

            html.Div([
                html.P('Bs  {0:,.0f}'.format(revenues),
                       style = {
                           'color': 'white',
                           'fontSize': 25,
                           'font-weight': 'bold'
                       }, className = 'monthly_value'
                       ),
            ], className = 'value_and_indicator'),

            html.Div([
                html.Div([
                    html.P('0.00',
                           style = {
                               'color': 'white',
                               'fontSize': 14,
                           }, className = 'monthly_difference_value'
                           ),

                    html.P('0.0%',
                           style = {
                               'color': 'white',
                               'fontSize': 14,
                           }, className = 'monthly_pct_change'
                           ),
                ], className = 'difference_value_row'),

                html.P('vs previous month',
                       style = {
                           'color': 'white',
                           'fontSize': 13,
                           'font-weight': 'bold'
                       },
                       className = 'text_previous_month'
                       ),
            ], className = 'difference_value_column')
        ]


@app.callback(Output('chart77', 'figure'),
              [Input('select_years','value')]
              )
              
def update_graph(select_years):
    resumen6 = resumen.groupby(['Año','Mes'])['Total_Egresos'].sum().reset_index()
    resumen7 = resumen6[(resumen6['Año'] == select_years)]


    return {
        'data': [go.Scatter(
            x = resumen7['Mes'],
            y = resumen7['Total_Egresos'],
            mode = 'lines',
            line = dict(width = 3, color = '#00b300'),
            hoverinfo = 'skip',
        )],

        'layout': go.Layout(
            height = 50,
            width = 150,
            plot_bgcolor = 'rgba(0, 0, 0, 0)',
            paper_bgcolor = 'rgba(0, 0, 0, 0)',
            margin = dict(t = 0, b = 0, r = 0, l = 0),
            xaxis = dict(showline = False,
                         showgrid = False,
                         linecolor = 'white',
                         linewidth = 1,
                         ticks = 'outside',
                         tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'white')

                         ),

            yaxis = dict(showline = False,
                         showgrid = False,
                         linecolor = 'white',
                         linewidth = 1,
                         ticks = 'outside',
                         tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'white')

                         ),
        )

    }

####### TERMINA CALLBACK DE TEXT77 Y CHART77 ####### TOTAL EGRESOS


###### EMPIEZA CALLBACK DE TEXT88 Y CHART88###### RESULTADO BS



@app.callback(Output('text88', 'children'),
              [Input('select_months', 'value')],
              [Input('select_years', 'value')]
              )
def update_text(select_months, select_years):
    if select_months is None:
        raise PreventUpdate
    else:
        # Calculate difference between two months
        resumen['Revenues_Difference'] = resumen['Resultado_Bs'].diff()
        # Calculate percentage change difference between two months
        resumen['pct_Difference'] = (resumen['Resultado_Bs'].pct_change()) * 100
        resumen['Revenues_Difference'] = resumen['Revenues_Difference'].fillna(0)
        #filter_year = resumen[resumen['Ano'] == select_years]
        
        filter_month = resumen[(resumen['Año'] == select_years) & (resumen['Mes'] == select_months)]
        revenues = filter_month['Resultado_Bs'].iloc[0]
        revenues_difference = filter_month['Revenues_Difference'].iloc[0]
        revenues_pct_change = filter_month['pct_Difference'].iloc[0]

    if revenues_difference > 0:
        return [
            html.P('Resultado Bs',
                   style = {
                       'color': '#00622b',
                       'fontSize': 15,
                       'font-weight': 'bold',
                       
                   },
                   className = 'card_title'
                   ),

            html.Div([
                html.P('Bs  {0:,.0f}'.format(revenues),
                       style = {
                           'color': '#f18c24',
                           'fontSize': 17,
                           'font-weight': 'bold'
                       }, className = 'monthly_value'
                       ),

                html.Div([
                    html.I(className = "fas fa-caret-up",
                           style = {"font-size": "25px",
                                    'color': '#00cc00'},
                           ),
                ], className = 'value_indicator'),
            ], className = 'value_and_indicator'),

            html.Div([
                html.Div([
                    html.P('+Bs  {0:,.2f}'.format(revenues_difference),
                           style = {
                               'color': '#00cc00',
                               'fontSize': 12,
                           }, className = 'monthly_difference_value'
                           ),

                    html.P('+{0:,.1f}%'.format(revenues_pct_change),
                           style = {
                               'color': '#00cc00',
                               'fontSize': 12,
                           }, className = 'monthly_pct_change'
                           ),
                ], className = 'difference_value_row'),

                html.P('vs mes anterior',
                       style = {
                           'color': '#f18c24',
                           'fontSize': 13,
                           'font-weight': 'bold'
                       },
                       className = 'text_previous_month'
                       ),
            ], className = 'difference_value_column')
        ]

    elif revenues_difference < 0:
        return [
            html.P('Resultado Bs',
                   style = {
                       'color': '#00622b',
                       'fontSize': 15,
                       'font-weight': 'bold'
                   },
                   className = 'card_title'
                   ),

            html.Div([
                html.P('Bs {0:,.0f}'.format(revenues),
                       style = {
                           'color': '#f18c24',
                           'fontSize': 17,
                           'font-weight': 'bold'
                       }, className = 'monthly_value'
                       ),

                html.Div([
                    html.I(className = "fas fa-caret-down",
                           style = {"font-size": "25px",
                                    'color': '#EC1E3D'},
                           ),
                ], className = 'value_indicator'),
            ], className = 'value_and_indicator'),

            html.Div([
                html.Div([
                    html.P('-Bs  {0:,.2f}'.format(abs(revenues_difference)),
                           style = {
                               'color': '#EC1E3D',
                               'fontSize': 12,
                           }, className = 'monthly_difference_value'
                           ),

                    html.P('{0:,.1f}%'.format(revenues_pct_change),
                           style = {
                               'color': '#EC1E3D',
                               'fontSize': 12,
                           }, className = 'monthly_pct_change'
                           ),
                ], className = 'difference_value_row'),

                html.P('vs mes anterior',
                       style = {
                           'color': '#f18c24',
                           'fontSize': 13,
                           'font-weight': 'bold'
                       },
                       className = 'text_previous_month'
                       ),
            ], className = 'difference_value_column')
        ]

    elif revenues_difference == 0:
        return [
            html.P('Resultado Bs',
                   style = {
                       'color': '#00622b',
                       'fontSize': 17,
                       'font-weight': 'bold'
                   },
                   className = 'card_title'
                   ),

            html.Div([
                html.P('Bs  {0:,.0f}'.format(revenues),
                       style = {
                           'color': 'white',
                           'fontSize': 25,
                           'font-weight': 'bold'
                       }, className = 'monthly_value'
                       ),
            ], className = 'value_and_indicator'),

            html.Div([
                html.Div([
                    html.P('0.00',
                           style = {
                               'color': 'white',
                               'fontSize': 14,
                           }, className = 'monthly_difference_value'
                           ),

                    html.P('0.0%',
                           style = {
                               'color': 'white',
                               'fontSize': 14,
                           }, className = 'monthly_pct_change'
                           ),
                ], className = 'difference_value_row'),

                html.P('vs previous month',
                       style = {
                           'color': 'white',
                           'fontSize': 13,
                           'font-weight': 'bold'
                       },
                       className = 'text_previous_month'
                       ),
            ], className = 'difference_value_column')
        ]


@app.callback(Output('chart88', 'figure'),
              [Input('select_years','value')]
              )
              
def update_graph(select_years):
    resumen6 = resumen.groupby(['Año','Mes'])['Resultado_Bs'].sum().reset_index()
    resumen7 = resumen6[(resumen6['Año'] == select_years)]


    return {
        'data': [go.Scatter(
            x = resumen7['Mes'],
            y = resumen7['Resultado_Bs'],
            mode = 'lines',
            line = dict(width = 3, color = '#00b300'),
            hoverinfo = 'skip',
        )],

        'layout': go.Layout(
            height = 50,
            width = 150,
            plot_bgcolor = 'rgba(0, 0, 0, 0)',
            paper_bgcolor = 'rgba(0, 0, 0, 0)',
            margin = dict(t = 0, b = 0, r = 0, l = 0),
            xaxis = dict(showline = False,
                         showgrid = False,
                         linecolor = 'white',
                         linewidth = 1,
                         ticks = 'outside',
                         tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'white')

                         ),

            yaxis = dict(showline = False,
                         showgrid = False,
                         linecolor = 'white',
                         linewidth = 1,
                         ticks = 'outside',
                         tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'white')

                         ),
        )

    }

####### TERMINA CALLBACK DE TEXT88 Y CHART88 ####### Resultado Bs


###### INICIA CALLBACK DE Donut Chart ######
@app.callback(Output('donut_chart', 'figure'),
              [Input('select_years','value')],
              [Input('select_months','value')])
def update_graph(select_years, select_months):
    sales5 = df3.groupby(['Ano', 'Mes', 'Sindicato'])['Volumen'].sum().reset_index()
    sales6 = sales5[(sales5['Ano'] == select_years) & (sales5['Mes'] == select_months)].sort_values(by = ['Volumen'], ascending = False)#.nlargest(7, columns = ['Volumen'])
    
    fig = px.pie(sales6, values='Volumen', names='Sindicato',title="Ventas por Sindicato", width=800, height=800, hole=.3)
    return fig

    ####LOGRAR HACER QUE EL GRAFICO FUNCIONE!
    


  



#INICIO DE APP

if __name__ == '__main__':
    app.run_server(debug=True)