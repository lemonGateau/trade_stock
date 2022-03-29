import sys
sys.path.append("..")

from pandas_datareader import data
import pandas as pd
import matplotlib.pyplot as plt

try:
    from ..indicators import *
except:
    from indicators import *


class Simulater:
    def __init__(self, dates, prices):
        self.dates  = dates
        # self.prices = pd.Series(data=prices, index=dates, name="Price")
        self.prices = pd.DataFrame(data=prices.values, index=dates, columns=["Price"])

    def simulate_strats_trade(self, strats):
        hists   = []

        for strat in strats:
            hist = self._simulate_trade(strat)
            hists.append(hist)

        self._hists = pd.DataFrame(hists, columns=self.dates).T.dropna(how="all")

    def _simulate_trade(self, strat):
        strat.set_latest_buy_price(None) # 初期化に必要

        orders = {}

        for i, date in enumerate(self.dates[1:], 1):
            if strat.should_buy(i):
                strat.set_latest_buy_price(self.prices["Price"][i])
                orders[date] = "bid"

            elif strat.should_sell(i):
                strat.set_latest_buy_price(None)
                orders[date] = "ask"

        return pd.Series(orders, name=strat.get_strategy_name())


    def compute_profits(self):
        profits = []

        for strat_name in self._hists.columns.values:
            profit = self._compute_profit(self._hists[strat_name])
            profits.append(profit)

        self._profits = pd.DataFrame(profits).sort_values(by="profit", ascending=False)

    def _compute_profit(self, hist):
        bids, asks = self.adjust_hist(hist)

        profit = int(sum(asks) - sum(bids[:len(asks)]))

        return pd.Series([profit, len(bids), len(asks)], \
            index=["profit", "bid_count", "ask_count"], name=hist.name)

    def adjust_hist(self, hist):
        hist = pd.concat([self.prices, hist], axis=1)

        bids = hist.loc[hist.iloc[:, 1] == "bid", "Price"]
        asks = hist.loc[hist.iloc[:, 1] == "ask", "Price"]

        return bids, asks


    def extract_hists(self, extract_str):
        return self._hists.loc[:, self._hists.columns.str.contains(extract_str)]

    def extract_profits(self, extract_str):
        return self._profits.loc[self._profits.index.str.contains(extract_str)]


    def plot_trade_hists(self, strats):
        for strat in strats:
            strat_name = strat.get_strategy_name()

            hist = self.extract_hists(strat_name)
            bids, asks = self.adjust_hist(hist)

            self._plot_trade_hist(bids, asks, strat.build_indicators(), strat_name)

    def _plot_trade_hist(self, bids, asks, indicators, strat_name="trade"):
        if type(indicators) is list:
            indicators = [self.prices] + indicators
        else:
            indicators = [self.prices] + [indicators]

        fig, ax = plt.subplots(nrows=len(indicators), sharex="all", \
            figsize=(9.8, 4.6), constrained_layout=True)

        ax[0].set_title(strat_name)
        ax[0].scatter(bids.index, bids, marker="o", s=14, c="green")
        ax[0].scatter(asks.index, asks, marker="o", s=14, c="red")

        for i, ind in enumerate(indicators):
            ax[i].plot(ind, alpha=0.7)
            ax[i].grid(True)
            ax[i].legend(ind.columns, loc="upper left")

        plt.show()
