from smartapi import SmartConnect
import pyotp
import credentials

def login():
    obj=SmartConnect(api_key=credentials.API_KEY)
    return obj
    data = obj.generateSession(credentials.CLIENT_ID, credentials.PIN, pyotp.TOTP(credentials.TOKEN).now())
    refreshToken= data['data']['refreshToken']
    feedToken=obj.getfeedToken()
    credentials.FEED_TOKEN = feedToken
    print(feedToken)

def logout():
    try:
        obj=SmartConnect(api_key=credentials.API_KEY)
        logout=obj.terminateSession(credentials.CLIENT_ID)
        print("Logout Successfull")
    except Exception as e:
        print("Logout failed: {}".format(e.message))