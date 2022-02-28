import sys
sys.path.append("..")

from pandas_datareader import data
import pandas as pd
import numpy as np
from time import time

from common.print_funcs import *
from common.io_data import fetch_yahoo_short_bars

try:
    from ..indicators import *
except:
    from indicators import *


class Simulater:
    def __init__(self, dates, prices):
        self.dates  = dates
        self.prices = pd.Series(data=prices, index=dates, name="Price")

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


    def simulate_strats(self, strats):
        hists   = [self.prices]
        profits = []

        for strat in strats:
            hist   = self._simulate_trade(strat)
            profit = self._compute_profit(hist)

            hists.append(hist)
            profits.append(profit)

        self.hists = pd.DataFrame(hists, columns=self.dates).dropna(axis=1, how="all").T

    def simulate_combination_strats(self, strats, required_buy_strats=[], required_sell_strats=[]):
        ''' stratsの全組み合わせでシミュレート '''
        hists   = [self.prices]
        profits = []

        for buy_strat in strats:
            for sell_strat in strats:
                buy_strats  = required_buy_strats  + [buy_strat]
                sell_strats = required_sell_strats + [sell_strat]

                strat = CombinationStrategy(buy_strats, sell_strats)

                hist   = self._simulate_trade(strat)
                profit = self._compute_profit(hist)

                hists.append(hist)
                profits.append(profit)

        self.hists = pd.DataFrame(hists, columns=self.dates).dropna(axis=1, how="all").T


    def _compute_profit(self, hist):
        strat_name = hist.name

        hist = pd.concat([self.prices, hist], axis=1)

        bids = hist.loc[hist[strat_name] == "bid", "Price"]
        asks = hist.loc[hist[strat_name] == "ask", "Price"]

        profit = int(sum(asks) - sum(bids[:len(asks)]))

        return pd.Series([profit, len(bids), len(asks)], \
            index=["profit", "bid_count", "ask_count"], name=strat_name)


    def compute_profits(self):
        profits = []

        for strat_name in self.hists.columns.values:
            profit = self._compute_profit(self.hists[strat_name])
            profits.append(profit)

        self.profits = pd.DataFrame(profits).sort_values(by="profit", ascending=False)

    def extract_hists(self, extract_str=""):
        ''' extract_str = "" -> return self.hists '''
        return self.hists.loc[self.hists.columns.str.contains(extract_str)]

    def extract_profits(self, extract_str=""):
        ''' extract_str = "" -> return self.profits '''

        return self.profits.loc[self.profits.index.str.contains(extract_str)]

    def export_hists(self, path, index=True, encoding="utf-8"):
        self.hists.to_csv(path, index=index, encoding=encoding)

    def export_profits(self, path, index=True, encoding="utf-8"):
        self.profits.to_csv(path, index=index, encoding=encoding)
