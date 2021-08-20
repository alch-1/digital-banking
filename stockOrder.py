import requests
import json


def stockOrder(buyOrSell, user_id, pin, account, symbol, quantity):
    url = 'http://tbankonline.com/SMUtBank_API/Gateway'

    headerObj = {
        'Header': {
            'serviceName': 'placeMarketOrder',
            'userID': user_id,
            'PIN': pin,
            'OTP': '999999'
        }
    }

    contentObj = {
        'Content': {
            'settlementAccount': account,
            'symbol': symbol,
            'buyOrSell': buyOrSell,
            'quantity': quantity
        }
    }

    final_url = "{0}?Header={1}&Content={2}".format(
        url, json.dumps(headerObj), json.dumps(contentObj))

    response = requests.post(final_url)

    serviceRespHeader = response.json(
    )['Content']['ServiceResponse']['ServiceRespHeader']

    errorCode = serviceRespHeader['GlobalErrorID']

    if errorCode == '010000':
        marketOrder = response.json(
        )['Content']['ServiceResponse']['StockOrder']
        return marketOrder['orderID']
