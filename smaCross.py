import pandas
from trade1 import *

class SmaCross:
    def __init__(self, sma_short, sma_long):
        self.sma_short = sma_short
        self.sma_long  = sma_long

    def trade(self, i):
        if is_crossover(self.sma_short[i-1:i+1], self.sma_long[i-1:i+1]):
            self.buy(i)

        elif is_crossover(self.sma_long[i-1:i+1], self.sma_short[i-1:i+1]):
            self.sell(i)

    def sell(self, i):
        print_df_date(self.sma_short.index[i])
        print_prices([self.sma_short[i], self.sma_long[i]])


    def buy(self, i):
        print_df_date(self.sma_short.index[i])
        print_prices([self.sma_short[i], self.sma_long[i]])


