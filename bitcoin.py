import requests
import pandas as pd
import json
import os
from dotenv import load_dotenv

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


cryptodata =json['data']

for x in cryptodata:
    crydata=[x['symbol'], x['quote']['USD']['price']]

# data_dict = {d: cryptodata[d][0] for d in cryptodata}
df=pd.json_normalize(cryptodata) 


    


# df= pd.DataFrame(cryptodata)
df1=df[['name', 'symbol','quote.USD.price']]
print(df1)







