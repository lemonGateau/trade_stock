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

    def print_simulation_conditions(self, symbol, begin, end):
        print(symbol, end="  ")
        print_df_date(begin)
        print_df_date(end)
        print("\n")


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
        results = []

        for strat in strats:
            results.append(self._simulate_trade(strat))

        return pd.DataFrame(results, columns=self.dates).T.dropna(how="all")


    def simulate_combination_strats(self, strats, required_buy_strats=[], required_sell_strats=[]):
        ''' stratsの全組み合わせでシミュレート '''
        results = []

        for buy_strat in strats:
            for sell_strat in strats:
                buy_strats  = required_buy_strats  + [buy_strat]
                sell_strats = required_sell_strats + [sell_strat]

                strat = CombinationStrategy(buy_strats, sell_strats)

                results.append(self._simulate_trade(strat))

        return pd.DataFrame(results, columns=self.dates).T.dropna(how="all")


    def _compute_profit(self, result):
        strat_name = result.name

        result = pd.concat([self.prices, result], axis=1)

        bids = result.loc[result[strat_name] == "bid", "Price"]
        asks = result.loc[result[strat_name] == "ask", "Price"]

        profit = int(sum(asks) - sum(bids[:len(asks)]))

        return pd.Series([profit, len(bids), len(asks)], \
            index=["profit", "bid_count", "ask_count"], name=strat_name)


    def compute_profits(self, results):
        profits = []

        for strat_name in results.columns.values:
            profit = self._compute_profit(results[strat_name])
            profits.append(profit)

        return pd.DataFrame(profits).sort_values(by="profit", ascending=False)


    def extract_strat_profits(self, profits, extract_str):
        profits = profits.loc[profits.index.str.contains(extract_str)]

        return profits.sort_values(by="profit", ascending=False)
