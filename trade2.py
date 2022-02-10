import enum
from lib2to3.pgen2.literals import simple_escapes
from optparse import Values
from xmlrpc.client import FastParser
from pandas_datareader import data
import pandas as pd
import datetime

from print_funcs import *
from profit_funcs import *
from plot_funcs import  plot_df
from indicator_funcs import *
from util import *

from cross import Cross
from bollingerBands import BolligerBands
from finalizedprofit import FinalizedProfit
from dmi import Dmi
from momentum import Momentum
from rsiCutler import RsiCutler
from combinationStrategy import CombinationStrategy
from uniqueStrategy1 import UniqueStrategy1


def main():
    START = datetime.datetime(2017, 1, 1)
    END   = datetime.datetime.today().date()

    # SYMBOLS = ["^N225"]
    SYMBOLS = ["4347.T"]
    # SYMBOLS = ["3666.T"]
    # SYMBOLS = ["4776.T", "4347.T", "8226.T"]
    # SYMBOLS = ["BTC-JPY", "ETH-JPY", "XEM-JPY"]
    SOURCE  = "yahoo"

    SHORT_TERM         = 5
    LONG_TERM          = 25
    MACD_SIGNAL_TERM   = 9
    B_BANDS_TERM       = 25
    ADX_TERM           = 14
    ADXR_TERM          = 25
    MOMENTUM_TERM      = 26
    MOM_SIGNAL_TERM    = 10
    RSI_CUTLER_TERM    = 14

    PROFIT_RATIO   = 0.2
    LOSS_RATIO     = 0.05
    RSI_SELL_RATIO = 0.7
    RSI_BUY_RATIO  = 0.3

    dfs = {}

    for symbol in SYMBOLS:
        dfs[symbol] = data.DataReader(symbol, SOURCE, START, END)
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

        dmi = Dmi(df["High"], df["Low"], ADX_TERM, ADXR_TERM)

        momentum = Momentum()
        momentum.compute_moment(close, MOMENTUM_TERM)
        momentum.generate_signal(MOM_SIGNAL_TERM)
        momentum.generate_baseline(0)

        rsi = RsiCutler(RSI_SELL_RATIO, RSI_BUY_RATIO)
        rsi.compute_rsi(close, RSI_CUTLER_TERM)

        fp = FinalizedProfit(close, PROFIT_RATIO, LOSS_RATIO)

        df_dmi = dmi.build_df_indicator()
        df_bb  = bbands2.build_df_indicator()
        df_mom = momentum.build_df_indicator()
        df_rsi = rsi.build_df_indicator()

        df = pd.concat([df, df_dmi, df_bb, df_mom, df_rsi], axis=1)
        df = df.loc[:, ~df.columns.duplicated()]    # 重複列を削除


        umacd_bb2_fp = UniqueStrategy1([macd_cross]    , [bbands2, fp])
        macd_fp      = UniqueStrategy1([macd_cross, fp], [macd_cross, fp])
        umacd_rsi    = UniqueStrategy1([macd_cross]    , [rsi])


# ---------------------------------------------------------------
        # 取引シミュレーション
        print(symbol, end=" ")
        print_df_date(START)
        print_df_date(END)
        print("\n")

        """
        simulate_trade(sma_cross  , close)
        simulate_trade(ema_cross  , close)
        simulate_trade(macd_cross  , close)
        simulate_trade(bbands2     , close)
        simulate_trade(bbands3     , close)
        simulate_trade(dmi        , close)
        simulate_trade(momentum   , close)
        simulate_trade(rsi        , close)

        simulate_trade(umacd_bb2_fp, close)
        simulate_trade(macd_fp     , close)
        simulate_trade(umacd_rsi   , close)
        """


        # ToDo: (simulate)関数化
        strats = (sma_cross, ema_cross, macd_cross, bbands2, bbands3, dmi, momentum, rsi)
        # strats = (sma_cross, ema_cross, macd_cross)

        results1 = simulate_grand_trade(strats, close, required_buy_strats=[], required_sell_strats=[fp])
        results2 = simulate_grand_trade(strats, close, required_buy_strats=[], required_sell_strats=[])

        add_columns = generate_constant_df(values=(symbol, START, END), keys=('symbol', 'start', 'end'), length=len(results1.index))

        results1 = pd.concat([results1, add_columns], axis=1)
        results2 = pd.concat([results2, add_columns], axis=1)

        print_sorted_df(results1, 'profit'    , False)
        print_sorted_df(results1, 'sell_count', False)
        print_sorted_df(results1, 'buy_count' , False)

        print_sorted_df(results2, 'profit'    , False)
        print_sorted_df(results2, 'sell_count', False)
        print_sorted_df(results2, 'buy_count' , False)


# ---------------------------------------------------------------
def simulate_trade(strat, df_prices):
    strat.set_latest_buy_price(None) # 初期化に必要
    sell_dic = {}
    buy_dic  = {}

    for i in range(1, len(df_prices)):
        latest_date  = df_prices.index[i]
        latest_price = df_prices[i]

        if strat.should_buy(i):
            # print_order(latest_date, latest_price, "buy")
            strat.set_latest_buy_price(latest_price)

            buy_dic[latest_date] = latest_price
    
        if strat.should_sell(i):
            # print_order(latest_date, latest_price, "sell")
            strat.set_latest_buy_price(None)

            sell_dic[latest_date] = latest_price

    print("{:20}".format(strat.get_strategy_name()), end=" ")
    total_profit = print_summary_result(sell_dic, buy_dic)
    # total_profit = print_final_result(sell_dic, buy_dic)

    # strategy.plot_df_indicator()

    return total_profit, len(sell_dic), len(buy_dic)


def simulate_grand_trade(strats, df_prices, required_buy_strats=[], required_sell_strats=[]):
    buy_strats  = required_buy_strats
    sell_strats = required_sell_strats

    strat_names = []
    profits     = []
    sell_counts = []
    buy_counts  = []

    for buy_strat in strats:
        for sell_strat in strats:
            ustrat = UniqueStrategy1(buy_strats + [buy_strat], sell_strats + [sell_strat])
            profit, sell_count, buy_count = simulate_trade(ustrat, df_prices)

            strat_names.append(ustrat.get_strategy_name())
            profits.append(profit)
            sell_counts.append(sell_count)
            buy_counts.append(buy_count)

    columns = ('strat', 'profit', 'sell_count', 'buy_count')
    values  = (strat_names, profits, sell_counts, buy_counts)

    return pd.DataFrame(data={'strat': strat_names, 'profit': profits, \
        'sell_count': sell_counts, 'buy_count': buy_counts}, columns=columns)



def generate_constant_df(values, keys, length):
    data = {}

    for i, value in enumerate(values):
        data[keys[i]] = [value] * length

    return pd.DataFrame(data=data, columns=keys)




if __name__ == '__main__':
    main()
