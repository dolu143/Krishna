from smartapi import SmartConnect
import pyotp
from Krishna import credentials
import requests
import pandas as pd

def intializeSymbolTokenMap():
    url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
    d = requests.get(url).json()
    global token_df
    token_df = pd.DataFrame.from_dict(d)
    token_df['expiry'] = pd.to_datetime(token_df['expiry'])
    token_df = token_df.astype({'strike': float})
    credentials.TOKEN_MAP = token_df

def getTokenInfo (exch_seg, instrumenttype,symbol,strike_price,pe_ce):
    df = credentials.TOKEN_MAP
    strike_price = strike_price*100
    if exch_seg == 'NSE':
        eq_df = df[(df['exch_seg'] == 'NSE') & (df['symbol'].str.contains('EQ')) ]
        return eq_df[eq_df['name'] == symbol]
    elif exch_seg == 'NFO' and ((instrumenttype == 'FUTSTK') or (instrumenttype == 'FUTIDX')):
        return df[(df['exch_seg'] == 'NFO') & (df['instrumenttype'] == instrumenttype) & (df['name'] == symbol)].sort_values(by=['expiry'])
    elif exch_seg == 'NFO' and (instrumenttype == 'OPTSTK' or instrumenttype == 'OPTIDX'):
        return df[(df['exch_seg'] == 'NFO') & (df['instrumenttype'] == instrumenttype) & (df['name'] == symbol) & (df['strike'] == strike_price) & (df['symbol'].str.endswith(pe_ce))].sort_values(by=['expiry'])

def login():
    global obj
    obj=SmartConnect(api_key=credentials.API_KEY)
    data = obj.generateSession(credentials.CLIENT_ID, credentials.PIN, pyotp.TOTP(credentials.TOKEN).now())
    refreshToken= data['data']['refreshToken']
    feedToken=obj.getfeedToken()
    credentials.FEED_TOKEN = feedToken
    print(feedToken)

def logout():
    try:
        logout=obj.terminateSession(credentials.CLIENT_ID)
        print("Your Session was {}".format(logout['data']))
    except Exception as e:
        print("Logout failed: {}".format(e.message))

def place_order(token,symbol,qty,exch_seg,buy_sell,ordertype,price):
    try:
        orderparams = {
            "variety": "NORMAL",
            "tradingsymbol": symbol,
            "symboltoken": token,
            "transactiontype": buy_sell,
            "exchange": exch_seg,
            "ordertype": ordertype,
            "producttype": "INTRADAY",
            "duration": "DAY",
            "price": price,
            "squareoff": "0",
            "stoploss": "0",
            "quantity": qty
            }
        orderId=obj.placeOrder(orderparams)
        print("The order id is: {}".format(orderId))
    except Exception as e:
        print("Order placement failed: {}".format(e.message))

#Historic api
def fetch_histcandle(exch_seg,token,timeframe,fromdate,todate):
    try:
      historicParam={
      "exchange": exch_seg,
      "symboltoken": token,
      "interval": timeframe,
      "fromdate": fromdate, 
      "todate": todate
      }
    data = obj.getCandleData(historicParam)
    print(data)
    except Exception as e:
      print("Historic Api failed: {}".format(e.message))
