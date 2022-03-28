import pandas as pd
import json
import requests
from io import StringIO


def fetch_yahoo_short_bars(symbol, range, interval):
    ''' Open, High, Low, Close, Volume etc.'''
    url = _generate_yahoo_finance_url(symbol, range, interval)
    
    r = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})    # chromeからアクセス時のheaderにする

    r = json.load(StringIO(r.text))

    return _extract_bars(r)

def _generate_yahoo_finance_url(symbol="BTC-JPY", range="7d", interval="5m"):
    '''
    https://query1.finance.yahoo.com/v7/finance/chart/ETH_JPY?range=1d&interval=5m&indicators=quote&includeTimestamp=true

    "1d","5d","1mo","3mo","6mo","1y","2y","5y","10y","ytd","max"
    '''

    PATH = "https://query1.finance.yahoo.com/v7/finance/chart"

    return f"{PATH}/{symbol}?range={range}&interval={interval}&indicators=quote&includeTimestamps=true"


def _extract_bars(js_yahoo):
    bars = pd.DataFrame()

    bars['Open']       = js_yahoo['chart']['result'][0]['indicators']['quote'][0]['open']
    bars['High']       = js_yahoo['chart']['result'][0]['indicators']['quote'][0]['high']
    bars['Low']        = js_yahoo['chart']['result'][0]['indicators']['quote'][0]['low']
    bars['Adj Close']  = js_yahoo['chart']['result'][0]['indicators']['quote'][0]['close']
    bars['Volume']     = js_yahoo['chart']['result'][0]['indicators']['quote'][0]['volume']

    bars.index = pd.to_datetime(js_yahoo['chart']['result'][0]['timestamp'], unit="s", utc=True)
    bars.index = bars.index.tz_convert("Asia/Tokyo")

    return bars.dropna()
