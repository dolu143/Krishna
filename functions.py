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
def histcand(exch_seg,token,timeframe,fromdate,todate):
    try:
        historicParam={
          "exchange": exch_seg,
          "symboltoken": token,
          "interval": timeframe,
          "fromdate": fromdate, 
          "todate": todate
          }
        data = obj.getCandleData(historicParam)
        return data
    except Exception as e:
      print("Historic Api failed: {}".format(e.message))
def write_toxl(hist_candata):
    columns = ["time", "o","h","l","c","v"]
    hist_candata = pd.DataFrame(hist_candata["data"], columns = columns)
    hist_candata["time"] = pd.to_datetime(hist_candata["time"], format="%Y-%m-%dT%H:%M:%S")
    print(hist_candata)
    wb = xw.Workbook("C:\\Users\\pushp\\source\\repos\\Radha\\PythonApplication1\\Nifty.xlsx", {'remove_timezone': True})
    wb1 = wb.add_worksheet("NIFTY")
    wb1.write_row(0,0,columns)
    format1 = wb.add_format({'num_format': 'dd/mm/yy hh:mm'})                                   
    wb1.write_column(1,0, hist_candata['time'], format1)
    wb1.write_column(1,1, hist_candata['o'])
    wb1.write_column(1,2, hist_candata['h'])
    wb1.write_column(1,3, hist_candata['l'])
    wb1.write_column(1,4, hist_candata['c'])
    wb1.write_column(1,5, hist_candata['v'])
    wb.close()
