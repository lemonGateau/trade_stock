import pandas as pd
import json
import requests
from io import StringIO
from process_file import *


def generate_yahoo_finance_url(symbol="BTC-JPY", range="7d", interval="5m"):
    ''' https://query1.finance.yahoo.com/v7/finance/chart/3666.T?range=1d&interval=5m&indicators=quote&includeTimestamp=true '''

    PATH = "https://query1.finance.yahoo.com/v7/finance/chart"

    return f"{PATH}/{symbol}?range={range}&interval={interval}&indicators=quote&includeTimestamps=true"


def fetch_yahoo_past_data(symbol, range, interval):
    ''' Open, High, Low, Close, Volume etc.'''
    url = generate_yahoo_finance_url(symbol, range, interval)
    
    r = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})    # chromeからアクセス時のheaderにする

    # ToDo: raise 等でエラー処理
    return json.load(StringIO(r.text))


def extract_ohlcv(js_yahoo):
    ohlcv = pd.DataFrame()

    ohlcv['Open']       = js_yahoo['chart']['result'][0]['indicators']['quote'][0]['open']
    ohlcv['High']       = js_yahoo['chart']['result'][0]['indicators']['quote'][0]['high']
    ohlcv['Low']        = js_yahoo['chart']['result'][0]['indicators']['quote'][0]['low']
    ohlcv['Adj Close']  = js_yahoo['chart']['result'][0]['indicators']['quote'][0]['close']
    ohlcv['Volume']     = js_yahoo['chart']['result'][0]['indicators']['quote'][0]['volume']

    ohlcv.index = pd.to_datetime(js_yahoo['chart']['result'][0]['timestamp'], unit="s")

    return ohlcv.dropna()
