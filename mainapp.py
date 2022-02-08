import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import dash_table as dt
import glob
import os

col_list = ["Volumen", "Placa", "Vendedor", "Fecha"]
dirname = os.path.dirname(__file__)
path = os.path.join(dirname, 'otro/')

#path = r'C:\Users\pez_g\Desktop\proyecto cañaveral 2022\VICENTE' # use your path
all_files = glob.glob(path + "/*.xls")

li = []

for filename in all_files:
    df = pd.read_excel(filename, index_col=None, header=0, usecols=col_list)
    li.append(df)

sales = pd.concat(li, axis=0, ignore_index=True)






#cwd = os.path.abspath('') 
#files = os.listdir(cwd) 
#col_list = ["Volumen", "Placa", "Vendedor", "Fecha", "SubTotal", "Pago", "Inicio"]
#sales = pd.DataFrame()
#for file in files:
#     if file.endswith('.xls'):
#         sales = sales.append(pd.read_excel(file, usecols=col_list), ignore_index=True) 







#COLUMNAS QUE VAMOS A USAR
#col_list = ["Volumen", "Placa", "Vendedor", "Fecha", "SubTotal", "Pago", "Inicio"]

#IMPORTAR PRIMER DATAFRAME
#sales = pd.read_excel('T2021.xls', usecols=col_list)

#df2 = sales.groupby([(sales.Fecha.dt.month), (sales.Fecha.dt.day), ('Placa')])['Volumen'].count().nlargest(n=50)

#df2 = sales.groupby([(sales.Fecha.dt.month), (sales.Fecha.dt.day), ('Placa')])['Volumen'].count().nlargest(n=50)

#sales = pd.read_csv('12021.csv', usecols=col_list,encoding='latin-1')



sales['Fecha'] = pd.to_datetime(sales['Fecha'])
sales['Ano'] = sales['Fecha'].dt.year
sales['Mes'] = sales['Fecha'].dt.month
sales['Dia'] = sales['Fecha'].dt.day


#CREAR SEGUNDO DATAFRAME
df2 = sales.groupby(['Ano','Mes', 'Placa'])['Volumen'].count().nlargest(n=10000).reset_index()

#df2['Fecha'] = pd.to_datetime(sales['Fecha'])
#df2['Mes'] = sales['Fecha'].dt.month
#df2['Dia'] = sales['Fecha'].dt.day


app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])
server = app.server

#EMPIEZA LA APLICACION DASH
app.layout = html.Div([

#1
html.Div([

    #1.1 LOGO
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
]), 


#2 
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
                       value= 2021,
                       #marks={str(yr): str(yr) for yr in range(1, 13)},
                       

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
                       value= 12,
                       #marks={str(yr): str(yr) for yr in range(1, 13)},
                       

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
]),


#3
html.Div([



#3.1 PRIMER DIV DATATABLE
    html.Div([
html.Label("Top clientes del mes", style={'color': '#00622b',
                                                    'font' : 'Arial',
                                                    'font-weight': 'bold',
                                                    'fontSize': 14,}),
            dt.DataTable(id = 'my_datatable',
                         columns=[{'name': i, 'id': i} for i in
                                  df2.loc[:, ["Placa", "Volumen"]]],
                         virtualization=True,
                         style_cell={'textAlign': 'left',
                                     'min-width': '100px',
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
                         fixed_rows={'headers': True},
                         sort_action='native',
                         sort_mode='multi')


        ], className='create_container2 two columns', style={'height': '400px'}),

#3.2 SEGUNDO DIV LINECHART
    html.Div([

            dcc.Graph(id = 'line_chart', config={'displayModeBar': 'hover'},
                      style={'height': '350px'})

        ], className='create_container2 six columns', style={'height': '400px'}),

#3.3 TERCER DIV KPIs 
    html.Div([
           
            html.Div(id = 'text2'),
            html.Div(id = 'text6'),
            html.Div(id = 'text5'),
            html.Div(id = 'text1'),
            html.Div(id = 'text3'),
            html.Div(id = 'text4'),
            
            

        ], className='create_container2 two columns', style={'height': '400px'}),
 
]),

#4
html.Div([

    html.Div([

            dcc.Graph(id = 'bar_chart_1', config={'displayModeBar': 'hover'},
                      ),

        ], className='create_container2 three columns'),

]), 

], id = 'mainContainer', style={'display': 'flex', 'flex-direction': 'column'})


