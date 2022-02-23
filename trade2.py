import sys
sys.path.append('..')
from pandas_datareader import data
import pandas as pd
import datetime

from indicators import *
from common.print_funcs import *
from common.profit_funcs import *
from common.plot_funcs import  plot_df
from common.indicator_funcs import *
from common.fetch_data import *

from util import *
from simulater import *
from combinationStrategy import CombinationStrategy


def main():
    START = datetime.datetime(2017, 1, 1)
    END   = datetime.datetime.today().date()

    # SYMBOLS = ["^N225"]
    # SYMBOLS = ["3666.T"]
    # SYMBOLS = ["4776.T", "4347.T", "8226.T"]
    # SYMBOLS = ["BTC-JPY", "ETH-JPY", "XEM-JPY"]
    SYMBOLS = ["BTC-JPY"]
    SOURCE  = "yahoo"

    SHORT_TERM       = 12
    LONG_TERM        = 25
    MACD_SIGNAL_TERM = 9
    B_BANDS_TERM     = 25
    ADX_TERM         = 14
    ADXR_TERM        = 25
    MOMENTUM_TERM    = 26
    MOM_SIGNAL_TERM  = 10
    RSI_TERM         = 14

    PROFIT_RATIO     = 0.2
    LOSS_RATIO       = 0.05
    RSI_SELL_RATIO   = 0.7
    RSI_BUY_RATIO    = 0.3

    RANGE    = "10d"
    INTERVAL = "1h"

    for symbol in SYMBOLS:
        # ToDo: 関数名称等見直し
        js_yahoo = fetch_yahoo_past_data(symbol, RANGE, INTERVAL)
        df = extract_ohlcv(js_yahoo)

        START = df.index[0]
        END   = df.index[-1]

        #df = data.DataReader(symbol, SOURCE, START, END)

        print(df)

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

        bbands2 = BollingerBands(close, B_BANDS_TERM)
        bbands3 = BollingerBands(close, B_BANDS_TERM)

        bbands2.set_upper(coef=2)
        bbands2.set_lower(coef=2)
        bbands2.set_strategy_name("bb2")
        bbands3.set_strategy_name("bb3")

        dmi = Dmi(close, df["High"], df["Low"], ADX_TERM, ADXR_TERM)

        momentum = Momentum()
        momentum.compute_moment(close, MOMENTUM_TERM)
        momentum.generate_signal(MOM_SIGNAL_TERM)
        momentum.generate_baseline(0)

        rsi = Rsi(RSI_SELL_RATIO, RSI_BUY_RATIO)
        rsi.compute_rsi(close, RSI_TERM)

        fp = FinalizedProfit(close, PROFIT_RATIO, LOSS_RATIO)

        # df_dmi = dmi.build_df_indicator()
        # df_bb2  = bbands2.build_df_indicator()
        # df_mom = momentum.build_df_indicator()
        # df_rsi = rsi.build_df_indicator()

        # df = pd.concat([df, df_dmi, df_bb2, df_mom, df_rsi], axis=1)
        # df = df.loc[:, ~df.columns.duplicated()]    # 重複列を削除

        # ToDo: 関数化
        # CSV_PATH = "C:\\Users\\manab\\github_\\trade_stock\\1d2.csv"
        # df.to_csv(CSV_PATH, index=True, encoding='utf8')


# ---------------------------------------------------------------
        # 取引シミュレーション
        print_simulation_conditions(symbol, START, END)

        strats = (sma_cross, ema_cross, macd_cross, bbands2, bbands3, dmi, momentum, rsi)

        #results1 = simulate_grand_trade(strats, close, required_buy_strats=[], required_sell_strats=[fp])
        results2 = simulate_grand_trade(strats, close, required_buy_strats=[], required_sell_strats=[])

        add_columns = generate_constant_df(values=(symbol, START, END), keys=('symbol', 'start', 'end'), length=len(results2.index))
        #results1 = pd.concat([results1, add_columns], axis=1)
        results2 = pd.concat([results2, add_columns], axis=1)

        #print_sorted_df(results1, 'profit'    , False)
        print_sorted_df(results2, 'profit'    , False)

        # print_sorted_df(results1, 'sell_count', False)
        # print_sorted_df(results2, 'sell_count', False)

        print_extract_strats_df(results2, "", "dmi")
        print_extract_strats_df(results2, "dmi", "")





if __name__ == '__main__':
    main()

