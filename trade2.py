from pandas_datareader import data
import pandas
import datetime

from util import *
from print_funcs import *
from indicator_funcs import *
from plot_funcs import plot_df_sub

from cross import Cross
from bollingerBands import BolligerBands


def main():
    start = datetime.datetime(2018, 7, 28)
    end   = datetime.datetime.today()
    symbols = ["^N225"]
    # symbols = ["4776.T", "4347.T", "8226.T"]
    # symbols = ["BTC-JPY"]
    source  = "yahoo"

    short_term  = 5
    long_term   = 25
    signal_term = 9
    bb_term     = 25

    df = {}

    for symbol in symbols:
        df[symbol] = data.DataReader(symbol, source, start, end)

        df[symbol]["sma_short"] = generate_sma(df[symbol]["Adj Close"], short_term)
        df[symbol]["sma_long"]  = generate_sma(df[symbol]["Adj Close"], long_term)

        df[symbol]["ema_short"] = generate_ema(df[symbol]["Adj Close"], short_term)
        df[symbol]["ema_long"]  = generate_ema(df[symbol]["Adj Close"], long_term)
        df[symbol]["macd"]      = df[symbol]["ema_short"] - df[symbol]["ema_long"] 
        df[symbol]["signal"]    = generate_sma(df[symbol]["macd"], signal_term)

        # print(df[symbol])
        # print(df[symbol].info())

        sma_cross  = Cross(df[symbol]["sma_short"], df[symbol]["sma_long"], df[symbol]["Adj Close"])
        macd_cross = Cross(df[symbol]["macd"], df[symbol]["signal"], df[symbol]["Adj Close"])

        bb         = BolligerBands(df[symbol]["Adj Close"], term=bb_term)
        df[symbol]["upper"] = bb.get_upper()
        df[symbol]["lower"] = bb.get_lower()

        sell_dict = {}
        buy_dict  = {}

        print(symbol)
        print("\nindex\t      short  long  price  side\n")
        for i in range(1, len(df[symbol]["Adj Close"])):
            #sma_cross.execute(i)
            #macd_cross.execute(i)
            bb.execute(i)


        # 取引結果
        # print_trade_result(sell_dict, buy_dict)

        # plot_df_sub([df[symbol][["Adj Close", "upper", "lower"]]])
        plot_df_sub([df[symbol]["Adj Close"], df[symbol][["macd", "signal"]], df[symbol][["Adj Close", "upper", "lower"]]])
        # plot_df_sub([df[symbol]["Adj Close"], df[symbol][["Adj Close", "sma_short", "sma_long"]], df[symbol][["Adj Close", "ema_short", "ema_long"]], df[symbol][["macd", "signal"]], df[symbol][["Adj Close", "upper", "lower"]]])



if __name__ == '__main__':
    main()
