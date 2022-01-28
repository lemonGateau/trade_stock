from pandas_datareader import data
import datetime
import pandas
import matplotlib.pyplot as plt


def main():
    start = datetime.datetime(2021, 8, 3)
    end   = datetime.datetime.now()
    symbols = ["4776.T", "4347.T", "8226.T"]
    source  = "yahoo"

    short_term = 5
    long_term  = 25

    df = {}
    for symbol in symbols:
        df[symbol] = data.DataReader(symbol, source, start, end)


        df[symbol]["short_SMA"] = df[symbol]["Adj Close"].rolling(short_term).mean()
        df[symbol]["long_SMA"]  = df[symbol]["Adj Close"].rolling(long_term).mean()

        print(df[symbol][["Adj Close", "short_SMA", "long_SMA"]])
        print('\n')

        plot_df(df[symbol][["Adj Close", "short_SMA", "long_SMA"]])



def plot_df(df):
    df.plot(figsize=(8, 6), fontsize=18)

    # plt.legend(bbox_to_anchor=(0, 1), loc='upper left', borderaxespad=1, fontsize=18)
    plt.grid(True)
    plt.show()



if __name__ == '__main__':
    main()
