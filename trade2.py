from pandas_datareader import data
import pandas as pd
import datetime

from util import *
from print_funcs import *
from indicator_funcs import *
from plot_funcs import  plot_df_sub
from cross import Cross
from bollingerBands import BolligerBands
from finalizedprofit import FinalizedProfit
from dmi import Dmi
from momentum import Momentum
from rsiCutler import RsiCutler
from combinationStrategy import CombinationStrtegy


def main():
    START = datetime.datetime(2021, 1, 29)
    END   = datetime.datetime.today()
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

        #"""
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

        bbands    = BolligerBands(close, B_BANDS_TERM)
        df["upper"] = bbands.get_upper()
        df["lower"] = bbands.get_lower()

        dmi = Dmi(df["High"], df["Low"], ADX_TERM, ADXR_TERM)
        df["plus_di"], df["minus_di"] = dmi.get_dis()
        df["adx"]    , df["adxr"]     = dmi.get_adxs()

        momentum = Momentum()
        momentum.compute_moment(close, MOMENTUM_TERM)
        momentum.generate_signal(MOM_SIGNAL_TERM)

        df["momentum"]     = momentum.get_moment()
        df["mom_signal"]   = momentum.get_signal()
        df["mom_baseline"] = pd.DataFrame(data=[momentum.get_baseline_value()]*len(close), index=close.index)

        rsi = RsiCutler(RSI_SELL_RATIO, RSI_BUY_RATIO)
        rsi.compute_rsi(close, RSI_CUTLER_TERM)
        df["rsi"] = rsi.get_rsi()

        simpler = FinalizedProfit(close, PROFIT_RATIO, LOSS_RATIO)

        comb_strat1 = CombinationStrtegy([sma_cross , simpler])
        comb_strat2 = CombinationStrtegy([ema_cross , simpler])
        comb_strat3 = CombinationStrtegy([macd_cross, simpler])
        comb_strat4 = CombinationStrtegy([bbands    , simpler])
        comb_strat5 = CombinationStrtegy([dmi       , simpler])
        comb_strat6 = CombinationStrtegy([momentum  , simpler])
        comb_strat7 = CombinationStrtegy([rsi       , simpler])
        comb_strat8 = CombinationStrtegy([macd_cross, bbands, dmi])
        comb_strat9 = CombinationStrtegy([rsi       , bbands, dmi])

        comb_strat_all = CombinationStrtegy([sma_cross, ema_cross, macd_cross, bbands, dmi, momentum, rsi, simpler])
        comb_strat_all.set_strategy_name(["all"])

        # 取引シミュレーション
        print(symbol, end=" ")
        print_df_date(START)
        print_df_date(END)
        print("\n")

        simulate_trade(sma_cross  , close)
        simulate_trade(ema_cross  , close)
        simulate_trade(macd_cross , close)
        simulate_trade(bbands    , close)
        simulate_trade(dmi        , close)
        simulate_trade(momentum   , close)
        simulate_trade(rsi        , close)

        simulate_trade(comb_strat1, close)
        simulate_trade(comb_strat2, close)
        simulate_trade(comb_strat3, close)
        simulate_trade(comb_strat4, close)
        simulate_trade(comb_strat5, close)
        simulate_trade(comb_strat6, close)
        simulate_trade(comb_strat7, close)
        simulate_trade(comb_strat8, close)
        simulate_trade(comb_strat9, close)
        simulate_trade(comb_strat_all, close)

        # plot_df_sub([close, df["rsi"]])
        # plot_df_sub([close, df[["momentum", "mom_signal", "mom_baseline"]]])
        # plot_df_sub([close, df[["plus_di", "minus_di", "adx"]]])
        # plot_df_sub([df[["Adj Close", "upper", "lower"]]])
        plot_df_sub([close, df[["macd", "macd_signal"]], df[["Adj Close", "upper", "lower"]]])
        # plot_df_sub([close, df[["Adj Close", "sma_short", "sma_long"]], df[["Adj Close", "ema_short", "ema_long"]], df[["macd", "macd_signal"]], df[["Adj Close", "upper", "lower"]]])
        #"""


def simulate_trade(strategy, df_prices):
    # strategy.set_latest_buy_price(None)

    sell_dic = {}
    buy_dic  = {}

    for i in range(1, len(df_prices)):
        latest_date  = df_prices.index[i]
        latest_price = df_prices[i]

        if strategy.should_buy(i):
            # print_order(latest_date, latest_price, "buy")
            strategy.set_latest_buy_price(latest_price)

            buy_dic[latest_date] = latest_price
    
        if strategy.should_sell(i):
            # print_order(latest_date, latest_price, "sell")
            strategy.set_latest_buy_price(None)

            sell_dic[latest_date] = latest_price

    print("{:20}".format(strategy.get_strategy_name()), end=" ")
    print_summary_result(sell_dic, buy_dic)
    # print_final_result(sell_dic, buy_dic)

    return sell_dic, buy_dic


def execute_order(order_price, side="sell"):
    pass


if __name__ == '__main__':
    main()
