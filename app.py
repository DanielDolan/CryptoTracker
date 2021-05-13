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

json = requests.get(url, params=params, headers=headers).json()


cryptodata2 =json['data']

# for x in cryptodata:
#     crydata=[x['symbol'], x['quote']['USD']['price']]
dfline=pd.json_normalize(cryptodata2) 
df2=dfline[['name', 'symbol','quote.USD.percent_change_24h','quote.USD.last_updated']]
fig = go.Figure() # or any Plotly Express function e.g. px.bar(...)
fig.add_trace(go.Line(x=df2['name'],
							y=df2['quote.USD.percent_change_24h'],
							name="24 hour graph ",
							marker_color='rgb(162,162,162)'
							 ))

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
def format(x):
    return "${:,.4f}".format(x)
def serve_layout():
    json = requests.get(url, params=params, headers=headers).json()


    cryptodata =json['data']

    for x in cryptodata:
        crydata=[x['symbol'], x['quote']['USD']['price']]
    df=pd.json_normalize(cryptodata) 
   
    df1=df[['name', 'symbol','quote.USD.price','quote.USD.last_updated','quote.USD.percent_change_24h']]
    df1['quote.USD.price']=df1['quote.USD.price'].apply(format)
    return html.Div([
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
    html.A(html.Button('Refresh Data'),href='/'),
    html.H2('The time is: ' + str(datetime.datetime.now())),
    html.Div([html.P(),
			html.H5('Chose Range of Change'),
			dcc.Dropdown(
			id='slct_range',
			options=[ {'label': '1 Hour', 'value': 1},
			{'label': '24 hour', 'value': 24},
			{'label': '7 day', 'value': 7},
			{'label': '30 day', 'value': 30},
			{'label': '60 day', 'value': 60},
			{'label': '90 day', 'value': 90}],
			value=1,
			multi=False,
			className="innerdropdown"
					) 
                     
		]),
        html.Div(dcc.Graph(id='our_graph',style={
			'height': 700
        }))
    


])
app.layout = serve_layout

#------------------------------------------------------------------
@app.callback(
Output(component_id='our_graph', component_property='figure'),
[Input(component_id='slct_range', component_property='value')])


def build_graph(option_slctd):
    if(option_slctd==1):
        json = requests.get(url, params=params, headers=headers).json()
        cryptodata3 =json['data']
        dfgraph=pd.json_normalize(cryptodata3) 
        dfgraph1hr=dfgraph[['name', 'quote.USD.percent_change_1h']]
        fig=px.line(dfgraph1hr, x="name", y="quote.USD.percent_change_1h")
        return fig
    if(option_slctd==24):
        json = requests.get(url, params=params, headers=headers).json()
        cryptodata4 =json['data']
        dfgraph=pd.json_normalize(cryptodata4) 
        dfgraph1hr=dfgraph[['name', 'quote.USD.percent_change_24h']]
        fig=px.line(dfgraph1hr, x="name", y="quote.USD.percent_change_24h")
        return fig
    if(option_slctd==7):
        json = requests.get(url, params=params, headers=headers).json()
        cryptodata4 =json['data']
        dfgraph=pd.json_normalize(cryptodata4) 
        dfgraph1hr=dfgraph[['name', 'quote.USD.percent_change_7d']]
        fig=px.line(dfgraph1hr, x="name", y="quote.USD.percent_change_7d")
        return fig
    if(option_slctd==30):
        json = requests.get(url, params=params, headers=headers).json()
        cryptodata4 =json['data']
        dfgraph=pd.json_normalize(cryptodata4) 
        dfgraph1hr=dfgraph[['name', 'quote.USD.percent_change_30d']]
        fig=px.line(dfgraph1hr, x="name", y="quote.USD.percent_change_30d")
        return fig
    if(option_slctd==60):
        json = requests.get(url, params=params, headers=headers).json()
        cryptodata4 =json['data']
        dfgraph=pd.json_normalize(cryptodata4) 
        dfgraph1hr=dfgraph[['name', 'quote.USD.percent_change_60d']]
        fig=px.line(dfgraph1hr, x="name", y="quote.USD.percent_change_60d")
        return fig
    if(option_slctd==90):
        json = requests.get(url, params=params, headers=headers).json()
        cryptodata4 =json['data']
        dfgraph=pd.json_normalize(cryptodata4) 
        dfgraph1hr=dfgraph[['name', 'quote.USD.percent_change_90d']]
        fig=px.line(dfgraph1hr, x="name", y="quote.USD.percent_change_90d")
        return fig
    
    




    

#------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)
