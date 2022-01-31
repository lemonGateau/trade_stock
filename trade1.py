from pandas_datareader import data
import pandas
import datetime
import matplotlib.pyplot as plt
import numpy as np
from util import *
from print_funcs import *

def main():
    START = datetime.datetime(2021, 7, 28)
    END   = datetime.datetime.today()
    SYMBOLS = ["^N225"]
    # SYMBOLS = ["4776.T", "4347.T", "8226.T"]
    # SYMBOLS = ["BTC-JPY"]
    SOURCE  = "yahoo"

    SHORT_TERM  = 5
    LONG_TERM   = 25
    SIGNAL_TERM = 9

    df = {}

    for symbol in SYMBOLS:
        df = data.DataReader(symbol, SOURCE, START, END)

        df["sma_short"] = generate_sma(df["Adj Close"], SHORT_TERM)
        df["sma_long"]  = generate_sma(df["Adj Close"], LONG_TERM)

        df["macd"]      = df["sma_short"] - df["sma_long"]
        df["signal"]    = generate_sma(df["macd"], SIGNAL_TERM)

        # print(df)
        # print(df.info())

        sell_dic = {}
        buy_dic  = {}

        print(symbol)
        print("\nindex\t      short  long  price  side\n")
        for i in range(1, len(df["Adj Close"])):
            """
            # sma  ゴールデンクロス
            if is_crossover(df["sma_short"][i-1:i+1], df["sma_long"][i-1:i+1]):
                buy_dic[df.index[i]] = int(df["Adj Close"][i])

                print_df_date(df.index[i])
                print_prices((df["sma_short"][i], df["sma_long"][i], df["Adj Close"][i]))
 
            # sma  デッドクロス
            elif is_crossover(df["sma_long"][i-1:i+1], df["sma_short"][i-1:i+1]):
                sell_dic[df.index[i]] = int(df["Adj Close"][i])

                print_df_date(df.index[i])
                print_prices((df["sma_short"][i], df["sma_long"][i], df["Adj Close"][i]))

            #"""
            #"""
            # macd ゴールデンクロス
            if is_crossover(df["macd"][i-1:i+1], df["signal"][i-1:i+1]):
                buy_dic[df.index[i]] = int(df["Adj Close"][i])

                # print_df_date(df.index[i])
                # print_prices((df["macd"][i], df["signal"][i], df["Adj Close"][i]))

            # macd デッドクラス
            elif is_crossover(df["signal"][i-1:i+1], df["macd"][i-1:i+1]):
                sell_dic[df.index[i]] = int(df["Adj Close"][i])

                # print_df_date(df.index[i])
                # print_prices((df["macd"][i], df["signal"][i], df["Adj Close"][i]))
            #"""


        # 取引結果等表示
        print(f'sell_count: {len(sell_dic)} buy_count: {len(buy_dic)}')
        print(f'total_profit: {compute_total_profit(sell_dic, buy_dic):>10d}\n')

        print("sell_history: ")
        print_trade_hist(sell_dic)
        print("buy_history:")
        print_trade_hist(buy_dic)

        plot_df_sub([df[["Adj Close", "sma_short", "sma_long"]], df[["macd", "signal"]]])


def generate_sma(df_prices, window):
    return df_prices.rolling(window).mean()


# Tips: nanが含まれる不等式は必ずFalse
def is_crossover(ma1_list, ma2_list):
    ''' 直近値で ma1 が ma2 を上回るか '''
    if (len(ma1_list) < 2) or (len(ma1_list) < 2):
        return False

    if (ma1_list[-2] < ma2_list[-2]) and (ma1_list[-1] >= ma2_list[-1]):
        return True

    return False


def plot_df_sub(dfs):
    fig = plt.figure(figsize=(10, 20))

    for i in range(len(dfs)):
        plt.subplot(len(dfs), 1, i+1)

        plt.xlim(dfs[i].index[0], dfs[i].index[-1])
        plt.plot(dfs[i])
        plt.grid(True)

    plt.show()


def compute_total_profit(sell_dic, buy_dic):
    s = list(sell_dic.values())
    b = list(buy_dic.values()) 

    small_len = confirm_smaller_length(sell_dic, buy_dic)

    return sum(s[-small_len:]) - sum(b[-small_len:])


if __name__ == '__main__':
    main()
