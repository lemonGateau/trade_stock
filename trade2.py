from pandas_datareader import data
import pandas
import datetime

from util import *
from print_funcs import *
from indicator_funcs import *
from plot_funcs import  plot_df_sub
from cross import Cross
from bollingerBands import BolligerBands
from finalizedprofit import FinalizedProfit
from dmi import Dmi



def main():
    START = datetime.datetime(2022, 1, 1)
    END   = datetime.datetime.today()
    # SYMBOLS = ["^N225"]
    SYMBOLS = ["3666.T"]
    # SYMBOLS = ["4776.T", "4347.T", "8226.T"]
    # SYMBOLS = ["BTC-JPY"]
    SOURCE  = "yahoo"

    SHORT_TERM   = 5
    LONG_TERM    = 25
    SIGNAL_TERM  = 9
    B_BANDS_TERM = 25

    PROFIT_RATIO = 0.2
    LOSS_RATIO   = 0.05

    dfs = {}

    for symbol in SYMBOLS:
        dfs[symbol] = data.DataReader(symbol, SOURCE, START, END)
        df = dfs[symbol]

        dmi = Dmi(df["High"], df["Low"])
        dmi.compute_tr()
        dmi.compute_dms()
        dmi.compute_dis(14)
        print(dmi.get_tr())
        print(dmi.get_dms())

        """
        df["sma_short"] = generate_sma(df["Adj Close"], SHORT_TERM)
        df["sma_long"]  = generate_sma(df["Adj Close"], LONG_TERM)

        df["ema_short"] = generate_ema(df["Adj Close"], SHORT_TERM)
        df["ema_long"]  = generate_ema(df["Adj Close"], LONG_TERM)
        df["macd"]      = df["ema_short"] - df["ema_long"] 
        df["signal"]    = generate_sma(df["macd"], SIGNAL_TERM)

        sma_cross  = Cross(df["sma_short"], df["sma_long"])
        ema_cross  = Cross(df["ema_short"], df["ema_long"])
        macd_cross = Cross(df["macd"], df["signal"])

        b_bands    = BolligerBands(df["Adj Close"], B_BANDS_TERM)

        df["upper"] = b_bands.get_upper()
        df["lower"] = b_bands.get_lower()

        simpler_s = FinalizedProfit(PROFIT_RATIO, LOSS_RATIO, df["Adj Close"], add_strategy=sma_cross)
        simpler_e = FinalizedProfit(PROFIT_RATIO, LOSS_RATIO, df["Adj Close"], add_strategy=ema_cross)
        simpler_m = FinalizedProfit(PROFIT_RATIO, LOSS_RATIO, df["Adj Close"], add_strategy=macd_cross)
        simpler_b = FinalizedProfit(PROFIT_RATIO, LOSS_RATIO, df["Adj Close"], add_strategy=b_bands)

        # 取引シミュレーション
        print(symbol)

        simulate_trade(sma_cross , df["Adj Close"])
        simulate_trade(ema_cross , df["Adj Close"])
        simulate_trade(macd_cross, df["Adj Close"])
        simulate_trade(b_bands   , df["Adj Close"])

        simulate_trade(simpler_s , df["Adj Close"])
        simulate_trade(simpler_e , df["Adj Close"])
        simulate_trade(simpler_m , df["Adj Close"])
        simulate_trade(simpler_b , df["Adj Close"])


        # plot_df_sub([df[["Adj Close", "upper", "lower"]]])
        # plot_df_sub([df[["Adj Close", "upper", "lower"]]])
        # plot_df_sub([df["Adj Close"], df[["macd", "signal"]], df[["Adj Close", "upper", "lower"]]])
        # plot_df_sub([df["Adj Close"], df[["Adj Close", "sma_short", "sma_long"]], df[["Adj Close", "ema_short", "ema_long"]], df[["macd", "signal"]], df[["Adj Close", "upper", "lower"]]])
        """

def simulate_trade(strategy, df_prices):
    strategy.set_latest_buy_price(None)
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

    print_summary_result(sell_dic, buy_dic)
    # print_final_result(sell_dic, buy_dic)

    return sell_dic, buy_dic




def execute_order(order_price, side="sell"):
    pass


if __name__ == '__main__':
    main()
