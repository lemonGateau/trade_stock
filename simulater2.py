import sys
from common.plot_funcs import plot_df
sys.path.append("..")

from pandas_datareader import data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

try:
    from ..indicators import *
except:
    from indicators import *


class Simulater:
    def __init__(self, dates, prices):
        self.dates   = dates
        self.prices  = pd.Series(data=prices, index=dates, name="Price")

    def simulate_strats_trade(self, strats):
        hists   = []

        for strat in strats:
            hist = self._simulate_trade(strat)
            hists.append(hist)

        self.hists = pd.DataFrame(hists, columns=self.dates).T.dropna(how="all")

    def compute_profits(self):
        profits = []

        for strat_name in self.hists.columns.values:
            profit = self._compute_profit(self.hists[strat_name])
            profits.append(profit)

        self.profits = pd.DataFrame(profits).sort_values(by="profit", ascending=False)


    def _simulate_trade(self, strat):
        strat.set_latest_buy_price(None) # 初期化に必要

        orders = {}

        for i, date in enumerate(self.dates[1:], 1):
            if strat.should_buy(i):
                strat.set_latest_buy_price(self.prices[i])
                orders[date] = "bid"

            elif strat.should_sell(i):
                strat.set_latest_buy_price(None)
                orders[date] = "ask"

        return pd.Series(orders, name=strat.get_strategy_name())


    def _compute_profit(self, hist):
        strat_name = hist.name

        hist = pd.concat([self.prices, hist], axis=1)

        bids = hist.loc[hist[strat_name] == "bid", "Price"]
        asks = hist.loc[hist[strat_name] == "ask", "Price"]

        profit = int(sum(asks) - sum(bids[:len(asks)]))

        return pd.Series([profit, len(bids), len(asks)], \
            index=["profit", "bid_count", "ask_count"], name=strat_name)


    def extract_hists(self, extract_str):
        return self.hists.loc[:, self.hists.columns.str.contains(extract_str)]

    def extract_profits(self, extract_str):
        return self.profits.loc[self.profits.index.str.contains(extract_str)]

    def plot_indicators(self, strat):
        pass
