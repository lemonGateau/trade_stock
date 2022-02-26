import sys
sys.path.append("..")

from pandas_datareader import data
import pandas as pd
import numpy as np

from common.print_funcs import *
from common.profit_funcs import *
from io_data import fetch_yahoo_short_bars

try:
    from ..indicators import *
except:
    from indicators import *

class Simulater:
    def __init__(self, symbol, begin, end):
        self._print_simulation_conditions(symbol, begin, end)

    def _print_simulation_conditions(self, symbol, begin, end):
        print(symbol, end="  ")
        print_df_date(begin)
        print_df_date(end)
        print("\n")

    def simulate_trade(self, prices, strat):
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


    def simulate_comb_strats_trade(self, prices, strats, required_buy_strats=[], required_sell_strats=[]):
        ''' stratsの全組み合わせでシミュレート '''
        buy_strats  = required_buy_strats
        sell_strats = required_sell_strats

        results = pd.DataFrame(data=prices, index=prices.index)

        for buy_strat in strats:
            for sell_strat in strats:
                comb_strat = CombinationStrategy(buy_strats + [buy_strat], sell_strats + [sell_strat])

                r = self.simulate_trade(prices, comb_strat)
                results[r.name] = r

        return results


    def compute_profit(self, result):
        strat_name = result.columns.values[1]

        result = result[:].dropna()

        bids = result.loc[result[strat_name] == "bid", "Adj Close"]
        asks = result.loc[result[strat_name] == "ask", "Adj Close"]

        profit = int(sum(asks) - sum(bids[:len(asks)]))

        return pd.Series([profit, len(bids), len(asks)], \
            index=["profit", "bid_count", "ask_count"], name=strat_name)


