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
    def __init__(self):
        pass

    def print_simulation_conditions(self, symbol, begin, end):
        print(symbol, end="  ")
        print_df_date(begin)
        print_df_date(end)
        print("\n")

    def _simulate_trade(self, prices, strat):
        strat.set_latest_buy_price(None) # 初期化に必要

        orders = [np.nan]*len(prices)

        for i in range(1, len(prices)):
            if strat.should_buy(i):
                strat.set_latest_buy_price(prices[i])
                orders[i] = "bid"

            elif strat.should_sell(i):
                strat.set_latest_buy_price(None)
                orders[i] = "ask"

        return pd.Series(orders, index=prices.index, name=strat.get_strategy_name())

    def simulate_strats(self, prices, strats):
        results = []

        for strat in strats:
            results.append(self._simulate_trade(prices, strat))

        return pd.DataFrame(results, columns=prices.index).T


    def simulate_combination_strats(self, prices, strats, required_buy_strats=[], required_sell_strats=[]):
        ''' stratsの全組み合わせでシミュレート '''
        results = []

        for buy_strat in strats:
            for sell_strat in strats:
                buy_strats  = required_buy_strats  + [buy_strat]
                sell_strats = required_sell_strats + [sell_strat]

                strat = CombinationStrategy(buy_strats, sell_strats)

                results.append(self._simulate_trade(prices, strat))

        return pd.DataFrame(results, columns=prices.index).T


    def _compute_profit(self, result):
        result = result[:].dropna()

        strat_name = result.columns.values[-1]

        bids = result.loc[result[strat_name] == "bid", "Adj Close"]
        asks = result.loc[result[strat_name] == "ask", "Adj Close"]

        profit = int(sum(asks) - sum(bids[:len(asks)]))

        return pd.Series([profit, len(bids), len(asks)], \
            index=["profit", "bid_count", "ask_count"], name=strat_name)

    def compute_profits(self, close, results):
        profits = []

        results = pd.concat([close, results], axis=1)

        for strat_name in results.columns.values[1:]:
            result = results.loc[:, ["Adj Close", strat_name]].dropna()

            profits.append(self._compute_profit(result))

        return pd.DataFrame(profits).sort_values(by="profit", ascending=False)


    def extract_strat_profits(self, profits, extract_str):
        profits = profits.loc[profits.index.str.contains(extract_str)]

        return profits.sort_values(by="profit", ascending=False)
