import pandas as pd
from indicator_funcs import generate_ema
from strategy import Strategy
from print_funcs import *


class RsiCutler(Strategy):
    def __init__(self):
        pass

    def should_sell(self, i):
        pass

    def should_buy(self, i):
        pass

    def compute_rs(self, df_close, term):
        rs = {}
        up = {}
        down = {}
        index = df_close.index

        for j in range(term):
            rs[index[j]] = 0
            up[index[j]] = 0
            down[index[j]] = 0

        for i in range(term+1, len(df_close)):
            sum_up   = 0
            sum_down = 0
            for j in range(i-term, i):
                diff = df_close[j] - df_close[j-1]
                if diff > 0:
                    sum_up += diff
                    up[index[j]] = diff
                    down[index[j]] = 0
                else:
                    sum_down += diff
                    up[index[j]] = 0
                    down[index[j]] = diff

            rs[index[j]] = sum_up / (sum_up + abs(sum_down)) * 100

            print_df_date(index[j])
            print_prices([df_close[j], df_close[j] - df_close[j-1], up[index[j]], down[index[j]], rs[index[j]]])

        self.rs = pd.DataFrame(data=rs.values(), index=rs.keys())

    def get_rsi(self):
        return self.rs
