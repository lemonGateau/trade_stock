import pandas
from indicator_funcs import *
from print_funcs import *


class Cross:
    def __init__(self, ma1, ma2, df_close):
        self.ma1 = ma1
        self.ma2 = ma2
        self.close = df_close

    def execute(self, i):
        if is_crossover(self.ma1[i-1:i+1], self.ma2[i-1:i+1]):
            self.buy(i)

        elif is_crossover(self.ma2[i-1:i+1], self.ma1[i-1:i+1]):
            self.sell(i)

    def sell(self, i):
        print_df_date(self.close.index[i])
        print_prices([self.ma1[i], self.ma2[i]])


    def buy(self, i):
        print_df_date(self.close.index[i])
        print_prices([self.ma1[i], self.ma2[i]])

