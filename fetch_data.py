import pandas as pd
import json
import requests
from io import StringIO
from process_file import *


def fetch_short_ohlcv(symbol):
    ''' Open, High, Low, Close, Volume '''
    URL = f"https://query1.finance.yahoo.com/v7/finance/chart/{symbol}?range=1d&interval=1m&indicators=quote&includeTimestamps=true"
    # URL = "https://query1.finance.yahoo.com/v7/finance/chart/3666.T?range=1d&interval=1m&indicators=quote&includeTimestamps=true"

    r = requests.get(URL, headers={'User-agent': 'Mozilla/5.0'})    # chromeからアクセス時のheaderにする
    j = json.load(StringIO(r.text))

    df = pd.DataFrame()
    df['Open'] = j['chart']['result'][0]['indicators']['quote'][0]['open']
    df['High'] = j['chart']['result'][0]['indicators']['quote'][0]['high']
    df['Low'] = j['chart']['result'][0]['indicators']['quote'][0]['low']
    df['Adj Close'] = j['chart']['result'][0]['indicators']['quote'][0]['close']
    df['Volume'] = j['chart']['result'][0]['indicators']['quote'][0]['volume']

    df.index = pd.to_datetime(j['chart']['result'][0]['timestamp'], unit="s")
    df = df.dropna()

    return df

