import pandas as pd
from indicator_funcs import generate_ema
from strategy import Strategy
from print_funcs import *


class RsiCutler(Strategy):
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
        df["close"] = df_close
        df["diff"] = df["close"].diff()

        df["up"] = df["diff"]
        df["down"] = df["diff"]

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
