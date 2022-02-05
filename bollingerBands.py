import pandas as pd
from indicator_funcs import *
from print_funcs import *
from strategy import Strategy

class BolligerBands(Strategy):
    def __init__(self, df_close, term):
        self.df = pd.DataFrame()

        self.df["close"] = df_close
        self.df["std"]   = df_close.rolling(term).std()
        self.df["sma"]   = generate_sma(df_close, term)

        self.set_latest_buy_price(None)
        self.set_upper(coef=3)
        self.set_lower(coef=3)

        # print(self.df)

    def should_sell(self, i):
        if self.latest_buy_price is None:
            return False

        return self.df["close"][i] > self.df["upper"][i]

    def should_buy(self, i):
        if self.latest_buy_price:
            return False

        return self.df["close"][i] < self.df["lower"][i]

    def set_upper(self, coef=3):
        self.df["upper"] = self.df["sma"] + coef * self.df["std"]

    def set_lower(self, coef=3):
        self.df["lower"] = self.df["sma"] - coef * self.df["std"]

    def get_upper(self):
        return self.df["upper"]

    def get_lower(self):
        return self.df["lower"]
