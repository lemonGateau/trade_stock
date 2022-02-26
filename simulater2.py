import sys
sys.path.append("..")

from pandas_datareader import data
import pandas as pd
import numpy as np

from common.print_funcs import *
from common.profit_funcs import *
from io_data import fetch_yahoo_short_bars


class Simulater:
    def __init__(self, symbol):
        self.symbol = symbol


    def simulate_trade(self, strat, dates, prices):
        strat.set_latest_buy_price(None)
        buy_dic  = {}
        sell_dic = {}

        for i in range(1, len(prices)):
            date  = dates[i]
            price = prices[i]

            if strat.should_buy(i):
                strat.set_latest_buy_price(price)
                buy_dic[date]  = price
    
            if strat.should_sell(i):
                strat.set_latest_buy_price(None)
                sell_dic[date] = price

        return buy_dic, sell_dic

    def simulate_by_short_bars(self, range, interval):
        bars = fetch_yahoo_short_bars(self.symbol, range, interval)

        buy_dic, sell_dic = self.simulate_trade(bars["Adj Close"])

    def simulate_by_long_bars(self, source, begin, end):
        bars = data.DataReader(self.symbol, source, begin, end)

        buy_dic, sell_dic = self.simulate_trade(bars["Adj Close"])

    def print_final_result(buy_dic, sell_dic):
        pass

    def print_summary_result(buy_dic, sell_dic):
        pass
