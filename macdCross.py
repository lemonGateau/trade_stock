import pandas
from trade1 import *

class MacdCross:
    def __init__(self, macd, signal):
        self.macd   = macd
        self.signal = signal

    def trade(self, i):
        if is_crossover(self.macd[i-1:i+1], self.signal[i-1:i+1]):
            self.buy(i)

        elif is_crossover(self.signal[i-1:i+1], self.macd[i-1:i+1]):
            self.sell(i)

    def sell(self, i):
        print_df_date(self.macd.index[i])
        print_prices([self.macd[i], self.signal[i]])


    def buy(self, i):
        print_df_date(self.macd.index[i])
        print_prices([self.macd[i], self.signal[i]])
