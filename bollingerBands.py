import pandas
from indicator_funcs import *
from print_funcs import *
from strategy import Strategy

class BolligerBands(Strategy):
    def __init__(self, df_close, term):
        self.sma = generate_sma(df_close, term)
        self.std  = df_close.rolling(term).std()
        self.df_close = df_close

        self.set_latest_buy_price(None)
        self.set_upper(coef=3)
        self.set_lower(coef=3)

    def should_sell(self, i):
        if self.latest_buy_price is None:
            return False

        return (self.df_close[i] > self.upper[i])

    def should_buy(self, i):
        if self.latest_buy_price:
            return False

        return (self.df_close[i] < self.lower[i])

    def set_upper(self, coef=3):
        self.upper = self.sma + coef * self.std

    def set_lower(self, coef=3):
        self.lower = self.sma - coef * self.std

    def get_upper(self):
        return self.upper

    def get_lower(self):
        return self.lower