#****CALLBACKS***CALLBACKS***CALLBACKS***CALLBACKS***CALLBACKS***

#CALLBACK PARA DATATABLE
@app.callback(Output('my_datatable', 'data'),
              [Input('select_years','value')],
              [Input('select_months','value')]
              )
def update_graph(select_years, select_months):
    data_table = df2[(df2['Mes'] == select_months) & (df2['Ano'] == select_years) ]
    #print(df2['Volumen'].value_counts())
    return data_table.to_dict('records')
    

#CALLBACK PARA LINE CHART
@app.callback(Output('line_chart', 'figure'),
              [Input('select_years','value')],
              [Input('select_months','value')]
              )
              
def update_graph(select_years, select_months):
    sales6 = sales.groupby(['Ano','Mes', 'Dia'])['Volumen'].sum().reset_index()
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
                
                '<b>Sales</b>: $' + [f'{x:,.0f}' for x in sales7['Volumen']] + '<br>'

            ),

        ],


        'layout': go.Layout(
            title={'text': 'Venta de GNV en m3' + ' ' + str((select_months)),
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

#CALLBACK KPI 1
@app.callback(Output('text1', 'children'),
              [Input('select_years','value')])
def update_graph(select_years):
    sales8 = sales.groupby(['Ano'])['Volumen'].sum().reset_index()
    current_year = sales8[(sales8['Ano'] == select_years)]['Volumen'].sum()

    return [

        html.H6(children='Ventas por Año',
                style={'textAlign': 'center',
                       'color': '#00622b'}),

        html.P('m3  {0:,.2f}'.format(current_year),
               style={'textAlign': 'center',
                      'color': '#f18c24',
                      'font-weight': 'bold',
                      'fontSize': 17,
                      'margin-top': '-10px'})

    ]

#CALLBACK KPI 2
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
                       
                       'color': '#00622b'}),

        html.P('m3  {0:,.2f}'.format(current_month),
               style={'textAlign': 'center',
                      'color': '#f18c24',
                      'font-weight': 'bold',
                      'fontSize': 17,
                      'margin-top': '-10px'})

    ]

#CALLBACK KPI 3


@app.callback(Output('text3', 'children'),
              [Input('select_years','value')])
def update_graph(select_years):
    sales10 = sales.groupby(['Ano'])['Volumen'].sum().reset_index()
    sales10['PY'] = sales10['Volumen'].shift(1)
    previous_year = sales10[(sales10['Ano'] == select_years)]['PY'].sum()

    return [

        html.H6(children='Ventas Año Pasado',
                style={'textAlign': 'center',
                       'color': '#00622b'}),

        html.P('m3  {0:,.2f}'.format(previous_year),
               style={'textAlign': 'center',
                      'color': '#f18c24',
                      'font-weight': 'bold',
                      'fontSize': 17,
                      'margin-top': '-10px'})

    ]

#CALLBACK KPI 4
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
                       'color': '#00622b'}),

        html.P('{0:,.2f}%'.format(growth_year),
               style={'textAlign': 'center',
                      'color': '#f18c24',
                      'font-weight': 'bold',
                      'fontSize': 17,
                      'margin-top': '-10px'})

    ]

#CALLBACK KPI 5
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
                       'color': '#00622b'}),

        html.P('{0:,.2f}%'.format(growth_year),
               style={'textAlign': 'center',
                      'color': '#f18c24',
                      'font-weight': 'bold',
                      'fontSize': 17,
                      'margin-top': '-10px'})

    ]


#CALLBACK KPI 6


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
                       'color': '#00622b'}),

        html.P('m3  {0:,.2f}'.format(previous_year),
               style={'textAlign': 'center',
                      'color': '#f18c24',
                      'font-weight': 'bold',
                      'fontSize': 17,
                      'margin-top': '-10px'})

    ]
#CALLBACK BAR CHART
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






#INICIO DE APP

if __name__ == '__main__':
    app.run_server(debug=True)