import json
import requests
import pandas as pd
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
from datetime import datetime

stocklist = ["AAPL", "AMZN", "NFLX", "GOOG", "MSFT"]

url = 'http://tbankonline.com/SMUtBank_API/Gateway'

df = pd.DataFrame(columns=['date'])
df.set_index('date', inplace=True)


def getStockHistory(ticker):
    # Header
    serviceName = 'getStockHistory'
    userID = '01332738'
    PIN = '877324'
    OTP = '999999'
    # Content
    symbol = ticker
    startDate = datetime.utcfromtimestamp(0).strftime('%Y-%m-%d')
    endDate = datetime.now().strftime('%Y-%m-%d')

    headerObj = {
        'Header': {
            'serviceName': serviceName,
            'userID': userID,
            'PIN': PIN,
            'OTP': OTP
        }
    }
    contentObj = {
        'Content': {
            'symbol': symbol,
            'startDate': startDate,
            'endDate': endDate
        }
    }
    final_url = "{0}?Header={1}&Content={2}".format(
        url, json.dumps(headerObj), json.dumps(contentObj))
    response = requests.post(final_url)
    serviceRespHeader = response.json(
    )['Content']['ServiceResponse']['ServiceRespHeader']
    errorCode = serviceRespHeader['GlobalErrorID']

    if errorCode == '010000':
        stockHistory = json.loads(response.json()[
                                  'Content']['ServiceResponse']['Stock_History']['jsonTimeSeries'])['chart']['result'][0]

        df2 = pd.DataFrame(
            {"time": stockHistory['timestamp'], ticker: stockHistory['indicators']['quote'][0]['close']})
        df2['date'] = pd.to_datetime(df2['time'], unit='s')
        df2 = df2.drop(['time'], axis=1)
        df2 = df2.set_index(['date'])
        global df
        df = pd.merge(df, df2, how="outer", on="date")


for ticker in stocklist:
    print(ticker)
    getStockHistory(ticker)

mu = expected_returns.mean_historical_return(df)
S = risk_models.sample_cov(df)
ef = EfficientFrontier(mu, S)
raw_weights = ef.max_sharpe()
weights = ef.clean_weights()

latest_prices = get_latest_prices(df)

da = DiscreteAllocation(weights, latest_prices, total_portfolio_value=10000)
allocation, leftover = da.lp_portfolio()
print("Discrete allocation:", allocation)
print("Funds remaining: ${:.2f}".format(leftover))
