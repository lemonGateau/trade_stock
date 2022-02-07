from pandas_datareader import data
import pandas as pd
import datetime

from util import *
from print_funcs import *
from indicator_funcs import *
from plot_funcs import  plot_df
from cross import Cross
from bollingerBands import BolligerBands
from finalizedprofit import FinalizedProfit
from dmi import Dmi
from momentum import Momentum
from rsiCutler import RsiCutler
from combinationStrategy import CombinationStrategy
from uniqueStrategy1 import UniqueStrategy1


def main():
    START = datetime.datetime(2013, 1, 1)
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

        simpler = FinalizedProfit(close, PROFIT_RATIO, LOSS_RATIO)

        df_dmi = dmi.build_df_indicator()
        df_bb  = bbands2.build_df_indicator()
        df_mom = momentum.build_df_indicator()
        df_rsi = rsi.build_df_indicator()

        df = pd.concat([df, df_dmi, df_bb, df_mom, df_rsi], axis=1)
        df = df.loc[:, ~df.columns.duplicated()]    # 重複列を削除

        macd_bb2 = CombinationStrategy([macd_cross, bbands2])
        macd_bb3 = CombinationStrategy([macd_cross, bbands3])

        u1 = UniqueStrategy1([macd_cross], [bbands2, simpler])

        """
        comb_strat1 = CombinationStrategy([sma_cross , simpler])
        comb_strat2 = CombinationStrategy([ema_cross , simpler])
        comb_strat3 = CombinationStrategy([macd_cross, simpler])
        comb_strat4 = CombinationStrategy([bbands    , simpler])
        comb_strat5 = CombinationStrategy([dmi       , simpler])
        comb_strat6 = CombinationStrategy([momentum  , simpler])
        comb_strat7 = CombinationStrategy([rsi       , simpler])
        comb_strat8 = CombinationStrategy([macd_cross, bbands, dmi])
        comb_strat9 = CombinationStrategy([rsi       , bbands, dmi])

        comb_strat_all = CombinationStrategy([sma_cross, ema_cross, macd_cross, bbands, dmi, momentum, rsi, simpler])
        comb_strat_all.set_strategy_name("all")
        """

        # 取引シミュレーション
        print(symbol, end=" ")
        print_df_date(START)
        print_df_date(END)
        print("\n")


        #"""
        #simulate_trade(sma_cross  , close)
        #simulate_trade(ema_cross  , close)
        simulate_trade(macd_cross  , close)
        simulate_trade(bbands2     , close)
        simulate_trade(bbands3     , close)
        #simulate_trade(dmi        , close)
        #simulate_trade(momentum   , close)
        #simulate_trade(rsi        , close)
        #"""
        simulate_trade(macd_bb2   , close)
        simulate_trade(macd_bb3   , close)
        simulate_trade(u1         , close)

        """
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
        """

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

    # strategy.plot_df_indicator()

    return sell_dic, buy_dic


if __name__ == '__main__':
    main()
