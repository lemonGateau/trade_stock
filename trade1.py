from audioop import cross
from mimetypes import init
from re import S
from select import select
from pandas_datareader import data
import datetime
import pandas
import matplotlib.pyplot as plt


def main():
    start = datetime.datetime(2020, 8, 28)
    end   = datetime.datetime.today()
    # symbols = ["4776.T", "4347.T", "8226.T"]
    symbols = ["BTC_"]
    source  = "yahoo"

    short_term  = 5
    long_term   = 25
    signal_term = 9

    df = {}

    for symbol in symbols:
        df[symbol] = data.DataReader(symbol, source, start, end)

        df[symbol]["short_SMA"] = df[symbol]["Adj Close"].rolling(window=short_term).mean()
        df[symbol]["long_SMA"]  = df[symbol]["Adj Close"].rolling(window=long_term).mean()
        df[symbol]["MACD"]      = df[symbol]["short_SMA"] - df[symbol]["long_SMA"]
        df[symbol]["SIGNAL"]    = df[symbol]["MACD"].rolling(window=signal_term).mean()

        # print(df[symbol])
        # print(df[symbol].info())

        hist = {"buy": [], "sell": [], "profit": []}

        print("\nindex\t      short  long  price  side\n")
        for i in range(long_term, len(df[symbol]["Adj Close"])):

            # SMA  ゴールデンクロス
            if is_crossover(df[symbol]["short_SMA"][i-1:i+1], df[symbol]["long_SMA"][i-1:i+1]):
                print_df_date(df[symbol].index[i])
                print(f'{int(df[symbol]["short_SMA"][i]):>6d} {int(df[symbol]["long_SMA"][i]):>6d} {int(df[symbol]["Adj Close"][i]):>6d} (buy )')

            # SMA  デッドクロス
            elif is_crossover(df[symbol]["long_SMA"][i-1:i+1], df[symbol]["short_SMA"][i-1:i+1]):
                print_df_date(df[symbol].index[i])
                print(f'{int(df[symbol]["short_SMA"][i]):>6d} {int(df[symbol]["long_SMA"][i]):>6d} {int(df[symbol]["Adj Close"][i]):>6d} (sell)')

            # MACD ゴールデンクロス
            if is_crossover(df[symbol]["MACD"][i-1:i+1], df[symbol]["SIGNAL"][i-1:i+1]):
                print_df_date(df[symbol].index[i])
                print(f'{int(df[symbol]["MACD"][i]):>6d} {int(df[symbol]["SIGNAL"][i]):>6d} {int(df[symbol]["Adj Close"][i]):>6d} (buy )(MACD)')

                hist["buy"].append(int(df[symbol]["Adj Close"][i]))

            # MACD デッドクラス
            elif is_crossover(df[symbol]["SIGNAL"][i-1:i+1], df[symbol]["MACD"][i-1:i+1]):
                print_df_date(df[symbol].index[i])
                print(f'{int(df[symbol]["MACD"][i]):>6d} {int(df[symbol]["SIGNAL"][i]):>6d} {int(df[symbol]["Adj Close"][i]):>6d} (sell)(MACD)')

                hist["sell"].append(int(df[symbol]["Adj Close"][i]))

        # 取引結果
        if len(hist["sell"]) <= len(hist["buy"]):
            for i in range(len(hist["sell"])):
                hist["profit"].append((hist["sell"][i] - hist["buy"][i])*100)
                print(f'{hist["sell"][i]:>6d} - {hist["buy"][i]:>6d} -> {hist["profit"][i]:>6d}')
        else:
            for i in range(len(hist["buy"])):
                hist["profit"].append((hist["sell"][i] - hist["buy"][i])*100)
                print(f'{hist["sell"][i]:>6d} - {hist["buy"][i]:>6d} -> {hist["profit"][i]:>6d}')

        print(f'total_profit  : {sum(hist["profit"]):>10d}')


        plot_df_sub([df[symbol][["Adj Close", "short_SMA", "long_SMA"]], df[symbol][["MACD", "SIGNAL"]]])




def is_crossover(ma1, ma2):
    ''' 直近値で ma1 が ma2 を上回るか '''
    if (len(ma1) < 2) or (len(ma2) < 2):
        print(len(ma1))
        return False

    if (ma1[-2] < ma2[-2]) and (ma1[-1] >= ma2[-1]):
        return True

    return False

def print_df_date(index):
    print(f'{index.year:>4d}/{index.month:>2d}/{index.day:>2d}', end="  ")


def plot_df_sub(dfs):
    fig = plt.figure(figsize=(10, 20))

    for i in range(len(dfs)):
        plt.subplot(len(dfs), 1, i+1)

        plt.xlim(dfs[i].index[0], dfs[i].index[-1])
        plt.plot(dfs[i])
        plt.grid(True)

    plt.show()



if __name__ == '__main__':
    main()
