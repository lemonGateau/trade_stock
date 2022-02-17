from pandas_datareader import data
import pandas as pd
import datetime

from print_funcs import *
from profit_funcs import *
from plot_funcs import  plot_df
from indicator_funcs import *
from util import *
from simulater import *

from cross import Cross
from bollingerBands import BolligerBands
from finalizedprofit import FinalizedProfit
from dmi import Dmi
from momentum import Momentum
from rsiCutler import RsiCutler
from combinationStrategy import CombinationStrategy
from uniqueStrategy1 import UniqueStrategy1


def main():
    END   = datetime.datetime.today().date()
    # START = datetime.datetime(2017, 1, 1)
    START = END - datetime.timedelta(days=365*5)

    # SYMBOLS = ["^N225"]
    # SYMBOLS = ["4347.T"]
    SYMBOLS = ["3666.T"]
    # SYMBOLS = ["4776.T", "4347.T", "8226.T"]
    # SYMBOLS = ["BTC-JPY", "ETH-JPY", "XEM-JPY"]
    # SYMBOLS = ["BTC-JPY"]
    SOURCE  = "yahoo"

    SHORT_TERM         = 12
    LONG_TERM          = 25
    MACD_SIGNAL_TERM   = 9
    B_BANDS_TERM       = 25
    ADX_TERM           = 14
    ADXR_TERM          = 25
    MOMENTUM_TERM      = 26
    MOM_SIGNAL_TERM    = 10
    RSI_CUTLER_TERM    = 14

    PROFIT_RATIO       = 0.2
    LOSS_RATIO         = 0.05
    RSI_SELL_RATIO     = 0.7
    RSI_BUY_RATIO      = 0.3

    dfs = {}

    for symbol in SYMBOLS:
        dfs[symbol] = fetch_short_bars(symbol)
        #dfs[symbol] = data.DataReader(symbol, SOURCE, START, END)

        df = dfs[symbol]
        close = df["Adj Close"]

        # 取引戦略
        df["sma_short"]   = generate_sma(close, SHORT_TERM)
        df["sma_long"]    = generate_sma(close, LONG_TERM)
        df["ema_short"]   = generate_ema(close, SHORT_TERM)
        df["ema_long"]    = generate_ema(close, LONG_TERM)

        df["macd"]        = df["ema_short"] - df["ema_long"] 
        df["macd_signal"] = generate_sma(df["macd"], MACD_SIGNAL_TERM)

        sma_cross  = Cross(df["sma_short"], df["sma_long"])
        ema_cross  = Cross(df["ema_short"], df["ema_long"])
        macd_cross = Cross(df["macd"]     , df["macd_signal"])

        sma_cross.set_strategy_name("sma")
        ema_cross.set_strategy_name("ema")
        macd_cross.set_strategy_name("macd")

        bbands2 = BolligerBands(close, B_BANDS_TERM)
        bbands2.set_upper(coef=2)
        bbands2.set_lower(coef=2)

        bbands3 = BolligerBands(close, B_BANDS_TERM)

        bbands2.set_strategy_name("bb2")
        bbands3.set_strategy_name("bb3")

        dmi = Dmi(close, df["High"], df["Low"], ADX_TERM, ADXR_TERM)

        momentum = Momentum()
        momentum.compute_moment(close, MOMENTUM_TERM)
        momentum.generate_signal(MOM_SIGNAL_TERM)
        momentum.generate_baseline(0)

        rsi = RsiCutler(RSI_SELL_RATIO, RSI_BUY_RATIO)
        rsi.compute_rsi(close, RSI_CUTLER_TERM)

        fp = FinalizedProfit(close, PROFIT_RATIO, LOSS_RATIO)

        df_dmi = dmi.build_df_indicator()
        df_bb2  = bbands2.build_df_indicator()
        df_mom = momentum.build_df_indicator()
        df_rsi = rsi.build_df_indicator()

        df = pd.concat([df, df_dmi, df_bb2, df_mom, df_rsi], axis=1)
        df = df.loc[:, ~df.columns.duplicated()]    # 重複列を削除

# ---------------------------------------------------------------
        # 取引シミュレーション
        print(symbol, end=" ")
        print_df_date(START)
        print_df_date(END)
        print("\n")

        """
        simulate_trade(macd_cross, close)

        umacd_bb2_fp = UniqueStrategy1([macd_cross], [bbands2   , fp])
        umacd_rsi    = UniqueStrategy1([macd_cross], [rsi])

        simulate_trade(umacd_bb2_fp, close)
        simulate_trade(umacd_rsi   , close)
        """

        strats = (sma_cross, ema_cross, macd_cross, bbands2, bbands3, dmi, momentum, rsi)
        # strats = (sma_cross, ema_cross, macd_cross)

        results1 = simulate_grand_trade(strats, close, required_buy_strats=[]          , required_sell_strats=[fp])
        results2 = simulate_grand_trade(strats, close, required_buy_strats=[]          , required_sell_strats=[])
        results3 = simulate_grand_trade(strats, close, required_buy_strats=[macd_cross], required_sell_strats=[])


        add_columns = generate_constant_df(values=(symbol, START, END), keys=('symbol', 'start', 'end'), length=len(results2.index))
        results1 = pd.concat([results1, add_columns], axis=1)
        results2 = pd.concat([results2, add_columns], axis=1)
        results3 = pd.concat([results3, add_columns], axis=1)


        print_sorted_df(results1, 'profit'    , False)
        print_sorted_df(results2, 'profit'    , False)
        print_sorted_df(results3, 'profit'    , False)

        # print_sorted_df(results1, 'sell_count', False)
        # print_sorted_df(results2, 'sell_count', False)

        print_extract_strats_df(results1, "", "dmi")
        print_extract_strats_df(results2, "macd")




import json
import requests
from io import StringIO
from process_file import *

def fetch_short_bars(symbol):
    URL = f"https://query1.finance.yahoo.com/v7/finance/chart/{symbol}?range=1d&interval=1m&indicators=quote&includeTimestamps=true"
    # URL = "https://query1.finance.yahoo.com/v7/finance/chart/3666.T?range=1d&interval=1m&indicators=quote&includeTimestamps=true"

    CSV_PATH = "C:\\Users\\manab\\github_\\trade_stock\\1d.csv"
    TXT_PATH = "C:\\Users\\manab\\github_\\trade_stock\\data2.txt"

    """
    r = requests.get(URL)
    print(r)
    s = StringIO(r.text)
    j = json.load(s)
    """

    j = json_read(TXT_PATH)

    df = pd.DataFrame()
    df['Open'] = j['chart']['result'][0]['indicators']['quote'][0]['open']
    df['Low'] = j['chart']['result'][0]['indicators']['quote'][0]['low']
    df['High'] = j['chart']['result'][0]['indicators']['quote'][0]['high']
    df['Adj Close'] = j['chart']['result'][0]['indicators']['quote'][0]['close']
    df['Volume'] = j['chart']['result'][0]['indicators']['quote'][0]['volume']
    df.index = pd.to_datetime(j['chart']['result'][0]['timestamp'], unit="s")

    df = df.dropna()
    df.to_csv(CSV_PATH, index=False, encoding='utf8')

    print(df)
    return df


if __name__ == '__main__':
    main()



