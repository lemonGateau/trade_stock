# coding utf-8
from pandas_datareader import data
import pandas
import datetime
import matplotlib.pyplot as plt
from smaCross import SmaCross
from macdCross import MacdCross
from util import *
from print_funcs import *

def main():
    start = datetime.datetime(2021, 7, 28)
    end   = datetime.datetime.today()
    symbols = ["^N225"]
    # symbols = ["4776.T", "4347.T", "8226.T"]
    # symbols = ["BTC-JPY"]
    source  = "yahoo"

    short_term  = 5
    long_term   = 25
    signal_term = 9

    df = {}

    for symbol in symbols:
        df[symbol] = data.DataReader(symbol, source, start, end)

        df[symbol]["short_sma"] = generate_sma(df[symbol]["Adj Close"], short_term)
        df[symbol]["long_sma"]  = generate_sma(df[symbol]["Adj Close"], long_term)

        df[symbol]["macd"]      = df[symbol]["short_sma"] - df[symbol]["long_sma"]
        df[symbol]["signal"]    = generate_sma(df[symbol]["macd"], signal_term)

        # print(df[symbol])
        # print(df[symbol].info())

        sma_cross  = SmaCross(df[symbol]["short_sma"], df[symbol]["long_sma"])
        macd_cross = MacdCross(df[symbol]["macd"], df[symbol]["signal"])

        sell_dict = {}
        buy_dict  = {}

        print(symbol)
        print("\nindex\t      short  long  price  side\n")
        for i in range(1, len(df[symbol]["Adj Close"])):
            #sma_cross.execute(i)
            macd_cross.execute(i)




        # 取引結果等表示
        print(f'sell_count: {len(sell_dict)} buy_count: {len(buy_dict)}')
        print(f'total_profit: {compute_total_profit(sell_dict, buy_dict):>10d}\n')

        print("sell_history: ")
        print_trade_hist(sell_dict)
        print("buy_history:")
        print_trade_hist(buy_dict)

        plot_df_sub([df[symbol][["Adj Close", "short_sma", "long_sma"]], df[symbol][["macd", "signal"]]])


def generate_sma(df_prices, window):
    return df_prices.rolling(window).mean()

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


def compute_total_profit(sell_dict, buy_dict):
    s = list(sell_dict.values())
    b = list(buy_dict.values()) 

    small_len = confirm_smaller_length(sell_dict, buy_dict)

    return sum(s[-small_len:]) - sum(b[-small_len:])


def sell():
    pass

def buy():
    pass

if __name__ == '__main__':
    main()
