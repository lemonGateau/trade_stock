import sys
sys.path.append("..")

from pandas_datareader import data
import pandas as pd
import numpy as np

from common.print_funcs import *
from io_data import fetch_yahoo_short_bars

# ImportError: attempted relative import with no known parent package
try:
    from ..indicators import CombinationStrategy
except:
    from indicators import CombinationStrategy


def simulate_trade(dates, prices, strat):
    strat.set_latest_buy_price(None) # 初期化に必要

    orders = [np.nan]*len(dates)

    for i in range(1, len(prices)):
        if strat.should_buy(i):
            strat.set_latest_buy_price(prices[i])
            orders[i] = "bid"

        elif strat.should_sell(i):
            strat.set_latest_buy_price(None)
            orders[i] = "ask"

    column = strat.get_strategy_name()

    return pd.DataFrame(data={column: orders}, index=dates)



def simulate_grand_trade(dates, prices, strats, required_buy_strats=[], required_sell_strats=[]):
    ''' stratsの全組み合わせでシミュレート '''


    results = pd.DataFrame(data=prices, index=dates)

    for buy_strat in strats:
        for sell_strat in strats:
            buy_strats  = required_buy_strats
            sell_strats = required_sell_strats

            r = simulate_trade(dates, prices, CombinationStrategy(buy_strats, sell_strats))
            results = pd.concat([results, r], axis=1)

    return results
