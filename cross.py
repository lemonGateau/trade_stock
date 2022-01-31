import pandas
from indicator_funcs import *
from print_funcs import *


class Cross:
    def __init__(self, ma1, ma2):
        self.ma1 = ma1
        self.ma2 = ma2

    def should_sell(self, i):
        return is_crossover(self.ma1[i-1:i+1], self.ma2[i-1:i+1])

    def should_buy(self, i):
        return is_crossover(self.ma2[i-1:i+1], self.ma1[i-1:i+1])

    """
    def sell(self, i):
        print_df_date(self.close.index[i])
        print("sell: ", end="")
        print_prices([self.ma1[i], self.ma2[i], self.close[i]])


    def buy(self, i):
        print_df_date(self.close.index[i])
        print("buy : ", end="")
        print_prices([self.ma1[i], self.ma2[i], self.close[i]])
    """

