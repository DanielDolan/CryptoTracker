import pandas as pd
import plotly.express as px

import requests
import json
import os
from dotenv import load_dotenv


import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State
import plotly.graph_objects as go
import datetime

load_dotenv()

ApiEnv = os.getenv('APIKEY')

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': ApiEnv,
}
crydata=[]
params = {
    'start' : '1',
    'limit' : '5',
    'convert' : 'USD'
}

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

# json = requests.get(url, params=params, headers=headers).json()


# cryptodata =json['data']

# for x in cryptodata:
#     crydata=[x['symbol'], x['quote']['USD']['price']]


app = dash.Dash(__name__)
server = app.server

#---------------------------------------------------------------
#Taken from https://www.ecdc.europa.eu/en/geographical-distribution-2019-ncov-cases
# df = pd.read_csv("COVID-19-geographic-disbtribution-worldwide-2020-03-29.csv")

# dff = df.groupby('countriesAndTerritories', as_index=False)[['deaths','cases']].sum()
# print (dff[:5])
# df=pd.json_normalize(cryptodata) 

# df= pd.DataFrame(cryptodata)
# df1=df[['name', 'symbol','quote.USD.price']]
# print(df1)
#---------------------------------------------------------------
def serve_layout():
    json = requests.get(url, params=params, headers=headers).json()


    cryptodata =json['data']

    for x in cryptodata:
        crydata=[x['symbol'], x['quote']['USD']['price']]
    df=pd.json_normalize(cryptodata) 
    df1=df[['name', 'symbol','quote.USD.price']]
    return html.Div([
    html.A(html.Button('Refresh Data'),href='/'),
    html.Div([
        dt.DataTable(
            id='dt1',
            data=df1.to_dict('records'),
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": False} for i in df1.columns
            ],
            # editable=False,
            # filter_action="native",
            # sort_action="native",
            # sort_mode="multi",
            # row_selectable="multi",
            # row_deletable=False,
            # selected_rows=[],
            # page_action="native",
            # page_current= 0,
            # page_size= 6,
            # page_action='none',
            # style_cell={
            # 'whiteSpace': 'normal'
            # },
            # fixed_rows={ 'headers': True, 'data': 0 },
            # virtualization=False,
            style_cell_conditional=[
                {'if': {'column_id': 'name'},
                 'width': '40%', 'textAlign': 'left'},
                {'if': {'column_id': 'symbol'},
                 'width': '30%', 'textAlign': 'left'},
                {'if': {'column_id': 'quote.USD.price'},
                 'width': '30%', 'textAlign': 'left'},
            ],
        ),
    ],className='row'),
    html.H1('The time is: ' + str(datetime.datetime.now()))
    # html.Button('Refresh Data', id='button'),
    # html.Div(id="div-1"),

    # html.Div([
    #     html.Div([
    #         dcc.Dropdown(id='linedropdown',
    #             options=[
    #                      {'label': 'Deaths', 'value': 'deaths'},
    #                      {'label': 'Cases', 'value': 'cases'}
    #             ],
    #             value='deaths',
    #             multi=False,
    #             clearable=False
    #         ),
    #     ],className='six columns'),

    #     html.Div([
    #     dcc.Dropdown(id='piedropdown',
    #         options=[
    #                  {'label': 'Deaths', 'value': 'deaths'},
    #                  {'label': 'Cases', 'value': 'cases'}
    #         ],
    #         value='cases',
    #         multi=False,
    #         clearable=False
    #     ),
    #     ],className='six columns'),

    # ],className='row'),

    # html.Div([
    #     html.Div([
    #         dcc.Graph(id='linechart'),
    #     ],className='six columns'),

    #     html.Div([
    #         dcc.Graph(id='piechart'),
    #     ],className='six columns'),

    # ],className='row'),


])
app.layout = serve_layout

#------------------------------------------------------------------
# @app.callback(
# #    Output('dt1', 'data'),
# #    [Input('refresh-data','n_clicks')],
# #    [State('refresh-data','n_clicks')])
#     dash.dependencies.Output('div-1', 'children'),
#     [dash.dependencies.Input('button', 'n_clicks')])

# def refresh_data(n_clicks):
#     if n_clicks:
#         cryptodata2 =json['data']
#         df=pd.json_normalize(cryptodata2) 
#         df2=df[['name', 'symbol','quote.USD.price']]
#         return [
#          dt.DataTable(
#             id='dt2',
#             data=df2.to_dict('records'),
#             columns=[
#                 {"name": i, "id": i, "deletable": False, "selectable": False} for i in df2.columns
#             ],
#             # editable=False,
#             # filter_action="native",
#             # sort_action="native",
#             # sort_mode="multi",
#             # row_selectable="multi",
#             # row_deletable=False,
#             # selected_rows=[],
#             # page_action="native",
#             # page_current= 0,
#             # page_size= 6,
#             # page_action='none',
#             # style_cell={
#             # 'whiteSpace': 'normal'
#             # },
#             # fixed_rows={ 'headers': True, 'data': 0 },
#             # virtualization=False,
#             style_cell_conditional=[
#                 {'if': {'column_id': 'name'},
#                  'width': '40%', 'textAlign': 'left'},
#                 {'if': {'column_id': 'symbol'},
#                  'width': '30%', 'textAlign': 'left'},
#                 {'if': {'column_id': 'quote.USD.price'},
#                  'width': '30%', 'textAlign': 'left'},
#             ],
#         ),
#     ]


    

#------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)
