import pandas as pd

from common.indicator_funcs import *
from common.plot_funcs import plot_df
from common.print_funcs import *
from strategy import Strategy


class Rsi(Strategy):
    def __init__(self, sell_ratio=0.7, buy_ratio=0.3):
        self.set_sell_ratio(sell_ratio)
        self.set_buy_ratio(buy_ratio)

        self.set_latest_buy_price(None)
        self.set_strategy_name("rsi")

    def should_sell(self, i):
        if self.latest_buy_price is None:
            return False

        if self.rsi[i] > self.sell_ratio:
            return True

        return False

    def should_buy(self, i):
        if self.latest_buy_price:
            return False

        if self.rsi[i] < self.buy_ratio:
            return True

        return False

    def compute_rsi(self, df_close, term):
        df = pd.DataFrame()

        df["diff"] = df_close.diff()
        df["up"]   = df["diff"]
        df["down"] = df["diff"]

        # upの0未満とdownの0より大を0に 
        df["up"].loc[df["up"] < 0]     = 0
        df["down"].loc[df["down"] > 0] = 0

        df["up_sum"]   = df["up"].rolling(term).sum()
        df["down_sum"] = df["down"].rolling(term).sum().abs()

        df["rsi"] = df["up_sum"] / (df["up_sum"] + df["down_sum"])

        # print(df)
        self.rsi = df["rsi"]

    def get_rsi(self):
        return self.rsi

    def set_sell_ratio(self, sell_ratio):
        self.sell_ratio = sell_ratio

    def set_buy_ratio(self, buy_ratio):
        self.buy_ratio = buy_ratio

    def build_df_indicator(self):
        indicator = pd.DataFrame()
        indicator["rsi"] = self.rsi

        return indicator

    def plot_df_indicator(self):
        plot_df([self.build_df_indicator()])

