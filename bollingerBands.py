# coding utf-8
import pandas
from indicator_funcs import *
from print_funcs import *


class BolligerBands:
    def __init__(self, df_close, term):
        self.sma1 = generate_sma(df_close, term)
        self.std  = df_close.rolling(term).std()
        self.close = df_close

        self.set_upper(coef=3)
        self.set_lower(coef=3)

    def execute(self, i):
        if self.close[i] > self.upper[i]:
            self.sell(i)
        elif self.close[i] < self.lower[i]:
            self.buy(i)

    def sell(self, i):
        print_df_date(self.close.index[i])
        print_prices([self.upper[i], self.lower[i], self.close[i]])

    def buy(self, i):
        print_df_date(self.close.index[i])
        print_prices([self.upper[i], self.lower[i], self.close[i]])

    def set_upper(self, coef=3):
        self.upper = self.sma1 + coef * self.std

    def set_lower(self, coef=3):
        self.lower = self.sma1 - coef * self.std

    def get_upper(self):
        return self.upper

    def get_lower(self):
        return self.lower
